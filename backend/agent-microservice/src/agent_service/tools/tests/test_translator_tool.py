import unittest
from unittest.mock import patch, MagicMock
import sys, os

testdir = os.path.dirname(__file__)
sys.path.insert(0, os.path.abspath(os.path.join(testdir, "../../../")))

from agent_service.tools.translator_tool import Translator


class TestTranslator(unittest.TestCase):
    def setUp(self):
        self.translator = Translator(
            name="Test Translator",
            description="A test translator",
            llm=None,
            prompt_id="test_id",
            prompt_template="template",
            max_tokens=0,
        )

    @patch("deepl.Translator")
    def test_initialization(self, mock_translator):
        examples = """
        Beispiele: 
        Как я могу сказать "Меня зовут Али" по-немецки?
        Action: Übersetzer
        Action Input: Меня зовут Али - [DE]

        Перекладіть "Ich habe heute eine Katze gesehen".
        Action: Übersetzer
        Action Input: Ich habe heute eine Katze gesehen - [UK]

        """
        self.assertEqual(self.translator.name, "Test Translator")
        self.assertEqual(self.translator.description, "A test translator" + examples)

    def test_parse_target_language(self):
        self.assertEqual(
            self.translator.parse_target_language("Translate this - [DE]"), "de"
        )
        self.assertEqual(
            self.translator.parse_target_language("Translate this - [EN]"), "en-us"
        )
        self.assertEqual(
            self.translator.parse_target_language("Translate this - [XX]"), ""
        )

    @patch("deepl.Translator.translate_text")
    def test_run_success(self, mock_deepl_translator_text):
        mock_deepl_translator_text.return_value = "Ich bin Ali"

        input_str = "My name is Ali - [DE]"

        result = self.translator.run(input_str)

        self.assertIn("Die Übersetztung lautet:\nIch bin Ali", result)

    @patch("deepl.Translator")
    def test_run_invalid_format(self, mock_deepl_translator):
        input_str = "My name is Ali - DE"

        result = self.translator.run(input_str)

        # Assert the expected output
        self.assertIn("Du hast das falsche Format als Action Input gegeben", result)

    @patch("deepl.Translator")
    def test_run_unsupported_language(self, mock_deepl_translator):
        input_str = "My name is Ali - [XX]"

        result = self.translator.run(input_str)

        # Assert the expected output
        self.assertIn("Du hast das falsche Format als Action Input gegeben", result)


if __name__ == "__main__":
    unittest.main()
