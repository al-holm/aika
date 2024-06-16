import os
import sys, os
testdir = os.path.dirname(__file__)
sys.path.insert(0, os.path.abspath(os.path.join(testdir, '../../../')))
from pydantic import ValidationError
import unittest, xmlrunner
from agent_service.agent.agent_step import AgentStep
from agent_service.exeptions.step_exception import ActionInputNotFoundException, ActionNotFoundException, InvalidToolException
from agent_service.parsers.agent_step_parser import StepParser  # Ensure this import matches your module's structure

class TestStepParser(unittest.TestCase):

    def setUp(self):
        self.tool_names = ["ToolA", "ToolB"]
        self.parser = StepParser(self.tool_names)

    def test_parse_step(self):
        input_str = "Thought: This is a thought\nAction: ToolA\nAction Input: Some input"
        expected_step = AgentStep(thought="This is a thought", action="ToolA", action_input="Some input")
        result = self.parser.parse_step(input_str)
        self.assertEqual(result, expected_step)

    def test_parse_step_missing_action(self):
        input_str = "Thought: This is a thought\nAction Input: Some input"
        with self.assertRaises(ActionNotFoundException):
            self.parser.parse_step(input_str)

    def test_parse_step_invalid_action(self):
        input_str = "Thought: This is a thought\nAction: ToolX\nAction Input: Some input"
        with self.assertRaises(InvalidToolException):
            self.parser.parse_step(input_str)

    def test_parse_step_missing_action_input(self):
        input_str = "Thought: This is a thought\nAction: ToolA"
        with self.assertRaises(ActionInputNotFoundException):
            self.parser.parse_step(input_str)

    def test_extract_thought(self):
        first_line = "Thought: This is a thought"
        expected_thought = "This is a thought"
        result = self.parser.extract_thought(first_line)
        self.assertEqual(result, expected_thought)

        first_line_no_prefix = "This is a thought"
        result = self.parser.extract_thought(first_line_no_prefix)
        self.assertEqual(result, first_line_no_prefix)

    def test_parse_step_model_validation(self):
        with self.assertRaises(ValidationError):
            AgentStep(thought="This is a thought", action=None, action_input="Some input")
        
        with self.assertRaises(ValidationError):
            AgentStep(thought="This is a thought", action="ToolA", action_input=None)
        
        with self.assertRaises(ValidationError):
            AgentStep(thought=None, action="ToolA", action_input="Some input")

    def test_extract_action(self):
        remaining_text = "Action: ToolA\nAction Input: Some input"
        expected_action = "ToolA"
        expected_action_input = "Some input"
        action, action_input = self.parser.extract_action(remaining_text)
        self.assertEqual(action, expected_action)
        self.assertEqual(action_input, expected_action_input)

    def test_extract_action_with_quotes(self):
        remaining_text = 'Action: "ToolA"\nAction Input: "Some input"'
        expected_action = "ToolA"
        expected_action_input = "Some input"
        action, action_input = self.parser.extract_action(remaining_text)
        self.assertEqual(action, expected_action)
        self.assertEqual(action_input, expected_action_input)

    def test_remove_quotes(self):
        self.assertEqual(self.parser.remove_quotes('"Quoted"'), 'Quoted')
        self.assertEqual(self.parser.remove_quotes("'Quoted'"), 'Quoted')
        self.assertEqual(self.parser.remove_quotes('NoQuotes'), 'NoQuotes')
        self.assertIsNone(self.parser.remove_quotes(None))

if __name__ == '__main__':
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'))