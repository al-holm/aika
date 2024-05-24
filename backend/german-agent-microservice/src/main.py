#### FOR DEBUGGING PURPOSES
from scripts.setup_logging import setup_logging
from agent_service.agent.agent import Agent




if __name__ == "__main__":
    setup_logging()
    a = Agent()
    a.run("Übersetze für mich auf Russisch 'In Rahmen dieser Arbeit werden viel über KI erfahren.'.")
    