import os
import sys

testdir = os.path.dirname(__file__)
sys.path.insert(0, os.path.abspath(os.path.join(testdir, "../../../")))
from pathlib import Path
import unittest
from unittest.mock import patch, mock_open
from agent_service.agent.agent_step import (
    AgentStep,
    AgentFinalStep,
)
from agent_service.agent.reasoning_trace import ReasoningLogger
import json
from agent_service.agent.task_type import TaskType


class TestReasoningLogger(unittest.TestCase):

    def setUp(self):
        self.trace = ReasoningLogger(task_type=TaskType.ANSWERING, model_id="mix")

    def test_add_exception(self):
        """Test if exceptions are added correctly to the errors list."""
        exception = Exception("Test exception")
        self.trace.add_exception(exception)
        self.assertIn(exception, self.trace.errors)

    def test_add_step(self):
        """Test if steps are added correctly to the trace list."""
        step = AgentStep(
            thought="Test thought",
            action="Test action",
            action_input="Test input",
            observation="Test observation",
        )
        self.trace.add_step(step)
        self.assertIn(step, self.trace.trace)

    def test_remove_step(self):
        """Test if steps are removed correctly from the trace list."""
        step1 = AgentStep(
            thought="Thought1",
            action="Action1",
            action_input="Input1",
            observation="Observation1",
        )
        step2 = AgentStep(
            thought="Thought2",
            action="Action2",
            action_input="Input2",
            observation="Observation2",
        )
        self.trace.add_step(step1)
        self.trace.add_step(step2)
        self.trace.remove_step(0)
        self.assertNotIn(step1, self.trace.trace)
        self.assertIn(step2, self.trace.trace)

    def test_remove_step_invalid_index(self):
        """Test that no error is raised when removing a step with an invalid index."""
        step = AgentStep(
            thought="Test thought",
            action="Test action",
            action_input="Test input",
            observation="Test observation",
        )
        self.trace.add_step(step)
        self.trace.remove_step(5)  # No error should be raised
        self.assertIn(step, self.trace.trace)

    def test_get_last_step(self):
        """Test if the last step is retrieved correctly."""
        step1 = AgentStep(
            thought="Thought1",
            action="Action1",
            action_input="Input1",
            observation="Observation1",
        )
        step2 = AgentStep(
            thought="Thought2",
            action="Action2",
            action_input="Input2",
            observation="Observation2",
        )
        self.trace.add_step(step1)
        self.trace.add_step(step2)
        self.assertEqual(self.trace.get_last_step(), step2)

    def test_get_last_step_empty(self):
        """Test that None is returned when the trace list is empty."""
        self.assertIsNone(self.trace.get_last_step())

    def test_str(self):
        """Test the string representation of the trace."""
        step = AgentStep(
            thought="Test thought",
            action="Test action",
            action_input="Test input",
            observation="Test observation",
        )
        self.trace.add_step(step)
        expected_str = "Thought: Test thought\nAction: Test action\nAction Input: Test input\nObservation: Test observation\n\n"
        self.assertEqual(str(self.trace), expected_str)

    @patch("builtins.open", new_callable=mock_open)
    @patch("os.makedirs")
    @patch("uuid.uuid4", return_value="test-uuid")
    def test_to_json(self, mock_uuid, mock_makedirs, mock_open):
        """Test the JSON conversion and file writing functionality."""
        step = AgentStep(
            thought="Test thought",
            action="Test action",
            action_input="Test input",
            observation="Test observation",
        )
        self.trace.add_step(step)
        self.trace.set_query("Test query")
        self.trace.get_final_answer(reached_max_iterations=False)
        final_step = AgentFinalStep(final_answer="Test observation")
        self.trace.to_json()

        expected_dict = {
            "query": "Test query",
            "reasoning_steps": [step.model_dump(), final_step.model_dump()],
            "final_answer": "Test observation",
            "errors": [],
            "model": "mix",
            "task_type": "qa",
            "query_id": "test-uuid",
        }

        expected_json = json.dumps(expected_dict, indent=4, ensure_ascii=False)

        mock_open.assert_called_once_with(
            Path("out/test-uuid_mix.json"), "w", encoding="utf8"
        )
        handle = mock_open()
        written_content = "".join(
            call_args[0][0] for call_args in handle.write.call_args_list
        )
        self.assertEqual(written_content, expected_json)

    def test_set_query(self):
        """Test setting the query."""
        self.trace.set_query("Test query")
        self.assertEqual(self.trace.query, "Test query")

    def test_get_final_answer(self):
        """Test the final answer building functionality."""
        step = AgentStep(
            thought="Test thought",
            action="Test action",
            action_input="Test input",
            observation="Test observation",
        )
        self.trace.add_step(step)
        self.trace.get_final_answer(reached_max_iterations=False)
        final_step = self.trace.get_last_step()
        self.assertIsInstance(final_step, AgentFinalStep)
        self.assertEqual(final_step.final_answer, "Test observation")


if __name__ == "__main__":
    unittest.main()
