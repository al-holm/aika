from agent_service.prompts.task_generation_examples import READING_TASKS_EXAMPLES_1, READING_TASKS_EXAMPLES_2, GRAMMAR_TASKS_EXAMPLES_1, GRAMMAR_TASKS_EXAMPLES_2
from agent_service.tools.tool import Tool
from agent_service.exeptions.step_exception import ExtractingExercisesError
from typing import Literal, Dict
import os, uuid, re, logging
class TaskGenerator(Tool):

    def __init__(self, name: str, description: str, llm: str, 
                    prompt_id: str, prompt_template: str, max_tokens:int) -> None:
        super().__init__(name, description, llm, prompt_id, prompt_template, max_tokens)
        self.dir_path = "out/tasks/"

    def run(self, input:str):
        """
        generates exercises for a given input

        Returns:
        --------
        tool_answer: str
            concatenated input and generated exercises
        """
        parsed_input = self.parse_input(input)
        first_query, second_query = self.build_prompts(parsed_input)
        # reduce max tokens for generating exercises
        tokens = self.llm.max_tokens

        single_choice_and_gap_filling = None
        open_qs = None

        # try to generate exercises until they're generated correctly or generation attempts aren't left
        gen_attempts = 5
        areInvalid = True
        first = False
        second = False
        
        while areInvalid and gen_attempts != 0:
            try: 

                # if the extracting fails it means that the exercises weren't generated correctly
                # so the programs doesn't set areInvalid to False and the loop continues
                if not first:
                    self.llm.set_max_tokens(1000)
                    raw_single_choice_and_gap_filling = self.llm.run(first_query)
                    logging.info(f"\n\n\nTaskGenerator:run: raw_sg = {raw_single_choice_and_gap_filling}")
                    single_choice_and_gap_filling = self.extract_exercises(raw_single_choice_and_gap_filling, int(parsed_input["single-choice"]) + int(parsed_input["gap-filling"]))
                    logging.info(f"\n\n\nTaskGenerator:run: parsed_sg = {single_choice_and_gap_filling}")
                    first = True
                if not second:
                    self.llm.set_max_tokens(100)
                    raw_open_qs = self.llm.run(second_query) 
                    open_qs = self.extract_exercises(raw_open_qs, int(parsed_input["open"]))
                    second = True
                areInvalid = False
            except ExtractingExercisesError:
                # the program gets there when an error occured during the extraction of the exercises
                gen_attempts -= 1
                pass
    

        self.llm.set_max_tokens(tokens)

        # if generation attempts aren't left it means that the generating exercises failed
        if gen_attempts == 0:
            return "I can't complete the given task"

        exercises = single_choice_and_gap_filling + open_qs

        self.save_exercises(exercises)

        tool_answer = input + "\n\n" + exercises
        return tool_answer
    
    def build_prompts(self, input: Dict[str,str]):
        """
        Builds prompts for generating exercises
        """
        examples_1 = ""
        examples_2 = ""
        first_input = ""
        second_input = ""
        main_topic, secondary_topic = input["main-topic"], input["secondary-topic"]
        single_choice, gap_filling, open_q = input["single-choice"], input["gap-filling"], input["open"]
        if input["type"] == "Grammar":
            # When we need to generate single-choice questions and gap-filling exercises, 
            # we retrieve examples not from the GRAMMAR_TASKS_EXAMPLES_1, but from the good exercises database
            # That's why we have GRAMMAR_TASKS_EXAMPLES_1 + self.get_examples(main_topic)
            examples_1, examples_2 = GRAMMAR_TASKS_EXAMPLES_1 + self.get_examples(main_topic), GRAMMAR_TASKS_EXAMPLES_2
            logging.info(f"TaskGenerator:build_prompts: examples_1 = {examples_1}")
            first_input = f"[{main_topic}][{secondary_topic}][{single_choice}][{gap_filling}]"
            second_input = f"[{main_topic}][{second_input}][{open_q}]"
        else:
            examples_1, examples_2 = READING_TASKS_EXAMPLES_1, READING_TASKS_EXAMPLES_2
            first_input = f"[{single_choice}][{gap_filling}]"
            second_input = f"[{open_q}]"

        first_query = self.prompt.generate_prompt(name_id=self.prompt_id, input_format_and_examples=examples_1, text=(first_input + f"[{input['text']}]"))
        second_query = self.prompt.generate_prompt(name_id=self.prompt_id, input_format_and_examples=examples_2, text=(second_input + f"[{input['text']}]"))
        
        return (first_query,second_query)
    
    def get_examples(self, grammar_topic: str) -> str:
        filepath = "agent_service/tools/res/lesson_generation_db/good_exercises.md"
        logging.info(f"TaskGenerator:get_examples: called with grammar_topic = {grammar_topic}")
        try:
            with open(filepath, 'r', encoding='utf8') as file:
                content = file.read()
                logging.info("TaskGenerator:get_examples: content read")
                # Define the pattern to capture relevant sections based on the grammar topic
                pattern = r'\{' + re.escape(grammar_topic) + r'\}{GPT-4o}\n\[START\](.*?)\[END\]'
                
                # Find all matches in the content
                matches = re.findall(pattern, content, re.DOTALL)

                logging.info(f"TaskGenerator:get_examples: found examples = {matches}")
                
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
            logging.error("TaskGenerator:get_examples:file not found")    




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
                parsed_input["single-choice"] = matches[3]
                parsed_input["gap-filling"] = matches[4]
                parsed_input["open"] = matches[5]
                parsed_input["text"] = matches[6]
            else:
                # then we have [Type][Single-Choice-Questions-Number][Gaps-filling-exercises-number][Open-Questions-Number][Text for which exercises must be provided]
                parsed_input["single-choice"] = matches[1]
                parsed_input["gap-filling"] = matches[2]
                parsed_input["open"] = matches[3]
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


        




