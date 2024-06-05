import deepl
import os
from agent_service.tools.tool import Tool
from agent_service.prompts.prompt_builder import PromptBuilder
from agent_service.prompts.tool_prompt import TRANSLATION_TEMPLATE
class Translator(Tool):
    PROMPT_ID = "translator"
    TEMPLATE = TRANSLATION_TEMPLATE
    def __init__(self, llm, target_language:str="RU")->None:
        self.name = "Übersetzer"
        self.description = """
        Hilfreich bei der Übersetzung von Texten. Verfügbare Sprachen: Deutsch [DE], Russisch [Ru], Englisch [EN], Türkisch [TR], Arabisch [AR], Ukrainisch [UK].
        Action Input Format: der zu übersetzende Text in der Originalsprache - [DE/RU/EN/TR/AR/UK]
        Beispiele: 
        Как я могу сказать "Меня зовут Али" по-немецки?
        Action: Übersetzer
        Action Input: Меня зовут Али - [DE]

        Перекладіть "Ich habe heute eine Katze gesehen".
        Action: Übersetzer
        Action Input: Ich habe heute eine Katze gesehen - [UK]

        """
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
        if target_language=="":
            answer="Du hast das falsche Format als Action Input gegeben. Bitte benutzte das Action Input Format: der zu übersetzende Text in der Originalsprache - [DE/RU/EN/TR/AR]"
        else:
            input = input.split("- [")[0]
            answer = str(self.translator.translate_text(
            input, target_lang=target_language
            ))
        return answer

    def parse_target_language(self, input):
        lang = input.split("[")[1].split("]")[0]
        if str.lower(lang) in ["de", "ru", "tr", "uk", "ar", "en"]:
            if str.lower(lang) == "en":
                lang = "en-us"
            return lang
        else:
            return ""

    def set_target_language(self, lang:str)->None:
        self._target_language =lang
