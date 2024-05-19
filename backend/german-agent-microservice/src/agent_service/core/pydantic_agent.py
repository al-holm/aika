from pydantic import BaseModel, Field

class AgentConfigModel(BaseModel):
    max_iterations: int = Field(gt=0, le=20, description="Maximum reasoning iterations" )
    llm:str