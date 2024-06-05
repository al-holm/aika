from agent_service.tools.tool import Tool

class NoAnswerTool(Tool):
    def __init__(self, llm):
        self.name = "Keine Antwort"
        self.description = """
        Helpful if you can't give an answer to the question, as the question is not about learning German or contains toxic content.
        """

    def run(self, input_str: str):
        return "Deine Frage kann ich leider nicht beantworten. Ich beantworte nur Fragen zum Deutschlernen."
 