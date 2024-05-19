from agent_service.tools.tool import Tool
class ToolExecutor:
    def __init__(self) -> None:
        self.tools = None

    def execute(self, tool:Tool, input:str) -> str:
        pass

    def parse_config(self):
        pass #configure tools