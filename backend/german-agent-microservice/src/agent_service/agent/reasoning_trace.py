from typing import List, Union
from agent_service.agent.agent_step import AgentStep, AgentValidationStep, AgentFinalStep
import json, uuid
from pathlib import Path
import os
class ReasoningTrace:
    def __init__(self) -> None:
        self.steps : List[Union[AgentStep, AgentValidationStep, AgentFinalStep]] = []
        self.query = None
        self.errors : List[Exception] = []
    
    def add_exception(self, e:Exception):
        self.errors.append(e)
    
    def add_step(self, step: Union[AgentStep, AgentValidationStep, AgentFinalStep]):
        self.steps.append(step)

    def remove_step(self, index: int) -> None:
        if 0 <= index < len(self.steps):
            self.steps.pop(index)

    def get_last_step(self) -> Union[AgentStep, AgentValidationStep, AgentFinalStep]:
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

    def to_json(self):
        dict_f = {"query": self.query}
        dict_f["reasoning_steps"] = [step.model_dump() for step in self.steps]
        dict_f["errors"] = self.errors

        filepath = Path("backend/german-agent-microservice/src/out/" + str(uuid.uuid4()) + ".json")
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        with open(filepath, 'w', encoding='utf8') as file:
            json.dump(dict_f, file, indent=4, ensure_ascii=False)
    
    def set_query(self, query:str):
        self.query = query

    def get_final_answer(self):
        for i in reversed(self.steps):
            if isinstance(i, AgentStep):
                self.add_step(AgentFinalStep(final_answer=i.observation))
                break


