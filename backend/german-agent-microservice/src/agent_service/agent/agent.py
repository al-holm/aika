from agent_service.core.config import Config
from agent_service.core.pydantic_agent import AgentConfigModel
from pydantic import ValidationError
from agent_service.agent.llm import LLMBedrock
from typing import List
from agent_service.agent.agent_step import AgentStep
from agent_service.prompts.react_prompt import REACT_PROMPT
from agent_service.agent.reasoning_trace import ReasoningTrace
from agent_service.prompts.prompt_builder import PromptBuidler
from agent_service.tools.tool_executor import ToolExecutor
from agent_service.parsers.agent_answer_parser import AnswerParser
from agent_service.parsers.agent_step_parser import StepParser
import logging
class Agent:
    def __init__(self) -> None:
        self.parse_config()
        self.reasoning_trace = ReasoningTrace()
        self.tool_executor = ToolExecutor()
        self.prompt_builder = PromptBuidler(REACT_PROMPT) # variables: tools, tool_names, input, reasoning_trace
        self.answer_parser = AnswerParser()
        print(self.tool_executor.tool_names)
        self.step_parser = StepParser(self.tool_executor.tool_names)

    def take_step(self):
        self.prompt_builder.set_prompt(self.user_prompt) 
        current_prompt = self.prompt_builder.update(reasoning_trace=self.reasoning_trace.toString())
        llm_answer = self.llm.run(current_prompt)
        step = self.step_parser.parse_step(llm_answer)
        print(step.action_input)
        print(step.toString())
        observation = self.tool_executor.execute(step.action, step.action_input)
        step.observation = observation
        return step.toString()
        #return is_final, current_step

    def run(self, query:str):
        self.user_prompt = self.prompt_builder.update(
            tools=self.tool_executor.toolstoString,
            tool_names=self.tool_executor.tool_names,
            input=query
        )
        iteration = 0
        while iteration < self.max_iterations:
            answer = self.take_step()
            break
        return answer

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


