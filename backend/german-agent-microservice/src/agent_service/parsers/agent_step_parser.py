from agent_service.agent.agent_step import AgentStep
from typing import List
import re
import logging
class StepParser:
    def __init__(self, tool_names:List[str]):
        self.tool_names:List[str]=tool_names
        self.logger = logging.getLogger('StepParser')


    def parse_step(self, input:str) -> AgentStep:
        # Define regex patterns for each component
        action_pattern = r'Action:\s*(.*?)(?=\n|$)'
        action_input_pattern = r'Action Input:\s*(.*?)(?=\n|$)'

        # Split input into lines and handle the first line as thought
        lines = input.split('\n')
        first_line = lines[0].strip()
        if first_line.startswith('Thought:'):
            thought = first_line[len('Thought:'):].strip()
        else:
            thought = first_line

        # Remaining text to process
        remaining_text = '\n'.join(lines[1:])

        # Search for patterns in the remaining text
        action_match = re.search(action_pattern, remaining_text, re.DOTALL)
        action_input_match = re.search(action_input_pattern, remaining_text, re.DOTALL)

        # Extract values from the matches
        action = action_match.group(1).strip() if action_match else None
        action_input = action_input_match.group(1).strip() if action_input_match else None

        if action is None:
            raise ValueError("Missing 'Action:' in input")
        elif action not in self.tool_names:
            raise ValueError(f"Unknown action: {action}")
        if action_input is None:
            raise ValueError("Missing 'Action Input:' in input")
        
        if action_input.startswith('"') and action_input.endswith('"'):
            action_input = action_input[1:-1]

        step = AgentStep(
            thought=thought,
            action=action,
            action_input=action_input
        )
        self.logger.info(step.toString())
        return step 
