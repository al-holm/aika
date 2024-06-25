import unittest
from unittest.mock import Mock, call
from agent_service.tools.task_generation_tool import TaskGenerator
from agent_service.prompts.task_generation_examples import READING_GAP_FILLING, READING_OPEN_ENDED, READING_SINGLE_CHOICE

class TestTaskGenerator(unittest.TestCase):

    def setUp(self):
        self.task_gen = TaskGenerator(name="name", description="desc",
                                      llm="bedrock", prompt_id="prompt_id",
                                      prompt_template="prompt_template", max_tokens= 1000)
    
    def test_parse_input_reading(self):
        input_data = "[Reading][2][0][1][text]"
        result = self.task_gen.parse_input(input_data)

        self.assertEqual(result["type"], "Reading")
        self.assertEqual(result["single-choice"], 2)
        self.assertEqual(result["gap-filling"], 0)
        self.assertEqual(result["open-ended"], 1)
        self.assertEqual(result["text"], "text")

    def test_build_prompts_reading(self):
        self.task_gen.prompt.generate_prompt = Mock(return_value="generated_prompt")
        query = {"type": "Reading", "single-choice": 2, "gap-filling": 0, "open-ended": 1, "text": "text"}
        query_single_choice, query_gap_filling, query_open_ended = self.task_gen.build_prompts(query)

        self.assertEqual(query_single_choice, "generated_prompt")
        self.assertEqual(query_gap_filling, "generated_prompt")
        self.assertEqual(query_open_ended, "generated_prompt")


        # expected_input_format_and_examples_1 = READING_SINGLE_CHOICE
        # expected_input_format_and_examples_2 = READING_GAP_FILLING
        # expected_input_format_and_examples_3 = READING_OPEN_ENDED
        # expected_text_1 = "[2][text]"
        # expected_text_2 = "[0]text"
        # expected_text_3 = "[1]text"
        # self.task_gen.prompt.generate_prompt.assert_has_calls([
        #     call(name_id=self.task_gen.prompt_id, input_format_and_examples=expected_input_format_and_examples_1, text=expected_text_1),
        #     call(name_id=self.task_gen.prompt_id, input_format_and_examples=expected_input_format_and_examples_2, text=expected_text_2),
        #     call(name_id=self.task_gen.prompt_id, input_format_and_examples=expected_input_format_and_examples_3, text=expected_text_3)
        # ])


        

