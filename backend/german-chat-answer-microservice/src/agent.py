from document_handler import DocumentStoreHandler
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_community.llms import Ollama
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain_community.tools.tavily_search import TavilySearchResults
import boto3
from langchain_community.llms.bedrock import Bedrock
from langchain.tools.retriever import create_retriever_tool
from langchain.tools import StructuredTool
import deepl
import os
import warnings
warnings.filterwarnings("ignore")
"""
A class for Retrieval Augmented Generation that combines different retrievers and language models for question answering.
@param model_path - the path to the model
@param documents_path - the path to the documents
"""
class LLMAgent:
    def __init__(self, model_path='', bedrock=None, documents_path='backend/german-chat-answer-microservice/res'):
        self.model_path = model_path
        self.bedrock = bedrock
        self.doc_handler = DocumentStoreHandler(documents_path)
        self.doc_store = self.doc_handler.doc_store
        self.embedder = self.doc_handler.embedder
        self.retriever = self.doc_store.as_retriever(search_kwargs={"k": 4})
        self.configure_tools()
        # Get the prompt to use - you can modify this!
        #self.prompt = hub.pull("hwchase17/react")
        self.build_prompt()
        self.configure_llm()
        #self.configure_rag_chain()
        # Construct the ReAct agent
        self.agent = create_react_agent(self.llm, self.tools, self.prompt)
        # Create an agent executor by passing in the agent and tools
        self.agent_executor = AgentExecutor(agent=self.agent, tools=self.tools, verbose=True, 
                                            handle_parsing_errors="Check you output and make sure it conforms! Do not output an action and a final answer at the same time.")
        print('Agent Build')

    def configure_tools(self):
        tool_search = create_retriever_tool(
            retriever=self.retriever,
            name="Suche in Lehrbücher",
            description="Hilfreich, wenn man nach Erklärungen oder Beispielen sucht",
        )
        self.translator = deepl.Translator(os.environ["DEEPL_AUTH_KEY"])
        self.tranlation_tool = StructuredTool.from_function(
            func=self.translate_function,
            name="Übersetzer",
            description="Hilfreich, wenn man Text übersetzen möchte",
        )
        self.tools = [TavilySearchResults(max_results=4), tool_search, self.tranlation_tool]
    
    def translate_function(self, text : str):
        return self.translator.translate_text(text, target_lang='RU', formality='more') # use more polite language

    def configure_llm(self):
        '''The function `configure_llm` sets the `llm` attribute of an object to an instance of the
        `Ollama` class with a specific model parameter.
        
        '''
        if self.bedrock==None:
            self.llm = Ollama(model="mixtral:8x7b")
        else:
            self.llm = Bedrock(model_id="mistral.mixtral-8x7b-instruct-v0:1", 
                    client=self.bedrock, model_kwargs={"max_tokens": 512})

    def configure_rag_chain(self):
        '''The function `configure_rag_chain` creates a chain of components including an LLM chain and a
        RAG chain.
        
        '''
        # Creating an LLM Chain 
        self.llm_chain = self.prompt | self.llm

        # RAG Chain
        self.rag_chain = ( 
        {"context": self.retriever, "question": RunnablePassthrough()}
            | self.llm_chain 
        )

    def run(self,  query: str):
        '''The `run` function takes a query as input and invokes the `rag_chain` method with that query.
        Parameters
        ----------
        query : str
            The `query` parameter in the `run` method is a string that represents the query to be passed to
        the `invoke` method of the `rag_chain` object.
        
        Returns
        -------
            The `run` method is returning the result of invoking the `invoke` method of the `rag_chain`
        object with the `query` parameter.
        
        '''
        return self.agent_executor.invoke({'input' : query})

    def build_prompt(self):
        template = """
        [INST] 
Du bist ein Deutschlehrer. Beantworte die Fragen deines Studenten. Benutze einfache Sprache. 
Beantworte die folgenden Fragen so gut wie du kannst. Du hast Zugang zu den folgenden Tools:
{tools}

Verwende das folgende Format:

Question: die Eingangsfrage, die Du beantworten musst
Thought: Du solltest immer darüber nachdenken, was zu tun ist
Action: die zu ergreifende Maßnahme, sollte eine von [{tool_names}] sein
Action Input: die Eingabe für die Aktion
Observation: wie schätzt du das Ergebnis der Handlung ein?
...
... (dieser Thought/Action/Action Input/Observation kann N-mal wiederholt werden)
Thought: Ich kenne jetzt die endgültige Antwort
Final Answer: die endgültige Antwort auf die ursprüngliche Eingangsfrage

Beginne! Übersetze immer kurze Erklärungen und kurze Beispiele ins Russisch!!!
Such minimal in Lehrbücher & benutzte immer Prefixe wie Thought/Action/Action Input/Observation/Final Answer.
Wenn du die endgültige Antwort gefunden hast, gib "Final Answer: [deine Antwort]." zurück. 
[/INST]
Question: {input}

Thought:{agent_scratchpad} """

        self.prompt = PromptTemplate.from_template(template)