import deepl
import os
from agent_service.tools.tool import Tool
from agent_service.prompts.prompt_builder import PromptBuilder
from agent_service.prompts.task_generation_prompt import TRANSLATION_TEMPLATE
class Translator(Tool):
    PROMPT_ID = "translator"
    TEMPLATE = TRANSLATION_TEMPLATE
    def __init__(self, llm, target_language:str="RU")->None:
        self.name = "Übersetzer"
        self.description = "Hilfreich, wenn man Text übersetzen möchte"
        self._target_language = target_language
        self.translator = deepl.Translator(os.environ["DEEPL_AUTH_KEY"])
        self.set_llm(llm)
        self.llm.set_max_tokens(20)
        self.prompt = PromptBuilder()
        self.prompt.create_prompts(
            {self.PROMPT_ID : self.TEMPLATE}
            )

    def run(self, input:str)->str:
        target_language = self.parse_target_language(input)
        print(target_language)
        try:
            answer = str(self.translator.translate_text(
            input, target_lang=target_language
            ))
        except Exception:
            answer = str(self.translator.translate_text(
            input, target_lang=self._target_language
            ))
        return answer

    def parse_target_language(self, input):
            self.query = self.prompt.generate_prompt(name_id=self.PROMPT_ID, 
                                                                text=input)
            target_language = self.llm.run(self.query) 
            target_language = target_language.split("\n")[0].replace("Target language:", "").replace(" ", "")[:2]
            return target_language

    def set_target_language(self, lang:str)->None:
        self._target_language =lang
