from agent_service.tools.translator_tool import Translator
from agent_service.tools.reading_generation_tool import ReadingGenerator
from agent_service.tools.web_search_tool import WebSearch
from agent_service.tools.listening_generation_tool import ListeningGenerator
from agent_service.tools.task_generation_tool import TaskGenerator
# The ToolFactory class initializes tools based on configuration attributes and adds them to a tool
# list.
class ToolFactory:
    def __init__(self, config):
        self.tool_map = {
            'web_search': WebSearch,
            'translator': Translator,
            'listening_generator':ListeningGenerator,
            'reading_generator': ReadingGenerator,
            'task_generator':TaskGenerator
        } # for now implemented tools mapping, 
        # toDo add other tools later to the mapping
        self.config = config
        self.tools = []
        self.tool_names = []
        self.initialize_tools()

    def initialize_tools(self):
        '''The `initialize_tools` function initializes tools based on configuration attributes and adds them to
        a tool list.
        
        '''
        for config_attr, tool_class in self.tool_map.items():
            if getattr(self.config, config_attr, False):
                tool_instance = tool_class()
                self.tools.append(tool_instance)
                self.tool_names.append(tool_instance.name)