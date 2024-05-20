from agent_service.agent.agent_step import AgentStep
from agent_service.exeptions.step_exception import ActionInputNotFoundException, ActionNotFoundException, InvalidToolException
from typing import List
import re
import logging
class StepParser:
    def __init__(self, tool_names:List[str]):
        self.tool_names:List[str]=tool_names
        self.logger = logging.getLogger('StepParser')


    def parse_step(self, input:str) -> AgentStep:
        lines = input.split('\n')
        first_line = lines[0].strip()
        thought = self.extract_thought(first_line)

        remaining_text = '\n'.join(lines[1:])

        action, action_input = self.extract_action(remaining_text)

        self.validate_action(action, action_input)

        step = AgentStep(
            thought=thought,
            action=action,
            action_input=action_input
        )
        self.logger.info(step.toString())
        return step 

    def validate_action(self, action, action_input):
        if action is None:
            raise ActionNotFoundException("Missing 'Action:' in input")
        elif action not in self.tool_names:
            raise InvalidToolException(f"Unknown action: {action}")
        if action_input is None:
            raise ActionInputNotFoundException("Missing 'Action Input:' in input")

    def extract_action(self, remaining_text):
        action_pattern = r'Action:\s*(.*?)(?=\n|$)'
        action_input_pattern = r'Action Input:\s*(.*?)(?=\n|$)'
        action_match = re.search(action_pattern, remaining_text, re.DOTALL)
        action_input_match = re.search(action_input_pattern, remaining_text, re.DOTALL)

        # Extract values from the matches
        action = action_match.group(1).strip() if action_match else None
        action_input = action_input_match.group(1).strip() if action_input_match else None

        action_input = self.remove_quotes(action_input)
        action = self.remove_quotes(action)
        return action, action_input

    def extract_thought(self, first_line):
        if first_line.startswith('Thought:'):
            thought = first_line[len('Thought:'):].strip()
        else:
            thought = first_line
        return thought

    def remove_quotes(self, input):
        if input is None:
            return None
        if input.startswith('"') and input.endswith('"'):
            input = input[1:-1]
        if input.startswith("'") and input.endswith("'"):
            input = input[1:-1]
        return input
