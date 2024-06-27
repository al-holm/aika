import unittest
from unittest.mock import Mock, call, patch
from agent_service.tools.task_generation_tool import TaskGenerator
from agent_service.exceptions.lesson_exceptions import ExercisesNotGeneratedException 
from agent_service.prompts.task_generation_examples import READING_GAP_FILLING, READING_OPEN_ENDED, READING_SINGLE_CHOICE, GRAMMAR_SINGLE_CHOICE, GRAMMAR_GAP_FILLING, GRAMMAR_OPEN_ENDED

class TestTaskGenerator(unittest.TestCase):

    def setUp(self):
        self.task_gen = TaskGenerator(name="name", description="desc",
                                      llm="bedrock", prompt_id="prompt_id",
                                      prompt_template="prompt_template", max_tokens= 1000)

    @patch('agent_service.tools.task_generation_tool.TaskGenerator.parse_input', return_value={"single-choice": 1, "gap-filling": 1, "open-ended": 1})
    @patch('agent_service.tools.task_generation_tool.TaskGenerator.build_prompts', return_value=("prompt_1", "prompt_2", "prompt_3"))
    @patch('agent_service.tools.task_generation_tool.TaskGenerator.generate_exercises', return_value="exercises generated")
    def test_run_exercises_can_be_generated_scenario(self, mock_generate_exercises, mock_build_prompts, mock_parse_input):
        input_data = "input data"
        result = self.task_gen.run(input_data)

        self.assertEqual(result, "input data" + "\n\n" + "exercises generated"*3)



    @patch('agent_service.tools.task_generation_tool.TaskGenerator.parse_input', return_value={"single-choice": 1, "gap-filling": 1, "open-ended": 1})
    @patch('agent_service.tools.task_generation_tool.TaskGenerator.build_prompts', return_value=("prompt_1", "prompt_2", "prompt_3"))
    @patch('agent_service.tools.task_generation_tool.TaskGenerator.generate_exercises', side_effect=ExercisesNotGeneratedException())
    def test_run_exercises_cant_be_generated_scenario(self, mock_generate_exercises, mock_build_prompts, mock_parse_input):
        input_data = "input data"

        with self.assertRaises(ExercisesNotGeneratedException) as context: 
            self.task_gen.run(input_data)
        
    def test_parse_input_reading(self):
        input_data = "[Reading][2][0][1][text]"
        result = self.task_gen.parse_input(input_data)

        self.assertEqual(result["type"], "Reading")
        self.assertEqual(result["single-choice"], 2)
        self.assertEqual(result["gap-filling"], 0)
        self.assertEqual(result["open-ended"], 1)
        self.assertEqual(result["text"], "text")  

    def test_parse_input_listening(self):
        input_data = "[Listening][2][0][1][text]"
        result = self.task_gen.parse_input(input_data)

        self.assertEqual(result["type"], "Listening")
        self.assertEqual(result["single-choice"], 2)
        self.assertEqual(result["gap-filling"], 0)
        self.assertEqual(result["open-ended"], 1)
        self.assertEqual(result["text"], "text")  

    def test_parse_input_grammar(self):
        input_data = "[Grammar][Perfekt][None][1][0][3][text]"
        result = self.task_gen.parse_input(input_data)

        self.assertEqual(result["type"], "Grammar")
        self.assertEqual(result["main-topic"], "Perfekt")
        self.assertEqual(result["secondary-topic"], "None")
        self.assertEqual(result["single-choice"], 1)
        self.assertEqual(result["gap-filling"], 0)
        self.assertEqual(result["open-ended"], 3)
        self.assertEqual(result["text"], "text")  
    
    @patch('agent_service.lesson.lesson_generation_retriever.LessonRetriever.get_examples', return_value="example exercises")
    def test_build_prompts_grammar(self, mock_get_examples):
        input_data = {"type": "Grammar", "main-topic": "Perfekt", "secondary-topic": "None", "single-choice": 2, "gap-filling": 0, "open-ended": 1, "text": "text"}
        original_generate_prompt = self.task_gen.prompt.generate_prompt
        self.task_gen.prompt.generate_prompt = Mock(return_value="generated_prompt")
        query_single_choice, query_gap_filling, query_open_ended = self.task_gen.build_prompts(input_data)

        self.assertEqual(query_single_choice, "generated_prompt")
        self.assertEqual(query_gap_filling, "generated_prompt")
        self.assertEqual(query_open_ended, "generated_prompt")

        expected_input_format_and_examples_1 = GRAMMAR_SINGLE_CHOICE + "example exercises"
        expected_input_format_and_examples_2 = GRAMMAR_GAP_FILLING + "example exercises"
        expected_input_format_and_examples_3 = GRAMMAR_OPEN_ENDED
        expected_text_1 = "[Perfekt][None][2][text]"
        expected_text_2 = "[Perfekt][None][0][text]"
        expected_text_3 = "[Perfekt][None][1][text]"
        self.task_gen.prompt.generate_prompt.assert_has_calls([
            call(name_id=self.task_gen.prompt_id, input_format_and_examples=expected_input_format_and_examples_1, text=expected_text_1),
            call(name_id=self.task_gen.prompt_id, input_format_and_examples=expected_input_format_and_examples_2, text=expected_text_2),
            call(name_id=self.task_gen.prompt_id, input_format_and_examples=expected_input_format_and_examples_3, text=expected_text_3)
        ])

        # restore the original method
        self.task_gen.prompt.generate_prompt = original_generate_prompt

    def test_build_prompts_reading(self):
        input_data = {"type": "Reading", "single-choice": 2, "gap-filling": 0, "open-ended": 1, "text": "text"}
        original_generate_prompt = self.task_gen.prompt.generate_prompt
        self.task_gen.prompt.generate_prompt = Mock(return_value="generated_prompt")
        query_single_choice, query_gap_filling, query_open_ended = self.task_gen.build_prompts(input_data)

        self.assertEqual(query_single_choice, "generated_prompt")
        self.assertEqual(query_gap_filling, "generated_prompt")
        self.assertEqual(query_open_ended, "generated_prompt")

        expected_input_format_and_examples_1 = READING_SINGLE_CHOICE
        expected_input_format_and_examples_2 = READING_GAP_FILLING
        expected_input_format_and_examples_3 = READING_OPEN_ENDED
        expected_text_1 = "[2][text]"
        expected_text_2 = "[0][text]"
        expected_text_3 = "[1][text]"
        self.task_gen.prompt.generate_prompt.assert_has_calls([
            call(name_id=self.task_gen.prompt_id, input_format_and_examples=expected_input_format_and_examples_1, text=expected_text_1),
            call(name_id=self.task_gen.prompt_id, input_format_and_examples=expected_input_format_and_examples_2, text=expected_text_2),
            call(name_id=self.task_gen.prompt_id, input_format_and_examples=expected_input_format_and_examples_3, text=expected_text_3)
        ])

        # restore the original method
        self.task_gen.prompt.generate_prompt = original_generate_prompt
    
    def test_build_prompts_listening(self):
        input_data = {"type": "Listening", "single-choice": 2, "gap-filling": 0, "open-ended": 1, "text": "text"}
        original_generate_prompt = self.task_gen.prompt.generate_prompt
        self.task_gen.prompt.generate_prompt = Mock(return_value="generated_prompt")
        query_single_choice, query_gap_filling, query_open_ended = self.task_gen.build_prompts(input_data)

        self.assertEqual(query_single_choice, "generated_prompt")
        self.assertEqual(query_gap_filling, "generated_prompt")
        self.assertEqual(query_open_ended, "generated_prompt")

        expected_input_format_and_examples_1 = READING_SINGLE_CHOICE
        expected_input_format_and_examples_2 = READING_GAP_FILLING
        expected_input_format_and_examples_3 = READING_OPEN_ENDED
        expected_text_1 = "[2][text]"
        expected_text_2 = "[0][text]"
        expected_text_3 = "[1][text]"
        self.task_gen.prompt.generate_prompt.assert_has_calls([
            call(name_id=self.task_gen.prompt_id, input_format_and_examples=expected_input_format_and_examples_1, text=expected_text_1),
            call(name_id=self.task_gen.prompt_id, input_format_and_examples=expected_input_format_and_examples_2, text=expected_text_2),
            call(name_id=self.task_gen.prompt_id, input_format_and_examples=expected_input_format_and_examples_3, text=expected_text_3)
        ])

        # restore the original method
        self.task_gen.prompt.generate_prompt = original_generate_prompt


        

