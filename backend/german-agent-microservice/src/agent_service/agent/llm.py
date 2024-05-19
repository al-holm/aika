from abc import ABC, abstractmethod
from pydantic import ValidationError
import logging
import boto3
import json
from dotenv import load_dotenv
from agent_service.core.config import Config
from agent_service.core.pydantic_llm import BedrockLLMConfigModel
load_dotenv()
# The class LLM is an abstract base class for running LLM with a method run that takes a prompt as input.
class LLM(ABC):
    @abstractmethod
    def run(prompt: str):
        '''The function "run" takes a prompt as input and does not perform any specific actions.
        Parameters
        ----------
        prompt : str
            The `run` function takes a single parameter `prompt` of type `str`.
        '''
        pass

# The `LLMBedrock` class is a Python class that extends `LLM`, initializes configuration settings, and
# provides methods to run a language model using AWS Bedrock and retrieve the model response.
class LLMBedrock(LLM):
    def __init__(self) -> None:
        super().__init__()
        self.parse_config()
        self.client = boto3.client(
                                    service_name=self.config.service_name, 
                                    region_name=self.config.region_name,
                                )

    def run(self, prompt: str):
        """
        This Python function takes a prompt, retrieves the body, invokes a model with the body, and
        returns the text output from the model response.
        """
        body = self.get_body(prompt)
        response = self.client.invoke_model(
            body=body, modelId=self.config.llm_id, 
            accept=self.config.accept, contentType=self.config.content_type
            )

        response_body = json.loads(response.get('body').read())
        return response_body['outputs'][0]['text']

    def get_body(self, prompt:str):
        """
        The `get_body` function returns a JSON object with a prompt, max tokens, and temperature.
        """
        return json.dumps({
            "prompt": prompt,
            "max_tokens": self.config.max_tokens,
            "temperature": self.config.temperature,
            }
        )

    def parse_config(self):
        '''The function `parse_config` reads settings from a configuration file (*.ini), 
        validates types, creates a pydantic model object config with those settings.
        '''
        try:
            config = Config("llm-bedrock")
            settings = config.get_settings()
            print(settings)
            self.config = BedrockLLMConfigModel(**settings) # parse & validate dict from config, create attributes
        except ValidationError as e:
            logging.ERROR(f'Bedrock attributes error: {e}')