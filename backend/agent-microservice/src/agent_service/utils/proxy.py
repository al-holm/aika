from abc import ABC, abstractmethod
from typing import Callable, Any
import json

class LessonProxy():
    DATA_PATH = 'agent_service/utils/res/'
    def __init__(self, service_text: Callable[[], Any], service_exercises: Callable[[], Any]) -> None:
        self.service_text = service_text
        self.service_exercises = service_exercises

    def create_text(self, request: str):
        if request.startswith("[Listening][Ich stelle mich vor."):
            with open(self.DATA_PATH + 'layla/text.txt', 'r') as f:
                text = f.read()
                print(text)
            self.request = request
            return text
        else:
            self.request = request
            return self.service_text(request)
        
    def create_exercises(self):
        if self.request.startswith("[Listening][Ich stelle mich vor."):
            with open(self.DATA_PATH + 'layla/tasks.json', 'r') as f:
                tasks = json.load(f)
            return {'tasks' :tasks }
        else: 
            return self.service_exercises()
