from haystack.components.writers import DocumentWriter
from haystack.components.converters import PyPDFToDocument
from haystack.components.preprocessors import DocumentSplitter, DocumentCleaner
from haystack.components.routers import FileTypeRouter
from haystack.components.joiners import DocumentJoiner
from haystack.components.embedders import SentenceTransformersDocumentEmbedder
from haystack import Pipeline
from haystack.components.embedders import OpenAIDocumentEmbedder
from pathlib import Path
from haystack_integrations.document_stores.opensearch import OpenSearchDocumentStore
from dotenv import load_dotenv
import os

load_dotenv()

#openai.api_key = os.getenv('OPENAI_API_KEY')


class DocumentStoreHandler:
    def __init__(self, data_dir) -> None:
        self.data_dir = data_dir
        self.document_store = OpenSearchDocumentStore()
        self.file_type_router = FileTypeRouter(mime_types=["application/pdf"])
        self.pdf_converter = PyPDFToDocument()
        self.document_joiner = DocumentJoiner()

        self.document_cleaner = DocumentCleaner()
        self.document_splitter = DocumentSplitter(
            split_by="word", split_length=150, split_overlap=50
            )
        self.document_embedder = OpenAIDocumentEmbedder(model="text-embedding-3-large")
        self.document_writer = DocumentWriter(self.document_store)
        self.preprocessing_pipeline = Pipeline()

    def init_pipeline(self) -> None:
        self.preprocessing_pipeline.add_component(instance=self.file_type_router, name="file_type_router")
        self.preprocessing_pipeline.add_component(instance=self.pdf_converter, name="pypdf_converter")
        self.preprocessing_pipeline.add_component(instance=self.document_joiner, name="document_joiner")
        self.preprocessing_pipeline.add_component(instance=self.document_cleaner, name="document_cleaner")
        self.preprocessing_pipeline.add_component(instance=self.document_splitter, name="document_splitter")
        self.preprocessing_pipeline.add_component(instance=self.document_embedder, name="document_embedder")
        self.preprocessing_pipeline.add_component(instance=self.document_writer, name="document_writer")  

        self.preprocessing_pipeline.connect("file_type_router.application/pdf", "pypdf_converter.sources")
        self.preprocessing_pipeline.connect("pypdf_converter", "document_joiner")
        self.preprocessing_pipeline.connect("document_joiner", "document_cleaner")
        self.preprocessing_pipeline.connect("document_cleaner", "document_splitter")
        self.preprocessing_pipeline.connect("document_splitter", "document_embedder")
        self.preprocessing_pipeline.connect("document_embedder", "document_writer")

    def write_docs2docstore(self):
        self.preprocessing_pipeline.run({"file_type_router": {"sources": list(Path(self.data_dir))}})

