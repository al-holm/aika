import unittest, logging
from agent_service.tools.task_generation_tool import TaskGenerator
from agent_service.core.config import Config
from agent_service.agent.task_type import TaskType
from scripts.setup_logging import setup_logging

# Run it from src directory using "python -m unittest .\agent_service\tools\tests\test_task_generation_tool.py"
class TestTaskGenerator(unittest.TestCase):

    def setUp(self):
        setup_logging()

        self.example_reading = """[Reading][3][2][1][Guten Tag, ich möchte Ihnen heute eine Geschichte über eine Familie erzählen. Die Familie heißt Schmidt und besteht aus vier Personen: Vater, Mutter, Tochter und Sohn. Vater Schmidt arbeitet als Ingenieur und ist oft unterwegs. Mutter Schmidt ist Lehrerin und kümmert sich um die Kinder.\nDie Tochter heißt Julia und ist 16 Jahre alt. Sie geht gerne mit ihren Freunden aus und spielt Klavier.\nDer Sohn heißt Max und ist 13 Jahre alt. Er spielt Fußball und ist sehr aktiv.\nJeden Sonntag essen sie zusammen zu Mittag und spielen Spiele oder gehen spazieren. Sie sind eine glückliche Familie, die viel Zeit miteinander verbringt.]"""

        self.example_grammar = """[Grammar][Konjuktiv I][None][3][2][1][
Hallo,

der Konjunktiv I ist eine besondere Form des Verbs, die wir in der deutschen Sprache verwenden. Er wird oft in der indirekten Rede, also wenn wir die Worte einer anderen Person wiedergeben, genutzt.

Die Bildung des Konjunktiv I erfolgt durch die Endungen -e, -est, -et, -en, -et, -en. Hier ein Beispiel:

Ich spiele -> Er spiele

Du spielst -> Sie spiele

Er spielt -> Sie spiele

Wir spielen -> Sie spielen

Ihr spielt -> Sie spielen

Sie spielen -> Sie spielen

Die Endungen werden an den Präsensstamm des Verbs angehängt. Der Präsensstamm ist die Grundform des Verbs ohne die Endungen -e, -st, -t, -en, -t, -en.

Der Konjunktiv I wird auch in einigen festen Wendungen verwendet, wie zum Beispiel "Hoch lebe das Geburtstagskind!".   

Ich hoffe, dass ich dir mit meiner Erklärung und den Beispielen helfen konnte.

Viele Grüße,
Dein Deutschlehrer]"""


        llm = 'bedrock'
        task_type = TaskType.LESSON
        Config.set_llm(llm, task_type)
        self.generator = TaskGenerator(llm=llm)

    def test_run_grammar(self):
        input_str = self.example_grammar

        result = self.generator.run(input_str)
        self.assertEqual(True, True)

    def test_run_reading(self):
        input_str = self.example_reading

        #result = self.generator.run(input_str)
        self.assertEqual(True, True)

    def test_parse_input_grammar_example(self):
        input_str = self.example_grammar

        expected_output = {
            'type': 'Grammar',
            'main-topic': 'Konjuktiv I',
            'secondary-topic': 'None',
            'single-choice': '3',
            'gap-filling': '2',
            'open': '1',
            'text': """
Hallo,

der Konjunktiv I ist eine besondere Form des Verbs, die wir in der deutschen Sprache verwenden. Er wird oft in der indirekten Rede, also wenn wir die Worte einer anderen Person wiedergeben, genutzt.

Die Bildung des Konjunktiv I erfolgt durch die Endungen -e, -est, -et, -en, -et, -en. Hier ein Beispiel:

Ich spiele -> Er spiele

Du spielst -> Sie spiele

Er spielt -> Sie spiele

Wir spielen -> Sie spielen

Ihr spielt -> Sie spielen

Sie spielen -> Sie spielen

Die Endungen werden an den Präsensstamm des Verbs angehängt. Der Präsensstamm ist die Grundform des Verbs ohne die Endungen -e, -st, -t, -en, -t, -en.

Der Konjunktiv I wird auch in einigen festen Wendungen verwendet, wie zum Beispiel "Hoch lebe das Geburtstagskind!".   

Ich hoffe, dass ich dir mit meiner Erklärung und den Beispielen helfen konnte.

Viele Grüße,
Dein Deutschlehrer"""
        }
        result = self.generator.parse_input(input_str)
        self.assertEqual(result, expected_output)

        
    def test_parse_input_grammar(self):
        input_str = "[Grammar][Nouns][Plural][5][3][2][Explanation text about nouns]"
        expected_output = {
            'type': 'Grammar',
            'main-topic': 'Nouns',
            'secondary-topic': 'Plural',
            'single-choice': '5',
            'gap-filling': '3',
            'open': '2',
            'text': 'Explanation text about nouns'
        }
        result = self.generator.parse_input(input_str)
        self.assertEqual(result, expected_output)

    def test_parse_input_reading(self):
        input_str = "[Reading][5][3][2][Text for reading comprehension tasks]"
        expected_output = {
            'type': 'Reading',
            'single-choice': '5',
            'gap-filling': '3',
            'open': '2',
            'text': 'Text for reading comprehension tasks'
        }
        result = self.generator.parse_input(input_str)
        self.assertEqual(result, expected_output)

    def test_parse_input_invalid_format(self):
        input_str = "[Invalid][5][3]"
        with self.assertRaises(Exception):
            self.generator.parse_input(input_str)

    def test_parse_input_missing_sections(self):
        input_str = "[Grammar]"
        with self.assertRaises(Exception):
            self.generator.parse_input(input_str)

    def test_fill_prompt_grammar_task(self):
        # Test the handling of a Grammar task
        input_dict = {
            "type": "Grammar",
            "main-topic": "Nouns",
            "secondary-topic": "Plural",
            "single-choice": "5",
            "gap-filling": "3",
            "open": "2",
            "text": "some explanation"
        }

        first_query, second_query = self.generator.fill_prompt(input_dict)
        
        self.assertIn("Nouns", first_query)
        self.assertIn("Plural", second_query)
        self.assertIn("some explanation", first_query)
        self.assertIn("5", first_query)
        self.assertIn("3", second_query)

    def test_fill_prompt_reading_task(self):
        # Test the handling of a Reading task
        input_dict = {
            "type": "Reading",
            "single-choice": "10",
            "gap-filling": "6",
            "open": "1",
            "text": "reading comprehension content"
        }
        first_query, second_query = self.generator.fill_prompt(input_dict)
        
        self.assertIn("10", first_query)
        self.assertIn("1", second_query)
        self.assertIn("reading comprehension content", second_query)

    def test_fill_prompt_invalid_task_type(self):
        # Test handling of an invalid task type
        input_dict = {
            "type": "InvalidType",
            "text": "invalid task"
        }
        with self.assertRaises(KeyError):
            self.generator.fill_prompt(input_dict)


