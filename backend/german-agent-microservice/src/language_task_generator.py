from langchain_core.prompts import PromptTemplate
from typing import Literal
class LanguageTaskGenerator:
    def __init__(self, llm, task_type=Literal['Hör', 'Lese']):
        self.llm = llm  # tlanguage model
        self.reading = False # if  invoked reading function set True
        self.create_task_template(task_type=task_type)

    def create_task_template(self, task_type: str):
        """
        Creates a task template for generating language learning tasks.
        
        Parameters:
            text (str): The initial prompt or input text.
            task_type (str): The type of task to generate ('reading' or 'listening').

        Returns:
            str: A formatted task template.
        """
        self.task_type = task_type
        if task_type == 'Lese':
            self.task_type_specific_instructions = "Du bist ein Deutschlehrer, du bekommst eine Aufgabe einen Lesetext zu generieren."
            self.tool_usage_instruction = "Diese Anleitung ist nicht relevant für Hörtexte."
            self.alternative_tool_instruction = "Wenn ein Hörtext erstellt werden soll, gebe 'Benutze den Tool Erslellung von Hörtexte' zurück. "
        elif task_type == 'Hör':
            self.task_type_specific_instructions = "Du bist ein Deutschlehrer, du bekommst eine Aufgabe einen Hörtext zu generieren."
            self.tool_usage_instruction = "Anschließend verwende das 'Audio Generation' Tool und dein Script (generierte Geschichte, alle Sätze) als Input, um das Audio zu deiner Höraufgabe zu erstellen."
            self.alternative_tool_instruction = "Wenn ein Lesetext erstellt werden soll, gebe 'Benutze den Tool Erstellung von Lesetexten' zurück."
        else:
            raise ValueError("Unsupported task type. Choose 'reading' or 'listening'.")

        template = """
[INST]
{task_instructions} Hier, was du bisher bekommen hast: {text}

Für einen {task_type}text musst du eine Geschichte erfinden. Die Texte sollten aus 6-7 Sätzen bestehen, die miteinander verbunden sind. Der Text sollte eine Geschichte sein und den spezifischen Wortschatz verwenden.
Generiere keine Fragen zum Text.

Beispiele:
Question: Generiere einen Text zum Thema 'Essen'.
Answer:
"Script:
Anna geht jeden Freitag zum Markt, um frische Zutaten zu kaufen. Heute macht sie eine Gemüsesuppe. Sie wäscht Karotten, Kartoffeln und Brokkoli und schneidet alles klein. Das Gemüse kommt mit Wasser und Salz in einen Topf.
Während die Suppe kocht, backt Anna Brot. Zum Abendessen genießen alle die heiße Suppe und das frische Brot."

Question: Erstelle einen {task_type}text zum Thema 'Sich Vorstellen'
Answer:
"Script: 
Hallo, ich heiße Emma und ich komme aus Berlin. Ich bin 28 Jahre alt und arbeite als Grafikdesignerin. In meiner Freizeit male ich gerne und gehe oft wandern. 
Ich liebe es, neue Kulturen zu entdecken und reise deshalb so oft es geht. Nächstes Jahr plane ich, Japan zu besuchen, um mehr über seine Kunst und Geschichte zu lernen.
"

{tool_usage_instruction}
{alternative_tool_instruction}
Wenn es um etwas anderes geht, gebe 'Benutze ein anderes Tool' zurück.
[/INST]
        """

        prompt = PromptTemplate.from_template(template)

        self.chain = prompt | self.llm


    def tool_invoke_task_gen(self, text: str):
        """
        invokes a chain with specific parameters for a task generation.
        @param {str} text - a string that represents the text input for the task being invoked
        @returns response 
        """
        if self.task_type == 'Lese':
            self.reading = True
        return self.chain.invoke(
            {
                "text": text,
                'task_instructions' : self.task_type_specific_instructions, 
                'task_type' : self.task_type, 
                'tool_usage_instruction' : self.tool_usage_instruction, 
                'alternative_tool_instruction' : self.alternative_tool_instruction
            }
        )