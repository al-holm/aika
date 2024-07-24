import os
import pandas as pd
from milvus_db.milvus_db import MilvusDBClient
from pymilvus.model import hybrid
from typing import Dict, Tuple
from agent_service.utils.document_handler import DocumentHandler, DocumentType
import logging


class TrajectoryRetriever:
    """
    A class used to manage the retrieval of trajectory examples into the agent's prompt.

    Methods
    -------
    inject_trajectories(self, query: str, top_k: int = 3) -> Tuple[str,str]
        Queries the trajectory library and parses examples from the results.
    """

    COLLECTION_NAME = "trajectoryLibrary"
    ROOT_PATH = "agent_service/agent/"
    DOC_PATH = ROOT_PATH + "res/trajectories_data/"

    def __init__(self, init=False) -> None:
        self.document_handler = DocumentHandler()
        self.ef = hybrid.BGEM3EmbeddingFunction(
            model_name="BAAI/bge-m3",  # Specify the model name
            device="cpu",  # Specify the device to use, e.g., 'cpu' or 'cuda:0'
            use_fp16=False,  # Specify whether to use fp16. Set to `False` if `device` is `cpu`.
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

        tmp = self.document_handler.load_docs(self.DOC_PATH, DocumentType.TRAJECTORY)

        doc_embeddings = self.ef.encode_documents(tmp["docs"])["dense"]
        data = [
            {
                "id": i,
                "vector": doc_embeddings[i],
                "text": tmp["docs"][i],
                "cat_act": tmp["cat_act"][i],
                "cat_val": tmp["cat_val"][i],
            }
            for i in range(len(doc_embeddings))
        ]

        self.client.insert_data(collection_name=self.COLLECTION_NAME, data=data)
        logging.info("Vector store reinitialized")

    def inject_trajectories(self, query: str, top_k=5) -> Tuple[str, str]:
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
        query_vectors = self.ef.encode_queries([query])["dense"]

        results = self.client.search(
            collection_name=self.COLLECTION_NAME,  # target collection
            data=query_vectors,  # query vectors
            limit=top_k,  # number of returned entities
            output_fields=[
                "text",
                "cat_act",
                "cat_val",
            ],  # specifies fields to be returned
        )
        plan, val = self.parse_examples(results[0])
        return plan, val

    def parse_examples(self, results: Dict) -> Tuple[str, str]:
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
        examples_plan, examples_val = [], []
        for i in results:
            node = i["entity"]
            metadata = {
                "cat_act": node["cat_act"],
                "cat_val": node["cat_val"],
            }
            plan, val = self.parse_doc(node["text"], metadata)
            examples_plan.append(plan)
            examples_val.append(val)

        concatenated_plan = "\n\n".join(examples_plan)
        concatenated_val = "\n\n".join(examples_val)

        return concatenated_plan, concatenated_val

    def parse_doc(self, doc: str, metadata: Dict) -> Tuple[str, str]:
        """
        Parse a single document and its metadata into plan and value examples.

        Parameters
        ----------
        doc : str
            The document text to parse.
        metadata : dict
            The metadata associated with the document.

        Returns
        -------
        Tuple[str, str]
            The parsed plan and value examples.
        """
        plan_text, comment = doc.split("\nMy Thought: ")

        if metadata["cat_act"] == "good_a":
            plan = "Hier ist ein gutes Beispiel:\n"
        else:
            plan = "Hier ist ein schlechtes Beispiel:\nWieso? "
            plan += comment.split("nicht vorhanden. ")[1] + "\n"
        plan += plan_text.split("Observation: ")[0]

        if metadata["cat_val"] == "good_v":
            val = "Hier ist ein gutes Beispiel:\n"
        else:
            val = "Hier ist ein schlechtes Beispiel:\n"
        val += doc

        return plan, val
