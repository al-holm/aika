from agent_service.agent.agent_step import AgentStep, AgentValidationStep
from agent_service.exeptions.step_exception import ActionInputNotFoundException, ActionNotFoundException, InvalidToolException
from typing import List
import re
import logging
from abc import ABC, abstractmethod

# The class `Parser` is an abstract class with a method `parse_step` that must be implemented by
# subclasses.
class Parser(ABC):
    @abstractmethod
    def parse_step(self, input:str):
        '''takes an input string and parses it
        
        '''
        pass

# This class `StepParser` parses input text to extract thought, action, and action input for an
# `AgentStep` object, validating the action and action input.
class StepParser(Parser):
    def __init__(self, tool_names:List[str]):
        self.tool_names:List[str]=tool_names
        self.logger = logging.getLogger('StepParser')


    def parse_step(self, input:str) -> AgentStep:
        '''parses input text to extract thought, action, and action input
        for an `AgentStep` object.
        
        Returns
        -------
            An instance of the `AgentStep`
        
        '''
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
        self.logger.info(str(step))
        return step 

    def validate_action(self, action, action_input):
        '''checks if the provided action and action input are valid, raising
        exceptions if they are missing or unknown.
         
        '''
        if action is None:
            raise ActionNotFoundException("Missing 'Action:' in input")
        elif action not in self.tool_names:
            raise InvalidToolException(f"Unknown action: {action}")
        if action_input is None:
            raise ActionInputNotFoundException("Missing 'Action Input:' in input")

    def extract_action(self, remaining_text):
        '''extracts action and action input values from a given text,
        removing any surrounding quotes.
        
        '''
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
        '''extracts thought in the first line from the input

        '''
        if first_line.startswith('Thought:'):
            thought = first_line[len('Thought:'):].strip()
        else:
            thought = first_line
        return thought

    def remove_quotes(self, input):
        '''removes quotation marks from the beginning and end of a string input.
        
        '''
        if input is None:
            return None
        if input.startswith('"') and input.endswith('"'):
            input = input[1:-1]
        if input.startswith("'") and input.endswith("'"):
            input = input[1:-1]
        return input

# This class `ValidationParser` parses an input string to extract validation thought
# in an `AgentValidationStep` object.
class ValidationParser(Parser):
    def __init__(self) -> None:
        self.logger = logging.getLogger("FinalAnswer")
         
    def parse_step(self, input:str) -> AgentValidationStep:
        '''parses an input string to extract the first line and returns it as an
        AgentValidationStep object.
        
        
        '''
        validation_thought = input.split("\n")[0]
        self.logger.info(validation_thought)
        return AgentValidationStep(validation_thought=validation_thought)
    