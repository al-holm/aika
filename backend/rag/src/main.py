from document_handler import DocumentStoreHandler
from rag_german import RetrievalAugmentedGeneration
import logging


if __name__ == "__main__":
    model_path = 'backend/rag/models/mixtral-8x7b-v0.1.Q4_K_M.gguf'
    rag = RetrievalAugmentedGeneration(model_path=model_path)
    response = rag.run('Erklär mir mit Beispielen wie benutze ich weil')
    print(response)