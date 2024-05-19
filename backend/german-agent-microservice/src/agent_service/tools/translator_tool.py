import deepl
import os
from agent_service.tools.tool import Tool
class Translator(Tool):
    def __init__(self, target_language:str="RU")->None:
        self.name = "Übersetzer"
        self.description = "Hilfreich, wenn man Text übersetzen möchte"
        self._target_language = target_language
        self.translator = deepl.Translator(os.environ["DEEPL_AUTH_KEY"])

    def run(self, input:str)->str:
        return self.translator.translate_text(
            input, target_lang=self._target_language
            )

    def set_target_language(self, lang:str)->None:
        self._target_language =lang
