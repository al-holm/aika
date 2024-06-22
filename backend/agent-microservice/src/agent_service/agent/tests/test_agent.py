import unittest, xmlrunner
import sys, os
testdir = os.path.dirname(__file__)
sys.path.insert(0, os.path.abspath(os.path.join(testdir, '../../../')))
from unittest.mock import patch, MagicMock
from agent_service.agent.agent import Agent, AgentMode
from agent_service.agent.task_type import TaskType
from agent_service.agent.agent_step import AgentStep
from agent_service.prompts.react_prompt import ACTION_PROMPT_QA, VALIDATION_PROMPT_QA, VAL_STOP_PREFIX
from agent_service.agent.reasoning_trace import ReasoningLogger
from agent_service.tools.tool_executor import ToolExecutor
from agent_service.agent.llm import LLMBedrock
from agent_service.agent.agent_step import AgentValidationStep
from agent_service.parsers.agent_step_parser import StepParser, ValidationParser
from agent_service.prompts.trajectory_library import TrajectoryInjector


class TestAgent(unittest.TestCase):
    @patch('agent_service.prompts.trajectory_library.TrajectoryInjector.__init__', lambda x: None)
    def setUp(self):
        """Sets up a new Agent instance before each test."""
        with patch('agent_service.prompts.trajectory_library.TrajectoryInjector') as MockTrajectoryInjector:
            MockTrajectoryInjector.return_value = MagicMock()
            self.agent = Agent()

    @patch('agent_service.prompts.prompt_builder.PromptBuilder.create_prompts')
    def test_init_prompts(self, mock_create_prompts):
        """Tests the initialization of prompts."""
        self.agent.init_prompts(TaskType.ANSWERING)
        mock_create_prompts.assert_called_once_with({
            AgentMode.PLAN: ACTION_PROMPT_QA,
            AgentMode.VAL: VALIDATION_PROMPT_QA
        })

    @patch('agent_service.prompts.prompt_builder.PromptBuilder.update_prompt')
    @patch('agent_service.agent.agent.Agent.add_trajectory_examples_to_prompts', return_value="Injection..")
    def test_update_prompts_for_query(self, mock_trajcotory_add, mock_update_prompt):
        """Tests updating prompts with a query and available tools."""
        query = "Test query"
        self.agent.update_prompts_for_query(query)
        update = {
            "tools": str(self.agent.tool_executor),
            "tool_names": self.agent.tool_executor.tool_names,
            "input": query
        }
        calls = [
            unittest.mock.call(name_id=AgentMode.PLAN, **update),
            unittest.mock.call(name_id=AgentMode.VAL, **update)
        ]
        mock_update_prompt.assert_has_calls(calls, any_order=True)
        self.assertEqual(self.agent.reasoning_logger.query, query)

    @patch('agent_service.prompts.prompt_builder.PromptBuilder.generate_prompt', return_value="Generated Prompt")
    def test_get_current_prompt(self, mock_generate_prompt):
        """Tests getting the current prompt with a reasoning trace."""
        self.agent.reasoning_logger.add_step(
            AgentStep(thought="Test thought", action="Test action", action_input="Test input", observation="Test observation"))
        result = self.agent.get_current_prompt(mode=AgentMode.PLAN)
        self.assertEqual(result, "Generated Prompt")
        mock_generate_prompt.assert_called_once_with(
            name_id=AgentMode.PLAN, reasoning_trace=str(self.agent.reasoning_logger))

    @patch('agent_service.tools.tool_executor.ToolExecutor.execute', return_value="Mock Observation")
    def test_execute_step(self, mock_execute):
        """Tests executing a step and updating the reasoning logger."""
        step = AgentStep(thought="Test thought", action="Test action", action_input="Test input")
        self.agent.execute_step(step)
        mock_execute.assert_called_once_with("Test action", "Test input")
        self.assertEqual(step.observation, "Mock Observation")
        self.assertIn(step, self.agent.reasoning_logger.trace)

    @patch('agent_service.agent.llm.LLMBedrock.run', return_value="Validation Thought")
    def test_validate_step(self, mock_llm_run):
        """Tests validating a step and processing the validation thought."""
        self.agent.llm = LLMBedrock()
        with patch.object(self.agent, 'process_validation_thought', return_value=True) as mock_process_validation_thought:
            is_final = self.agent.validate_step()
            self.assertTrue(is_final)
            mock_llm_run.assert_called_once()
            mock_process_validation_thought.assert_called_once_with("Validation Thought")

    @patch('agent_service.agent.llm.LLMBedrock.run', return_value="Planned Step")
    def test_plan_step(self, mock_llm_run):
        """Tests planning a step and parsing the output."""
        self.agent.llm = LLMBedrock()
        with patch.object(self.agent.step_parser, 'parse_step', return_value=AgentStep(thought="Planned thought", action='Action', action_input='Input')) as mock_parse_step:
            step = self.agent.plan_step()
            self.assertEqual(step.thought, "Planned thought")
            mock_llm_run.assert_called_once()
            mock_parse_step.assert_called_once_with("Planned Step")

    @patch('agent_service.parsers.agent_step_parser.ValidationParser.parse_step', return_value=AgentValidationStep(validation_thought=VAL_STOP_PREFIX))
    def test_process_validation_thought(self, mock_parse_step):
        """Tests processing a validation thought and updating the reasoning trace."""
        val_answer = VAL_STOP_PREFIX
        is_final = self.agent.process_validation_thought(val_answer)
        mock_parse_step.assert_called_once_with(val_answer)
        self.assertIn(mock_parse_step.return_value, self.agent.reasoning_logger.trace)
        self.assertTrue(is_final)

    @patch('agent_service.prompts.prompt_builder.PromptBuilder.generate_prompt', return_value="Generated Prompt")
    def test_get_final_response(self, mock_generate_prompt):
        """Tests building and returning the final answer."""
        self.agent.reasoning_logger.add_step(AgentStep(thought="Test thought", action="Test action", action_input="Test input", observation="Test observation"))
        final_response = self.agent.get_final_response(iteration=1)
        self.assertIn("Test observation", final_response)

    @patch('agent_service.prompts.trajectory_library.TrajectoryInjector')
    def test_reset(self, mock_trajectory_injector):
        """Tests resetting the agent."""
        mock_trajectory_injector.return_value = MagicMock()
        initial_reasoning_logger = self.agent.reasoning_logger
        self.agent.reset()
        self.assertNotEqual(initial_reasoning_logger, self.agent.reasoning_logger)
        self.assertIsInstance(self.agent.reasoning_logger, ReasoningLogger)

if __name__ == '__main__':
    unittest.main()