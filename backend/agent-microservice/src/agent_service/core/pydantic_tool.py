from pydantic import BaseModel, Field


class ToolConfigModel(BaseModel):
    prompt_id: str = None
    name: str
    description: str
    llm: str = None
    max_tokens: int = Field(
        ge=0, le=800, description="Maximum tokens for llm generation", default=0
    )
