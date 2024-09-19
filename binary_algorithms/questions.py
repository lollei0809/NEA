import random
from abc import ABC, abstractmethod

class Question(ABC):  # abstract base class which other question objects inherit from
    def __init__(self):
        self.answers = [0, 0, 0]
        self.correct_answer = 0
        self.user_answer = 0
        self.question = ""
        self.wrongly_answered = 0

    @abstractmethod # virtual/abstract method that subclasses will overwrite
    def generate_question(self):
        pass

    @abstractmethod
    def generate_answer(self):
        pass
    @abstractmethod
    def generate_plausible_answers(self):
        pass

    def check_answer(self):
        return self.user_answer == self.correct_answer

if __name__ == "__main__": #importing this module wont run the code
    question = Question()
    question.generate_question()
    question.generate_answer()
    question.generate
