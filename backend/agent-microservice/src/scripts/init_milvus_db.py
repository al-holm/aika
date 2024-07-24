from milvus_db.milvus_db import MilvusDBClient
from agent_service.utils.document_handler import DocumentHandler, DocumentType
from pymilvus.model import hybrid

ef = hybrid.BGEM3EmbeddingFunction(
        model_name="BAAI/bge-m3", device="cpu", use_fp16=False
    )

document_handler = DocumentHandler()

client = MilvusDBClient()

client.create_collection(
    collection_name="trajectoryLibrary",
    dimension=1024
)

tmp = document_handler.load_docs("agent_service/agent/res/trajectories_data/", DocumentType.TRAJECTORY)

doc_embeddings = ef.encode_documents(tmp["docs"])["dense"]
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

client.insert_data(collection_name="trajectoryLibrary", data=data)


client.create_collection(
    collection_name="LawAndLifeLibrary",
    dimension=1024
)

tmp = document_handler.load_docs("agent_service/rag/res/data/", DocumentType.RAG)
doc_embeddings = ef.encode_documents(tmp["docs"])["dense"]

data = [
    {
        "id": i,
        "vector": doc_embeddings[i],
        "text": tmp["docs"][i],
        "source": tmp["source"][i],
    }
    for i in range(len(doc_embeddings))
]

client.insert_data(collection_name="LawAndLifeLibrary", data=data)