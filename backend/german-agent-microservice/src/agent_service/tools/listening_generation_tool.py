from agent_service.prompts.task_generation_prompt import LISTENING_TEMPLATE
from agent_service.agent.llm import LLMBedrock
from agent_service.prompts.prompt_builder import PromptBuilder
from agent_service.tools.tool import Tool
import uuid, os

class ListeningGenerator(Tool):
    """
    a tool for the listening task generation
    """
    PROMPT_ID = "listening"
    TEMPLATE = LISTENING_TEMPLATE
    def __init__(self, llm):
        self.name = "Hörtext mit Audiodatei erstellen"
        self.description = "Benutzte zur Erstellung von Hörtexten, Generierung von Hörtexten und Audiodatei."
        self.set_llm(llm)
        self.prompt = PromptBuilder()
        self.prompt.create_prompts(
            {self.PROMPT_ID : self.TEMPLATE}
            )

    def run(self, input:str):
        """
        runs LLM to get an answer,
        is the entry point for using the tool from the outside
        """
        self.query = self.prompt.generate_prompt(name_id=self.PROMPT_ID, text=input)
        answer = self.llm.run(self.query)
        filepath = "C:/Users/tommc/OneDrive/Dokumente/progs/nest/aika/backend/german-agent-microservice/src/out/audio/" + str(uuid.uuid4()) + ".txt"
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf8') as file:
            file.write(answer)
        return answer