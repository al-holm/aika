READING_TASKS_EXAMPLES_1 = """
Your input format is: 
[Single-Choice-Questions-Number][Gaps-filling-exercises-number][Text for which exercises must be provided]

Generate exactly as many exercises of each type as are specified in the input. 
If the input is zero, no exercises of that type should be generated at all


Use the following examples to generate exercises:

Example 1:
Input:
[2][2][Letzten Sommer war ich in Italien im Urlaub. Ich besuchte Rom, Florenz und Venedig. In Rom sah ich das Kolosseum und das Pantheon. In Florenz ging ich in die Uffizien und sah viele schöne Kunstwerke. In Venedig gefielen mir die Kanäle und Brücken. Jeden Tag aß ich leckeres italienisches Essen und genoss das gute Wetter. Der Urlaub war wunderbar.]
Your answer:
[START]
Type: [single-choice]
Question: [Welche Städte besuchte der Erzähler in Italien?]
Answer options: [a) Rom, Florenz und Venedig b) Mailand, Rom und Florenz c) Rom, Venedig und Neapel d) Florenz, Venedig und Mailand]
Solution: [a) Rom, Florenz und Venedig]
[END]
[START]
Type: [single-choice]
Question: [Was sah der Erzähler in Rom?]
Answer options: [a) Das Kolosseum und das Pantheon b) Die Uffizien c) Die Kanäle und Brücken d) Das schöne Wetter]
Solution: [a) Das Kolosseum und das Pantheon]
[END]
[START]
Type: [gaps]
Question: [Füllen Sie die Lücken basierend auf dem Text]
Answer options: [1. In Florenz ging ich in die (Uffizien, Museen, Kirchen). 2. In Venedig gefielen mir die (Kanäle, Straßen, Gebäude) und Brücken.]
Solution: [Uffizien, Kanäle]
[END]
[START]
Type: [gaps]
Question: [Füllen Sie die Lücken basierend auf dem Text]
Answer options: [1. Jeden Tag aß ich (leckeres, langweiliges, teures) italienisches Essen. 2. Letzten Sommer war ich in (Spanien, Frankreich, Italien) im Urlaub.]
Solution: [leckeres, Italien]
[END]

Example 2:
Input:
[3][0][Ich gehe jeden Tag zur Schule. Meine Lieblingsfächer sind Mathematik und Geschichte. In Mathematik lernen wir gerade Brüche und in Geschichte sprechen wir über das Mittelalter. Mein bester Freund heißt Paul und wir sitzen zusammen in der Klasse. Nach der Schule spielen wir oft Fußball oder gehen ins Kino. Unsere Lehrerin, Frau Müller, ist sehr nett und hilft uns immer bei den Hausaufgaben. Ich mag meine Schule sehr.]
Your answer:
[START]
Type: [single-choice]
Question: [Was sind die Lieblingsfächer des Erzählers?]
Answer options: [a) Mathematik und Geschichte b) Mathematik und Biologie c) Geschichte und Kunst d) Biologie und Kunst]
Solution: [a) Mathematik und Geschichte]
[END]
[START]
Type: [single-choice]
Question: [Was machen der Erzähler und Paul oft nach der Schule?]
Answer options: [a) Sie spielen Fußball oder gehen ins Kino b) Sie lernen zusammen c) Sie gehen schwimmen d) Sie spielen Videospiele]
Solution: [a) Sie spielen Fußball oder gehen ins Kino]
[END]
[START]
Type: [single-choice]
Question: [Wie heißt die Lehrerin des Erzählers?]
Answer options: [a) Frau Schmidt b) Frau Müller c) Frau Meier d) Frau Becker]
Solution: [b) Frau Müller]
[END]
"""

