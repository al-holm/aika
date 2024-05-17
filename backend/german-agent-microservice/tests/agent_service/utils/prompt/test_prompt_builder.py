from agent_service.utils.prompt.prompt_builder import PromptBuidler
import unittest

class TestPromptBuidler(unittest.TestCase):
    def test_simple_substitute(self):
        """
        Test that it can sum a list of integers
        """
        prompt = PromptBuidler("It's your ${x} ${y}.")
        result = prompt.update(x="black")
        self.assertEqual(result, "It's your black ${y}.")

if __name__ == '__main__':
    unittest.main()