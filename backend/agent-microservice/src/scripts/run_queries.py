import logging, pandas as pd
from typing import List
from agent_service.agent.agent import Agent
from scripts.setup_logging import setup_logging
from agent_service.agent.task_type import TaskType
from agent_service.core.config import Config
from typing import Literal

def run_queries(queries: pd.DataFrame, task_type: TaskType) -> None:
    """
    Calls Agent.run for each query in the provided list of strings

    Parameters
    ----------
    queries : pandas.dataframe
        the queries for which the Agent.run method should be run
    task_type : TaskType
        a value from the TaskType Enum, can be either LESSON or ANSWERING
    """

    logging.info("Entered run_queries")
    try:
        for row in queries.itertuples():
            agent = Agent(query_id=row.ID, task_type=task_type)
            logging.info(f"Agent gets the query '{row.query}'")
            agent.run(row.query)
            logging.info("Exited Agent.run")
        logging.info("The run_queries script has been successfully executed")
    except Exception:
        logging.exception("During executing the run_queries script an exception has been raised")

def load_queries_csv(path: str):
    """
    loads queries from a given .csv file

    Parameters:
    -----------
    path: str

    Returns
    -------
    pandas.dataframe
        contains only ID and queries
    """

    df = pd.read_csv(path, sep=",").sample(3)

    return df[["ID","query"]]


def run_test_script():
    llm = 'bedrock'
    task_type = TaskType.ANSWERING
    Config.set_llm(llm, task_type)

    run_queries(queries=load_queries_csv("/Users/ali/Desktop/code/aika/backend/german-agent-microservice/src/in/queries_qa_translation.csv"), task_type=task_type)


if __name__ == "__main__":
    setup_logging()
    run_test_script()


    