from agent_service.tools.tool import Tool
from agent_service.prompts.prompt_builder import PromptBuilder
from agent_service.prompts.tool_prompt import RETRIEVER_TEMPLATE
import os
from typing import Dict
import logging
from pymilvus import MilvusClient
from pymilvus.model import hybrid
from tqdm import tqdm
class RetrievalTool(Tool):
    PROMPT_ID = "retrieve"
    TEMPLATE = RETRIEVER_TEMPLATE
    
    COLLECTION_NAME = "LawAndLifeLibrary"
    ROOT_PATH = "agent_service/tools/"
    DB_PATH = ROOT_PATH + "res/rag_db/"
    DOC_PATH = ROOT_PATH + "res/data/"

    def __init__(self, name:str=None, description:str=None, llm:str='bedrock', 
                    prompt_id:str='retriever',
                    prompt_template:str=RETRIEVER_TEMPLATE, 
                    max_tokens:int=300, init:bool=False) -> None:
        super().__init__(name, description, llm, prompt_id, prompt_template, max_tokens)
        self.min_chunk_len = 200
        self.max_chunk_len = 600
        self.load_docs()
        self.ef = hybrid.BGEM3EmbeddingFunction(
            model_name='BAAI/bge-m3', 
            device='cpu', 
            use_fp16=False
        )
        self.start_vector_store(init)
        if init:
            self.add_docs()

    def load_docs(self):
        markdown_text_list = self.read_markdown_folder(self.DOC_PATH)
        txt_text_list = self.read_txt_folder(self.DOC_PATH)
        md_list_src, md_list_docs = self.parse_info(markdown_text_list, mode="md")
        txt_list_src, txt_list_docs = self.parse_info(txt_text_list, mode="txt")
        self.list_docs, self.list_src = [], []
        self.list_docs.extend(md_list_docs)
        self.list_docs.extend(txt_list_docs)
        self.list_src.extend(md_list_src)
        self.list_src.extend(txt_list_src)
        self.get_stats_chunks(self.list_docs)
        
    def get_stats_chunks(self, list_docs):
        len_list = [len(i) for i in list_docs]
        logging.info(f"\nLen: {len(len_list)}, Mean len docs: {sum(len_list)//len(len_list)}, Min: {min(len_list)}, Max: {max(len_list)}\n")
    
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
    
    def read_txt_folder(self, folder_path):
        """
        Reads all txt files in a folder and saves the text in a list.

        Returns
        -------
            A list of strings, where each string is the text content of a txt file.
        """
        text_list = []
        for filename in os.listdir(folder_path):
            if filename.endswith(".txt"):
                file_path = os.path.join(folder_path, filename)
                with open(file_path, 'r', encoding="utf-8") as f:
                    text_list.append(f.read())
        return text_list

    def parse_info(self, text_list, mode="md"):
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
        from time import sleep
        for i in tqdm(range(len(text_list))):
            text=text_list[i]
            if mode=="md":
                src_list, chunks = self.get_src_chunks_md(text)
            else:
                print(len(list(text)))
                src_list, chunks = self.get_src_chunks_txt(text)
                self.get_stats_chunks(chunks)
            list_docs.extend(chunks)
            list_src.extend(src_list)
        return (list_src, list_docs)
    
    def get_src_chunks_md(self, text: str):
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


    def get_src_chunks_txt(self, text: str):
        src = text.split("URL: ")[1].split("\n")[0]
        chunk = text.split("Body Text:\n")[1].split("Related:")[0]
        chunks = [chunk]
        temp = True
        while temp:
            len_chunk = len(chunks)
            new_chunks = []
            for chunk in chunks:
                if len(chunk) > self.max_chunk_len:
                    dots = [i for i, char in enumerate(list(chunk)) if char == "."]
                    mid = len(chunk) // 2  
                    ind = min(dots, key=lambda x: abs(x-mid))
                    new_chunks.extend([chunk[:ind+1], chunk[ind+1:]])
                else:
                    new_chunks.append(chunk)
            temp = len(new_chunks) != len_chunk
            chunks = new_chunks
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
            collection_name=self.COLLECTION_NAME,
            data=query_vectors,               
            limit=2,                          
            output_fields=["text", "source"], 
        )
        parsed_result = self.parse_retrieval_results(results[0])
        self.query = self.prompt.generate_prompt(name_id=self.prompt_id, 
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


