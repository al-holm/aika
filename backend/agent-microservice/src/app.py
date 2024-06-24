from flask import request, url_for, jsonify
from flask_api import FlaskAPI
import logging
import boto3
from agent_service.agent.agent import Agent
from agent_service.agent.task_type import TaskType
import warnings
from agent_service.core.config import Config
from agent_service.rag.rag import RAG
from agent_service.parsers.exercises_parser import ExercisesParser
from flasgger import Swagger
from agent_service.core.swagger import GERMAN_ANSWER_API, LAW_ANSWER_API, LESSON_API
from flasgger.utils import swag_from
# http://localhost:5000/apidocs/ for API docs
import logging.config
from scripts.setup_logging import setup_logging
for _ in logging.root.manager.loggerDict:
    logging.getLogger(_).setLevel(logging.CRITICAL)
setup_logging()

app = FlaskAPI(__name__)
swagger = Swagger(app)

bedrock = boto3.client(service_name='bedrock-runtime', region_name="eu-west-3")

llm = 'bedrock'
task_type = TaskType.ANSWERING
Config.set_llm(llm, task_type)
aika_qa = Agent(task_type=TaskType.ANSWERING)
task_type = TaskType.LESSON
Config.set_llm(llm, task_type)
aika_lesson = Agent(task_type=TaskType.LESSON)
lesson_parser = ExercisesParser()

retriever = RAG()

@app.route("/get_answer", methods=["Post"])
@swag_from(GERMAN_ANSWER_API)
def get_german_answer():
    """
    Returns agent's answer
    """
    answer =  aika_qa.run(request.json["question"])
    aika_qa.reset()
    answer = '.'.join(answer.strip().split('.')[:-1]) + '.'
    return {"answer": answer}

@app.route("/get_lesson", methods=["Post"])
@swag_from(LESSON_API)
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
    aika_lesson.reset()
    return jsonify(parsed_lesson)

@app.route("/get_answer_law_life", methods=["Post"])
@swag_from(LAW_ANSWER_API)
def getAnswerLawLife():
    """
    Returns an answer to the law and life topic
    """
    
    answer = retriever.run(request.json["question"])
    answer = '.'.join(answer.strip().split('.')[:-1]) + '.'

    return {"answer": answer}



if __name__ == "__main__":
    app.run(debug=True)