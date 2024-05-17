from abc import ABC, abstractmethod
from configparser import ConfigParser
from pathlib import Path
from utils.prompt.prompt_builder import PromptBuidler
import boto3
class LLM(ABC):
    @abstractmethod
    def run(prompt: str):
        pass

class LLMBedrock(LLM):
    CONFIG_PATH = Path("src/agent-service/core/llm-config.ini")
    def __init__(self) -> None:
        super().__init__()
        self.parse_config()
        self.client = boto3.client(
                                    service_name=self.service_name, 
                                    region_name=self.region_name,
                                )

    def run(self, prompt: PromptBuidler):
        pass

    def parse_config(self):
        # instantiate
        config = ConfigParser()

        # parse existing file
        config.read(self.CONFIG_PATH)

        self.service_name = config.get("bedrock", "service_name")
        self.region_name = config.get("bedrock", "region_name")
        self.max_tokens = config.getint("bedrock", "max_tokens")
        self.temperature = config.getint("bedrock", "temperature")
        self.model_id = config.get("bedrock", "model_id")
        self.accept = config.get("bedrock", "accept")
        self.contentType = config.get("bedrock", "contentType")
