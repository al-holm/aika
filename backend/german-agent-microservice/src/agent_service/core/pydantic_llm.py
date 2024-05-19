from pydantic import BaseModel, Field

class BedrockLLMConfigModel(BaseModel):
    service_name: str
    region_name: str
    llm_id: str
    accept: str
    content_type: str
    max_tokens: int = Field(gt=0, description="The maximum number of tokens to generate.")
    temperature: float = Field(ge=0.0, le=1.0, description="The randomness of the output.")