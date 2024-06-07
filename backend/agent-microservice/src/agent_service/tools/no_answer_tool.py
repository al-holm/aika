from agent_service.tools.tool import Tool

class NoAnswerTool(Tool):
    def __init__(self, name: str, description: str, llm: str, 
                    prompt_id: str, prompt_template: str, max_tokens:int) -> None:
        super().__init__(name, description, llm, prompt_id, prompt_template, max_tokens)

    def run(self, input_str: str):
        return "Deine Frage kann ich leider nicht beantworten. Ich beantworte nur Fragen zum Deutschlernen."
 