import unittest
from unittest.mock import patch, MagicMock
import sys, os
testdir = os.path.dirname(__file__)
sys.path.insert(0, os.path.abspath(os.path.join(testdir, '../../../')))
from agent_service.agent.llm import LLMBedrock
from agent_service.tools.web_search_tool import WebSearch
class TestWebSearch(unittest.TestCase):

    @patch('requests.post')
    @patch('agent_service.agent.llm.LLMBedrock.run')
    def test_run_success(self, mock_llm_run, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "answers": [],
            "results": [
                {"title": "Title1", "content": "Content1"},
                {"title": "Title2", "content": "Content2"}
            ]
        }
        mock_post.return_value = mock_response

        mock_llm_run.return_value = "Mock LLM response"

        web_search = WebSearch(name="Test Search", description="A test search", llm="bedrock",
                               prompt_id="test_id", prompt_template="template", max_tokens=100)

        result = web_search.run("Test query")

        self.assertIn("Mock LLM response", result)

    @patch('requests.post')
    @patch('agent_service.agent.llm.LLMBedrock.run')
    def test_run_empty_results(self, mock_llm_run, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {"answers": [], "results": []}
        mock_post.return_value = mock_response


        mock_llm_run.return_value = "Mock LLM response for empty results"

        web_search = WebSearch(name="Test Search", description="A test search", llm="bedrock",
                               prompt_id="test_id", prompt_template="template", max_tokens=100)

        result = web_search.run("Test query with no results")

        self.assertIn("Mock LLM response for empty results", result)

    @patch('requests.post')
    @patch('agent_service.agent.llm.LLMBedrock.run')
    def test_run_exception_handling(self, mock_llm_run, mock_post):
        mock_post.side_effect = Exception("API failure")

        web_search = WebSearch(name="Test Search", description="A test search", llm="bedrock",
                               prompt_id="test_id", prompt_template="template", max_tokens=100)

        result = web_search.run("Test query causing exception")

        self.assertIn("Wiederhole die Anfrage noch mal", result)

    def test_setup_request(self):
        web_search = WebSearch(name="Test Search", description="A test search", llm="bedrock",
                               prompt_id="test_id", prompt_template="template", max_tokens=100)
        querystring, headers = web_search.setup_request("Test query")
        self.assertEqual(querystring['q'], "Test query")
        self.assertEqual(headers['X-RapidAPI-Key'], os.environ["RAPIDAPI_KEY"])

    @patch('requests.post')
    @patch('agent_service.agent.llm.LLMBedrock.run')
    def test_run_with_partial_results(self, mock_llm_run, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "answers": [{"text": "Partial answer"}],
            "results": [
                {"title": "Title1", "content": "Content1"},
            ]
        }
        mock_post.return_value = mock_response

        mock_llm_run.return_value = "Mock LLM response for partial results"

        web_search = WebSearch(name="Test Search", description="A test search", llm="bedrock",
                               prompt_id="test_id", prompt_template="template", max_tokens=100)

        result = web_search.run("Test query with partial results")

        self.assertIn("Mock LLM response for partial results", result)

if __name__ == '__main__':
    unittest.main()