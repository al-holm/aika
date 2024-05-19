#### FOR DEBUGGING PURPOSES
from agent_service.agent.llm import LLMBedrock
from agent_service.tools.reading_generation_tool import ReadingGenerator
import logging
from agent_service.core.logging import ColoredFormatter
from agent_service.agent.agent_step import AgentStep
def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(ColoredFormatter())
    logger.addHandler(ch)

setup_logging()
if __name__ == "__main__":
    """ llm = LLMBedrock()
    llm.run("Wie benutzte ich 'weil'?") """
    #rg =  ReadingGenerator()
    #rg.run("Aufgabe: Generiere einen Lesetext zum Thema 'Familie'.")
    inp = AgentStep(thought="A", action="s", action_input="dd", tool_names=["s", "k"])
    inp.observation = "f"
    print(inp.toString())

    