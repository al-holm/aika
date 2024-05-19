from tools import reading_generation_tool 
import unittest

class TestReadingGenTool(unittest.TestCase):
    def test_prompt(self):
        """
        The `test_prompt` function tests the `update` method of a `ReadingGenerator` object by checking
        if the updated text matches a specific regular expression pattern.
        """
        rg = reading_generation_tool.ReadingGenerator()
        res = rg.prompt.update(text="Generiere einen Lesetext zum Thema 'Familie'.")
        self.assertRegexpMatches(res, r"Generiere einen Lesetext zum Thema 'Familie'.")

if __name__ == '__main__':
    unittest.main()