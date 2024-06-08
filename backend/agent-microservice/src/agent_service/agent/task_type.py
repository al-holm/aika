from enum import Enum

class TaskType(Enum):
    """
    defines an enumeration with two members, LESSON and ANSWERING, each associated
    with different task type: creation of a lesson & answering user queries or answering the questions about law an evaryday life.
    """
    LESSON = 'lesson'
    ANSWERING = 'qa'
    LAWLIFE = 'law'