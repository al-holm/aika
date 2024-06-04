from agent_service.tools.tool import Tool
from agent_service.prompts.prompt_builder import PromptBuilder
from agent_service.prompts.task_generation_prompt import RETRIEVER_TEMPLATE
import os
from typing import List, Dict, Tuple
import logging
from pymilvus import MilvusClient
from pymilvus.model import hybrid
from agent_service.prompts.task_generation_prompt import RETRIEVER_TEMPLATE
class RetrievalTool(Tool):
    PROMPT_ID = "retrieve"
    TEMPLATE = RETRIEVER_TEMPLATE
    
    COLLECTION_NAME = "LawAndLifeLibrary"
    ROOT_PATH = "agent_service/tools/"
    DB_PATH = ROOT_PATH + "res/rag_db/"
    DOC_PATH = ROOT_PATH + "res/data/"

    def __init__(self, init=False, llm='bedrock') -> None:
        self.name = "Suche in Fachbücher"
        self.description = "Hilfe mit Infos"
        self.set_llm(llm)
        self.llm.set_max_tokens(450)
        self.prompt = PromptBuilder()
        self.prompt.create_prompts(
            {self.PROMPT_ID : self.TEMPLATE}
        )

        self.min_chunk_len = 200
        markdown_text_list = self.read_markdown_folder(self.DOC_PATH)
        self.list_src, self.list_docs = self.parse_info(markdown_text_list)
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
        src = blocks[1]
        chunks = []
        chunk_buff = ''
        for block in blocks[2:]:
            if len(block) < self.min_chunk_len and chunk_buff == "":
                chunk_buff = block
            else:
                if chunk_buff != "":
                    new_chunk = chunk_buff + block
                    chunk_buff = ""
                else:
                    new_chunk = block
                new_chunk.replace('\n', ' ')
                chunks.append(new_chunk)
        

        return ([src for chunk in chunks], chunks) 


        
    
    def start_vector_store(self, init):
        """
        Initialize the vector store client and create a new collection.
        """
        self.client = MilvusClient(self.DB_PATH + "milvus_rag.db")
        if init:
            self.collection = self.client.create_collection(collection_name=self.COLLECTION_NAME, dimension=1024)

    def add_docs(self):
        """
        Prepare document embeddings and add them to the vector store collection.
        """
        logging.info(len(self.list_docs))
        doc_embeddings  = self.ef.encode_documents(self.list_docs)['dense']
        logging.info('embeddings ready')

        data = [ {"id": i, "vector": doc_embeddings[i], "text": self.list_docs[i], "source": self.list_src[i]} for i in range(len(self.list_docs)) ]

        self.client.insert(
            collection_name=self.COLLECTION_NAME,
            data=data
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
        query_vectors = self.ef.encode_queries([input])['dense']

        results = self.client.search(
            collection_name=self.COLLECTION_NAME, # target collection
            data=query_vectors,                # query vectors
            limit=2,                           # number of returned entities
            output_fields=["text", "source"], # specifies fields to be returned
        )
        parsed_result = self.parse_retrieval_results(results[0])
        self.query = self.prompt.generate_prompt(name_id=self.PROMPT_ID, 
                                                     text=input,
                                                     results=parsed_result)
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
        res = ''
        for i in results:
            node = i['entity']
            res += node['text'] + '\nSource: ' + node['source'] + '\n\n'
        return res


