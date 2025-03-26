from typing import Optional
from main_code.questions import Question, UnsignedQuestion, SignAndMagnitude, HexToDec, TwosComplement
from main_code.user import User
import random


class ControlGame:
    def __init__(self):
        self.user: Optional[User] = None
        self.question: Optional[Question] = None  # self.question can be none or a question object or its subclasses
        self.graph_user1 = ""
        self.graph_user2 = ""
        self.graph_question_type = ""
        self.correct = 0
        self.incorrect = 0
        self.type_acr = "ubtd"
        self.recommend = False
        self.type = "unsigned binary to decimal"
        self.types = {"unsigned binary to decimal": "ubtd",
                      "decimal to unsigned binary": "dtub",
                      "sign and magnitude binary to decimal": "smtd",
                      "decimal to sign and magnitude binary": "dtsm",
                      "two's complement binary to decimal": "tctd",
                      "decimal to two's complement binary": "dttc",
                      "hexadecimal to decimal": "htd",
                      "decimal to hexadecimal": "dth"}

    def get_question_type(self, type):
        if self.recommend:
            type = self.recommend_question()
        if type in self.types.keys():
            self.type = type
            self.type_acr = self.types[self.type]

    def gen_question(self):  # after question type is chosen
        if self.type_acr in UnsignedQuestion.allowed_types.keys():
            self.question = UnsignedQuestion(self.type_acr)
        elif self.type_acr in SignAndMagnitude.allowed_types.keys():
            self.question = SignAndMagnitude(self.type_acr)
        elif self.type_acr in TwosComplement.allowed_types.keys():
            self.question = TwosComplement(self.type_acr)
        elif self.type_acr in HexToDec.allowed_types.keys():
            self.question = HexToDec(self.type_acr)
        else:
            return "incorrect acronym"
        self.question.run()

    def set_answer(self, answer):
        self.question.user_answer = answer

    def update_scores(self):  # only in cli
        if self.question.check_answer():
            self.correct += 1
            return "correct"
        else:
            self.incorrect += 1
            return "incorrect"

    def define_user(self, option, name: None, username, password):
        self.user = User()
        self.user.get_details()
        if option == "sign in":
            return self.user.sign_in(username, password)
        else:
            self.user.sign_up(name, username, password)

    def update_recorded_scores(self):
        self.user.details_dict[self.user.username][self.type]["correct"].append(self.correct)
        self.user.details_dict[self.user.username][self.type]["incorrect"].append(self.incorrect)

    def calc_average_correct(self, type):
        correct_sum = 0
        incorrect_sum = 0
        for item in self.user.details_dict[self.user.username][type]["correct"]:
            correct_sum += int(item)
        for item in self.user.details_dict[self.user.username][type]["incorrect"]:
            incorrect_sum += int(item)
        try:
            percent = correct_sum / (correct_sum + incorrect_sum)
        except ZeroDivisionError:
            percent = 0.5
        return round(percent, 2)

    def recommend_question(self):
        """Recommend a question type based on the user's scores."""
        self.user.get_queue()
        print(self.user.queue.show())
        if self.user.queue.is_empty():
            for question_type in self.types:
                correct = self.calc_average_correct(question_type)
                #lowest possible % 33
                if 0 <= correct <= 0.40:
                    duplicates = 3
                elif 0.4 < correct <= 0.7:
                    duplicates = 2
                elif 0.8 < correct <= 1:
                    duplicates = 1
                for i in range(duplicates):
                    priority = random.randint(0, 100)
                    self.user.queue.enqueue((question_type, priority))
        print(self.user.queue.show())
        print(self.user.queue.show_front())
        return self.user.queue.dequeue()[0]

