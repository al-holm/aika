import os
import sys, os
testdir = os.path.dirname(__file__)
sys.path.insert(0, os.path.abspath(os.path.join(testdir, '../../../')))
import unittest
from agent_service.prompts.react_prompt import REACT_PROMPT
from agent_service.prompts.final_answer_prompt import VALIDATION_PROMPT, VAL_STOP_PREFIX
from unittest.mock import patch, MagicMock, mock_open
from agent_service.agent.agent_step import AgentStep, AgentValidationStep, AgentFinalStep
from agent_service.prompts.prompt_builder import PromptBuilder
from agent_service.agent.reasoning_trace import ReasoningTrace
from agent_service.core.config import Config
from agent_service.core.pydantic_agent import AgentConfigModel
from agent_service.agent.llm import LLMBedrock
from agent_service.agent.agent import Agent  # Adjust the import according to your module's actual name
# HINT MOCKOBJECTS 
# with patch.object(ProductionClass, 'method', return_value=None) as mock_method:
#     thing = ProductionClass()
#     thing.method(1, 2, 3)

class TestAgent(unittest.TestCase):

    def setUp(self):
        self.agent = Agent()

    def test_init_prompts(self):
        with patch.object(PromptBuilder, 'create_prompts') as mock_create_prompts:
            self.agent.init_prompts()
            mock_create_prompts.assert_called_once_with({
                self.agent.PLAN: REACT_PROMPT,
                self.agent.VAL: VALIDATION_PROMPT
            })

    def test_set_prompts_for_query(self):
        with patch.object(PromptBuilder, 'update_prompt') as mock_update_prompt:
            query = "Test query"
            self.agent.set_prompts_for_query(query)
            update = {
                "tools": str(self.agent.tool_executor),
                "tool_names": self.agent.tool_executor.tool_names,
                "input": query
            }
            calls = [
                unittest.mock.call(name_id=self.agent.PLAN, **update),
                unittest.mock.call(name_id=self.agent.VAL, **update)
            ]
            mock_update_prompt.assert_has_calls(calls, any_order=True)
            self.assertEqual(self.agent.reasoning_logger.query, query)

    def test_get_current_prompt(self):
        self.agent.reasoning_logger.add_step(AgentStep(thought="Test thought", action="Test action", action_input="Test input", observation="Test observation"))
        with patch.object(PromptBuilder, 'generate_prompt', return_value="Generated Prompt") as mock_generate_prompt:
            result = self.agent.get_current_prompt(mode="plan")
            self.assertEqual(result, "Generated Prompt")
            mock_generate_prompt.assert_called_once_with(name_id=self.agent.PLAN, reasoning_trace=str(self.agent.reasoning_logger))

if __name__ == '__main__':
    unittest.main()