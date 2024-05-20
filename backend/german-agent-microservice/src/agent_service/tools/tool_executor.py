from agent_service.tools.tool import Tool
from agent_service.agent.agent_step import AgentStep
from agent_service.tools.tool_factory import ToolFactory
from agent_service.core.config import Config
from agent_service.core.pydantic_tool_exe import ToolExecutorConfigModel
from pydantic import ValidationError
import logging
from typing import List
# The `ToolExecutor` class is responsible for executing tools based on user input and configuration
# settings (tool list).
class ToolExecutor:
    def __init__(self) -> None:
        self.parse_config()
        self.factory = ToolFactory(self.config)
        self.tools: List[Tool] = self.factory.tools
        self.tool_names: List[str] = self.factory.tool_names
        self.logger = logging.getLogger("Observation")

    def execute(self, tool_name:str, input:str) -> str:
        '''The function executes a specified tool with a given input 
        and returns the observation or anerror message if the tool or input is invalid.
        
        '''
        if  "Aufgaben zu einem Text" in tool_name:
            for i in reversed(self.reasoning_trace.steps):
                if isinstance(i, AgentStep):
                    if "Lese" or "Hör" in i.action:
                        input=i.observation
                        break
        try:
            tool = self.get_tool_by_name(tool_name)
            observation = tool.run(input)
        except ValueError as e:
            observation = "Invalid tool or tool input"
        self.logger.info("Observation: " + observation)
        return observation

    def get_tool_by_name(self, name:str)->Tool:
        '''The function `get_tool_by_name` searches for a tool by name in a list of tools and returns the
        tool if found.
        
        '''
        for tool in self.tools:
            if tool.name==name:
                return tool
        return ValueError
    
    def toolstoString(self) -> str:
        res = "Tools:\n"
        for tool in self.tools:
            res += tool.toString()
            res += "\n"
        return res

    
    def parse_config(self):
        '''The function `parse_config` reads settings from a configuration file and creates a
        `ToolExecutorConfigModel` object.
        
        '''
        try:
            config = Config("tool-exe")
            settings = config.get_settings()
            self.config = ToolExecutorConfigModel(**settings)
        except ValidationError as e:
            logging.error(f"Tool attributes error {e}")

        

