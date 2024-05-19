#### FOR DEBUGGING PURPOSES
from agent_service.agent.llm import LLMBedrock
from agent_service.tools.reading_generation_tool import ReadingGenerator
import logging
from agent_service.core.log import ColoredFormatter
from agent_service.agent.agent_step import AgentStep
from agent_service.agent.agent import Agent
from agent_service.tools.tool_executor import ToolExecutor
from time import sleep
def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(ColoredFormatter())
    logger.addHandler(ch)

setup_logging()
if __name__ == "__main__":
    a = Agent()
    print(a.run("Gib mir wichtige Wortschtatz für Artztbesuch."))
    