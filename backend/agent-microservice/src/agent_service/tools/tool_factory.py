from agent_service.tools.translator_tool import Translator
from agent_service.tools.reading_generation_tool import ReadingGenerator
from agent_service.tools.web_search_tool import WebSearch
from agent_service.tools.listening_generation_tool import ListeningGenerator
from agent_service.tools.task_generation_tool import TaskGenerator
from agent_service.tools.phrasing_tool import PhrasingTool
from agent_service.tools.no_answer_tool import NoAnswerTool
from agent_service.core.pydantic_tool import ToolConfigModel
from agent_service.core.config import Config
from agent_service.prompts.tool_prompt import (
    READING_TEMPLATE,
    LISTENING_TEMPLATE,
    TASK_TEMPLATE,
    WEB_SUMMARY_TEMPLATE,
    TRANSLATION_TEMPLATE,
    PHRASING_TEMPLATE,
    RETRIEVER_TEMPLATE,
)
from pydantic import ValidationError
import logging


class ToolFactory:
    """
    initializes tools based on configuration attributes and adds them to the tools list.
    """

    def __init__(self, config):
        self.tool_map = {
            "web_search": (WebSearch, WEB_SUMMARY_TEMPLATE),
            "translator": (Translator, TRANSLATION_TEMPLATE),
            "listening_generator": (ListeningGenerator, LISTENING_TEMPLATE),
            "reading_generator": (ReadingGenerator, READING_TEMPLATE),
            "task_generator": (TaskGenerator, TASK_TEMPLATE),
            "phrasing_tool": (PhrasingTool, PHRASING_TEMPLATE),
            "retriever": (WebSearch, RETRIEVER_TEMPLATE),
            "no_answer": (NoAnswerTool, ""),
        }
        self.config = config
        self.tools = []
        self.tool_names = []
        self.initialize_tools()

    def initialize_tools(self):
        """
        initializes tools based on configuration attributes and adds them to
        the tools list.
        """
        for config_attr, map_set in self.tool_map.items():
            if getattr(self.config, config_attr, False):
                tool_class, prompt_template = map_set
                config = self.parse_config(config_attr)
                name, description = config.name, config.description
                llm, prompt_id, max_tokens = (
                    config.llm,
                    config.prompt_id,
                    config.max_tokens,
                )
                tool_instance = tool_class(
                    name, description, llm, prompt_id, prompt_template, max_tokens
                )
                self.tools.append(tool_instance)
                self.tool_names.append(tool_instance.name)
        logging.info(f"Created following tools: {self.tool_names}")

    def parse_config(self, tool_name):
        """
        reads settings from a configuration file and creates a
        ToolConfigModel object.
        """
        try:
            config = Config(f"tool-{tool_name}")
            settings = config.get_settings()
            config = ToolConfigModel(**settings)
        except ValidationError as e:
            logging.error(f"Tool attributes error {e}")
            config = {}
        return config
