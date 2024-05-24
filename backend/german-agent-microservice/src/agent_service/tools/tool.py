from abc import ABC, abstractmethod
from agent_service.agent.llm import LLMBedrock, LLMRunPod
class Tool(ABC):
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

