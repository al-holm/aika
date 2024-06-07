from agent_service.prompts.tool_prompt import LISTENING_TEMPLATE
from agent_service.prompts.prompt_builder import PromptBuilder
from agent_service.tools.tool import Tool
import uuid, os

class ListeningGenerator(Tool):
    """
    a tool for the listening task generation
    """
    def __init__(self, name: str, description: str, llm: str, 
                    prompt_id: str, prompt_template: str, max_tokens:int) -> None:
        super().__init__(name, description, llm, prompt_id, prompt_template, max_tokens)


    def run(self, input:str):
        """
        runs LLM to get an answer,
        is the entry point for using the tool from the outside
        """
        self.query = self.prompt.generate_prompt(name_id=self.prompt_id, text=input)
        answer = self.llm.run(self.query)
        filepath = "out/audio/" + str(uuid.uuid4()) + ".txt"
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf8') as file:
            file.write(answer)
        return answer