import logging
from typing import List
from agent_service.agent.agent import Agent
from scripts.setup_logging import setup_logging

def run_queries(queries: List[str]) -> None:
    """
    Calls Agent.run for each query in the provided list of strings

    Parameters
    ----------
    queries : List[str]
        the queries for which the Agent.run method should be run
    """

    try:
        for query in queries:
            agent = Agent()
            logging.info(f"Agent gets the query '{query}'")
            agent.run(query)
        logging.info("The run_queries script has been successfully executed")
    except Exception:
        logging.exception("During executing the run_queries script an exception has been raised")

def run_test_script_1():

    queries = ["Übersetz mir bitte das Wort Apfel","Wie verwende ich Weil?"]

    run_queries(queries)

def run_test_script_2():

    queries = ["Generiere mir Übungen zu einem Text zum Thema Familie", "Generiere mir eine Höraufgabe",]

    run_queries(queries)


if __name__ == "__main__":
    setup_logging()
    run_test_script_1()
    run_test_script_2()


    