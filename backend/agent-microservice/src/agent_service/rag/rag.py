from agent_service.tools.tool import Tool
from agent_service.prompts.prompt_builder import PromptBuilder
from agent_service.prompts.tool_prompt import RETRIEVER_TEMPLATE
import os
from typing import Dict, List
import logging
from milvus_db.milvus_db import MilvusDBClient
from agent_service.utils.document_handler import DocumentHandler, DocumentType
from pymilvus.model import hybrid
from tqdm import tqdm


class RAG(Tool):
    PROMPT_ID = "retrieve"
    TEMPLATE = RETRIEVER_TEMPLATE

    COLLECTION_NAME = "LawAndLifeLibrary"
    ROOT_PATH = "agent_service/rag/"
    DOC_PATH = ROOT_PATH + "res/data/"

    def __init__(
        self,
        name: str = None,
        description: str = None,
        llm: str = "bedrock",
        prompt_id: str = "retriever",
        prompt_template: str = RETRIEVER_TEMPLATE,
        max_tokens: int = 1000,
        init: bool = False,
        test: bool = False,
    ) -> None:
        super().__init__(name, description, llm, prompt_id, prompt_template, max_tokens)
        self.min_chunk_len = 200
        self.max_chunk_len = 1000
        self.document_handler = DocumentHandler(self.max_chunk_len)
        if not test:
            self.ef = hybrid.BGEM3EmbeddingFunction(
                model_name="BAAI/bge-m3", device="cpu", use_fp16=False
            )
            self.start_vector_store(init)
        if init:
            self.add_docs()


    def start_vector_store(self, init):
        """
        Initialize the vector store client and create a new collection.
        """
        self.client = MilvusDBClient()
        if init:
            self.collection = self.client.create_collection(
                collection_name=self.COLLECTION_NAME, dimension=1024
            )

    def add_docs(self):
        """
        Prepare document embeddings and add them to the vector store collection.
        """
        tmp = self.document_handler.load_docs(self.DOC_PATH, DocumentType.RAG)
        doc_embeddings = self.ef.encode_documents(tmp["docs"])["dense"]
        logging.info("embeddings ready")

        data = [
            {
                "id": i,
                "vector": doc_embeddings[i],
                "text": tmp["docs"][i],
                "source": tmp["source"][i],
            }
            for i in range(len(doc_embeddings))
        ]

        self.client.insert_data(collection_name=self.COLLECTION_NAME, data=data)
        logging.info("Vector store reinitialized")

    def run(self, input: str) -> str:
        """
        Query the trajectory library and parse examples from the results.

        Parameters
        ----------
        query : str
            The query text to search in the collection.
        top_k : int, optional
            The number of top results to return (default is 5).

        Returns
        -------
        Tuple[str, str]
            A tuple containing containing the parsed examples for planning and validation.
        """
        query_vectors = self.ef.encode_queries([input])["dense"]

        results = self.client.search(
            collection_name=self.COLLECTION_NAME,
            data=query_vectors,
            limit=3,
            output_fields=["text", "source"],
        )
        parsed_result = self.parse_retrieval_results(results[0])
        self.query = self.prompt.generate_prompt(
            name_id=self.prompt_id, text=input, results=parsed_result
        )
        answer = self.llm.run(self.query)
        return answer

    def parse_retrieval_results(self, results: Dict) -> str:
        """
        Parse examples from the query results.

        Parameters
        ----------
        results : dict
            The dictionary containing the query results with keys 'metadatas' and 'documents'.

        Returns
        -------
        Tuple[str, str]
            A tuple containing the concatenated examples for planning and validation.
        """
        res = ""
        for i in results:
            node = i["entity"]
            res += node["text"] + "\nSource: " + node["source"] + "\n\n"
        return res
