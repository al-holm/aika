import os
import sys, os
testdir = os.path.dirname(__file__)
sys.path.insert(0, os.path.abspath(os.path.join(testdir, '../../../')))

from agent_service.prompts.prompt_builder import PromptBuilder, Prompt
import unittest

class TestPrompt(unittest.TestCase):

    def setUp(self):
        self.prompt = Prompt('greeting', 'Hello, ${name}!')

    def test_initialization(self):
        self.assertEqual(self.prompt.name, 'greeting')
        self.assertEqual(self.prompt.prompt, 'Hello, ${name}!')

    def test_name_property(self):
        self.prompt.name = 'welcome'
        self.assertEqual(self.prompt.name, 'welcome')

    def test_prompt_property(self):
        self.prompt.prompt = 'Hi, ${name}!'
        self.assertEqual(self.prompt.prompt, 'Hi, ${name}!')

    def test_str_method(self):
        self.assertEqual(str(self.prompt), 'Hello, ${name}!')

if __name__ == '__main__':
    unittest.main()