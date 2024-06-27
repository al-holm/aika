class TextNotFoundException(Exception):

    def __init__(self):
        super().__init__("The text for generating exercises is not found")


class ExercisesNotGeneratedException(Exception):

    def __init__(self):
        super().__init__("TaskGenerator couldn't generate exercises")


class ExplanationNotFoundException(Exception):

    def __init__(self, topic: str):
        super().__init__(
            f"LessonRetriever didn't find an explanation to the topic '{topic}'"
        )


class ExtractingExercisesError(Exception):
    """
    Raised if extracting generated exercises from the LLM response failed
    """

    def __init__(self):
        super().__init__("Extracting exercises failed")
