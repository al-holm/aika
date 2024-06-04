from pydantic import BaseModel


class AgentStep(BaseModel):
    """
    contains attributes for a single step in the agent's decision-making process, 
    such as the agent's thought, the required action, the necessary input for the action, and 
    an observation
    """
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
    

class AgentFinalStep(BaseModel):
    """
    represents the final step of the agent loop with the final answer
    """
    final_answer:str

    def __str__(self) -> str:
        res = "Final Answer: " + self.final_answer + "\n"
        return res
    

class AgentValidationStep(BaseModel):
    """
    represents a validation step
    """
    validation_thought:str

    def __str__(self) -> str:
        res = "Hint : " + self.validation_thought + "\n"
        return res



