from flask import request, url_for, jsonify
from flask_api import FlaskAPI
import logging
import boto3
from agent_service.agent.agent import Agent
from agent_service.agent.task_type import TaskType
import warnings
from agent_service.core.config import Config
from agent_service.tools.retrieval_tool import RetrievalTool
from agent_service.parsers.exercises_parser import ExercisesParser

for _ in logging.root.manager.loggerDict:
    logging.getLogger(_).setLevel(logging.CRITICAL)

logging.basicConfig(format='%(asctime)s | %(levelname)s: %(message)s', level=logging.NOTSET)
logger = logging.getLogger('REACT Agent')
logger.setLevel(logging.INFO)
warnings.filterwarnings("ignore")

app = FlaskAPI(__name__)

bedrock = boto3.client(service_name='bedrock-runtime', region_name="eu-west-3")

llm = 'bedrock'
task_type = TaskType.LESSON
Config.set_llm(llm, task_type)
aika_qa = Agent(task_type=TaskType.ANSWERING)
aika_lesson = Agent(task_type=TaskType.LESSON)
lesson_parser = ExercisesParser()

retriever = RetrievalTool(False)

@app.route("/get_answer", methods=["Post"])
def getAnswer():
    """
    Returns agent's answer
    """
    
    return {"answer": aika_qa.run(request.json["question"])}

@app.route("/get_lesson", methods=["Post"])
def getLesson():
    """
    Returns generated exercises for a new lesson
    """

    raw_lesson = aika_lesson.run(request.json["question"])
    if raw_lesson == "I can't complete the given task":
        parsed_lesson = {"Text": "I can't complete the given task"}
    else:
        parsed_lesson = lesson_parser.parse(raw_lesson)
    logging.info(f"Parsed_lesson: {parsed_lesson}\n\n\n")
    return jsonify(parsed_lesson)

@app.route("/get_answer_law_life", methods=["Post"])
def getAnswerLawLife():
    """
    Returns an answer to the law and life topic
    """
    
    result = retriever.run(request.json["question"])

    return {"answer": result}



if __name__ == "__main__":
    app.run(debug=True)