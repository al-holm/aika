from pydantic import BaseModel

# defines attributes for a step in an agent's decision-making process,
# including thought, action, action input, and observation.
class AgentStep(BaseModel):
    thought:str
    action:str
    action_input:str
    observation:str=None

    def __str__(self) -> str:
        res = ""
        res += "Thought: " + self.thought
        res += "\nAction: " + self.action
        res += "\nAction Input: " + self.action_input
        if self.observation is not None:
            res += "\nObservation: " + self.observation
        res += "\n"
        return res
    
# Final Answer class
class AgentFinalStep(BaseModel):
    final_answer:str

    def __str__(self) -> str:
        res = "Final Answer: " + self.final_answer + "\n"
        return res
    

# This class represents an AgentValidationStep with a validation thought attribute.
class AgentValidationStep(BaseModel):
    validation_thought:str

    def __str__(self) -> str:
        res = "Hint : " + self.validation_thought + "\n"
        return res



