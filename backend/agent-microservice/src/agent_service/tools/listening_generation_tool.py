from agent_service.prompts.tool_prompt import LISTENING_TEMPLATE
from agent_service.prompts.prompt_builder import PromptBuilder
from agent_service.tools.tool import Tool
import uuid, os
import torch
from typing import Literal
from TTS.api import TTS
import base64
import os
class ListeningGenerator(Tool):
    """
    a tool for the listening task generation
    """
    MALE_VOICE_MODEL = "tts_models/de/thorsten/tacotron2-DDC"
    FEMALE_VOICE_MODEL = "tts_models/de/css10/vits-neon"
    def __init__(self, name: str, description: str, llm: str, 
                    prompt_id: str, prompt_template: str, max_tokens:int) -> None:
        super().__init__(name, description, llm, prompt_id, prompt_template, max_tokens)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"


    def run(self, text:str, voice:Literal['m', 'f']='f'):
        """
        runs LLM to get an answer,
        is the entry point for using the tool from the outside
        """
        model = self.FEMALE_VOICE_MODEL
        if voice=='m':
            model = self.MALE_VOICE_MODEL
        tts = TTS(model).to(self.device)
        id = str(uuid.uuid4())
        filepath = "out/audio/" + id + ".wav"
        tts.tts_to_file(text=text, file_path=filepath)
        with open(filepath, "rb") as audio_file:
            encoded_string = base64.b64encode(audio_file.read()).decode('utf-8')
        os.remove(filepath) 
        return encoded_string