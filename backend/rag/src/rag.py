from document_handler import DocumentStoreHandler
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import LlamaCpp
from langchain_core.runnables import RunnablePassthrough
from langchain.chains import LLMChain
from langchain_community.llms import Ollama
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever

"""
A class for Retrieval Augmented Generation that combines different retrievers and language models for question answering.
@param model_path - the path to the model
@param documents_path - the path to the documents
"""
class RetrievalAugmentedGeneration:
    def __init__(self, model_path, documents_path='backend/rag/data'):
        self.model_path = model_path
        self.doc_handler = DocumentStoreHandler(documents_path)
        self.doc_store = self.doc_handler.doc_store
        self.embedder = self.doc_handler.embedder
        self.retriever = self.doc_store.as_retriever(search_kwargs={"k": 5})
        self.build_prompt()
        self.configure_llm()
        self.configure_rag_chain()
        print('RAG Build')

    def configure_llm(self):
        '''The function `configure_llm` sets the `llm` attribute of an object to an instance of the
        `Ollama` class with a specific model parameter.
        
        '''
        self.llm = Ollama(model="mixtral:8x7b")

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
        return self.rag_chain.invoke(query)

    def build_prompt(self):
        template = """
        [INST] 
Du bist ein Deutschlehrer. Beantworte die Fragen deines Studenten. Benutze einfache Sprache. Benutze Information unten zur Hilfe.
[/INST]
{context}

Frage:
{question} 

Antwort: """

        self.prompt = PromptTemplate.from_template(template)