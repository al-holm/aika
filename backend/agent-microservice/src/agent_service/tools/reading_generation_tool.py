from agent_service.prompts.tool_prompt import READING_TEMPLATE
from agent_service.tools.tool import Tool
from agent_service.prompts.prompt_builder import PromptBuilder

class ReadingGenerator(Tool):
    """
    a tool for the reading task generation
    """
    def __init__(self, name: str, description: str, llm: str, 
                    prompt_id: str, prompt_template: str, max_tokens:int) -> None:
        super().__init__(name, description, llm, prompt_id, prompt_template, max_tokens)

    def run(self, input:str):
        """
        runs LLM with input. 
        """
        self.query = self.prompt.generate_prompt(name_id=self.prompt_id, text=input)
        answer = self.llm.run(self.query)
        return answer