from pydantic import BaseModel

class ToolExecutorConfigModel(BaseModel):
    web_search:bool
    translator:bool
    reading_generator:bool
    listening_generator:bool
    task_generator:bool
    retriever:bool
    phrasing_tool:bool
    llm:str
