from agent_service.core.config import Config
from agent_service.core.pydantic_agent import AgentConfigModel
from agent_service.agent.agent_step import AgentStep
from pydantic import ValidationError
from agent_service.agent.llm import LLMBedrock
from agent_service.prompts.react_prompt import REACT_PROMPT
from agent_service.prompts.final_answer_prompt import VALIDATION_PROMPT
from agent_service.agent.reasoning_trace import ReasoningTrace
from agent_service.prompts.prompt_builder import PromptBuidler
from agent_service.tools.tool_executor import ToolExecutor
from agent_service.parsers.agent_answer_parser import ValidationParser
from agent_service.parsers.agent_step_parser import StepParser
import logging

class Agent:
    def __init__(self) -> None:
        self.parse_config()
        self.reasoning_trace = ReasoningTrace()
        self.tool_executor = ToolExecutor()
        self.tool_executor.reasoning_trace = self.reasoning_trace
        self.prompt_builder_action = PromptBuidler(REACT_PROMPT) # variables: tools, tool_names, input, reasoning_trace
        self.prompt_builder_final_answer = PromptBuidler(VALIDATION_PROMPT)
        self.validation_parser = ValidationParser()
        self.step_parser = StepParser(self.tool_executor.tool_names)

    def run(self, query:str):
        self.set_prompts_for_query(query)
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
        return self.get_final_response(iteration)

    def take_step(self):
        step = self.plan()
        self.execute_step(step)
        is_final = self.validate()
        return is_final

    def validate(self):
        validation_prompt = self.prepare_validation_prompt()
        validation_thought = self.llm.run(validation_prompt, "val")
        is_final = self.process_validation_answer(validation_thought)
        return is_final

    def plan(self) -> AgentStep:
        self.prepare_prompts()
        current_prompt = self.get_current_prompt()
        llm_answer = self.llm.run(current_prompt)
        step = self.step_parser.parse_step(llm_answer)
        return step

    def process_validation_answer(self, val_answer):
        self.parse_validation_answer(val_answer)
        if "Antwort ist vorhanden" in val_answer:
            is_final = True
        else:
            is_final = False
        return is_final

    def parse_validation_answer(self, val_answer):
        val_answer = self.validation_parser.parse_step(val_answer)
        self.reasoning_trace.add_step(val_answer)

    def execute_step(self, step):
        observation = self.tool_executor.execute(step.action, step.action_input)
        step.observation = observation
        self.reasoning_trace.add_step(step)

    def prepare_validation_prompt(self):
        reasoning_steps = self.reasoning_trace.toString()
        final_answer_prompt = self.prompt_builder_final_answer.update(reasoning_trace=reasoning_steps)
        return final_answer_prompt

    def get_current_prompt(self):
        reasoning_steps = self.reasoning_trace.toString()
        current_prompt = self.prompt_builder_action.update(reasoning_trace=reasoning_steps)
        return current_prompt

    def prepare_prompts(self):
        self.prompt_builder_action.set_prompt(self.user_prompt) 
        self.prompt_builder_final_answer.set_prompt(self.final_prompt)
    
    def get_final_response(self, iteration: int):
        self.reasoning_trace.to_json()
        if iteration == self.max_iterations:
            return "Reached iterations limit"
        self.reasoning_trace.get_final_answer()
        final_answer = self.reasoning_trace.get_last_step().final_answer
        logging.info(final_answer)
        return final_answer

    def set_prompts_for_query(self, query):
        self.user_prompt = self.prompt_builder_action.update(
            tools=self.tool_executor.toolstoString(),
            tool_names=self.tool_executor.tool_names,
            input=query
        )
        self.final_prompt = self.prompt_builder_final_answer.update(
            input=query, tools=self.tool_executor.toolstoString()
        )
        self.reasoning_trace.set_query(query)

    def parse_config(self):
        try:
            config = Config("agent")
            settings = config.get_settings()

            self.config = AgentConfigModel(**settings)
            if self.config.llm=='bedrock':
                self.llm = LLMBedrock()
            self.max_iterations = self.config.max_iterations
        except ValidationError as e:
            logging.ERROR(f'Agent attributes error: {e}')


