from document_handler import DocumentStoreHandler
from agent import LLMAgent
from rag import RetrievalAugmentedGeneration
import logging
import boto3
import warnings
import uuid
from dotenv import load_dotenv
import os
load_dotenv()

warnings.filterwarnings("ignore")
if __name__ == "__main__":
    #ds = DocumentStoreHandler()
    #ds.parse_pdf()
    # Load the Bedrock client using Boto3.
    bedrock = boto3.client(service_name='bedrock-runtime')
    model = LLMAgent(bedrock=bedrock)
    #model_path = 'backend/rag/models/mixtral-8x7b-v0.1.Q4_K_M.gguf'
    #model = RetrievalAugmentedGeneration(model_path)
    #response = model.run('wo kann ich einen Integrationskurs in Marburg besuchen?')
    response = model.run("Generiere bitte einen Hörtext zum Thema 'Meine Familie' für das Niveau A2.")
    print(response)
