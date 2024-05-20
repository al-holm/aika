from pydantic import BaseModel, field_validator, Field
from typing import List, Any

class AgentStep(BaseModel):
    thought:str
    action:str
    action_input:str
    observation:str=None

    def toString(self):
        """
        The `toString` function in Python creates a formatted string representation of an object's
        attributes.
        """
        res = ""
        res += "Thought: " + self.thought
        res += "\nAction: " + self.action
        res += "\nAction Input: " + self.action_input
        if self.observation is not None:
            res += "\nObservation: " + self.observation
        res += "\n"
        return res
    
class AgentFinalStep(BaseModel):
    final_answer:str

    def toString(self):
        """
        The `toString` function in Python creates a formatted string representation of an object's
        attributes.
        """
        res = "Final Answer: " + self.final_answer + "\n"
        return res
    

class AgentValidationStep(BaseModel):
    validation_thought:str

    def toString(self):
        """
        The `toString` function in Python creates a formatted string representation of an object's
        attributes.
        """
        res = "Hint : " + self.validation_thought + "\n"
        return res



