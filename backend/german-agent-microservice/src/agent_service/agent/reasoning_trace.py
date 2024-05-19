from typing import List, Union
from agent_service.agent.agent_step import AgentStep, AgentFinalStep
import json
class ReasoningTrace:
    def __init__(self) -> None:
        self.steps : List[Union[AgentStep, AgentFinalStep]] = []
    
    def add_step(self, step: Union[AgentStep, AgentFinalStep]):
        self.steps.append(step)

    def remove_step(self, index: int) -> None:
        if 0 <= index < len(self.steps):
            self.steps.pop(index)

    def get_last_step(self) -> Union[AgentStep, AgentFinalStep]:
        if self.steps:
            return self.steps[-1]
        return None

    def toString(self):
        res = ""
        if len(self.steps) == 0:
            return res
        for step in self.steps:
            res += step.toString() + "\n"
        return res

    def to_json(self, filepath: str):
        with open(filepath, 'w') as file:
            json.dump([step.model_dump(mode='json') for step in self.steps], file, indent=4)
