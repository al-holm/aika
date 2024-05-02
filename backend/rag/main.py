from rag_german import RAG
import logging

logging.basicConfig(format="%(levelname)s - %(name)s -  %(message)s", level=logging.WARNING)
logging.getLogger("haystack").setLevel(logging.INFO)
if __name__ == "__main__":
    rag = RAG()
    print(rag.run('Erklär mir, wie man kausale Nebensätze bildet? Gib ein paar Beispiele.'))
      
    # docker pull opensearchproject/opensearch:2.11.0
    # docker run -p 9200:9200 -p 9600:9600 -e "discovery.type=single-node" -e "OPENSEARCH_JAVA_OPTS=-Xms1024m -Xmx1024m" opensearchproject/opensearch:2.11.0
    # pip install --upgrade --force-reinstall opensearch-haystack
