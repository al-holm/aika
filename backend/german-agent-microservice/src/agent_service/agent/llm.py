from abc import ABC, abstractmethod
from pydantic import ValidationError
import logging, os
import boto3
import json
from dotenv import load_dotenv
from agent_service.core.config import Config
from agent_service.core.pydantic_llm import BedrockLLMConfigModel, RunpodLLMConfigModel
import requests

load_dotenv()

class LLM(ABC):
    """
    an abstract base class for running LLM with the run method that takes a prompt as input.
    """
    @abstractmethod
    def run(prompt: str):
        """
        an abstract method that every child class must implement
        takes a prompt and returns the text output from the model response
        Parameters
        ----------
        prompt : str
        """
        pass

    def set_max_tokens_by_mode(self, mode="plan"):
        if mode != "plan":
            self.max_tokens = 90
        else:
            self.max_tokens = 512
    
    def set_max_tokens(self, max_tokens:int):
        self.max_tokens = max_tokens


# The `LLMBedrock` class is a Python class that extends `LLM`, initializes configuration settings, and
# provides methods to run a language model using AWS Bedrock and retrieve the model response.
class LLMBedrock(LLM):
    """
    a child class of LLM
    initializes configuration settings and
    provides methods to run a language model using AWS Bedrock and retrieve the model response.
    """
    def __init__(self) -> None:
        super().__init__()
        self.parse_config()
        self.max_tokens = self.config.max_tokens
        self.client = boto3.client(
                                    service_name=self.config.service_name, 
                                    region_name=self.config.region_name,
                                )

    def run(self, prompt: str, mode="plan"):
        """
        takes a prompt, retrieves the body, invokes a model with the body, and
        returns the text output from the model response.
        """
        self.set_max_tokens_by_mode(mode)
        body = self.get_body(prompt)
        response = self.client.invoke_model(
            body=body, modelId=self.config.llm_id, 
            accept=self.config.accept, contentType=self.config.content_type
            )

        response_body = json.loads(response.get('body').read())
        return response_body['outputs'][0]['text']

    def get_body(self, prompt:str):
        """
        returns a JSON object with a prompt, max tokens, and temperature.
        """
        return json.dumps({
            "prompt": prompt,
            "max_tokens": self.max_tokens,
            "temperature": self.config.temperature,
            }
        )

    def parse_config(self):
        """
        reads settings from a configuration file (*.ini), 
        validates types, creates a pydantic model object config with those settings.
        """
        try:
            config = Config("llm-bedrock")
            settings = config.get_settings()
            self.config = BedrockLLMConfigModel(**settings) # parse & validate dict from config, create attributes
        except ValidationError as e:
            logging.ERROR(f'Bedrock attributes error: {e}')


class LLMRunPod(LLM):
    """
    a child class of LLM
    provides methods to run a language model using RunPod Cloud GPU and retrieve the model response.
    """
    def __init__(self) -> None:
        super().__init__()
        self.parse_config()
        self.max_tokens = self.config.max_tokens
        self.temperature = self.config.temperature
        self.config.llm_id = self.config.llm_id
        self.url = os.environ['RUNPOD_URL']


    def run(self, prompt: str, mode="plan"):
        """
        takes a prompt, retrieves the body, invokes a model with the body, and
        returns the text output from the model response.
        """
        self.set_max_tokens_by_mode(mode)
        
        data = {
            "model": self.llm_id,
            "prompt": prompt,
            "stream": False,
            "options": {
                'temperature' : self.temperature,
            }
        }

        response = requests.post(self.url, json=data)    
        return response.json()["response"]
    
    def parse_config(self):
        """
        reads settings from a configuration file (*.ini), 
        validates types, creates a pydantic model object config with those settings.
        """
        try:
            config = Config("llm-runpod")
            settings = config.get_settings()
            self.config = RunpodLLMConfigModel(**settings) # parse & validate dict from config, create attributes
        except ValidationError as e:
            logging.ERROR(f'Bedrock attributes error: {e}')

