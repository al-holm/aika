from agent_service.core.config import Config
from agent_service.core.pydantic_agent import AgentConfigModel
from agent_service.agent.agent_step import AgentStep
from pydantic import ValidationError
from agent_service.agent.llm import LLMBedrock
from agent_service.prompts.react_prompt import REACT_PROMPT
from agent_service.prompts.final_answer_prompt import VALIDATION_PROMPT, VAL_STOP_PREFIX
from agent_service.agent.reasoning_trace import ReasoningTrace
from agent_service.prompts.prompt_builder import PromptBuilder
from agent_service.tools.tool_executor import ToolExecutor
from agent_service.parsers.agent_step_parser import StepParser, ValidationParser
import logging

# The `Agent` class represents a ReAct agent that can plan actions, execute steps using tools, 
# validate results, and provide final answers based on reasoning traces and prompts.
class Agent:
    PLAN = "plan"
    VAL = "validate"
    def __init__(self) -> None:
        self.parse_config()
        self.reasoning_trace = ReasoningTrace()
        self.tool_executor = ToolExecutor(self.reasoning_trace)
        self.prompt_builder = PromptBuilder()
        self.init_prompts() 
        self.validation_parser = ValidationParser()
        self.step_parser = StepParser(self.tool_executor.tool_names)

    def init_prompts(self):
        '''The `init_prompts` function sets prompt templates for a given plan and validation steps
        
        '''
        self.prompt_builder.create_prompts(
            {
                self.PLAN : REACT_PROMPT,
                self.VAL : VALIDATION_PROMPT
            }
        )

    def run(self, query:str)->str:
        '''runs an agent loop for a specified number of iteration
        
        '''
        self.set_prompts_for_query(query)
        logging.info("Entering agent loop...")
        iteration = 0
        while iteration < self.max_iterations:
            try:
                is_final = self.take_step()
                if is_final:
                    break
            except Exception as e:
                logging.error(e)
                self.reasoning_trace.add_exception(str(e))
            iteration += 1
        logging.info("Exiting agent loop...")
        return self.get_final_response(iteration)

    def take_step(self) -> bool:
        '''plans an action, executes a planned step, validates the result, and returns a boolean
        indicating if it is the final step.
        
        '''
        step = self.plan()
        self.execute_step(step)
        is_final = self.validate()
        return is_final

    def validate(self) -> bool:
        '''retrieves a validation prompt, runs it through a llm,
        processes the output, and returns a boolean indicating indicating if it is the final step.
        
        '''
        validation_prompt = self.get_current_prompt(mode="val")
        validation_thought = self.llm.run(validation_prompt, mode="val")
        is_final = self.process_validation_thought(validation_thought)
        return is_final

    def plan(self) -> AgentStep:
        '''retrieves the current prompt, runs it through a llm, parses the
        output, and returns a AgentStep.
        
        '''
        current_prompt = self.get_current_prompt(mode="plan")
        llm_answer = self.llm.run(current_prompt)
        step = self.step_parser.parse_step(llm_answer)
        return step

    def process_validation_thought(self, val_answer:str) -> bool:
        '''parses a validation step, adds it to a reasoning trace
        
        Parameters
        ----------
        val_answer : str
            val_answer is a string & represents the answer provided during a validation process.
        
        Returns
        -------
            a boolean indicating if the final answer can be derived from the reasoning trace.
        '''
        val_step = self.validation_parser.parse_step(val_answer)
        self.reasoning_trace.add_step(val_step)

        if VAL_STOP_PREFIX in val_step.validation_thought:
            return True
        else:
            return False

    def execute_step(self, step:AgentStep)->None:
        '''takes an `AgentStep` object, executes an action using a tool
        executor, updates the observation in the step, and adds the step to a reasoning trace.
        
        '''
        observation = self.tool_executor.execute(step.action, step.action_input)
        step.observation = observation
        self.reasoning_trace.add_step(step)

    
    def get_current_prompt(self, mode="plan"):
        '''returns a prompt with a reasoning trace based on the specified mode.
        
        Parameters
        ----------
        mode, optional
             to determine which type of prompt to generate.
        
        '''
        reasoning_steps = str(self.reasoning_trace)
        if mode=="val":
            name_id = self.VAL
        elif mode=="plan":
            name_id = self.PLAN
        else:
            raise NotImplementedError
        current_prompt = self.prompt_builder.generate_prompt(name_id=name_id,
                                                             reasoning_trace=reasoning_steps)
        return current_prompt

    
    def get_final_response(self, iteration: int) -> str:
        ''' returns the final answer
        Parameters
        ----------
        iteration : int
            the final iteration number after exiting the run loop.
        
        '''
        if iteration == self.max_iterations:
            return "Reached iterations limit"
        self.reasoning_trace.build_final_answer()
        self.reasoning_trace.to_json()
        final_answer = self.reasoning_trace.final_answer
        logging.info(final_answer)
        return final_answer

    def set_prompts_for_query(self, query:str) -> None:
        '''updates prompts with a query and availiable tools
        
        '''
        update = {
            "tools": str(self.tool_executor),
            "tool_names": self.tool_executor.tool_names,
            "input": query
        } 

        self.prompt_builder.update_prompt(
            name_id=self.PLAN,
            **update
        )
        
        self.prompt_builder.update_prompt(
            name_id=self.VAL,
            **update
        )
        self.reasoning_trace.set_query(query)

    def parse_config(self) -> None:
        '''reads settings from a configuration file, creates an pydantic validation `AgentConfigModel` object, 
        and sets additional attributes based on the configuration.
        
        '''
        try:
            config = Config("agent")
            settings = config.get_settings()

            self.config = AgentConfigModel(**settings)
            if self.config.llm=='bedrock':
                self.llm = LLMBedrock()
            self.max_iterations = self.config.max_iterations
        except ValidationError as e:
            logging.ERROR(f'Agent attributes error: {e}')


