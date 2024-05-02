
from haystack.components.retrievers.in_memory import InMemoryBM25Retriever, InMemoryEmbeddingRetriever
from haystack.components.embedders import OpenAITextEmbedder
from document_handler import DocumentStoreHandler
from haystack.components.joiners import DocumentJoiner
from haystack.components.rankers import TransformersSimilarityRanker
from haystack_integrations.components.generators.llama_cpp import LlamaCppGenerator
from haystack import Pipeline
from haystack.components.builders.answer_builder import AnswerBuilder
from haystack.components.builders import PromptBuilder
from dotenv import load_dotenv
load_dotenv()

class RAG:
    def __init__(self, model_path="backend/rag/models/llama-2-13b.Q4_K_M.gguf") -> None:
        self.doc_store_handler = DocumentStoreHandler('backend/rag/data')
        self.doc_store_handler.write_docs2docstore()

        self.document_store = self.doc_store_handler.document_store
        self.text_embedder = OpenAITextEmbedder(model="text-embedding-3-large")
        self.build_hybrid_retrieval()
        # Load the LLM using LlamaCppGenerator
        self.generator = LlamaCppGenerator(model=model_path, n_ctx=4096, n_batch=128)
        self.build_rag()
        print('RAG initialised')

    def build_rag(self):
        self.rag_pipeline = self.retrieval
        self.build_prompt()

        self.rag_pipeline.add_component(instance=self.prompt_builder, name="prompt_builder")
        self.rag_pipeline.add_component(instance=self.generator, name="llm")
        self.rag_pipeline.add_component(instance=AnswerBuilder(), name="answer_builder")
        
        self.rag_pipeline.connect("embedding_retriever", "prompt_builder.documents")
        self.rag_pipeline.connect("prompt_builder", "llm")
        self.rag_pipeline.connect("llm.replies", "answer_builder.replies")
        #self.rag_pipeline.connect("ranker.documents", "answer_builder.documents")


    def build_hybrid_retrieval(self):
        self.embedding_retriever = InMemoryEmbeddingRetriever(self.document_store)
        self.bm25_retriever = InMemoryBM25Retriever(self.document_store)
        self.document_joiner = DocumentJoiner(join_mode="concatenate")
        #self.ranker = TransformersSimilarityRanker(model="BAAI/bge-reranker-large")
        #self.ranker.warm_up()
        
        self.retrieval = Pipeline()
        self.retrieval.add_component("text_embedder", self.text_embedder)
        self.retrieval.add_component("embedding_retriever", self.embedding_retriever)
        #self.retrieval.add_component("bm25_retriever", self.bm25_retriever)
        
        #self.retrieval.add_component("document_joiner", self.document_joiner)
        #self.retrieval.add_component("ranker", self.ranker)

        self.retrieval.connect("text_embedder", "embedding_retriever.query_embedding")
        #self.retrieval.connect("bm25_retriever", "document_joiner")
        #self.retrieval.connect("embedding_retriever", "document_joiner")
        #self.retrieval.connect("document_joiner", "ranker")

    def visualize_retrieval(self): 
        self.retrieval.draw("retrieval.png")

    def run_retrieval(self, query:str):
        result = self.retrieval.run(
            {"text_embedder": {"text": query}, 
             "bm25_retriever": {"query": query}, 
             "ranker": {"query": query}}
             )
        return result["ranker"]
    
    def run(self, query:str): 
        result = self.rag_pipeline.run(
            {
                "text_embedder": {"text": query},
                #"bm25_retriever": {"query": query}, 
                #"ranker": {"query": query},
                "prompt_builder": {"question": query},
                "llm": {"generation_kwargs": {"max_tokens": 128, "temperature": 0.1}},
                "answer_builder": {"query": query},
            }
        )
        return result["answer_builder"]["answers"]
    
    def build_prompt(self):
        template = """
Du bist ein Deutschlehrer. Antworte auf die Fragen von deinen Schülern. 
Wenn die Frage kein Bezug zur deutschen Sprache hat, schreib: 'Ich kann keine Antwort geben'.
Benutze Information unten, um die Frage, wenn die Frage über Deutsch ist, zu beantworten. 
{% for document in documents %}
    {{ document.content }}
{% endfor %}

Question: {{question}}
Answer:
"""
        self.prompt_builder = PromptBuilder(template=template)
    

    

