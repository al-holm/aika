import os, xmlrunner
import sys, os
testdir = os.path.dirname(__file__)
sys.path.insert(0, os.path.abspath(os.path.join(testdir, '../../../')))

import unittest
from agent_service.parsers.agent_step_parser import ValidationParser
from agent_service.agent.agent_step import AgentValidationStep  # Ensure this import matches your module's structure

class TestValidationParser(unittest.TestCase):

    def setUp(self):
        self.parser = ValidationParser()

    def test_parse_step(self):
        input_str = "This is a validation thought.\nAdditional information."
        expected_step = AgentValidationStep(validation_thought="This is a validation thought.")

        result = self.parser.parse_step(input_str)
        self.assertEqual(result, expected_step)


    def test_parse_step_empty_input(self):
        input_str = ""
        expected_step = AgentValidationStep(validation_thought="")

        result = self.parser.parse_step(input_str)

        self.assertEqual(result, expected_step)


if __name__ == '__main__':
    unittest.main()