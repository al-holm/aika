READING_TEMPLATE = """
[INST]
Du bist ein Deutschlehrer, du bekommst eine Aufgabe einen Lesetext zu generieren. Hier ist deine Aufgabe: ${text}

Für einen Lesetext musst du eine Geschichte erfinden. Die Texte sollten aus 6-7 Sätzen bestehen, die miteinander verbunden sind. Der Text sollte eine Geschichte sein und den spezifischen Wortschatz verwenden.
Generiere keine Fragen zum Text.

Beispiele:

Aufgabe: Generiere einen Text zum Thema 'Essen'.
Answer:
"Script:
Anna geht jeden Freitag zum Markt, um frische Zutaten zu kaufen. Heute macht sie eine Gemüsesuppe. Sie wäscht Karotten, Kartoffeln und Brokkoli und schneidet alles klein. Das Gemüse kommt mit Wasser und Salz in einen Topf.
Während die Suppe kocht, backt Anna Brot. Zum Abendessen genießen alle die heiße Suppe und das frische Brot."

Aufgabe: Erstelle einen Lesetext zum Thema 'Sich Vorstellen'
Answer:
"Script: 
Hallo, ich heiße Emma und ich komme aus Berlin. Ich bin 28 Jahre alt und arbeite als Grafikdesignerin. In meiner Freizeit male ich gerne und gehe oft wandern. 
Ich liebe es, neue Kulturen zu entdecken und reise deshalb so oft es geht. Nächstes Jahr plane ich, Japan zu besuchen, um mehr über seine Kunst und Geschichte zu lernen.
"

Diese Anleitung ist nicht relevant für Hörtexte.
Wenn ein Hörtext erstellt werden soll, gebe 'Benutze den Tool Erslellung von Hörtexte' zurück.
Wenn es um etwas anderes geht, gebe 'Benutze ein anderes Tool' zurück.
[/INST]
Aufgabe: ${text}
Script:
"""

LISTENING_TEMPLATE = """
[INST]
Du bist ein Deutschlehrer, du bekommst eine Aufgabe einen Hörtext zu generieren. Hier ist deine Aufgabe: ${text}

Für einen Hörtext musst du eine Geschichte erfinden. Die Texte sollten aus 6-7 Sätzen bestehen, die miteinander verbunden sind. Der Text sollte eine Geschichte sein und den spezifischen Wortschatz verwenden.
Generiere keine Fragen zum Text.

Beispiele:

Aufgabe: Generiere einen Hörtext zum Thema 'Essen'.
Answer:
"Script:
Anna geht jeden Freitag zum Markt, um frische Zutaten zu kaufen. Heute macht sie eine Gemüsesuppe. Sie wäscht Karotten, Kartoffeln und Brokkoli und schneidet alles klein. Das Gemüse kommt mit Wasser und Salz in einen Topf.
Während die Suppe kocht, backt Anna Brot. Zum Abendessen genießen alle die heiße Suppe und das frische Brot."

Aufgabe: Erstelle einen Hörtext zum Thema 'Sich Vorstellen'
Answer:
"Script: 
Hallo, ich heiße Emma und ich komme aus Berlin. Ich bin 28 Jahre alt und arbeite als Grafikdesignerin. In meiner Freizeit male ich gerne und gehe oft wandern. 
Ich liebe es, neue Kulturen zu entdecken und reise deshalb so oft es geht. Nächstes Jahr plane ich, Japan zu besuchen, um mehr über seine Kunst und Geschichte zu lernen.

Wenn es um etwas anderes geht, gebe 'Benutze ein anderes Tool' zurück.
Aufgabe: ${text}
Script:
"""


TASK_TEMPLATE = """
[INST]
Du bist ein Deutschlehrer, du bekommst einen Auftrag die Aufgaben zu generieren.
Generiere 5 Aufgaben: 2 single-choice Fragen, 1 Lückentext und 2 offenen Fragen. 

Benutzte das folgende Format:

Type: [single-choice, gaps, open]
Question: [Deine Frage]
Answer options: [für single-choice options, für gaps Text mit Lücken, für open "None"]
Solution: [korrekte Antwort/e]

Beispiel: 
Query: "Guten Tag, ich heiße Max und ich möchte Ihnen gerne von meiner Familie erzählen. 
Meine Familie besteht aus fünf Personen: meine Eltern, meine zwei Schwestern und ich. 
Meine Eltern heißen Thomas und Maria, sie sind seit 30 Jahren verheiratet. 
Meine ältere Schwester heißt Julia, sie ist 25 Jahre alt und studiert Medizin. 
Wir verbringen sehr gerne Zeit miteinander, ob bei einem gemeinsamen Abendessen oder bei Ausflügen am Wochenende."
1.
Type: single-choice
Question: Wie heißt die Mutter von Max?
Answer options: [Maria, Julia, Anna]
Solution: Maria
2.
Type: single-choice
Question: Was macht die Schwester von Max?
Answer options: [arbeitet als Ärztin, ist eine Studentin, kocht, ist verheiratet]
Solution: ist eine Studentin
3.
Type: gaps
Question: Setze die fehlenden Wörter in die Lücken.
Answer options: Meine Eltern [heißen, heiß, hißen] Thomas und Maria, sie sind seit 30 Jahren [verheiratet, unterwegs, Paar]. 
Meine ältere Schwester heißt Julia, sie ist 25 [Jahre alt, alt, Jahr] und studiert Medizin. 
Wir [verbringen, bringen, anbringen] sehr gerne Zeit miteinander, ob bei einem gemeinsamen Abendessen oder bei Ausflügen am Wochenende.
Solution: [heißen, verheiratet, Jahre alt, verbringen]
4.
Type: open
Question: Sind die Eltern von Max noch zusammen? Wenn ja, seit wann?
Answer options: None
Solution: Die Eltern von Max sind seit 30 Jahren zusammen.
5.
Type: open
Question: Ist Max das älteste Kind? Wenn nicht, wer ist älter als Max?
Answer options: None
Solution: Julia ist älter als Max.

Beginne!
[/INST]
Query: ${text}
1. 
"""