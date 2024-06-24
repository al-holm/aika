import unittest, re
from unittest.mock import Mock
from agent_service.tools.lesson_master import LessonMaster


class TestLessonMaster(unittest.TestCase):

    def setUp(self):
        self.lesson_master = LessonMaster()


    def test_parse_query_correct_input(self):
        query = "[Grammar][Perfekt][None][1][1][1]"
        result = self.lesson_master.parse_query(query)

        self.assertEqual(result["type"], "Grammar")
        self.assertEqual(result["main-topic"], "Perfekt")
        self.assertEqual(result["secondary-topic"], "None")
        self.assertEqual(result["single-choice"], "1")
        self.assertEqual(result["gap-filling"], "1")
        self.assertEqual(result["open-ended"], "1")

    def test_parse_query_correct_input(self):
        query = "[Reading][Ich stelle mich vor. Wie alt bin ich? Woher komme ich? Was mache ich beruflich (kurz)? Was mache ich in der Freizeit?][None][2][1][1]"
        result = self.lesson_master.parse_query(query)

        self.assertEqual(result["type"], "Reading")
        self.assertEqual(result["main-topic"], "Ich stelle mich vor. Wie alt bin ich? Woher komme ich? Was mache ich beruflich (kurz)? Was mache ich in der Freizeit?")
        self.assertEqual(result["secondary-topic"], "None")
        self.assertEqual(result["single-choice"], "2")
        self.assertEqual(result["gap-filling"], "1")
        self.assertEqual(result["open-ended"], "1")
    
    def test_create_text_reading(self):
        self.lesson_master.tool_executor.execute = Mock(return_value="text")
        query = "[Reading][Ich stelle mich vor. Wie alt bin ich? Woher komme ich? Was mache ich beruflich (kurz)? Was mache ich in der Freizeit?][None][2][1][1]"
        result = self.lesson_master.create_text(query)

        self.assertEqual(result, "text")
        
        matches = re.findall(r'\[(.*?)\]', self.lesson_master.task_generator_query, re.DOTALL)
        self.lesson_master.tool_executor.execute.assert_called()
        self.assertEqual(matches[0], "Reading")
        self.assertEqual(matches[1], "2")
        self.assertEqual(matches[2], "1")
        self.assertEqual(matches[3], "1")
        self.assertEqual(matches[4], "text")

