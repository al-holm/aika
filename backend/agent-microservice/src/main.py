#### FOR DEBUGGING PURPOSES
from scripts.setup_logging import setup_logging
from agent_service.agent.agent import Agent
from agent_service.agent.task_type import TaskType
from agent_service.core.config import Config
from agent_service.prompts.trajectory_library import TrajectoryInjector
from agent_service.prompts.tool_prompt import READING_TEMPLATE
from agent_service.rag.rag import RAG
from agent_service.tools.reading_generation_tool import ReadingGenerator
if __name__ == "__main__":
    setup_logging()
    llm = 'bedrock' # bedrock or runpod
    task_type = TaskType.LESSON
    Config.set_llm(llm, task_type)
    #rt = RAG(init=True)
    """ while True:
        print('\n\n')
        print(rt.run(input('\n\n\nType your question:'))) """
    #tj = TrajectoryInjector(True)
    #print(tj.inject_trajectories('Wie kann ich sagen ich komme später.'))
    #a = Agent(task_type=task_type)
    tool = ReadingGenerator('', '', llm, 'reading', READING_TEMPLATE, 350)
    query = "" 
    while query != "stop":
        query = input("\n\nYour query: ")
        print(tool.run(query))
