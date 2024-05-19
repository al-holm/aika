from agent_service.core.config import Config
from agent_service.core.pydantic_agent import AgentConfigModel
from pydantic import ValidationError
from llm import LLMBedrock
from typing import List
from agent_step import AgentStep
from agent_service.prompts.react_prompt import REACT_PROMPT
from agent_service.prompts.prompt_builder import PromptBuidler
from agent_service.tools.tool_executor import ToolExecutor
from agent_service.parsers.agent_answer_parser import AnswerParser
from agent_service.parsers.agent_step_parser import StepParser
import logging
class Agent:
    def __init__(self) -> None:
        self.parse_config()
        self.reasoning_trace : List[AgentStep] = []
        self.prompt = PromptBuidler(REACT_PROMPT) # variables: tools, tool_names, input, reasoning_trace
        self.tool_executor = ToolExecutor()
        self.answer_parser = AnswerParser()
        self.step_parser = StepParser()

    def take_step(self):
        pass

    def run(self, query:str):
        pass

    def reasoning_trace_to_string(self):
        pass

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


