import unittest
from agent_service.parsers.exercises_parser import ExercisesParser

class TestExercisesParser(unittest.TestCase):

    def setUp(self):
        self.parser = ExercisesParser()
        self.grammar_example = """[Grammar][main-topic][secondary-topic][1][1][1][explanation-text. ]

[START]
Type: [single-choice]
Question: [Welches Verb ist richtig konjugiert im Präteritum?]
Answer options: [a) Er gehe b) Er ging c) Er geht]
Solution: [b) Er ging]
[END]
[START]
Type: [gaps]
Question: [Füllen Sie die Lücken mit der richtigen Präteritumform des Verbs]
Answer options: [1. Gestern (sah, sahen, gesehen) ich einen interessanten Film. 2. Wir (fuhren, fahr, fahrten) letztes Jahr nach Spanien. 3. Er (schreibte, schrieben, schrieb) einen langen Brief.]
Solution: [sah, fuhren, schrieb]
[END]
[START]
Type: [open]
Question: [Schreiben Sie über ein Erlebnis aus Ihrer Kindheit im Präteritum. Beschreiben Sie, was passiert ist, und wie Sie sich dabei gefühlt haben.]
Answer options: None
Solution: None
[END]"""
        self.reading_example = """[Reading][1][1][1][text-to-read. ]

[START]
Type: [single-choice]
Question: [Welches Verb ist richtig konjugiert im Präteritum?]
Answer options: [a) Er gehe b) Er ging c) Er geht]
Solution: [b) Er ging]
[END]
[START]
Type: [gaps]
Question: [Füllen Sie die Lücken mit der richtigen Präteritumform des Verbs]
Answer options: [1. Gestern (sah, sahen, gesehen) ich einen interessanten Film. 2. Wir (fuhren, fahr, fahrten) letztes Jahr nach Spanien. 3. Er (schreibte, schrieben, schrieb) einen langen Brief.]
Solution: [sah, fuhren, schrieb]
[END]
[START]
Type: [open]
Question: [Schreiben Sie über ein Erlebnis aus Ihrer Kindheit im Präteritum. Beschreiben Sie, was passiert ist, und wie Sie sich dabei gefühlt haben.]
Answer options: None
Solution: None
[END]"""
        self.listening_example = """[Listening][1][1][1][text-to-listen. ]

[START]
Type: [single-choice]
Question: [Welches Verb ist richtig konjugiert im Präteritum?]
Answer options: [a) Er gehe b) Er ging c) Er geht]
Solution: [b) Er ging]
[END]
[START]
Type: [gaps]
Question: [Füllen Sie die Lücken mit der richtigen Präteritumform des Verbs]
Answer options: [1. Gestern (sah, sahen, gesehen) ich einen interessanten Film. 2. Wir (fuhren, fahr, fahrten) letztes Jahr nach Spanien. 3. Er (schreibte, schrieben, schrieb) einen langen Brief.]
Solution: [sah, fuhren, schrieb]
[END]
[START]
Type: [open]
Question: [Schreiben Sie über ein Erlebnis aus Ihrer Kindheit im Präteritum. Beschreiben Sie, was passiert ist, und wie Sie sich dabei gefühlt haben.]
Answer options: None
Solution: None
[END]"""

    def test_parse_grammar_correct_input(self):
        result = self.parser.parse(self.grammar_example)
        self.assert_correct_input(result)
        self.assertEqual(result["text"], "explanation-text.")

    def test_parse_reading_correct_input(self):
        result = self.parser.parse(self.reading_example)
        self.assert_correct_input(result)
        self.assertEqual(result["text"], "text-to-read.")

    def test_parse_listening_correct_input(self):
        result = self.parser.parse(self.listening_example)
        self.assert_correct_input(result)
        self.assertEqual(result["text"], "text-to-listen.")

    def assert_correct_input(self, result):
        exercises = result["tasks"]
        self.assertEqual(exercises[0]["type"], "single-choice")
        self.assertEqual(exercises[0]["question"], "Welches Verb ist richtig konjugiert im Präteritum?")
        self.assertEqual(exercises[0]["answer_options"], [['Er gehe', 'Er ging', 'Er geht']])
        self.assertEqual(exercises[0]["solution"], [' Er ging'])

        self.assertEqual(exercises[1]["type"], "gaps")
        self.assertEqual(exercises[1]["question"], "1. Gestern __ ich einen interessanten Film. 2. Wir __ letztes Jahr nach Spanien. 3. Er __ einen langen Brief.")
        self.assertEqual(exercises[1]["answer_options"], [["sah", "sahen", "gesehen"], ["fuhren", "fahr", "fahrten"], ["schreibte", "schrieben", "schrieb"]])
        self.assertEqual(exercises[1]["solution"], [["sah", "fuhren", "schrieb"]])
        
        self.assertEqual(exercises[2]["type"], "open")
        self.assertEqual(exercises[2]["question"], "Schreiben Sie über ein Erlebnis aus Ihrer Kindheit im Präteritum. Beschreiben Sie, was passiert ist, und wie Sie sich dabei gefühlt haben.")
        self.assertEqual(exercises[2]["answer_options"], [[""]])
        self.assertEqual(exercises[2]["solution"], [""])


if __name__ == '__main__':
    unittest.main()