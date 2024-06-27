class ActionNotFoundException(Exception):
    """
    can be raised by StepParser if the action is not in the answer
    """

    def __init__(self, message):
        super().__init__(message)


class InvalidToolException(Exception):
    """
    can be raised by StepParser if the action contains a tool that is not available
    """

    def __init__(self, message):
        super().__init__(message)


class ActionInputNotFoundException(Exception):
    """
    can be raised by StepParser if the action input is not found.
    """

    def __init__(self, message):
        super().__init__(message)
