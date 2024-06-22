import unittest
from unittest.mock import Mock
from agent_service.tools.task_generation_tool import TaskGenerator
from agent_service.prompts.tool_prompt import TASK_TEMPLATE
from agent_service.agent.task_type import TaskType
from agent_service.core.config import Config

# Run it from src directory using "python -m unittest .\agent_service\tools\tests\test_task_generation_tool.py"
class TestTaskGenerator(unittest.TestCase):

    def setUp(self):
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


        self.llm = 'bedrock'
        task_type = TaskType.LESSON
        Config.set_llm(self.llm, task_type)

    def setUpForBuildPrompts(self):
        self.generator = TaskGenerator(
                    name="name", description="description", llm="bedrock", 
                    prompt_id="prompt_id", prompt_template="TASK_TEMPLATE", max_tokens=1000)
        self.generator.get_examples = Mock(return_value="Example")
        self.generator.prompt = Mock()
        self.generator.prompt.generate_prompt.return_value = "Generated Prompt"

    def test_build_prompts_grammar_correct_input(self):
        self.setUpForBuildPrompts()
        input = {
            "type": "Grammar",
            "main-topic": "main_topic",
            "secondary-topic": "secondary_topic",
            "single-choice": 1,
            "gap-filling": 1,
            "open-ended": 1,
            "text": "text"
        }
        result = self.generator.build_prompts(input)
        self.generator.get_examples.assert_called()
        self.generator.prompt.generate_prompt.assert_called()
    
    def test_build_prompts_grammar_missing_key(self):
        self.setUpForBuildPrompts()
        input = {
            "main-topic": "main_topic",
            "secondary-topic": "secondary_topic",
            "single-choice": 1,
            "gap-filling": 1,
            "open-ended": 1
        }
        with self.assertRaises(Exception) as context:
            self.generator.build_prompts(input)
        
        self.assertEqual(str(context.exception), "'type'")
    
    def test_build_prompts_grammar_wrong_value(self):
        self.setUpForBuildPrompts()
        input = {
            "type": "Grammar",
            "main-topic": "main_topic",
            "secondary-topic": "secondary_topic",
            "single-choice": "Single-choice",
            "gap-filling": "Gap-filling",
            "open-ended": "Open-Ended",
            "text": "text"
        }
        with self.assertRaises(Exception) as context:
            self.generator.build_prompts(input)
        
        self.assertEqual(str(context.exception), "Wrong value type")

if __name__ == '__main__':
    unittest.main()