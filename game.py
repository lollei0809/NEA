from typing import Optional
from questions import Question, UnsignedQuestion
from user import User


class GamePlay():
    def __init__(self):
        self.user_answer: str = ""  # type hint and set default to empty string
        self.username: str = ""
        self.question: Optional[Question] = None # self.question can be none or a question object or its subclasses
        self.score = 0
        self.question_type = ""

    def get_question_type(self):
        pass

    def gen_question(self):
        self.question = UnsignedQuestion()
        self.question.run()

    def get_answer(self):
        user_answer = "!"
        while user_answer not in self.question.plausible_answers:
            self.user_answer = input(f'{self.question.question_phrase} {self.question.plausible_answers}')

    def update_score(self, ):
        if self.question.check_answer(self.user_answer):
            self.score += 1
        else:
            self.score -= 1

    def define_user(self):
        pass

# if __name__ == "__main__":
#     game = GamePlay()
#     game.signup()
