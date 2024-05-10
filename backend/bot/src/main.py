from document_handler import DocumentStoreHandler
from agent import LLMAgent
from rag import RetrievalAugmentedGeneration
import logging
import boto3
import warnings
warnings.filterwarnings("ignore")
if __name__ == "__main__":
    ds = DocumentStoreHandler()
    ds.parse_pdf()
    # Load the Bedrock client using Boto3.
    #bedrock = boto3.client(service_name='bedrock-runtime')
    #model = LLMAgent(bedrock=bedrock)
    #model_path = 'backend/rag/models/mixtral-8x7b-v0.1.Q4_K_M.gguf'
    #model = RetrievalAugmentedGeneration(model_path)
    #response = model.run('Erklär mir mit Beispielen wie benutze ich weil.')
    # response = rag.run("Generiere bitte Aufgaben für das Thema 'Nebensätze mit weil'")
    #print(response)