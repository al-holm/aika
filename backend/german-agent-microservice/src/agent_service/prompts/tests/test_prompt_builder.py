import os
import sys, os
testdir = os.path.dirname(__file__)
sys.path.insert(0, os.path.abspath(os.path.join(testdir, '../../../')))

from agent_service.prompts.prompt_builder import PromptBuidler
import unittest

class TestPromptBuidler(unittest.TestCase):
    def test_simple_substitute(self):
        """
        The function `test_simple_substitute` tests the substitution functionality of a prompt builder
        class in Python.
        """
        prompt = PromptBuidler("It's your ${x} ${y}.")
        result = prompt.update(x="black")
        self.assertEqual(result, "It's your black ${y}.")

    def test_double_substitute(self):
        """
        The function `test_double_substitute` tests the functionality of substituting  variables in a
        prompt string using a PromptBuilder class in Python.
        """
        prompt = PromptBuidler("It's your ${x} ${y}.")
        result = prompt.update(x="black", y="cat")
        self.assertEqual(result, "It's your black cat.")

    def test_reverse_substitute(self):
        """
        The function `test_double_substitute` tests the functionality of substituting  variables in a
        prompt string using a PromptBuilder class in Python.
        """
        prompt = PromptBuidler("It's your ${adj} ${noun}.")
        result = prompt.update(noun="dog", adj="white")
        self.assertEqual(result, "It's your white dog.")

    def test_consequent_substitute(self):
        """
        The function `test_double_substitute` tests the functionality of substituting  variables in a
        prompt string using a PromptBuilder class in Python.
        """
        prompt = PromptBuidler("It's your ${adj} ${noun}. I like ${obj}.")
        result = prompt.update(noun="dog")
        result = prompt.update(adj="black")
        result = prompt.update(obj="pythons")
        self.assertEqual(prompt.get_prompt(), "It's your black dog. I like pythons.")

    def test_consequent_reverse_substitute(self):
        """
        The function `test_double_substitute` tests the functionality of substituting  variables in a
        prompt string using a PromptBuilder class in Python.
        """
        prompt = PromptBuidler("It's your ${adj} ${noun}. I like ${obj}.")
        result1 = prompt.update(noun="dog")
        result2 = prompt.update(adj="black")
        result3 = prompt.update(obj="pythons")
        prompt.set_prompt(result2)
        result = prompt.update(obj="cats")
        self.assertEqual(prompt.get_prompt(), "It's your black dog. I like cats.")

    def test_last_substitute(self):
        """
        The function `test_last_substitute` tests the functionality of updating a specific placeholder in a
        prompt string using a PromptBuilder class in Python.
        """
        prompt = PromptBuidler("It's your ${x} ${y}.")
        result = prompt.update(y="cat")
        self.assertEqual(result, "It's your ${x} cat.")


if __name__ == '__main__':
    unittest.main()