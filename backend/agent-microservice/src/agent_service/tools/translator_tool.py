import deepl
import os
from agent_service.tools.tool import Tool
from agent_service.prompts.prompt_builder import PromptBuilder
from agent_service.prompts.tool_prompt import TRANSLATION_TEMPLATE
class Translator(Tool):
    """
    A tool for translating text using the DeepL API.
    """
    def __init__(self, name: str, description: str, llm: str, 
                    prompt_id: str, prompt_template: str, max_tokens:int) -> None:
        super().__init__(name, description, llm, prompt_id, prompt_template, max_tokens)
        self.description += """
        Beispiele: 
        Как я могу сказать "Меня зовут Али" по-немецки?
        Action: Übersetzer
        Action Input: Меня зовут Али - [DE]

        Перекладіть "Ich habe heute eine Katze gesehen".
        Action: Übersetzer
        Action Input: Ich habe heute eine Katze gesehen - [UK]

        """
        self.translator = deepl.Translator(os.environ["DEEPL_AUTH_KEY"])

    def run(self, input:str)->str:
        """
        Runs the translation tool with the provided input.
        """
        target_language = self.parse_target_language(input)
        if target_language=="":
            answer="Du hast das falsche Format als Action Input gegeben. Bitte benutzte das Action Input Format: der zu übersetzende Text in der Originalsprache - [DE/RU/EN/TR/AR]"
        else:
            input = input.split("- [")[0]
            answer = str(self.translator.translate_text(
            input, target_lang=target_language
            ))
            answer = 'Die Übersetztung lautet:\n' + answer
        return answer

    def parse_target_language(self, input):
        """
        Parses the target language from the input string. 
        """
        try:
            lang = input.split("[")[1].split("]")[0]
            lang = str.lower(lang)
            if lang in ["de", "ru", "tr", "uk", "ar", "en"]:
                if lang == "en":
                    lang = "en-us" # using the us english for deepl
                return lang
        except Exception:
            pass
        return ""
