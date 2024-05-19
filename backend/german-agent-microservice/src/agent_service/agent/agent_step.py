from pydantic import BaseModel, field_validator, Field
from typing import List, Any

class AgentStep(BaseModel):
    thought:str
    tool_names:List[str]
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

    @field_validator('thought')
    def validate_thought(cls, value):
        if ''==value:
            raise ValueError('You should start with "Thought:" (think about what you should do next).')
        return value
    
    @field_validator('action')
    def validate_action(cls, value, info: dict[str, Any]):
        if ''==value:
            raise ValueError('No action were given.')
        if value not in info.data["tool_names"]:
            raise ValueError(f'An action name is incorrect, select an available tool: {info.data["tool_names"]}')
        return value
    
    @field_validator('action_input')
    def validate_action_input(cls, value):
        if ''==value:
            raise ValueError("Input shouldn't be empty.")
        return value
    
    @field_validator('observation')
    def validate_observation(cls, value):
        if '' not in value:
            raise ValueError("Observation shouldn't be empty.")
        return value
    
    @field_validator('tool_names')
    def validate_observation(cls, value):
        if len(value)==0:
            raise ValueError("Tools shouldn't be empty.")
        return value

