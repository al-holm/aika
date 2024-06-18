import unittest, logging, xmlrunner
import sys, os
testdir = os.path.dirname(__file__)
sys.path.insert(0, os.path.abspath(os.path.join(testdir, '../../../')))
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
        print(result)
        self.assertEqual(True, True)

    def test_run_reading(self):
        input_str = self.example_reading

        result = self.generator.run(input_str)
        print(result)
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'))