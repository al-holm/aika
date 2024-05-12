from document_handler import DocumentStoreHandler
from rag_german import LLMAgent
import logging
import boto3

if __name__ == "__main__":
    # Load the Bedrock client using Boto3.
    bedrock = boto3.client(service_name='bedrock-runtime')
    #model_path = 'backend/rag/models/mixtral-8x7b-v0.1.Q4_K_M.gguf'
    rag = LLMAgent(bedrock=bedrock)
    response = rag.run('Erklär mir mit Beispielen wie benutze ich weil')
    # response = rag.run("Generiere bitte Aufgaben für das Thema 'Nebensätze mit weil'")
    print(response)