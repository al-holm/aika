from agent_service.tools.tool import Tool
from agent_service.prompts.task_generation_prompt import PHRASING_TEMPLATE
from agent_service.prompts.prompt_builder import PromptBuilder

class PhrasingTool(Tool):
    PROMPT_ID = "phrasing"
    TEMPLATE = PHRASING_TEMPLATE
    def __init__(self, llm):
        self.name = "Vokabeln und Formulierungshilfe"
        self.description = "Hilfreich, wenn man ein Formulierungsbeispiel oder wichtige Vokabeln zu einem Thema braucht.\.\nAction Input Format: Muster/Vokabeln/Verben, das Thema."
        self.set_llm(llm)
        self.llm.set_max_tokens(200)
        self.prompt = PromptBuilder()
        self.prompt.create_prompts(
            {self.PROMPT_ID : self.TEMPLATE}
            )

    def run(self, input_str: str):
        self.query = self.prompt.generate_prompt(name_id=self.PROMPT_ID, 
                                                     text=input_str)
        answer = self.llm.run(self.query) 
        return answer
 