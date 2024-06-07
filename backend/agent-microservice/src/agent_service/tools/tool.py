from abc import ABC, abstractmethod
from agent_service.agent.llm import LLMBedrock, LLMRunPod
from agent_service.prompts.prompt_builder import PromptBuilder
class Tool(ABC):
    def __init__(self, name: str, description: str, llm: str, 
                    prompt_id: str, prompt_template: str, max_tokens:int) -> None:
        self.name = name
        self.description = description
        self.set_llm(llm)
        self.prompt_id = prompt_id
        self.prompt_template = prompt_template
        self.max_tokens = max_tokens
        self.init_prompt()
        
    @abstractmethod
    def run(self, input:str):
        pass

    def __str__(self) -> str:
        res = "Tool: " + self.name
        res += " : " + self.description + "\n"
        return res
    
    def set_llm(self, llm):
        if llm=='bedrock':
            self.llm = LLMBedrock()
        elif llm=='runpod':
            self.llm = LLMRunPod()
        else:
            self.llm = None

    def init_prompt(self):
        if self.llm is not None:
            self.prompt = PromptBuilder()
            self.prompt.create_prompts(
                {self.prompt_id: self.prompt_template}
                )
        else:
            self.prompt = None

