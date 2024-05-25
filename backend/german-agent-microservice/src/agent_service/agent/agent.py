from agent_service.core.config import Config
from agent_service.core.pydantic_agent import AgentConfigModel
from agent_service.agent.agent_step import AgentStep
from agent_service.agent.task_type import TaskType
from pydantic import ValidationError
from agent_service.agent.llm import LLMBedrock, LLMRunPod
from agent_service.prompts.react_prompt import VAL_STOP_PREFIX, ACTION_PROMPT_QA, ACTION_PROMPT_LESSON, VALIDATION_PROMPT_LESSON, VALIDATION_PROMPT_QA
from agent_service.agent.reasoning_trace import ReasoningLogger
from agent_service.prompts.prompt_builder import PromptBuilder
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
    represents a ReAct agent that can plan actions, execute steps using tools, 
    validate results, and provide final answers based on reasoning traces and prompts.
    """

    def __init__(self, query_id:str, task_type: TaskType = TaskType.ANSWERING) -> None:
        self.parse_config()
        self.reasoning_logger = ReasoningLogger(query_id, self.llm.config.llm_id, task_type)
        self.tool_executor = ToolExecutor(
            reasoning_logger=self.reasoning_logger,
            task_type=task_type
            )
        self.prompt_builder = PromptBuilder()
        self.init_prompts(task_type) 
        self.validation_parser = ValidationParser()
        self.step_parser = StepParser(self.tool_executor.tool_names)

    def init_prompts(self, task_type: TaskType):
        """
        sets prompt templates for a given plan and validation steps
        """
        if task_type == TaskType.ANSWERING:
            plan_prompt = ACTION_PROMPT_QA
            val_prompt = VALIDATION_PROMPT_QA
        else:
            plan_prompt = ACTION_PROMPT_LESSON
            val_prompt = VALIDATION_PROMPT_LESSON
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
        logging.info("Exiting agent loop...")
        return self.get_final_response(iteration)

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
        is_final = self.validate()
        return is_final

    def validate(self) -> bool:
        """
        retrieves a validation prompt, runs it through the llm,
        processes the output.

        Returns
        -------
        is_final : bool 
            whether the result is the final answer or not
        """
        validation_prompt = self.get_current_prompt(mode=AgentMode.VAL)
        validation_thought = self.llm.run(validation_prompt, mode=AgentMode.VAL.value)
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
        observation = self.tool_executor.execute(step.action, step.action_input)
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
            return "Reached iterations limit"
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


