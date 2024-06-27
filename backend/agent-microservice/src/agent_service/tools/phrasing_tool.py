from agent_service.tools.tool import Tool


class PhrasingTool(Tool):
    """
    tool to help with phrasing some question/text in German or suggest important vocabulary for some situation
    """

    def __init__(
        self,
        name: str,
        description: str,
        llm: str,
        prompt_id: str,
        prompt_template: str,
        max_tokens: int,
    ) -> None:
        super().__init__(name, description, llm, prompt_id, prompt_template, max_tokens)

    def run(self, input_str: str):
        """
        runs LLM with input.
        """
        self.query = self.prompt.generate_prompt(name_id=self.prompt_id, text=input_str)
        answer = self.llm.run(self.query)
        return answer
