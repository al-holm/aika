import os
import pandas as pd
from pymilvus import MilvusClient
from pymilvus.model import hybrid
import uuid
from typing import List, Dict, Tuple
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
    ROOT_PATH = "agent_service/prompts/"
    DOC_PATH = ROOT_PATH + "res/trajectories_data/"
    DB_PATH = ROOT_PATH + "res/db/"
    def __init__(self, init=False) -> None:
        markdown_text_list = self.read_markdown_folder(self.DOC_PATH)
        self.df_docs = self.parse_trajectories(markdown_text_list)
        self.ef = hybrid.BGEM3EmbeddingFunction(
            model_name='BAAI/bge-m3', # Specify the model name
            device='cpu', # Specify the device to use, e.g., 'cpu' or 'cuda:0'
            use_fp16=False # Specify whether to use fp16. Set to `False` if `device` is `cpu`.
        )
        self.start_vector_store(init)
        if init:
            self.add_docs()
    
    def read_markdown_folder(self, folder_path):
        """
        Reads all markdown files in a folder and saves the text in a list.

        Parameters
        ----------
            folder_path: The path to the folder containing the markdown files.

        Returns
        -------
            A list of strings, where each string is the text content of a markdown file.
        """
        markdown_text_list = []
        for filename in os.listdir(folder_path):
            if filename.endswith(".md"):
                file_path = os.path.join(folder_path, filename)
                with open(file_path, 'r', encoding="utf-8") as f:
                    markdown_text_list.append(f.read())
        return markdown_text_list

    def parse_trajectories(self, markdown_text_list):
        """
        Parse a list of markdown texts into a DataFrame containing document information.

        Parameters
        ----------
        markdown_text_list : List[str]
            A list of markdown formatted strings to be parsed.

        Returns
        -------
        pd.DataFrame
            A DataFrame containing the parsed document information with columns 
            'cat_act', 'cat_val', 'context', and 'doc'.
        """
        list_docs = []
        for text in markdown_text_list:
            chunks = text.split("---")[1:]
            for chunk in chunks:
                text = chunk.split("Category: ")[1].split("\n")
                dict_doc = {}
                dict_doc["cat_act"], dict_doc["cat_val"], dict_doc["context"] = text[0].split(", ")
                dict_doc["doc"] = "\n".join(text[1:]).strip()
                list_docs.append(dict_doc)  
        df_docs = pd.DataFrame(list_docs)
        return df_docs
    
    def start_vector_store(self, init):
        """
        Initialize the vector store client and create a new collection.
        """
        self.client = MilvusClient(self.DB_PATH + "milvus_memory.db")
        if init:
            self.collection = self.client.create_collection(collection_name=self.COLLECTION_NAME, dimension=1024)

    def add_docs(self):
        """
        Prepare document embeddings and add them to the vector store collection.
        """
        doc_list = list(self.df_docs["doc"])
        list_act = list(self.df_docs['cat_act'])
        list_val= list(self.df_docs['cat_val'])
        doc_embeddings  = self.ef.encode_documents(doc_list)['dense']
        data = [ {"id": i, "vector": doc_embeddings[i], "text": doc_list[i], "cat_act": list_act[i], "cat_val": list_val[i]} for i in range(len(doc_list))]

        self.client.insert(
            collection_name=self.COLLECTION_NAME,
            data=data
        )
        logging.info("Vector store reinitialized")
    
    def inject_trajectories(self, query:str, top_k=5)->Tuple[str, str]:
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
        query_vectors = self.ef.encode_queries([query])['dense']

        results = self.client.search(
            collection_name=self.COLLECTION_NAME, # target collection
            data=query_vectors,                # query vectors
            limit=top_k,                           # number of returned entities
            output_fields=["text", "cat_act", 'cat_val'], # specifies fields to be returned
        )
        plan,val = self.parse_examples(results[0])
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
            node = i['entity']
            metadata = {
                'cat_act': node['cat_act'],
                'cat_val': node['cat_val'],
                }
            plan, val = self.parse_doc(node['text'], metadata)
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
        
        if metadata['cat_act'] == 'good_a':
            plan = "Hier ist ein gutes Beispiel:\n"
        else:
            plan = "Hier ist ein schlechtes Beispiel:\nWieso? "
            plan += comment.split("nicht vorhanden. ")[1] + "\n"
        plan += plan_text.split("Observation: ")[0]
        
        if metadata['cat_val'] == 'good_v':
            val = "Hier ist ein gutes Beispiel:\n"
        else:
            val = "Hier ist ein schlechtes Beispiel:\n"
        val += doc
        
        return plan, val



