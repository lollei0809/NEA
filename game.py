from questions import Question, UnsignedQuestion
import user
class GamePlay():
    def __init__(self):
        self.username = ""
        self.question = None
        self.score = 0
        self.question_type = ""

    def gen_question(self):
        self.question = UnsignedQuestion()
        self.question.run()

    def get_answer(self):
        user_answer = "!"
        while user_answer not in self.question.plausible_answers:
            self.user_answer = input(f'{self.question.question_phrase} {self.question.plausible_answers}')

    def update_score(self,):
        if self.question.check_answer(self.user_answer):
            self.score += 1
        else:
            self.score -= 1



#
# if __name__ == "__main__":
#     game = GamePlay()
#     game.signup()
