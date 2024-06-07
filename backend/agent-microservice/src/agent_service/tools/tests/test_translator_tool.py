import unittest, xmlrunner
from unittest.mock import patch, MagicMock
import sys, os
testdir = os.path.dirname(__file__)
sys.path.insert(0, os.path.abspath(os.path.join(testdir, '../../../')))

from agent_service.tools.translator_tool import Translator


class TestTranslator(unittest.TestCase):
    
    @patch('deepl.Translator')
    def test_initialization(self, mock_translator):
        translator = Translator(name="Test Translator", description="A test translator", llm="runpod",
                                prompt_id="test_id", prompt_template="template", max_tokens=100)
        examples= """
        Beispiele: 
        Как я могу сказать "Меня зовут Али" по-немецки?
        Action: Übersetzer
        Action Input: Меня зовут Али - [DE]

        Перекладіть "Ich habe heute eine Katze gesehen".
        Action: Übersetzer
        Action Input: Ich habe heute eine Katze gesehen - [UK]

        """
        self.assertEqual(translator.name, "Test Translator")
        self.assertEqual(translator.description, "A test translator"+examples)

    def test_parse_target_language(self):
        translator = Translator(name="Test Translator", description="A test translator", llm="runpod",
                                prompt_id="test_id", prompt_template="template", max_tokens=100)
        self.assertEqual(translator.parse_target_language("Translate this - [DE]"), "de")
        self.assertEqual(translator.parse_target_language("Translate this - [EN]"), "en-us")
        self.assertEqual(translator.parse_target_language("Translate this - [XX]"), "")

    @patch('deepl.Translator')
    def test_run_success(self, mock_deepl_translator):
        mock_translator_instance = mock_deepl_translator.return_value
        mock_translator_instance.translate_text.return_value = "Ich bin Ali"

        translator = Translator(
            name="Test Translator",
            description="A test translator",
            llm="runpod",
            prompt_id="test_id",
            prompt_template="template",
            max_tokens=100
        )

        input_str = "My name is Ali - [DE]"

        result = translator.run(input_str)

        self.assertIn("Die Übersetztung lautet:\nIch bin Ali", result)
    
    @patch('deepl.Translator')
    def test_run_invalid_format(self, mock_deepl_translator):
        translator = Translator(
            name="Test Translator",
            description="A test translator",
            llm="runpod",
            prompt_id="test_id",
            prompt_template="template",
            max_tokens=100
        )

        input_str = "My name is Ali - DE"

        result = translator.run(input_str)

        # Assert the expected output
        self.assertIn("Du hast das falsche Format als Action Input gegeben", result)

    @patch('deepl.Translator')
    def test_run_unsupported_language(self, mock_deepl_translator):
        # Initialize the Translator
        translator = Translator(
            name="Test Translator",
            description="A test translator",
            llm="runpod",
            prompt_id="test_id",
            prompt_template="template",
            max_tokens=100
        )

        input_str = "My name is Ali - [XX]"

        result = translator.run(input_str)

        # Assert the expected output
        self.assertIn("Du hast das falsche Format als Action Input gegeben", result)

if __name__ == '__main__':
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'))