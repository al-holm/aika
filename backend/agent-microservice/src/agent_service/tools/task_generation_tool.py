from agent_service.prompts.task_generation_examples import GRAMMAR_GAP_FILLING, GRAMMAR_OPEN_ENDED, GRAMMAR_SINGLE_CHOICE, READING_SINGLE_CHOICE, READING_GAP_FILLING, READING_OPEN_ENDED
from agent_service.tools.tool import Tool
from agent_service.exeptions.step_exception import ExtractingExercisesError
from typing import Literal, Dict
from agent_service.tools.lesson_generation_retriever import LessonRetriever
import os, uuid, re, logging
class TaskGenerator(Tool):

    def __init__(self, name: str, description: str, llm: str, 
                    prompt_id: str, prompt_template: str, max_tokens:int) -> None:
        super().__init__(name, description, llm, prompt_id, prompt_template, max_tokens)
        self.dir_path = "out/tasks/"
        self.lesson_retriever = LessonRetriever()

    def run(self, input:str):
        """
        generates exercises for a given input

        Returns:
        --------
        tool_answer: str
            concatenated input and generated exercises
        """
        parsed_input = self.parse_input(input)
        query_single_choice, query_gap_filling, query_open_ended = self.build_prompts(parsed_input)
        
        single_choice_questions = None
        gap_filling_exercises = None
        open_ended_questions = None

        # try to generate exercises until they're generated correctly or generation attempts aren't left
        gen_attempts = 5
        areInvalid = True
        done_single_choice = False
        done_gap_filling = False
        done_open_ended = False
        
        while areInvalid and gen_attempts != 0:
            try: 
                # if the extracting fails it means that the exercises weren't generated correctly
                # so the programs doesn't set areInvalid to False and the loop continues
                if not done_single_choice:
                    single_choice_questions = self.generate_exercises(query_single_choice, "single-choice", int(parsed_input["single-choice"]), 700)
                    done_single_choice = True
                if not done_gap_filling:
                    gap_filling_exercises = self.generate_exercises(query_gap_filling, "gap-filling", int(parsed_input["gap-filling"]), 700)
                    done_gap_filling = True
                if not done_open_ended:
                    open_ended_questions = self.generate_exercises(query_open_ended, "open-ended", int(parsed_input["open-ended"]), 100)
                    done_open_ended = True
                areInvalid = False
            except ExtractingExercisesError:
                # the program gets there when an error occured during the extraction of the exercises
                gen_attempts -= 1
                pass
    

        # if generation attempts aren't left it means that the generating exercises failed
        if gen_attempts == 0:
            return "I can't complete the given task"

        exercises = single_choice_questions + gap_filling_exercises + open_ended_questions

        logging.info(f"TaskGenerator:run: ALL EXERCISES = \n{exercises}\n\n")

        self.save_exercises(exercises)

        tool_answer = input + "\n\n" + exercises
        return tool_answer
    

    def build_prompts(self, input: Dict[str,str]):
        """
        Builds prompts for generating exercises
        """
        input_single_choice = ""
        input_gap_filling = ""
        input_open_ended = ""
        examples_single_choice = ""
        examples_gap_filling = ""
        examples_open_ended = ""

        main_topic, secondary_topic = input["main-topic"], input["secondary-topic"]
        num_single_choice, num_gap_filling, num_open_ended = input["single-choice"], input["gap-filling"], input["open-ended"]
        if not isinstance(num_single_choice, int) or not isinstance(num_gap_filling, int) or not isinstance(num_open_ended, int):
            raise Exception("Wrong value type")
        
        if input["type"] == "Grammar":
            examples_single_choice = GRAMMAR_SINGLE_CHOICE + self.lesson_retriever.get_examples(topic=main_topic, task_type="single-choice")
            examples_gap_filling = GRAMMAR_GAP_FILLING + self.lesson_retriever.get_examples(topic=main_topic, task_type="gap-filling")
            examples_open_ended = GRAMMAR_OPEN_ENDED
            
            input_single_choice = f"[{main_topic}][{secondary_topic}][{num_single_choice}]"
            input_gap_filling = f"[{main_topic}][{secondary_topic}][{num_gap_filling}]"
            input_open_ended = f"[{main_topic}][{secondary_topic}][{num_open_ended}]"
        else:
            examples_single_choice = READING_SINGLE_CHOICE
            examples_gap_filling = READING_GAP_FILLING
            examples_open_ended = READING_OPEN_ENDED

            input_single_choice = f"[{num_single_choice}]"
            input_gap_filling = f"[{num_gap_filling}]"
            input_open_ended = f"[{num_open_ended}]"
        

        query_single_choice = self.prompt.generate_prompt(name_id=self.prompt_id, input_format_and_examples=examples_single_choice, text=(input_single_choice + f"[{input['text']}]"))
        query_gap_filling = self.prompt.generate_prompt(name_id=self.prompt_id, input_format_and_examples=examples_gap_filling, text=(input_gap_filling + f"[{input['text']}]"))
        query_open_ended = self.prompt.generate_prompt(name_id=self.prompt_id, input_format_and_examples=examples_open_ended, text=(input_open_ended + f"[{input['text']}]"))
  
        return (query_single_choice, query_gap_filling, query_open_ended)    

    def generate_exercises(self, query: str, type: Literal["single-choice", "gap-filling", "open-ended"], num: int, max_tokens: int):
        """
        calls a llm and parses generated exercises

        Parameters:
        -----------
        query: str
            the query that is sent to the LLM
        
        type: "single-choice"/"gap-filling"/"open-ended"
            the type of the exercises that need to be generated
        
        num: int
            a number of the exercises that need to be generated 

        Returns:
        exercises: str
            a string of the generated exercises
            If num is zero, an empty string is returned
        """
        # set max tokens for generating exercises
        tokens = self.llm.max_tokens
        self.llm.set_max_tokens(max_tokens)
        logging.info(f"TaskGenerator:generate_exercises: \nQUERY = \n{query}\nTYPE = \n{type}\nNUM = \n{num}\n\n")
        if num == 0:
            return ""
        raw_exercises = self.llm.run(query)
        logging.info(f"TaskGenerator:generate_exercises: \nRAW_EXERCISES = \n{raw_exercises}\n\n")
        exercises = self.extract_exercises(raw_exercises, num)
        logging.info(f"TaskGenerator:generate_exercises: \nEXERCISES = \n{exercises}\n\n")
        # set original tokens num back
        self.llm.set_max_tokens(tokens)
        return exercises

    def parse_input(self, input: str) -> Dict[str, str]:
        """
        parses a given input and returns a dict with parsed input data

        Returns:
        --------
        parsed_input: Dict[str,str]
            a dict depending on the task type
        """

        matches = re.findall(r'\[(.*?)\]', input, re.DOTALL)
        if matches:
            parsed_input = {}
            task_type = matches[0]
            parsed_input["type"] = task_type
            if task_type == "Grammar":
                # then we have [Type][Main-grammar-topic][Secondary-grammar-topic][Single-Choice-Questions-Number][Gaps-filling-exercises-number][Open-Questions-Number][Main-grammar-topic-explanation-text]
                parsed_input["main-topic"] = matches[1]
                parsed_input["secondary-topic"] = matches[2]
                parsed_input["single-choice"] = int(matches[3])
                parsed_input["gap-filling"] = int(matches[4])
                parsed_input["open-ended"] = int(matches[5])
                parsed_input["text"] = matches[6]
            else:
                # then we have [Type][Single-Choice-Questions-Number][Gaps-filling-exercises-number][Open-Questions-Number][Text for which exercises must be provided]
                parsed_input["single-choice"] = int(matches[1])
                parsed_input["gap-filling"] = int(matches[2])
                parsed_input["open-ended"] = int(matches[3])
                parsed_input["text"] = matches[4]
            return parsed_input
        raise Exception(f"extract_task_type: failure during extracting from f{input}")
    
    def extract_exercises(self, message: str, exercises_num: int) -> str:
        """
        Extracts exercises from the message, cutting out hallucinations generated by LLM
        """

        try:
            res = ""
            matches = re.findall(r'\[START\](.*?)\[END\]', message, re.DOTALL)
            for i in range(exercises_num):
                #logging.info(f"\n\n\n{i}: {matches[i]}\n\n\n")
                res += "[START]" + matches[i] + "[END]\n"

            return res
        except Exception:
            raise ExtractingExercisesError()
        
    def save_exercises(self, exercises: str):
        """
        Saves given exercises to txt file
        """
        filepath =  self.dir_path + str(uuid.uuid4()) + ".txt"
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf8') as file:
            file.write(exercises)


        




