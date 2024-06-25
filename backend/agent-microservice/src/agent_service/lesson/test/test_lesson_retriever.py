import unittest
from agent_service.lesson.lesson_generation_retriever import LessonRetriever

class TestLessonRetriever(unittest.TestCase):

    def setUp(self):
        self.lesson_retriever = LessonRetriever()
        self.expected_result = ""

    def setUp_get_explanation_existing_topic(self):
        self.expected_result = """Das Perfekt wird verwendet, um über abgeschlossene Handlungen in der Vergangenheit zu sprechen. Es besteht aus zwei Teilen: einem Hilfsverb (haben oder sein) und dem Partizip II des Hauptverbs.

Hilfsverb:
Die meisten Verben verwenden "haben" als Hilfsverb. 
Verben der Bewegung oder Zustandsänderung verwenden "sein". Benutze sein mit folgenden Verben: gehen, kommen, fahren, laufen, fliegen, springen, schwimmen, reisen.

Partizip II:
Für regelmäßige Verben: ge + Verbstamm + t (z.B. machen → gemacht). Für unregelmäßige Verben: oft unregelmäßige Formen (z.B. essen → gegessen).

Beispiele:

Mit "haben":
Ich habe ein Buch gelesen. (Hilfsverb: habe, Partizip II: gelesen)
Du hast den Tisch gedeckt. (Hilfsverb: hast, Partizip II: gedeckt)

Mit "sein":
Er ist nach Hause gegangen. (Hilfsverb: ist, Partizip II: gegangen)
Wir sind früh aufgestanden. (Hilfsverb: sind, Partizip II: aufgestanden)

Regelmäßige Verben:
Ich habe gemacht (machen)
Sie hat gelernt (lernen)
Wir haben gespielt (spielen)

Unregelmäßige Verben:
Ich habe gegessen (essen)
Er hat gefunden (finden)
Wir sind gekommen (kommen)"""

    def setUp_get_explanation_last_topic(self):
        self.expected_result = """Der Konjunktiv II wird auch als Möglichkeitsform bezeichnet und beschreibt Vermutungen und irreale Dinge. Man verwendet ihn hauptsächlich, wenn man sich etwas vorstellt oder wünscht, was zurzeit nicht möglich ist. Außerdem wird er bei höflichen Fragen oder Aussagen, Vorschlägen und Ratschlägen benutzt.
Bildung des Konjunktiv II
Für regelmäßige Verben: würde + Infinitiv
Beispiele: 
machen → Ich würde machen, wünschen → Du würdest wünschen, gehen → Er würde gehen, 
lernen → Wir würden lernen, singen → Ihr würdet singen, sagen → Sie würden sagen.

Für unregelmäßige Verben: Präteritumstamm des Verbs + Konjunktiv-Endungen (-e, -est, -e, -en, -et, -en)
Beispiele: 
haben → Ich hätte, Du hättest, Er hätte, Wir hätten, Ihr hättet, Sie hätten.
sein → Ich wäre, Du wärst, Er wäre, Wir wären, Ihr wärt, Sie wären.

Weitere Beispiele:

Als höfliche Bitte:
Würdest du bitte das Fenster schließen? Mir ist kalt.
Ich hätte gern noch ein Bier.
Hätten Sie vielleicht einen Moment Zeit für mich?

Als Wunsch/Traum:
Ich wünschte, ich wäre am Strand.
Es wäre schön, wenn wir mehr Zeit zusammen hätten.
Ich hätte gern ein großes Haus.
Ich wünschte, ich hätte mehr Geld.

Für Vorschläge und Ratschläge:
Wir könnten heute Abend ins Kino gehen.
Würdest du mit mir spazieren gehen?
Es wäre gut, wenn du früher schlafen gehst.
Es wäre besser, wenn wir jetzt gehen.
Du solltest für deine Prüfung morgen lernen.
Es wäre gut, wenn du einen Regenschirm hättest."""

    def setUp_get_examples_existing_topic_correct_type(self):
        self.expected_result = """[START]
Type: [single-choice]
Question: [Welches Verb ist richtig konjugiert im Perfekt?]
Answer Options: [a) Er hat gesungen b) Er singen c) Er sang]
Solution Explanation: [Im Perfekt verwendet man das Hilfsverb "haben" oder "sein" und das Partizip II des Verbs. "Er singen" ist falsch, weil es kein Hilfsverb enthält. "Er sang" ist Präteritum, nicht Perfekt. "Er hat gesungen" ist korrekt, weil es das Hilfsverb "hat" und das Partizip II "gesungen" verwendet.]
Solution: [a) Er hat gesungen]
[END]
[START]
Type: [single-choice]
Question: [Welches ist die korrekte Form im Perfekt?]
Answer Options: [a) Sie haben gegessen b) Sie aßen c) Sie isst]
Solution Explanation: [Im Perfekt verwendet man das Hilfsverb "haben" oder "sein" und das Partizip II des Verbs. "Sie haben gegessen" ist korrekt.]
Solution: [a) Sie haben gegessen]
[END]
[START]
Type: [single-choice]
Question: [Welches Satz ist korrekt im Perfekt?]
Answer Options: [a) Ich bin gelaufen b) Ich läuft c) Ich lief]
Solution Explanation: [Im Perfekt verwendet man das Hilfsverb "haben" oder "sein" und das Partizip II des Verbs. "Ich läuft" ist Präsens, nicht Perfekt. "Ich lief" ist Präteritum, nicht Perfekt. "Ich bin gelaufen" ist korrekt, weil "laufen" ein Bewegungsverb ist und daher mit "sein" im Perfekt konjugiert wird.]
Solution: [a) Ich bin gelaufen]
[END]
[START]
Type: [single-choice]
Question: [Welches ist die richtige Perfektform?]
Answer Options: [a) Wir sind gefahren b) Wir fahrt c) Wir fuhr]
Solution Explanation: [Im Perfekt verwendet man das Hilfsverb "haben" oder "sein" und das Partizip II des Verbs. "Wir fahrt" ist Präsens, nicht Perfekt. "Wir fuhr" ist Präteritum, nicht Perfekt. "Wir sind gefahren" ist korrekt, weil "fahren" ein Bewegungsverb ist und daher mit "sein" im Perfekt konjugiert wird.]
Solution: [a) Wir sind gefahren]
[END]
"""

    def test_get_explanation_existing_topic(self):
        self.setUp_get_explanation_existing_topic()
        topic = "Perfekt"
        result = self.lesson_retriever.get_grammar_explanation(topic)
        self.assertEqual(result, self.expected_result)
    
    def test_get_explanation_last_topic(self):
        self.setUp_get_explanation_last_topic()
        topic = "Konkunktiv II"
        result = self.lesson_retriever.get_grammar_explanation(topic)
        self.assertEqual(result, self.expected_result)

    def test_get_examples_existing_topic_correct_type(self):
        self.setUp_get_examples_existing_topic_correct_type()
        topic = "Perfekt"
        type = "single-choice"
        result = self.lesson_retriever.get_examples(topic, type)
        self.assertEqual(result, self.expected_result)
