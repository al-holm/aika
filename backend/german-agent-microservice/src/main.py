#### FOR DEBUGGING PURPOSES
from scripts.setup_logging import setup_logging
from agent_service.agent.agent import Agent
from agent_service.agent.task_type import TaskType
from agent_service.core.config import Config

if __name__ == "__main__":
    setup_logging()
    llm = 'bedrock' # bedrock or runpod
    task_type = TaskType.LESSON
    Config.set_llm(llm, task_type)

    a = Agent(task_type)
    a.run("Bitte erstelle eine Grammatikerklärung mit Beispiele für das Thema 'Konjuktiv 2 (II)' und benutze danach ein Tool zur Aufgabenerstellung, damit du 5 Aufgaben erstellst.")