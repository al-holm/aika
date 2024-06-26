from flask import request, url_for, jsonify
from flask_api import FlaskAPI
import logging
import boto3
from agent_service.agent.agent import Agent
from agent_service.agent.task_type import TaskType
from agent_service.utils.proxy import LessonProxy
from agent_service.core.config import Config
from agent_service.rag.rag import RAG
from agent_service.lesson.lesson_master import LessonMaster
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
lesson_master = LessonMaster()
lesson_proxy = LessonProxy(
    lesson_master.create_text, lesson_master.create_exercises
    )


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

@app.route("/get_lesson_text", methods=["Post"])
@swag_from(LESSON_API)
def getLessonText():
    """
    Returns generated exercises for a new lesson
    """

    response = lesson_proxy.create_text(request.json["question"])
    return jsonify(response)

@app.route("/get_lesson_exercises", methods=["Get"])
@swag_from(LESSON_API)
def getLessonExercises():
    """
    Returns generated exercises for a new lesson
    """

    exercises = lesson_proxy.create_exercises()
    return jsonify(exercises)

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