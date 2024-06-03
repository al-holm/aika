from agent_service.tools.tool import Tool
from agent_service.agent.agent_step import AgentStep
from agent_service.agent.reasoning_trace import ReasoningLogger
from agent_service.tools.tool_factory import ToolFactory
from agent_service.core.config import Config
from agent_service.core.pydantic_tool_exe import ToolExecutorConfigModel
from pydantic import ValidationError
import logging
from typing import List
from agent_service.agent.task_type import TaskType
class ToolExecutor:
    """
    is responsible for executing tools based on user input and configuration settings (tool list).
    """
    def __init__(self, reasoning_logger:ReasoningLogger, task_type:TaskType) -> None:
        self.parse_config(task_type)
        self.task_type = task_type
        self.reasoning_logger = reasoning_logger
        self.factory = ToolFactory(self.config)
        self.tools: List[Tool] = self.factory.tools
        self.tool_names: List[str] = self.factory.tool_names
        self.logger = logging.getLogger("Observation")

    def execute(self, tool_name:str, input_str:str) -> str:
        """
        executes a specified tool with a given input 
        and returns the observation or an error message if the tool or the input is invalid.
        """
        if self.task_type == TaskType.LESSON:
            input_str = input_str + "[" + self.add_trace_for_task_generation(tool_name, input_str) + "]"
        try:
            tool = self.get_tool_by_name(tool_name)
            observation = tool.run(input_str)
        except ValueError as e:
            observation = "Invalid tool or tool input"
        self.logger.info("Observation: " + observation)
        return observation

    def add_trace_for_task_generation(self, tool_name, input):
        if  "Deutschaufgaben generieren" in tool_name:
            for i in reversed(self.reasoning_logger.trace):
                if isinstance(i, AgentStep):
                    if "Lese" in i.action or "Hör" in i.action or "Web-Suche" in i.action:
                        logging.info(f"add_trace_for_task_generation: action {i.action}, observation {i.observation}")
                        
                        input=i.observation
                        break
        return input

    def get_tool_by_name(self, name:str)->Tool:
        """
        searches for a tool by name in the tools list and returns the tool if found.
        """
        for tool in self.tools:
            if tool.name==name:
                return tool
        return ValueError
    
    def __str__(self) -> str:
        res = "Tools:\n"
        for tool in self.tools:
            res += str(tool)
            res += "\n"
        return res

    
    def parse_config(self, task_type:TaskType):
        """
        reads settings from a configuration file and creates a
        ToolExecutorConfigModel object.
        """
        try:
            config = Config(f"tool-exe-{task_type.value}")
            settings = config.get_settings()
            self.config = ToolExecutorConfigModel(**settings)
        except ValidationError as e:
            logging.error(f"Tool attributes error {e}")

        

