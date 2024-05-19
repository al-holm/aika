from prompts.prompt_builder import PromptBuidler
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