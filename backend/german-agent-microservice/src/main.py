#### FOR DEBUGGING PURPOSES
from scripts.setup_logging import setup_logging
from agent_service.agent.agent import Agent
from agent_service.agent.task_type import TaskType
from agent_service.core.config import Config
from agent_service.prompts.trajectory_library import TrajectoryInjector
from agent_service.tools.retrieval_tool import RetrievalTool
if __name__ == "__main__":
    setup_logging()
    llm = 'bedrock' # bedrock or runpod
    task_type = TaskType.ANSWERING
    Config.set_llm(llm, task_type)
    rt = RetrievalTool(True)
    print(rt.run('Was ist Wohnberechtigungsschein?'))
    #tj = TrajectoryInjector(True)
    #a = Agent(task_type=task_type)
    #a.run("Übersetze wie kann ich 'ich komme später' auf turkisch sagen.")
    #a.run("Как я могу объяснить Ausländerbehörde, что мне сначала надо продлить загранпаспорт, перед получением визы?")