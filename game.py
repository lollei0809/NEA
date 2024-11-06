from questions import Question, UnsignedQuestion
from user import User
import bcrypt
from getpass import getpass  # when using getpass you must edit the conficurations to emulate terminal in output console


# why wont this run in console
class GamePlay():
    def __init__(self):
        self.question = None
        self.score = 0
        self.question_type = ""

"""    
    def signin(self):
        username = input("username:")
        password = getpass("password(hidden whilst typing):")

    def signup(self):
        name = input("name:")
        username = input("username:")
        password = getpass("password(hidden whilst typing):")
        string = password.encode('utf-8')
        salt = bcrypt.gensalt()
        self.hash_password = bcrypt.hashpw(string, salt)
"""

    def gen_question(self):
        self.question = UnsignedQuestion()
        self.question.run()

    def ask_question(self):
        return self.question.question_phrase, self.question.plausible_answers

    def get_answer(self, user_answer):
        while user_answer not in self.question.plausible_answers:
            return f"must be one of {self.question.plausible_answers}"
            self.get_answer()
        if self.question.check_answer(user_answer):
            self.score += 1
        else:
            self.score -= 1



#
# if __name__ == "__main__":
#     game = GamePlay()
#     game.signup()
