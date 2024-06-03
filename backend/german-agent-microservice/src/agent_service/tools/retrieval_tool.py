from agent_service.tools.tool import Tool
from agent_service.prompts.prompt_builder import PromptBuilder
import os
import pandas as pd
import chromadb 
import chromadb.utils.embedding_functions as embedding_functions
import uuid
from typing import List, Dict, Tuple
import logging

class RetrievalTool(Tool):
    PROMPT_ID = "Infos abrufen"
    #TEMPLATE = RETRIEVE_TEMPLATE
    
    COLLECTION_NAME = "LawAndLifeLibrary"
    ROOT_PATH = "agent_service/prompts/"
    DOC_PATH = ROOT_PATH + "res/law_life_data/"
    CHROMA_PATH = ROOT_PATH + "res/law_life_chromadb/"

    def __init__(self, init=False) -> None:
        self.name = "Infos abrufen"
        self.description = "Hilfe mit Infos"
        self.min_chunk_len = 200
        markdown_text_list = self.read_markdown_folder(self.DOC_PATH)
        self.list_src, self.list_docs = self.parse_info(markdown_text_list)
        self.ef = embedding_functions.HuggingFaceEmbeddingFunction(
            api_key=os.environ["HF_API_TOKEN"],
            model_name="BAAI/bge-m3"
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

    def parse_info(self, markdown_text_list):
        """
        Parse a list of markdown texts into a DataFrame containing document information.

        Parameters
        ----------
        markdown_text_list : List[str]
            A list of markdown formatted strings to be parsed.

        Returns
        -------
        (list_src, list_docs)
        """
        list_docs = []
        list_src = []
        for text in markdown_text_list:
            src_list, chunks = self.get_src_chunks(text)
            list_docs.extend(chunks)
            list_src.extend(src_list)

        return (list_src, list_docs)
    
    def get_src_chunks(self, text: str):
        """
        """
        blocks = text.split("\n# ")
        src = blocks[0]
        chunks = []
        chunk_buff = ''
        for block in blocks[1:]:
            if len(block) < self.min_chunk_len and chunk_buff == "":
                chunk_buff = block
            else:
                if chunk_buff != "":
                    new_chunk = chunk_buff + block
                    chunk_buff = ""
                else:
                    new_chunk = block
                chunks.append(new_chunk)
        

        return ([src for chunk in chunks], chunks) 


        
    
    def start_vector_store(self, init):
        """
        Initialize the vector store client and create a new collection.
        """
        self.client = chromadb.PersistentClient(path=self.CHROMA_PATH)
        if init:
            try:
                self.client.delete_collection(name=self.COLLECTION_NAME)
            except Exception:
                logging.warning("No collection found")
            logging.info("Reinitializing a vector store")
            self.collection = self.client.create_collection(name=self.COLLECTION_NAME, embedding_function=self.ef)
        else:
            self.collection = self.client.get_collection(name=self.COLLECTION_NAME, embedding_function=self.ef)

    def add_docs(self):
        """
        Prepare document embeddings and add them to the vector store collection.
        """
        doc_embeddings = self.ef(self.list_docs)
        dict_src = [{"source": src} for src in self.list_src]

        ids = [str(uuid.uuid4()) for i in range(len(self.list_docs))]
        self.collection.add(
            documents=self.list_docs,
            embeddings=doc_embeddings,
            metadatas= dict_src,
            ids=ids
        )
        logging.info("Vector store reinitialized")

    
    def run(self, input: str)->str:
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
        patience = 3
        i=0
        while i<patience:
            try:
                results = self.collection.query(
                    query_texts=[input], 
                    n_results=3 
                )
            except Exception as e :
                logging.warning(e)
            i+=1
        #plan,val = self.parse_examples(results)
        return results
    
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
        metadatas = sum(results["metadatas"], []) # flatten the list
        docs = sum(results['documents'], [])
        
        for doc, metadata in zip(docs, metadatas):
            plan, val = self.parse_doc(doc, metadata)
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
        
 