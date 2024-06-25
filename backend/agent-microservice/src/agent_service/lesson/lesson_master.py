from agent_service.tools.tool_executor import ToolExecutor
from agent_service.agent.task_type import TaskType
from agent_service.parsers.exercises_parser import ExercisesParser
from agent_service.lesson.lesson_generation_retriever import LessonRetriever
from agent_service.exceptions.lesson_exceptions import TextNotFoundException, ExercisesNotGeneratedException
from typing import Dict
import re, logging


class LessonMaster:
    """
    responsible for generating exercises
    """
    
    def __init__(self):
        self.tool_executor = ToolExecutor(task_type=TaskType.LESSON)
        self.exercises_parser = ExercisesParser()
        self.lesson_retriever = LessonRetriever()
        
        # To split the generation exercises into two steps, the task generator query var contains 
        # the query for the task generator
        self.task_generator_query = None

    def create_text(self, query: str):
        """
        creates a text for a new lesson

        Parameters:
        -----------
        query: str
            a string containing the type, topic, and number of exercises of the desired lesson
            for instance, [Grammar][Präteritum][None][1][1][1]

        Returns:
        --------
        text: str
            a string containing the text for the lesson
        """
        parsed_query = self.parse_query(query)

        if parsed_query["type"] == "Grammar":
            text = self.lesson_retriever.get_grammar_explanation(parsed_query["main-topic"])
            # should look like that: [Grammar][Präteritum][None][1][1][1][text]
            self.task_generator_query = query + f"[{text}]"
        else:
            text = self.tool_executor.execute('Lesetext erstellen', parsed_query["main-topic"])
            # should look like that: [Reading][2][0][1][text]
            self.task_generator_query = f"[{parsed_query['type']}][{parsed_query['single-choice']}][{parsed_query['gap-filling']}][{parsed_query['open-ended']}][{text}]"

        return text
    
    def create_exercises(self):
        """
        if a text for the exercises is generated, it creates exercises,
        otherwise it raises an exception

        Raises:
        -------
        TextNotFound

        Returns:
        --------
        exercises: Dict
            a dictionary containing all generated exercises
        """

        if self.task_generator_query == None:
            raise TextNotFoundException
        
        try:
            raw_lesson = self.tool_executor.execute('Deutschaufgaben generieren', self.task_generator_query)
        except ExercisesNotGeneratedException:
            logging.error("ExercisesNotGenerated")
            return { "response": "I can't create exercises"}
        lesson = self.exercises_parser.parse(raw_lesson)

        # need to reset task_generator_query
        self.task_generator_query = None
        
        return lesson
    
    def parse_query(self, query: str) -> Dict[str, str]:
        """
        parses a query of the form
        [Type][Main-grammar-topic][Secondary-grammar-topic][Single-Choice-Questions-Number][Gaps-filling-exercises-number][Open-Questions-Number]
        
        Returns:
        --------
        parsed_query: Dict[str, str]
        """
        matches = re.findall(r'\[(.*?)\]', query, re.DOTALL)

        parsed_query = {}
        parsed_query["type"] = matches[0]
        parsed_query["main-topic"] = matches[1]
        parsed_query["secondary-topic"] = matches[2]
        parsed_query["single-choice"] = matches[3]
        parsed_query["gap-filling"] = matches[4]
        parsed_query["open-ended"] = matches[5]

        return parsed_query