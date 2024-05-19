from agent_service.tools.translator_tool import Translator
from agent_service.tools.reading_generation_tool import ReadingGenerator
from agent_service.tools.web_search_tool import WebSearch

class ToolFactory:
    def __init__(self, config):
        self.tool_map = {
            'web_search': WebSearch,
            'translator': Translator,
            'reading_generator': ReadingGenerator,
        } # for now implemented tools mapping, 
        # toDo add other tools later to the mapping
        self.config = config
        self.tools = []
        self.tool_names = []
        self.initialize_tools()

    def initialize_tools(self):
        for config_attr, tool_class in self.tool_map.items():
            if getattr(self.config, config_attr, False):
                tool_instance = tool_class()
                self.tools.append(tool_instance)
                self.tool_names.append(tool_instance.name)