from document_handler import DocumentStoreHandler
from agent import LLMAgent
from rag import RetrievalAugmentedGeneration
import logging
import boto3
import warnings
for _ in logging.root.manager.loggerDict:
    logging.getLogger(_).setLevel(logging.CRITICAL)

logging.basicConfig(format='%(asctime)s | %(levelname)s: %(message)s', level=logging.NOTSET)
logger = logging.getLogger('REACT Agent')
logger.setLevel(logging.INFO)

warnings.filterwarnings("ignore")
if __name__ == "__main__":
    #ds = DocumentStoreHandler()
    #ds.parse_pdf()
    # Load the Bedrock client using Boto3.
    bedrock = boto3.client(service_name='bedrock-runtime')
    model = LLMAgent(bedrock=bedrock)
    response = model.run('Erstelle bitte einen Lesetext zum Thema Familie für das Niveau A2')
    print(response)