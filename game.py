from typing import Optional
import pyinputplus as pyip
from questions import Question, UnsignedQuestion, SignAndMagnitude, HexToDec
from user import User


class GamePlay():
    def __init__(self):
        self.user: Optional[User] = None
        self.question: Optional[Question] = None  # self.question can be none or a question object or its subclasses
        self.score = 0
        self.type_acr = ""
        self.type = ""
        self.types: dict = {}

    def get_question_type(self):
        self.types = {"unsigned binary to decimal": "ubtd",
                      "decimal to unsigned binary": "dtub",
                      "sign and magnitude binary to decimal": "smtd",
                      "decimal to sign and magnitude binary": "dtsm",
                      "hexadecimal to decimal": "htd",
                      "decimal to hexadecimal": "dth"}

        self.type = pyip.inputMenu(list(self.types.keys()),
                                   prompt="enter question type (1-6):\n",
                                   numbered=True)
        # pyip doesnt have function to return a number, it returns the value so i check back in the dictionary
        self.type_acr = self.types[self.type]

    def gen_question(self):#after question type is chosen.
        if self.type_acr in ["dtub", "ubtd"]:
            self.question = UnsignedQuestion(self.type_acr)
        elif self.type_acr in ["smtd", "dtsm"]:
            self.question = SignAndMagnitude(self.type_acr)
        elif self.type_acr in ["htd", "dth"]:
            self.question = HexToDec(self.type_acr)
        else:
            print("incorrect acronym")
        self.question.run()

    def get_answer(self):
        user_answer = "!"
        while user_answer not in self.question.plausible_answers:
            user_answer = int(input(f'{self.question.question_phrase} {self.question.plausible_answers}'))
        self.question.user_answer = user_answer

    def update_score(self, ):
        if self.question.check_answer():
            self.score += 1
        else:
            self.score -= 1

    def define_user(self):
        self.user = User()
        option = pyip.inputMenu(["sign in", "sign up", "sign out"],
                                prompt="enter an option(1-3):\n",
                                numbered=True)
        if option == "sign in":
            self.user.sign_in()
        elif option == "sign up":
            self.user.sign_up()
        else:
            self.user.sign_out()

if __name__ == "__main__":
    game = GamePlay()
    game.define_user()
    repeat = "yes"
    while repeat == "yes":
        game.get_question_type()
        game.gen_question()
        game.get_answer()
        game.update_score()
        repeat = pyip.inputYesNo(prompt="do you want annother question?:")

    print(f"GAME OVER\nSCORE:{game.score}\nHIGH SCORE:{game.user.details[game.user.username]['high_score']}")
