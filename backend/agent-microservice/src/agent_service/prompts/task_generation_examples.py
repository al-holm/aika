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

Example 1:
Input: 
[Präteritum][None][1][1][Here should be a text explaining how to build Präteritum and where to use it.]
Your possible answer:
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

Example 2:
Input:
[Konjunktiv II][None][3][0][Here should be a text explaining how to build Konjuktiv II and where to use it.]
Your possible answer:
[START]
Type: [single-choice]
Question: [Welches Verb ist richtig konjugiert im Konjunktiv II?]
Answer options: [a) Er würde gehen b) Er ging c) Er geht]
Solution: [a) Er würde gehen]
[END]
[START]
Type: [single-choice]
Question: [Welches ist die Konjunktiv II Form von "haben"?]
Answer options: [a) hätte b) haben c) hattest]
Solution: [a) hätte]
[END]
[START]
Type: [single-choice]
Question: [Welche Form im Konjunktiv II ist korrekt?]
Answer options: [a) Sie wäre b) Sie war c) Sie ist]
Solution: [a) Sie wäre]
[END]

Example 3:
Input:
[Endungen von Adjektiven][Konjunktiv II][2][2][Here should be a text explaining how to build Präteritum and where to use it.]
Your possible answer:
[START]
Type: [single-choice]
Question: [Welche Endung hat das Adjektiv im Satz: "Wenn ich ein __ (schön) Auto hätte, würde ich durch die Stadt fahren."]
Answer options: [a) schön b) schöne c) schönen d) schöner]
Solution: [d) schöner]
[END]
[START]
Type: [single-choice]
Question: [Welcher Satz ist korrekt?]
Answer options: [a) Wenn ich ein klugem Mann wäre, hätte ich viele Freunde. b) Wenn ich eine kluge Frau wäre, hätte ich viel Erfolg. c) Wenn ich ein kluger Student wäre, würden die Prüfungen leicht sein. d) Wenn ich ein klein Hund wäre, würde ich viel bellen.]
Solution: [b) Wenn ich eine kluge Frau wäre, hätte ich viel Erfolg.]
[END]
[START]
Type: [gaps]
Question: [Füllen Sie die Lücken mit der richtigen Adjektivendung und Konjunktiv II Form]
Answer options: [1. Wenn ich ein (großes, großer, großen) Haus hätte, (könnte, können, könntest) ich viele Partys veranstalten. 2. Wenn ich einen (intelligent, intelligente, intelligenten) Hund hätte, (bräuchte, brauchen, bräuchten) ich keinen Trainer.]
Solution: [großes, könnte, intelligenten, bräuchte]
[END]
[START]
Type: [gaps]
Question: [Füllen Sie die Lücken mit der richtigen Adjektivendung und Konjunktiv II Form]
Answer options: [1. Wenn sie eine (neue, neuer, neu) Wohnung fände, (würde ziehen, ziehen würde, zöge) sie sofort um. 2. Wenn wir einen (freundlichen, freundlich, freundliche) Nachbarn hätten, (wäre, sein, wären) das Leben viel angenehmer.]
Solution: [neue, würde ziehen, freundlichen, wäre]
[END]
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
Solution: [Als ich acht Jahre alt war, besuchte ich mit meiner Familie einen Vergnügungspark. Wir gingen auf viele Fahrgeschäfte und aßen viel Eis. Es war ein sonniger Tag und ich fühlte mich sehr glücklich. Besonders erinnerte ich mich an die Achterbahn, die sehr aufregend war.]
[END]

Example 2:
Input:
[Konjunktiv II][None][1][Here should be a text explaining how to build Konjuktiv II and where to use it.]
Your possible answer:
[START]
Type: [open]
Question: [Schreiben Sie einen Wunsch oder eine Bedingung, die Sie haben, im Konjunktiv II.]
Answer options: None
Solution: [Ich wünschte, ich könnte fliegen. Wenn ich fliegen könnte, würde ich die Welt von oben sehen und überall hinreisen, ohne mir Sorgen um Verkehr oder Grenzen zu machen.]
[END]

Example 3:
Input:
[Endungen von Adjektiven][Konjunktiv II][1][Here should be a text explaining how to build Präteritum and where to use it.]
Your possible answer:
[START]
Type: [open]
Question: [Schreibe einen kurzen Text darüber, was du tun würdest, wenn du einen perfekten Tag planen könntest. Achte dabei auf die korrekten Adjektivendungen und benutze mindestens drei Sätze im Konjunktiv II.]
Answer options: None
Solution: [An einem perfekten Tag würde ich in einem gemütlichen Café sitzen und ein leckeres Frühstück genießen. Danach würde ich einen langen Spaziergang in einem wunderschönen Park machen. Am Abend würde ich in einem erstklassigen Restaurant essen gehen und den Tag mit einem interessanten Buch ausklingen lassen.]
[END]

You only generate open-ended questions for given topics! 
Once you have generated the required number of open questions, you generate nothing else!
"""