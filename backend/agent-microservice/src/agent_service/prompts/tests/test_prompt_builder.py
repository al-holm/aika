import os
import sys, os
testdir = os.path.dirname(__file__)
sys.path.insert(0, os.path.abspath(os.path.join(testdir, '../../../')))

from agent_service.prompts.prompt_builder import PromptBuilder, Prompt
import unittest

class TestPromptBuilder(unittest.TestCase):
    
    def setUp(self):
        self.builder = PromptBuilder()
        self.sample_prompts = {
            "greet": "Hello, ${name}!",
            "farewell": "Goodbye, ${name}. See you ${time}."
        }
        self.builder.create_prompts(self.sample_prompts)

    def test_create_prompts(self):
        self.assertEqual(len(self.builder._prompts), 2)
        self.assertIn("greet", self.builder._prompts)
        self.assertIn("farewell", self.builder._prompts)

    def test_generate_prompt(self):
        result = self.builder.generate_prompt("greet", **{'name': "Alice"})
        self.assertEqual(result, "Hello, Alice!")
        
        result = self.builder.generate_prompt("farewell",  **{'name':"Bob", 'time':"tomorrow"})
        self.assertEqual(result, "Goodbye, Bob. See you tomorrow.")

    def test_update_prompt(self):
        updated_prompt = self.builder.update_prompt("greet", name="Charlie")
        self.assertEqual(updated_prompt, "Hello, Charlie!")
        self.assertEqual(self.builder.get_prompt("greet"), "Hello, Charlie!")

    def test_get_prompt(self):
        prompt = self.builder.get_prompt("greet")
        self.assertEqual(prompt, "Hello, ${name}!")

    def test_set_prompt(self):
        self.builder.set_prompt("greet", "Hi, ${name}!")
        self.assertEqual(self.builder.get_prompt("greet"), "Hi, ${name}!")

if __name__ == '__main__':
    unittest.main()