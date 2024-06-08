from pydantic import BaseModel, Field

class AgentConfigModel(BaseModel):
    max_iterations: int = Field(gt=0, le=20, description="Maximum reasoning iterations" )
    llm:str
    max_tokens_plan:int=Field(ge=0, le=800, description="Maximum tokens for llm generation for action proposition", default=0)
    max_tokens_val:int=Field(ge=0, le=800, description="Maximum tokens for llm generation for action validation", default=0)