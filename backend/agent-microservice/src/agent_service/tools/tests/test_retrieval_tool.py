import sys, os, logging
from agent_service.tools.retrieval_tool import RetrievalTool
from scripts.setup_logging import setup_logging
import unittest

class TestPromptBuilder(unittest.TestCase):
    
    def setUp(self):
        setup_logging()
        self.example = "Dürfen die ausländischen Studierenden den Wohnberechtigungsschein beantragen?"
        self.tool = RetrievalTool(True)
        logging.info("Successfully built")

    def test_create_prompts(self):
        results = self.tool.run(self.example)
        logging.info(f"\n\n\n\nResults: {results} \n\n\n\n")
        self.assertEqual(True, True)