import random
from abc import ABC, abstractmethod


class Question(ABC):  # abstract base class which other question objects inherit from
    def __init__(self):
        self.plausible_answers = ["", "", ""]
        self.correct_answer = ""
        self.user_answer = ""
        self.question = ""
        self.wrongly_answered = 0
        self.question_type = ""

    @abstractmethod
    def generate_question_type(self):
        pass

    @abstractmethod  # protpery making virtual/abstract method that subclasses will overwrite
    def generate_question(self):
        pass

    @abstractmethod
    def generate_correct_answer(self):
        pass

    @abstractmethod
    def generate_plausible_answers(self):
        pass

    def enter_user_answer(self, answer):
        self.user_answer = answer

    def check_answer(self):
        return self.user_answer == self.correct_answer

    def update_wrongs(self):
        self.wrongly_answered += 1


class Unsigned_question(Question):
    def __init__(self):
        self.types = []
        self.num_bits = 8

    def generate_question_type(self):
        self.types = [f"convert this denery number {self.question} to unsigned binary",
                      f"convert this unsigned binary number {self.question} to denery"]
        self.question_type = random.choice(self.types)

    def generate_question(self):
        bits = ""
        if self.question_type == self.types[0]:
            self.question = random.randint(0, 2**self.num_bits-1)
        else:
            for i in range(self.num_bits):
                bits = bits + (random.choice([0, 1]))
            self.question = bits

    def generate_correct_answer(self):
        if self.question_type == self.question_type[1]:
            j = 2**self.num_bits
            total = ""
            temp = int(self.question)
            for i in range(self.num_bits):
                if temp > j:
                    total += "1"
                    temp -= j
                else:
                    total += "0"
                j /= 2
            self.correct_answer = total

        else:
            j = 1
            total = 0
            for i in range(self.num_bits):
                total += j * int(self.question [-(i + 1)])
                j *= 2
            self.correct_answer = str(total)
        self.plausible_answers.append(self.correct_answer)

    def generate_plausible_answers(self):
        if self.question_type == self.question_type[1]:
            for i in range(2):
                bit_index = random.randint(0,self.num_bits-1)
                temp = self.correct_answer                 #passing mutable objects calls by reference?
                if temp[bit_index] == 0:
                    temp[bit_index] = 1
                else:
                    temp[bit_index] = 0
                self.plausible_answers.append(temp)
        else:
            for i in range(2):
                num = random.randint(-1*int(self.correct_answer),int(self.correct_answer))
                temp = self.correct_answer+num
                self.plausible_answers.append(temp)
        random.shuffle(self.plausible_answers)

if __name__ == "__main__":  # importing this module wont run the code
    question = Unsigned_question()
    question.generate_question_type()
    question.generate_question()
    question.generate_correct_answer()
    question.generate_plausible_answers()
