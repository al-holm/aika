from agent_service.prompts.reading_generation_prompt import READING_TEMPLATE
from agent_service.tools.tool import Tool
from agent_service.agent.llm import LLMBedrock
from agent_service.prompts.prompt_builder import PromptBuidler
import logging 
class ReadingGenerator(Tool):
    def __init__(self):
        self.name = "Lesetext erstellen"
        self.description = "Benutzte als Erste zur Erstellung von Lesetexten (keine Hörtexte)."
        self.llm = LLMBedrock()
        self.prompt = PromptBuidler(READING_TEMPLATE)
        self.logger = logging.getLogger('ReadingGenerator')

    def run(self, input:str):
        self.query = self.prompt.update(text=input)
        answer = self.llm.run(self.query)
        self.logger.info(answer)
        return answer