from configparser import ConfigParser
from pathlib import Path
from llm import LLMBedrock
from typing import List
from agent_step import AgentStep
from agent_service.prompts.react_prompt import REACT_PROMPT
from agent_service.prompts.prompt_builder import PromptBuidler
from agent_service.tools.tool_executor import ToolExecutor
from agent_service.parsers.agent_answer_parser import AnswerParser
from agent_service.parsers.agent_step_parser import StepParser

class Agent:
    CONFIG_PATH = Path("/backend/german_agent_microservice/src/core/llm-config.ini")
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
        # instantiate
        config = ConfigParser()

        # parse existing file
        config.read(self.CONFIG_PATH)

        llm = config.get("agent", "llm")
        if llm=='bedrock':
            self.llm = LLMBedrock()
        self.max_iterations = config.getint("agent", "max_iterations")


