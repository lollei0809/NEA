from typing import Optional
import pyinputplus as pyip
from questions import Question, UnsignedQuestion, SignAndMagnitude, HexToDec
from user import User
import random


class GamePlay():
    def __init__(self):
        self.user: Optional[User] = None
        self.question: Optional[Question] = None  # self.question can be none or a question object or its subclasses
        self.correct = 0
        self.incorrect = 0
        self.type_acr = ""
        self.type = ""
        self.types = {"unsigned binary to decimal": "ubtd",
                      "decimal to unsigned binary": "dtub",
                      "sign and magnitude binary to decimal": "smtd",
                      "decimal to sign and magnitude binary": "dtsm",
                      "hexadecimal to decimal": "htd",
                      "decimal to hexadecimal": "dth"}

    def get_question_type(self):
        recommend = pyip.inputYesNo("do you want questions based on past scores?")
        if recommend == "no":
            self.type = pyip.inputMenu(list(self.types.keys()),
                                   prompt="enter question type (1-6):\n",
                                   numbered=True)
        else:
            self.type = self.recommend_question()
        self.type_acr = self.types[self.type]

    def gen_question(self):  # after question type is chosen
        if self.type_acr in UnsignedQuestion.allowed_types.keys():
            self.question = UnsignedQuestion(self.type_acr)
        elif self.type_acr in SignAndMagnitude.allowed_types.keys():
            self.question = SignAndMagnitude(self.type_acr)
        elif self.type_acr in HexToDec.allowed_types.keys():
            self.question = HexToDec(self.type_acr)
        else:
            print("incorrect acronym")
        self.question.run()

    def get_answer(self):
        user_answer = "!"
        while user_answer not in self.question.plausible_answers:
            if self.question.allowed_types[self.type_acr] == "int":  # question parent class has no attribute allowed
                # types but its subclasses do. here the question type is already estblished in gen question.
                user_answer = int(input(f'{self.question.question_phrase} {self.question.plausible_answers}'))
            else:
                user_answer = input(f'{self.question.question_phrase} {self.question.plausible_answers}')
        self.question.user_answer = user_answer

    def update_scores(self, ):
        if self.question.check_answer():
            print("correct")
            self.correct += 1
            # self.user.details_dict[self.user.username][self.type]["correct"][-1] += 1
        else:
            print("incorrect")
            self.incorrect += 1
            # self.user.details_dict[self.user.username][self.type]["correct"][-1] += 1

    def define_user(self):
        self.user = User()
        self.user.get_details()
        option = pyip.inputMenu(["sign in", "sign up"],
                                prompt="enter an option(1-2):\n",
                                numbered=True)
        if option == "sign in":
            self.user.sign_in()
        else:
            self.user.sign_up()

    def update_recorded_scores(self):
        self.user.details_dict[self.user.username][self.type]["correct"].append(self.correct)
        self.user.details_dict[self.user.username][self.type]["incorrect"].append(self.incorrect)

    def calc_average_correct(self, type):
        correct_sum = 0
        incorrect_sum = 0
        for item in self.user.details_dict[self.user.username][type]["correct"]:
            correct_sum += item
        for item in self.user.details_dict[self.user.username][type]["incorrect"]:
            incorrect_sum += item
        try:
            percent = correct_sum / (correct_sum + incorrect_sum)
        except ZeroDivisionError:
            percent = 0
        return round(percent, 2)

    def recommend_question(self):
        decimals = []
        for item in self.types.keys():
            decimals.append(self.calc_average_correct(item))
        #make weightings if no questions answered start 50%
        for decimal in decimals:
            decimal = 1-decimal # reverses so mostly correct is low decimal so less likely to be chosen
        choice = random.choices(self.types.keys(), weights=decimals, cum_weights=None)
        return choice

if __name__ == "__main__":
    game = GamePlay()
    game.define_user()
    game.recommend_question()
#     game.get_question_type()
#     while True:
#         game.gen_question()
#         game.get_answer()
#         game.update_scores()
#         go = input("continue?")
#         if go == "no":
#             break
#         same_type = input("same type?")
#         if same_type == "no":
#             game.update_recorded_scores()
#             game.correct = 0
#             game.incorrect = 0
#             game.get_question_type()
#
#     print(f"GAME OVER")
#     game.update_recorded_scores()
#     game.user.save_details_dict_to_json()
#     game.recommend_question()
#     game.user.sign_out()