READING_TASKS_EXAMPLES_2 = """
Your input format is: 
[Open-Questions-Number][Text for which exercises must be provided]

Generate exactly as many exercises of each type as are specified in the input and only for a given text! 
If the input is zero, no exercises of that type should be generated at all


Use the following examples to generate exercises:

Example 1:
Input:
[1][Letzten Sommer war ich in Italien im Urlaub. Ich besuchte Rom, Florenz und Venedig. In Rom sah ich das Kolosseum und das Pantheon. In Florenz ging ich in die Uffizien und sah viele schöne Kunstwerke. In Venedig gefielen mir die Kanäle und Brücken. Jeden Tag aß ich leckeres italienisches Essen und genoss das gute Wetter. Der Urlaub war wunderbar.]
Your possible answer:
[START]
Type: [open]
Question: [Warum war der Urlaub des Erzählers wunderbar? Nutzen Sie Details aus dem Text.]
Answer options: None
Solution: [Der Urlaub des Erzählers war wunderbar, weil er das Kolosseum und das Pantheon in Rom sah, viele schöne Kunstwerke in den Uffizien in Florenz bewunderte und die Kanäle und Brücken in Venedig genoss. Außerdem aß er jeden Tag leckeres italienisches Essen und hatte gutes Wetter.]
[END]

Example 2:
Input:
[1][Ich gehe jeden Tag zur Schule. Meine Lieblingsfächer sind Mathematik und Geschichte. In Mathematik lernen wir gerade Brüche und in Geschichte sprechen wir über das Mittelalter. Mein bester Freund heißt Paul und wir sitzen zusammen in der Klasse. Nach der Schule spielen wir oft Fußball oder gehen ins Kino. Unsere Lehrerin, Frau Müller, ist sehr nett und hilft uns immer bei den Hausaufgaben. Ich mag meine Schule sehr.]
Your possible answer:
[START]
Type: [open]
Question: [Warum mag der Erzähler seine Schule? Nutzen Sie Details aus dem Text.]
Answer options: None
Solution: [Der Erzähler mag seine Schule, weil er seine Lieblingsfächer Mathematik und Geschichte hat, in denen er interessante Themen wie Brüche und das Mittelalter lernt. Außerdem hat er einen besten Freund namens Paul, mit dem er zusammen in der Klasse sitzt und nach der Schule oft Fußball spielt oder ins Kino geht. Auch seine Lehrerin, Frau Müller, ist sehr nett und hilft ihm bei den Hausaufgaben.]
[END]

You only generate open-ended questions for a given text! 
Once you have generated the required number of open questions, you generate nothing else!
"""

GRAMMAR_TASKS_EXAMPLES_1 = """
Your input format is: 
[Main-grammar-topic][Secondary-grammar-topic][Single-Choice-Questions-Number][Gaps-filling-exercises-number][Main-grammar-topic-explanation-text]

Generate exactly as many exercises of each type as are specified in the input. 
If the input is zero, no exercises of that type should be generated at all


Use the following examples to generate exercises:


"""

GRAMMAR_TASKS_EXAMPLES_2 = """
Your input format is: 
[Main-grammar-topic][Secondary-grammar-topic][Open-Questions-Number][Main-grammar-topic-explanation-text]

Generate exactly as many exercises of each type as are specified in the input and only for given topics. 
If the input is zero, no exercises of that type should be generated at all

Use the following examples to generate exercises:

Example 1:
Input: 
[Präteritum][None][1][Here should be a text explaining how to build Präteritum and where to use it.]
Your possible answer:
[START]
Type: [open]
Question: [Schreiben Sie über ein Erlebnis aus Ihrer Kindheit im Präteritum. Beschreiben Sie, was passiert ist, und wie Sie sich dabei gefühlt haben.]
Answer options: None
Solution: None
[END]

Example 2:
Input:
[Konjunktiv II][None][1][Here should be a text explaining how to build Konjuktiv II and where to use it.]
Your possible answer:
[START]
Type: [open]
Question: [Schreiben Sie einen Wunsch oder eine Bedingung, die Sie haben, im Konjunktiv II.]
Answer options: None
Solution: None
[END]

Example 3:
Input:
[Endungen von Adjektiven][Konjunktiv II][1][Here should be a text explaining how to build Präteritum and where to use it.]
Your possible answer:
[START]
Type: [open]
Question: [Schreibe einen kurzen Text darüber, was du tun würdest, wenn du einen perfekten Tag planen könntest. Achte dabei auf die korrekten Adjektivendungen und benutze mindestens drei Sätze im Konjunktiv II.]
Answer options: None
Solution: None
[END]

You only generate open-ended questions for given topics! 
Once you have generated the required number of open questions, you generate nothing else!
"""