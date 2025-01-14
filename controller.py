from typing import Optional
from questions import Question, UnsignedQuestion, SignAndMagnitude, HexToDec
from user import User
import random


class ControlGame:
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

    def get_question_type(self, recommend, type):
        if recommend == "yes":
            type = self.recommend_question()
        if type in self.types.keys():
            self.type = type
            self.type_acr = self.types[self.type]

    def gen_question(self):  # after question type is chosen
        if self.type_acr in UnsignedQuestion.allowed_types.keys():
            self.question = UnsignedQuestion(self.type_acr)
        elif self.type_acr in SignAndMagnitude.allowed_types.keys():
            self.question = SignAndMagnitude(self.type_acr)
        elif self.type_acr in HexToDec.allowed_types.keys():
            self.question = HexToDec(self.type_acr)
        else:
            return "incorrect acronym"
        self.question.run()

    def set_answer(self, answer):
        self.question.user_answer = answer

    def update_scores(self, ):
        if self.question.check_answer():
            self.correct += 1
            return "correct"

            # self.user.details_dict[self.user.username][self.type]["correct"][-1] += 1
        else:
            self.incorrect += 1
            return "incorrect"

            # self.user.details_dict[self.user.username][self.type]["correct"][-1] += 1

    def define_user(self, option):
        self.user = User()
        self.user.get_details()
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
        # make weightings if no questions answered start 50%
        for i in range(len(decimals)):
            decimals[i] = 1 - decimals[i]  # reverses so mostly correct is low decimal so less likely to be chosen
        choice = random.choices(list(self.types.keys()), weights=decimals)
        # choice is returned as list with 1 item
        return choice[0]
