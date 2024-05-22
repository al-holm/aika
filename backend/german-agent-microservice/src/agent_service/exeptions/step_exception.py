# is raised by StepParser if the action is not in the answer
class ActionNotFoundException(Exception):
    def __init__(self, message):            
        super().__init__(message)

# is raised by StepParser if the action contains a tool that is not available
class InvalidToolException(Exception):
    def __init__(self, message):            
        super().__init__(message)

# is raised by StepParser if an action input is not found.
class ActionInputNotFoundException(Exception):
    def __init__(self, message):            
        super().__init__(message)


