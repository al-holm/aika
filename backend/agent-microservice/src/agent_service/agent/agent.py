from agent_service.core.config import Config
from agent_service.core.pydantic_agent import AgentConfigModel
from agent_service.agent.agent_step import AgentStep
from agent_service.agent.task_type import TaskType
from pydantic import ValidationError
from agent_service.agent.llm import LLMBedrock, LLMRunPod
from agent_service.prompts.react_prompt import VAL_STOP_PREFIX, ACTION_PROMPT_QA, ACTION_PROMPT_LESSON, VALIDATION_PROMPT_LESSON, VALIDATION_PROMPT_QA
from agent_service.agent.reasoning_trace import ReasoningLogger
from agent_service.prompts.prompt_builder import PromptBuilder
from agent_service.prompts.trajectory_library import TrajectoryInjector
from agent_service.tools.tool_executor import ToolExecutor
from agent_service.parsers.agent_step_parser import StepParser, ValidationParser
import logging
from enum import Enum

class AgentMode(Enum):
    """ 
    defines an enumeration `AgentMode` with two members `PLAN` and `VAL` representing
    different modes for an agent: action proposal & action validation.
    """
    PLAN = "plan"
    VAL = "validate"

class Agent:
    """
    Represents a ReAct agent that can plan actions, execute steps using tools, 
    validate results, and provide final answers based on reasoning traces and prompts.

    Attributes
    ----------
    task_type : TaskType
        The type of task the agent is performing, default is TaskType.ANSWERING.
    reasoning_logger : ReasoningLogger
        Logger for keeping track of the reasoning steps.
    tool_executor : ToolExecutor
        Executor for running tools based on the planned steps.
    prompt_builder : PromptBuilder
        Builder for generating prompts for the agent.
    validation_parser : ValidationParser
        Parser for processing validation steps.
    step_parser : StepParser
        Parser for processing planned steps.
    config : AgentConfigModel
        Configuration settings for the agent.
    llm : Any
        The large language model used for generating steps and validation.
    max_iterations : int
        The maximum number of iterations for the agent loop.
    trajectory_injector : TrajectoryInjector
        Injector of relevant trajectory examples into the agent's prompt.

    Methods
    -------
    __init__(self, task_type: TaskType = TaskType.ANSWERING) -> None
        Initializes the agent.
    init_prompts(self, task_type: TaskType) -> None
        Sets prompt templates for planning and validation steps.
    run(self, query: str) -> str
        Executes the agent loop to process the query until a final answer is obtained.
    take_step(self) -> bool
        Plans a step, executes it, and validates the result.
    validate_step(self) -> bool
        Retrieves and processes a validation prompt.
    plan_step(self) -> AgentStep
        Retrieves and processes the current planning prompt.
    process_validation_thought(self, val_answer: str) -> bool
        Parses the validation answer and updates the reasoning trace.
    execute_step(self, step: AgentStep) -> None
        Executes an action using the tool executor and updates the reasoning logger.
    get_current_prompt(self, mode: AgentMode = AgentMode.PLAN) -> str
        Returns a prompt with a reasoning trace based on the specified mode.
    get_final_response(self, iteration: int) -> str
        Builds and returns the final answer based on the last observation and iteration number.
    update_prompts_for_query(self, query: str) -> None
        Updates prompts with a query and available tools.
    parse_config(self) -> None
        Reads settings from a configuration file and sets attributes based on the configuration.
    add_trajectory_examples_to_prompts -> None
        Injects relevant trajectory examples into the agent's prompt.
    """

    def __init__(self, task_type: TaskType = TaskType.ANSWERING) -> None:
        self.parse_config()
        self.reasoning_logger = ReasoningLogger(
            model_id=self.llm.llm_id, 
            task_type=task_type
            )
        self.task_type = task_type
        self.tool_executor = ToolExecutor(task_type=task_type)
        self.prompt_builder = PromptBuilder()
        self.init_prompts(task_type) 
        self.validation_parser = ValidationParser()
        self.step_parser = StepParser(self.tool_executor.tool_names)
        if task_type  == TaskType.ANSWERING:
            self.trajectory_injector = TrajectoryInjector()

    def reset(self):
        """
        resets the reasoning trace and recreates prompts

        """
        self.reasoning_logger = ReasoningLogger(
             model_id=self.llm.llm_id, 
             task_type=self.task_type
            )
        self.init_prompts(self.task_type) 

    def init_prompts(self, task_type: TaskType):
        """
        sets prompt templates for a given plan and validation steps
        """
        if task_type == TaskType.ANSWERING:
            plan_prompt = ACTION_PROMPT_QA
            val_prompt = VALIDATION_PROMPT_QA
        elif task_type == TaskType.LESSON:
            plan_prompt = ACTION_PROMPT_LESSON
            val_prompt = VALIDATION_PROMPT_LESSON
        else: 
            raise NotImplementedError(f"No agent implemented for the task type: {task_type}")
        self.prompt_builder.create_prompts(
            {
                AgentMode.PLAN : plan_prompt,
                AgentMode.VAL : val_prompt
            }
        )

    def run(self, query:str)->str:
        """
        runs the agent loop to execute a series of steps based on a query until a final answer is obtained.
        
        Parameters
        ----------
        query : str
            representation of the query to be processed by the agent.
        
        Returns
        -------
        str 
            the final answer obtained after running the agent loop.
        """
        self.update_prompts_for_query(query)
        logging.info("Entering agent loop...")
        iteration = 0
        while iteration < self.max_iterations:
            try:
                is_final = self.take_step()
                if is_final:
                    break
            except Exception as e:
                logging.error(e)
                self.reasoning_logger.add_exception(str(e))
            iteration += 1
        final_answer = self.get_final_response(iteration)
        self.reset()
        logging.info("Reseting the agent...")
        return final_answer

    def take_step(self) -> bool:
        """
        plans a step, executes the step, validates the result if it's the final answer
         
        Returns
        -------
        is_final : bool 
            whether the result is the final answer or not
        """
        step = self.plan_step()
        self.execute_step(step)
        is_final = self.validate_step()
        return is_final

    def validate_step(self) -> bool:
        """
        retrieves a validation prompt, runs it through the llm,
        processes the output.

        Returns
        -------
        is_final : bool 
            whether the result is the final answer or not
        """
        self.llm.set_max_tokens(self.config.max_tokens_val)
        validation_prompt = self.get_current_prompt(mode=AgentMode.VAL)
        validation_thought = self.llm.run(validation_prompt)
        is_final = self.process_validation_thought(validation_thought)
        return is_final

    def plan_step(self) -> AgentStep:
        """
        retrieves the current prompt, runs it through the llm, parses the
        output.

        Returns
        -------
        step: AgentStep 
                   
        """
        current_prompt = self.get_current_prompt(mode=AgentMode.PLAN)
        self.llm.set_max_tokens(self.config.max_tokens_plan)
        llm_answer = self.llm.run(current_prompt)
        step = self.step_parser.parse_step(llm_answer)
        return step

    def process_validation_thought(self, val_answer:str) -> bool:
        """
        parses the validation answer, adds it to a reasoning trace
        
        Parameters
        ----------
        val_answer : str
            the answer provided during a validation process.

        Returns
        -------
        bool 
            whether the final answer can be derived from the reasoning trace or not
        """
        val_step = self.validation_parser.parse_step(val_answer)
        self.reasoning_logger.add_step(val_step)

        if VAL_STOP_PREFIX in val_step.validation_thought:
            return True
        else:
            return False

    def execute_step(self, step:AgentStep) ->None:
        """
        executes an action using the tool executor and the provided agent step, 
        updates the observation in the step, and logs the step with the reasoning logger.

        Parameters
        ----------
        step: AgentStep
            The agent step that contains the action to be performed and the input for that action. 
        """
        tool_input = step.action_input
        if self.task_type == TaskType.LESSON and step.action=="Deutschaufgaben generieren":
            tool_input += "[" + self.reasoning_logger.get_last_observation() + "]"
        observation = self.tool_executor.execute(step.action, tool_input)
        step.observation = observation
        self.reasoning_logger.add_step(step)
    
    def get_current_prompt(self, mode=AgentMode.PLAN) -> str:
        """
        returns a prompt with a reasoning trace based on the specified mode.
        
        Parameters
        ----------
        mode, optional : AgentMode
            the type of prompt to be generated.

        Returns
        -------
        current_prompt : str
            a prompt with a reasoning trace based on the specified mode
        """
        reasoning_steps = str(self.reasoning_logger)
        current_prompt = self.prompt_builder.generate_prompt(name_id=mode,
                                                             reasoning_trace=reasoning_steps)
        return current_prompt

    
    def get_final_response(self, iteration: int) -> str:
        """ 
        builds and returns final answer based on the last observation & the iteration number

        Parameters
        ----------
        iteration : int
            the iteration number after breaking the agent loop.

        Returns
        -------
        final_answer : str
            the final answer
        """
        if iteration == self.max_iterations:
            return "Etwas ist fehlgeschlagen, versuche es erneut!"
        self.reasoning_logger.build_final_answer()
        self.reasoning_logger.to_json()
        final_answer = self.reasoning_logger.final_answer
        logging.info(final_answer)
        return final_answer

    def update_prompts_for_query(self, query:str) -> None:
        """
        updates prompts with a query and availiable tools
        
        """
        update = {
            "tools": str(self.tool_executor),
            "tool_names": self.tool_executor.tool_names,
            "input": query
        } 

        self.prompt_builder.update_prompt(
            name_id=AgentMode.PLAN,
            **update
        )
        
        self.prompt_builder.update_prompt(
            name_id=AgentMode.VAL,
            **update
        )
        self.reasoning_logger.set_query(query)

        if self.task_type  == TaskType.ANSWERING:
            self.add_trajectory_examples_to_prompts(query)

    def add_trajectory_examples_to_prompts(self, query)->None:
        """
        Injects relevant trajectory examples into the agent's prompt.

        """
        plan_examples, val_examples = self.trajectory_injector.inject_trajectories(query)
        self.prompt_builder.update_prompt(
            name_id=AgentMode.PLAN,
            examples=plan_examples
        )
        
        self.prompt_builder.update_prompt(
            name_id=AgentMode.VAL,
            examples=val_examples
        )


    def parse_config(self) -> None:
        """
        reads settings from a configuration file, creates a pydantic validation `AgentConfigModel` object, 
        and sets additional attributes based on the configuration.
        """
        try:
            config = Config("agent")
            settings = config.get_settings()

            self.config = AgentConfigModel(**settings)
            if self.config.llm=='bedrock':
                self.llm = LLMBedrock()
            elif self.config.llm=='runpod':
                self.llm = LLMRunPod()
            self.max_iterations = self.config.max_iterations
        except ValidationError as e:
            logging.ERROR(f'Agent attributes error: {e}')


