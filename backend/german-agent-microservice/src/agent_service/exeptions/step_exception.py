# a custom exception class that is raised by StepParser
# if the action is not in the answer
class ActionNotFoundException(Exception):
    def __init__(self, message):            
        super().__init__(message)

class InvalidToolException(Exception):
    def __init__(self, message):            
        super().__init__(message)

class ActionInputNotFoundException(Exception):
    def __init__(self, message):            
        super().__init__(message)


