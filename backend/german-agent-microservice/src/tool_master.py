import os, uuid
from pathlib import Path
import deepl
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain.tools import StructuredTool
from langchain.tools.retriever import create_retriever_tool
from document_handler import DocumentStoreHandler
from langchain_community.tools import ElevenLabsText2SpeechTool
from langchain_community.llms.bedrock import Bedrock
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from language_task_generator import LanguageTaskGenerator
from time import sleep
load_dotenv()

# The `ToolMaster` class sets up various tools for tasks such as searching, translation, text
# generation, and more, with methods for translating text, explaining grammar, and generating audio.
class ToolMaster:
    DOCS_PATH = Path('backend/german-agent-microservice/res/data')
    def __init__(self, bedrock):
        self.web_search = GoogleSerperAPIWrapper(gl='de', hl='de')
        self.translator = deepl.Translator(os.environ["DEEPL_AUTH_KEY"])
        self.audio_gen = ElevenLabsText2SpeechTool()
        self.llm = Bedrock(model_id="mistral.mixtral-8x7b-instruct-v0:1", 
                    client=bedrock, model_kwargs={"max_tokens": 512})
        self.reading_task_gen = LanguageTaskGenerator(self.llm, task_type='Lese')
        self.listenin_task_gen = LanguageTaskGenerator(self.llm, task_type='Hör')
        self.tools = []
        self.tool_names = []
        self.audio_created = False

        #self.configure_retrieval()
        self.configure_tools()

    def configure_tools(self):
        """
        sets up various tools for tasks such as searching, translation, text generation, and more by creating structured tools from specified functions.
        """
        tools_info = [
            (self.reading_task_gen.tool_invoke_task_gen, "Erstellung von Lesetexten", "Benutzte als Erste zur Erstellung von Lesetexten (keine Hörtexte)."),
            (self.listenin_task_gen.tool_invoke_task_gen, "Erstellung von Hörtexten", "Benutze als Erste zur Erstellung von Hörtexten."),
            (self.tool_explain_grammar, "Anleitung Erstellung von Erklärungen zu Grammatik", "Die Anleitung ist hilfreich, wenn man Grammatikthemen einfach und mit Beispielen erklären möchte."),
            (self.web_search.run, "Web-Suche", "Hilfreich, wenn man Informationen im Internet nachschauen möchte"),
            (self.tool_translate, "Übersetzer", "Hilfreich, wenn man Text übersetzen möchte"),
            (self.tool_generate_audio, "Audio Generation", "Hilfreich, wenn man das Audio für einen Hörtext erstellen möchte. Gebe deinen generierten Hörtext als Action Input. (Benutze NICHT für Lesetexte)"),
        ]

        for func, name, description in tools_info:
            tool = StructuredTool.from_function(
                func=func,
                name=name,
                description=description
            )
            self.tools.append(tool)
            self.tool_names.append(name)

        #self.add_retriever_tool()

    def add_retriever_tool(self):
        """
        creates a retriever tool for searching in textbooks and adds it to a list of tools.
        """
        self.tool_search = create_retriever_tool(
            retriever=self.retriever,
            name="Suche in Lehrbücher",
            description="Hilfreich, wenn man nach Erklärungen oder Beispielen sucht",
        )
        self.tools.append(self.tool_search)
        self.tool_names.append(self.tool_search.name)

        
    def tool_translate(self, text : str):
        '''The `translate_function` method translates the input text into target language.'''
        return self.translator.translate_text(text, target_lang='RU', formality='more') # use more polite language

    
    def tool_explain_grammar(self, text : str):
        instructions = """
        Für die Grammatik:
        Finde eine gute Erklärung für das Grammatikthema. Generiere keine Fragen zum Text. Versuche es so einfach wie möglich zu erklären und benutze Beispiele. 
        Benutzte das folgende Format: 
        Erklärung: [INST] Verfasse die Erklärung mit Beispiele [/INST]
        """
        return instructions
    
    def configure_retrieval(self):
        """
        sets up document retrieval by initializing document store, embedder, and retriever with specific search parameters.
        """
        self.doc_handler = DocumentStoreHandler(self.DOCS_PATH)
        self.doc_store = self.doc_handler.doc_store
        self.embedder = self.doc_handler.embedder
        self.retriever = self.doc_store.as_retriever(search_kwargs={"k": 4})

    

    def tool_generate_audio(self, story : str) :
        '''The function generates audio from a given text and saves it as a WAV file in a specified directory. '''
        if len(story) < 20: # better way to detect if the input contain a story?
            return 'Du muss das Audio neu generieren. Action Input soll deinen Text beinthalten. Benutze noch mal das "Audio Generation" Tool.'
        if self.reading:
            return 'Das ist ein Lesetext, du muss kein Audio generieren.'
        speech_file = None
        while speech_file is None:
            try:
                speech_file = self.audio_gen.run(story)
            except RuntimeError:
                sleep(15)
            
        id = str(uuid.uuid4())
        path = Path('backend/german-agent-microservice/tmp/audio/' + id + ".wav")
        os.replace(speech_file, path)
        self.audio_created = True
        return 'Audio wurde erfolgreich generiert!'
    
   
