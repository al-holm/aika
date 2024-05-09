
from llama_parse import LlamaParse
from dotenv import load_dotenv
from os import listdir
from os.path import isfile, join
from langchain_community.document_loaders import UnstructuredMarkdownLoader, DirectoryLoader
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai.embeddings import OpenAIEmbeddings
import weaviate
from langchain_weaviate.vectorstores import WeaviateVectorStore
from langchain_community.embeddings import HuggingFaceEmbeddings


load_dotenv()

# The `DocumentStoreHandler` class initializes with a data directory, parses PDF files to extract
# text, loads and splits documents, connects to a Weaviate client, and creates a Weaviate vector store
# from the documents using an embedder.
class DocumentStoreHandler:
    def __init__(self, data_dir, parse_pdf=False) -> None:
        self.data_dir = data_dir
        self.parser = LlamaParse(
            result_type="markdown",  # "markdown" and "text" are available
            verbose=True
        )
        if parse_pdf:
            self.parse_pdf()
        self.loader = DirectoryLoader(data_dir, glob="**/*.md", loader_cls=UnstructuredMarkdownLoader)
        self.embedder = HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-large-instruct")
        self.text_splitter = SemanticChunker(self.embedder)
        self.load_data()

    def parse_pdf(self):
        '''The function `parse_pdf` takes PDF files from a directory, extracts text from them using a
        parser, and saves the text in Markdown format in new files.    
        '''
        files = [join(self.data_dir, f) for f in listdir(self.data_dir) if isfile(join(self.data_dir, f)) and f.endswith('.pdf')]
        documents = self.parser.load_data(files)
        for i in range(len(documents)):
            doc = documents[i]
            file_name = files[i].split('/')[-1].split('.')[0]
            name = file_name + str(i) + '.md'
            path = join(self.data_dir, name)
            with open(path, "w") as f:
                f.write(doc.text)
    
    def load_data(self):
        '''The `load_data` function loads documents, splits text, connects to a Weaviate client, and
        creates a Weaviate vector store from the documents using an embedder.  
        '''
        docs = self.loader.load()
        docs = self.text_splitter.split_documents(docs)
        self.weaviate_client = weaviate.connect_to_local()
        self.doc_store = WeaviateVectorStore.from_documents(docs, self.embedder, client=self.weaviate_client)




