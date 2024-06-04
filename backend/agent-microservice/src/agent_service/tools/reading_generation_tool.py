from agent_service.prompts.task_generation_prompt import READING_TEMPLATE
from agent_service.tools.tool import Tool
from agent_service.agent.llm import LLMBedrock
from agent_service.prompts.prompt_builder import PromptBuilder

class ReadingGenerator(Tool):
    """
    a tool for the reading task generation
    """
    PROMPT_ID = "reading"
    TEMPLATE = READING_TEMPLATE
    def __init__(self, llm):
        self.name = "Lesetext erstellen"
        self.description = "Benutzte als Erste zur Erstellung von Lesetexten (NICHT FÜR HÖRTEXTE BENUTZTEN)."
        self.set_llm(llm)
        self.prompt = PromptBuilder()
        self.prompt.create_prompts(
            {self.PROMPT_ID : self.TEMPLATE}
            )

    def run(self, input:str):
        """
        runs LLM with input. 
        """
        self.query = self.prompt.generate_prompt(name_id=self.PROMPT_ID, text=input)
        answer = self.llm.run(self.query)
        return answer