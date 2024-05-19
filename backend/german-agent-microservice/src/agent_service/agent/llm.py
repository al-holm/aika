from abc import ABC, abstractmethod
from configparser import ConfigParser
from pathlib import Path
import boto3
import json
from dotenv import load_dotenv
load_dotenv()
class LLM(ABC):
    @abstractmethod
    def run(prompt: str):
        pass

class LLMBedrock(LLM):
    CONFIG_PATH = Path("/Users/ali/Desktop/code/aika/backend/german_agent_microservice/src/agent_service/core/llm-config.ini")
    def __init__(self) -> None:
        super().__init__()
        self.parse_config()
        self.client = boto3.client(
                                    service_name=self.service_name, 
                                    region_name=self.region_name,
                                )

    def run(self, prompt: str):
        """
        This Python function takes a prompt, retrieves the body, invokes a model with the body, and
        returns the text output from the model response.
        """
        body = self.get_body(prompt)
        response = self.client.invoke_model(
            body=body, modelId=self.model_id, 
            accept=self.accept, contentType=self.contentType
            )

        response_body = json.loads(response.get('body').read())
        return response_body['outputs'][0]['text']

    def get_body(self, prompt:str):
        """
        The `get_body` function returns a JSON object with a prompt, max tokens, and temperature.
        """
        return json.dumps({
            "prompt": prompt,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            }
        )

    def parse_config(self):
        # instantiate
        config = ConfigParser()

        # parse existing file
        config.read(self.CONFIG_PATH)

        self.service_name = config.get("bedrock", "service_name")
        self.region_name = config.get("bedrock", "region_name")
        self.max_tokens = config.getint("bedrock", "max_tokens")
        self.temperature = config.getfloat("bedrock", "temperature")
        self.model_id = config.get("bedrock", "model_id")
        self.accept = config.get("bedrock", "accept")
        self.contentType = config.get("bedrock", "contentType")
