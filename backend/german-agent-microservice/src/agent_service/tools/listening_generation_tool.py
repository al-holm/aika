from agent_service.prompts.task_generation_prompt import LISTENING_TEMPLATE
from agent_service.agent.llm import LLMBedrock
from agent_service.prompts.prompt_builder import PromptBuilder
from agent_service.tools.tool import Tool
import uuid
# The ListeningGenerator class implements a tool for a listening task generation
class ListeningGenerator(Tool):
    PROMPT_ID = "listening"
    TEMPLATE = LISTENING_TEMPLATE
    def __init__(self):
        self.name = "Hörtext mit Audiodatei erstellen"
        self.description = "Benutzte zur Erstellung von Hörtexten, Generierung von Hörtexten und Audiodatei."
        self.llm = LLMBedrock()
        self.prompt = PromptBuilder()
        self.prompt.create_prompts(
            {self.PROMPT_ID : self.TEMPLATE}
            )

    def run(self, input:str):
        '''runs LLM to get answer, the entry point 
         
        '''
        self.query = self.prompt.generate_prompt(name_id=self.PROMPT_ID, text=input)
        answer = self.llm.run(self.query)
        filepath = "backend/german-agent-microservice/src/out/audio/" + str(uuid.uuid4()) + ".txt"
        with open(filepath, 'w', encoding='utf8') as file:
            file.write(answer)
        return answer