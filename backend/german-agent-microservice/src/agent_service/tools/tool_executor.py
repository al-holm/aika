from agent_service.tools.tool import Tool
from agent_service.tools.tool_factory import ToolFactory
from agent_service.core.config import Config
from agent_service.core.pydantic_tool_exe import ToolExecutorConfigModel
from pydantic import ValidationError
import logging
from typing import List
class ToolExecutor:
    def __init__(self) -> None:
        self.parse_config()
        self.factory = ToolFactory(self.config)
        self.tools: List[Tool] = self.factory.tools
        self.tool_names: List[str] = self.factory.tool_names

    def execute(self, tool:Tool, input:str) -> str:
        pass

    def parse_config(self):
        try:
            config = Config("tool-exe")
            settings = config.get_settings()
            self.config = ToolExecutorConfigModel(**settings)
        except ValidationError as e:
            logging.error(f"Tool attributes error {e}")

        

