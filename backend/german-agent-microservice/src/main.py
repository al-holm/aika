#### FOR DEBUGGING PURPOSES
import logging
from agent_service.core.log import ColoredFormatter
from agent_service.agent.agent import Agent

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
    a.run("Übersetze für mich auf Russisch 'In Rahmen dieser Arbeit werden viel über KI erfahren.'.")
    