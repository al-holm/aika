import sys, os
testdir = os.path.dirname(__file__)
srcdir = '../../../../src/agent_service/utils/prompt/'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))
print(os.path.abspath(os.path.join(testdir, srcdir)))
import prompt_builder
import unittest

class TestPromptBuidler(unittest.TestCase):
    def test_simple_substitute(self):
        """
        The function `test_simple_substitute` tests the substitution functionality of a prompt builder
        class in Python.
        """
        prompt = prompt_builder.PromptBuidler("It's your ${x} ${y}.")
        result = prompt.update(x="black")
        self.assertEqual(result, "It's your black ${y}.")

    def test_double_substitute(self):
        """
        The function `test_double_substitute` tests the functionality of substituting multiple variables in a
        prompt string using a PromptBuilder class in Python.
        """
        prompt = prompt_builder.PromptBuidler("It's your ${x} ${y}.")
        result = prompt.update(x="black", y="cat")
        self.assertEqual(result, "It's your black cat.")

    def test_last_substitute(self):
        """
        The function `test_last_substitute` tests the functionality of updating a specific placeholder in a
        prompt string using a PromptBuilder class in Python.
        """
        prompt = prompt_builder.PromptBuidler("It's your ${x} ${y}.")
        result = prompt.update(y="cat")
        self.assertEqual(result, "It's your ${x} cat.")


if __name__ == '__main__':
    unittest.main()