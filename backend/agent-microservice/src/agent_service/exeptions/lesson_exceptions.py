class TextNotFoundException(Exception):

    def __init__(self):
        super().__init__("The text for generating exercises is not found")