from flask import request, url_for
from flask_api import FlaskAPI
import logging
import boto3
from agent_service.agent.agent import Agent
from agent_service.agent.task_type import TaskType
import warnings
for _ in logging.root.manager.loggerDict:
    logging.getLogger(_).setLevel(logging.CRITICAL)

logging.basicConfig(format='%(asctime)s | %(levelname)s: %(message)s', level=logging.NOTSET)
logger = logging.getLogger('REACT Agent')
logger.setLevel(logging.INFO)
warnings.filterwarnings("ignore")

app = FlaskAPI(__name__)

bedrock = boto3.client(service_name='bedrock-runtime', region_name="eu-west-3")
model = Agent(task_type=TaskType.ANSWERING)

@app.route("/get_answer", methods=["Post"])
def getAnswer():
    """
    Returns agent's answer
    """
    return {"answer": model.run(request.json["question"])["output"]}

if __name__ == "__main__":
    app.run(debug=True)