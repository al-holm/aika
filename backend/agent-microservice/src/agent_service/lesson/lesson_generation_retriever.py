from typing import Literal
import logging, re

class ExplanationNotFound(Exception):

    def __init__(self, topic: str):
        super().__init__(f"LessonRetriever didn't find an explanation to the topic '{topic}'")


class LessonRetriever:
    """
    is responsible for finding sample exercises and explanations of grammar topics 
    in the database of good exercises and grammar topics
    """

    def __init__(self, dirpath= "agent_service/tools/res/lesson_generation_db/"):
        self.good_exercises_filepath = dirpath + "good_exercises.md"
        self.explanations_filepath = dirpath + "grammar_explanations.md"

    def get_examples(self, topic: str, task_type: Literal["single-choice", "gap-filling", "open-ended"]) -> str:
        """
        returns examples to the given topic and task type

        Parameters:
        -----------
        topic: str
            for instance, "Perfekt"
        
        task_type: Literal["single-choice", "gap-filling", "open-ended"]

        Returns:
        --------
        examples: str
            a string containing the found examples
        """

        try:
            with open(self.good_exercises_filepath, 'r', encoding='utf8') as file:
                content = file.read()
                
                # Define the pattern to capture relevant sections based on the grammar topic
                pattern = r'\{' + re.escape(topic) + r'\}\{' + re.escape(task_type) + r'\}{GPT-4o}\n\[START\](.*?)\[END\]'
                
                # Find all matches in the content
                matches = re.findall(pattern, content, re.DOTALL)
                
                exercises = ""
                for match in matches:
                    # Parsing details within each section
                    type_match = re.search(r'Type: \[(.*?)\]', match)
                    question_match = re.search(r'Question: \[(.*?)\]', match)
                    options_match = re.search(r'Answer options: \[(.*?)\]', match)
                    solution_match = re.search(r'Solution: \[(.*?)\]', match)
                    explanation_match = re.search(r'Solution explanation: \[(.*?)\]', match)
                    
                    exercise = "[START]\n" + f"Type: [{type_match.group(1) if type_match else 'N/A'}]\n" 
                    exercise += f"Question: [{question_match.group(1) if question_match else 'N/A'}]\n" 
                    exercise += f"Answer Options: [{options_match.group(1) if options_match else 'N/A'}]\n"
                    exercise += f"Solution Explanation: [{explanation_match.group(1) if explanation_match else 'N/A'}]\n"
                    exercise += f"Solution: [{solution_match.group(1) if solution_match else 'N/A'}]\n"
                    exercise += "[END]\n"
                    exercises += exercise
                return exercises
        except FileNotFoundError:
            logging.error("LessonRetriever:get_examples:file not found")
            return "GOOD EXERCISES FILE NOT FOUND"
        
    def get_grammar_explanation(self, topic: str) -> str:
        """
        returns a grammar explanation to the given topic

        Parameters:
        -----------
        topic: str
            for instance, "Perfekt"

        Returns:
        --------
        explanation: str
            a string containing the found explanation
        """

        try:
            with open(self.explanations_filepath, 'r', encoding='utf8') as file:
                content = file.read()
                
                # Define the pattern to capture relevant sections based on the grammar topic
                pattern = r'\{' + re.escape(topic) + r'\}{explanation}{GPT-4o}\n(.*?)\n\{'
                
                # Find all matches in the content
                explanation  = re.findall(pattern, content, re.DOTALL)
                # print(f"explanation: \n{explanation}")

                # Return the explanation if found, otherwise return a default message
                if explanation:
                    return explanation[0]
                else:
                    raise ExplanationNotFound(topic)
                
        except ExplanationNotFound:
            logging.error("LessonRetriever:get_examples:explanation not found")
            return "NO EXPLANATION FOUND FOR THE GIVEN TOPIC"
