import sys, os, logging
import sys, os
testdir = os.path.dirname(__file__)
sys.path.insert(0, os.path.abspath(os.path.join(testdir, '../../../')))
from agent_service.tools.retrieval_tool import RetrievalTool
from scripts.setup_logging import setup_logging
import unittest, xmlrunner
""" 
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

if __name__ == '__main__':
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports')) """