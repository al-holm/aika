from agent_service.prompts.task_generation_prompt import TASK_TEMPLATE
from agent_service.agent.llm import LLMBedrock
from agent_service.prompts.prompt_builder import PromptBuilder
from agent_service.tools.tool import Tool
import uuid
class TaskGenerator(Tool):
    PROMPT_ID = "tasks"
    TEMPLATE = TASK_TEMPLATE
    def __init__(self):
        self.name = "Aufgaben zu einem Text oder Grammatikthema generieren"
        self.description = "Benutzte als letzte, um die Aufgaben zu generieren. Nimmt als Eingabe deine generierte Text oder Grammatikerklärung."
        self.llm = LLMBedrock()
        self.prompt = PromptBuilder()
        self.prompt.create_prompts(
            {self.PROMPT_ID : self.TEMPLATE}
            )

    def run(self, input:str):
        self.query = self.prompt.generate_prompt(name_id=self.PROMPT_ID, text=input)
        answer = self.llm.run(self.query)
        filepath = "backend/german-agent-microservice/src/out/tasks/" + str(uuid.uuid4()) + ".txt"
        with open(filepath, 'w', encoding='utf8') as file:
            file.write(answer)
        return input + "\n\n" + answer