from utils.prompt.reading_generation_prompt import READING_TEMPLATE
from tools import Tool
from agent.llm import LLMBedrock
from utils.prompt.prompt_builder import PromptBuidler

class ReadingGenerator(Tool):
    def __init__(self):
        self.name = "Erstellung von Lesetexten"
        self.description = "Benutzte als Erste zur Erstellung von Lesetexten (keine Hörtexte)."
        self.llm = LLMBedrock()
        self.prompt = PromptBuidler(READING_TEMPLATE)

    def run(self, input:str):
        return self.llm.run(self.prompt.update(text=input))