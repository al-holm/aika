import sys, os

testdir = os.path.dirname(__file__)
sys.path.insert(0, os.path.abspath(os.path.join(testdir, "../../../")))
from agent_service.rag.rag import RAG
import unittest


class TestRAG(unittest.TestCase):

    def setUp(self):
        self.rag = RAG(init=False, llm="bedrock", test=True)
        self.rag.max_chunk_len = 50


if __name__ == "__main__":
    unittest.main()
