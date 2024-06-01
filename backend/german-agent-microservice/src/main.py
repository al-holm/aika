#### FOR DEBUGGING PURPOSES
from scripts.setup_logging import setup_logging
from agent_service.agent.agent import Agent
from agent_service.agent.task_type import TaskType
from agent_service.core.config import Config
from agent_service.prompts.trajectory_library import TrajectoryInjector
if __name__ == "__main__":
    setup_logging()
    llm = 'bedrock' # bedrock or runpod
    task_type = TaskType.ANSWERING
    Config.set_llm(llm, task_type)
    tj = TrajectoryInjector(True)
    #a = Agent(query_id="q001", task_type=task_type)
    #a.run("Übersetze wie kann ich 'ich komme später' auf turkisch sagen.")