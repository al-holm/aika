from abc import ABC, abstractmethod

class Tool(ABC):
    @abstractmethod
    def run(self, input:str):
        pass

    def __str__(self) -> str:
        res = "Tool: " + self.name
        res += " : " + self.description + "\n"
        return res

