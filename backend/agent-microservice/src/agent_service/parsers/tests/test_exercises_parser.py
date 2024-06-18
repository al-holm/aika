import unittest, xmlrunner
from agent_service.parsers.exercises_parser import ExercisesParser

class TestExercisesParser(unittest.TestCase):

    def test_parse_exercises(self):
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
Answer options: [1. Wenn ich ein (großes, großer, großen) Haus hätte, (könnte, können, könntest) ich viele Partys veranstalten. 2. Wenn ich einen (intelligent, intelligente, intelligenten) Hund hätte, (bräuchte, brauchen, bräuchten) ich keinen Trainer.]
Solution: [großes, hätte, intelligenten, bräuchte]
[END]
[START]
Type: [gaps]
Question: [Füllen Sie die Lücken mit der richtigen Konjunktiv I Form]
Answer options: [1. Wenn sie eine (neue, neuer, neu) Wohnung fände, (würde ziehen, ziehen würde, zöge) sie sofort um. 2. Wenn wir einen (freundlichen, freundlich, freundliche) Nachbarn hätten, (wäre, sein, wären) das Leben viel angenehmer.]
Solution: [neue, zöge, freundlichen, wäre]
[END]
[START]
Type: [open]
Question: [Schreibe einen Satz im Konjunktiv I.]
Answer options: None
Solution: [Er spiele Fußball, wenn er Zeit hätte.]
[END]"""
        exercises = parser.parse(input_text)


if __name__ == '__main__':
    unittest.main()