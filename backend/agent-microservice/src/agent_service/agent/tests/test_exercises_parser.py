import unittest
from agent_service.agent.exercises_parser import ExercisesParser

class TestExercisesParser(unittest.TestCase):

    def test_parse_single_choice_exercises(self):
        parser = ExercisesParser()
        input_text = """[Grammar][Konjuktiv I][None][3][2][1][
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
Dein Deutschlehrer]

[START]
Type: [single-choice]
Question: [Welches Verb ist richtig konjugiert im Konjunktiv I?]
Answer options: [a) Er spiele b) Er spielt c) Er ging]
Solution: [a) Er spiele]
[END]
[START]
Type: [single-choice]
Question: [Welches ist die Konjunktiv I Form von "haben"?]
Answer options: [a) hätte b) haben c) hattest]
Solution: [a) hätte]
[END]
[START]
Type: [single-choice]
Question: [Welche Form im Konjunktiv I ist korrekt?]
Answer options: [a) Sie wäre b) Sie war c) Sie sei]
Solution: [c) Sie sei]
[END]
[START]
Type: [gaps]
Question: [Füllen Sie die Lücken mit der richtigen Konjunktiv I Form]
Answer options: [1. Wenn ich ein [großes, großer, großen] Haus hätte, [könnte, können, könntest] ich viele Partys veranstalten. 2. Wenn ich einen [intelligent, intelligente, intelligenten] Hund hätte, [bräuchte, brauchen, bräuchten] ich keinen Trainer.]
Solution: [großes, hätte, intelligenten, bräuchte]
[END]
[START]
Type: [gaps]
Question: [Füllen Sie die Lücken mit der richtigen Konjunktiv I Form]
Answer options: [1. Wenn sie eine [neue, neuer, neu] Wohnung fände, [würde ziehen, ziehen würde, zöge] sie sofort um. 2. Wenn wir einen [freundlichen, freundlich, freundliche] Nachbarn hätten, [wäre, sein, wären] das Leben viel angenehmer.]
Solution: [neue, zöge, freundlichen, wäre]
[END]
[START]
Type: [open]
Question: [Schreibe einen Satz im Konjunktiv I.]
Answer options: None
Solution: [Er spiele Fußball, wenn er Zeit hätte.]
[END]"""
        exercises = parser.parse(input_text)
        
        # Check general structure
        self.assertIsInstance(exercises, list)
        self.assertTrue(len(exercises) > 0)

        # Check first single-choice exercise
        single_choice = exercises[0]
        self.assertEqual(single_choice['Type'], 'single-choice')
        self.assertIn('Welches Verb ist richtig konjugiert im Konjunktiv I?', single_choice['Question'])
        self.assertIn('a) Er spiele', single_choice['Answer Options'])
        self.assertEqual(single_choice['Solution'], ['a) Er spiele'])

        # Check second single-choice exercise
        single_choice = exercises[1]
        self.assertIn('Welches ist die Konjunktiv I Form von "haben"?', single_choice['Question'])

    def test_parse_gaps_filling_exercises(self):
        parser = ExercisesParser()
        input_text = """[Grammar][Konjuktiv I][None][3][2][1][
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
Dein Deutschlehrer]

[START]
Type: [single-choice]
Question: [Welches Verb ist richtig konjugiert im Konjunktiv I?]
Answer options: [a) Er spiele b) Er spielt c) Er ging]
Solution: [a) Er spiele]
[END]
[START]
Type: [single-choice]
Question: [Welches ist die Konjunktiv I Form von "haben"?]
Answer options: [a) hätte b) haben c) hattest]
Solution: [a) hätte]
[END]
[START]
Type: [single-choice]
Question: [Welche Form im Konjunktiv I ist korrekt?]
Answer options: [a) Sie wäre b) Sie war c) Sie sei]
Solution: [c) Sie sei]
[END]
[START]
Type: [gaps]
Question: [Füllen Sie die Lücken mit der richtigen Konjunktiv I Form]
Answer options: [1. Wenn ich ein [großes, großer, großen] Haus hätte, [könnte, können, könntest] ich viele Partys veranstalten. 2. Wenn ich einen [intelligent, intelligente, intelligenten] Hund hätte, [bräuchte, brauchen, bräuchten] ich keinen Trainer.]
Solution: [großes, hätte, intelligenten, bräuchte]
[END]
[START]
Type: [gaps]
Question: [Füllen Sie die Lücken mit der richtigen Konjunktiv I Form]
Answer options: [1. Wenn sie eine [neue, neuer, neu] Wohnung fände, [würde ziehen, ziehen würde, zöge] sie sofort um. 2. Wenn wir einen [freundlichen, freundlich, freundliche] Nachbarn hätten, [wäre, sein, wären] das Leben viel angenehmer.]
Solution: [neue, zöge, freundlichen, wäre]
[END]
[START]
Type: [open]
Question: [Schreibe einen Satz im Konjunktiv I.]
Answer options: None
Solution: [Er spiele Fußball, wenn er Zeit hätte.]
[END]"""
        exercises = parser.parse(input_text)
        
        # Check first gaps exercise
        gaps = exercises[3]  # Assuming this is the index where the gaps start
        self.assertEqual(gaps['Type'], 'gaps')
        self.assertIn('Füllen Sie die Lücken mit der richtigen Konjunktiv I Form', gaps['Question'])
        self.assertTrue('großes' in gaps['Solution'])
        self.assertTrue('intelligenten' in gaps['Solution'])

    def test_parse_open_question_exercises(self):
        parser = ExercisesParser()
        input_text = """[Grammar][Konjuktiv I][None][3][2][1][
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
Dein Deutschlehrer]

[START]
Type: [single-choice]
Question: [Welches Verb ist richtig konjugiert im Konjunktiv I?]
Answer options: [a) Er spiele b) Er spielt c) Er ging]
Solution: [a) Er spiele]
[END]
[START]
Type: [single-choice]
Question: [Welches ist die Konjunktiv I Form von "haben"?]
Answer options: [a) hätte b) haben c) hattest]
Solution: [a) hätte]
[END]
[START]
Type: [single-choice]
Question: [Welche Form im Konjunktiv I ist korrekt?]
Answer options: [a) Sie wäre b) Sie war c) Sie sei]
Solution: [c) Sie sei]
[END]
[START]
Type: [gaps]
Question: [Füllen Sie die Lücken mit der richtigen Konjunktiv I Form]
Answer options: [1. Wenn ich ein [großes, großer, großen] Haus hätte, [könnte, können, könntest] ich viele Partys veranstalten. 2. Wenn ich einen [intelligent, intelligente, intelligenten] Hund hätte, [bräuchte, brauchen, bräuchten] ich keinen Trainer.]
Solution: [großes, hätte, intelligenten, bräuchte]
[END]
[START]
Type: [gaps]
Question: [Füllen Sie die Lücken mit der richtigen Konjunktiv I Form]
Answer options: [1. Wenn sie eine [neue, neuer, neu] Wohnung fände, [würde ziehen, ziehen würde, zöge] sie sofort um. 2. Wenn wir einen [freundlichen, freundlich, freundliche] Nachbarn hätten, [wäre, sein, wären] das Leben viel angenehmer.]
Solution: [neue, zöge, freundlichen, wäre]
[END]
[START]
Type: [open]
Question: [Schreibe einen Satz im Konjunktiv I.]
Answer options: None
Solution: [Er spiele Fußball, wenn er Zeit hätte.]
[END]"""
        exercises = parser.parse(input_text)
        
        # Check open question
        open_question = exercises[5]  # Assuming this is the index for the open question
        self.assertEqual(open_question['Type'], 'open')
        self.assertIn('Schreibe einen Satz im Konjunktiv I.', open_question['Question'])
        self.assertEqual(open_question['Solution'], ['Er spiele Fußball, wenn er Zeit hätte.'])
