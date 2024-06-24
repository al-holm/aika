import unittest
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