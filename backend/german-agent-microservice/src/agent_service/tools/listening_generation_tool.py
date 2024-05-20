from agent_service.prompts.task_generation_prompt import LISTENING_TEMPLATE
from agent_service.agent.llm import LLMBedrock
from agent_service.prompts.prompt_builder import PromptBuidler
from agent_service.tools.tool import Tool
import uuid
class ListeningGenerator(Tool):
    def __init__(self):
        self.name = "Hörtext mit Audiodatei erstellen"
        self.description = "Benutzte zur Erstellung von Hörtexten, Generierung von Hörtexten und Audiodatei."
        self.llm = LLMBedrock()
        self.prompt = PromptBuidler(LISTENING_TEMPLATE)

    def run(self, input:str):
        self.query = self.prompt.update(text=input)
        answer = self.llm.run(self.query)
        filepath = "backend/german-agent-microservice/src/out/audio/" + str(uuid.uuid4()) + ".txt"
        with open(filepath, 'w', encoding='utf8') as file:
            file.write(answer)
        return answer