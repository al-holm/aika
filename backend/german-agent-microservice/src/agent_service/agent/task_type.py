from enum import Enum

class TaskType(Enum):
    """
    defines an enumeration with two members, LESSON and ANSWERING, each associated
    with different task type: creation of a lesson & answering user queries.
    """
    LESSON = 'lesson'
    ANSWERING = 'qa'