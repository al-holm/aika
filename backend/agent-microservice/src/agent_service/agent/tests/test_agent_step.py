import unittest
import os
import sys, os

testdir = os.path.dirname(__file__)
sys.path.insert(0, os.path.abspath(os.path.join(testdir, "../../../")))

from agent_service.agent.agent_step import (
    AgentStep,
    AgentFinalStep,
    AgentValidationStep,
)


class TestAgentStep(unittest.TestCase):

    def test_initialization(self):
        step = AgentStep(
            thought="Thinking",
            action="Action",
            action_input="Input",
            observation="Observation",
        )
        self.assertEqual(step.thought, "Thinking")
        self.assertEqual(step.action, "Action")
        self.assertEqual(step.action_input, "Input")
        self.assertEqual(step.observation, "Observation")

    def test_initialization_without_observation(self):
        step = AgentStep(thought="Thinking", action="Action", action_input="Input")
        self.assertEqual(step.observation, None)

    def test_str(self):
        step = AgentStep(
            thought="Thinking",
            action="Action",
            action_input="Input",
            observation="Observation",
        )
        expected_repr = "Thought: Thinking\nAction: Action\nAction Input: Input\nObservation: Observation\n"
        self.assertEqual(str(step), expected_repr)

    def test_str_without_observation(self):
        step = AgentStep(thought="Thinking", action="Action", action_input="Input")
        expected_repr = "Thought: Thinking\nAction: Action\nAction Input: Input\n"
        self.assertEqual(str(step), expected_repr)


class TestAgentFinalStep(unittest.TestCase):

    def test_initialization(self):
        final_step = AgentFinalStep(final_answer="This is the final answer.")
        self.assertEqual(final_step.final_answer, "This is the final answer.")

    def test_str(self):
        final_step = AgentFinalStep(final_answer="This is the final answer.")
        self.assertEqual(str(final_step), "Final Answer: This is the final answer.\n")


class TestAgentValidationStep(unittest.TestCase):

    def test_initialization(self):
        validation_step = AgentValidationStep(validation_thought="This is a hint.")
        self.assertEqual(validation_step.validation_thought, "This is a hint.")

    def test_str(self):
        validation_step = AgentValidationStep(validation_thought="This is a hint.")
        expected_repr = "Hint : This is a hint.\n"
        self.assertEqual(str(validation_step), expected_repr)


if __name__ == "__main__":
    unittest.main()
