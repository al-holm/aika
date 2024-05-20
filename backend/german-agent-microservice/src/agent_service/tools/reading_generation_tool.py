from agent_service.prompts.task_generation_prompt import READING_TEMPLATE
from agent_service.tools.tool import Tool
from agent_service.agent.llm import LLMBedrock
from agent_service.prompts.prompt_builder import PromptBuidler
class ReadingGenerator(Tool):
    def __init__(self):
        self.name = "Lesetext erstellen"
        self.description = "Benutzte als Erste zur Erstellung von Lesetexten (NICHT FÜR HÖRTEXTE BENUTZTEN)."
        self.llm = LLMBedrock()
        self.prompt = PromptBuidler(READING_TEMPLATE)

    def run(self, input:str):
        self.query = self.prompt.update(text=input)
        answer = self.llm.run(self.query)
        return answer