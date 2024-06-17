#### FOR DEBUGGING PURPOSES
from scripts.setup_logging import setup_logging
from agent_service.agent.agent import Agent
from agent_service.agent.task_type import TaskType
from agent_service.core.config import Config
from agent_service.prompts.trajectory_library import TrajectoryInjector
from agent_service.rag.rag import RAG
if __name__ == "__main__":
    setup_logging()
    llm = 'bedrock' # bedrock or runpod
    task_type = TaskType.ANSWERING
    Config.set_llm(llm, task_type)
    rt = RAG(init=False)
    while True:
        print('\n\n')
        print(rt.run(input('\n\n\nType your question:')))
    #tj = TrajectoryInjector(True)
    #print(tj.inject_trajectories('Wie kann ich sagen ich komme später.'))
    #a = Agent(task_type=task_type)
