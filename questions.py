import random
from abc import ABC, abstractmethod


class Question(ABC):  # abstract base class which other question objects inherit from
    def __init__(self):
        self.plausible_answers = []
        self.correct_answer = ""
        self.user_answer = ""
        self.question = ""
        self.wrongly_answered = 0
        self.question_phrase = ""
        self.question_phrases = []
        self.question_type = ""

    @abstractmethod
    def generate_question_phrase(self):
        pass

    @abstractmethod  # property making virtual/abstract method that subclasses will overwrite
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


class UnsignedQuestion(Question):
    def __init__(self):
        super().__init__()  # Call the parent constructor
        self.num_bits = 8
        self.types = ["dtb", "btd"]

    def generate_question(self):
        bits = ""
        self.question_type = random.choice(self.types)  # decimal to binary or binary to decimal
        if self.question_type == "dtb":
            self.question = random.randint(0, 2 ** self.num_bits - 1)
        else:
            for i in range(self.num_bits):
                bits = bits + str(random.choice([0, 1]))
            self.question = bits

    def generate_question_phrase(self):
        self.question_phrases = [f"convert this decimal number {self.question} to unsigned binary",
                                 f"convert this unsigned binary number {self.question} to decimal"]
        if isinstance(self.question, int):
            self.question_phrase = self.question_phrases[0]
        else:
            self.question_phrase = self.question_phrases[1]

    def generate_correct_answer(self):
        self.correct_answer = ""
        if self.question_type == "dtb":
            j = 2 ** (self.num_bits - 1)
            total = ""
            temp = int(self.question)
            for i in range(self.num_bits):
                if temp >= j:
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
                total += j * int(self.question[-(i + 1)])
                j *= 2
            self.correct_answer = total
        self.plausible_answers.append(self.correct_answer)

    def generate_plausible_answers(self):
        if self.question_type == "dtb":
            bit_index = -1
            for i in range(2):
                exclude = [bit_index]
                while True:
                    bit_index = random.randint(0, self.num_bits - 1)
                    if bit_index not in exclude:  # excludes the number that has already been used so plausible answers
                        # doesnt have duplicates
                        break
                temp = list(self.correct_answer)  # passing mutable objects calls by reference?
                if temp[bit_index] == "0":
                    temp[bit_index] = "1"
                else:
                    temp[bit_index] = "0"
                t = "".join(temp)
                self.plausible_answers.append(t)
        else:
            num = 0
            for i in range(2):
                exclude = [num] # excludes the correct answer and the answer added in the first loop
                while True:
                    num = random.randint(-1 * int(self.correct_answer) // 2,
                                         int(self.correct_answer) // 2)  # floor division
                    # by 2 so the number isn't too far off so less easy to rule out answers
                    if num not in exclude:
                        break
                temp = int(self.correct_answer) + num
                self.plausible_answers.append(temp)
        random.shuffle(self.plausible_answers)

    def __str__(self):
        return f'UnsignedQuestion(question={self.question}, answer={self.correct_answer})'

class SignAndMagnitude(Question):
    def __init__(self):
        super().__init__()  # Call the parent constructor
        self.types = ["smtd,dtsm"]
        self.num_bits = 8

    def generate_question(self):
        bits = ""
        self.question_type = random.choice(self.types)
        if self.question_type == "smtd":
            self.question = random.randint(int(-1 * (((2 ** self.num_bits) / 2) - 1)), (2 ** self.num_bits) / 2)
            # ^ generates decimal numbers eg. for 8 bits, -127 to 128
        else:
            for i in range(self.num_bits):
                bits = bits + str(random.choice([0, 1]))
                self.question = bits

    def generate_question_phrase(self):
        if self.question_type == "smtd":
            self.question_phrase = f"convert this sign and magnitude binary number{self.question} to decimal"
        else:
            self.question_phrase = f"convert this decimal number{self.question} to sign and magnitude binary"

    def generate_correct_answer(self):
        self.correct_answer = ""
        if self.question_type == "smtd":
            j = 1
            total = 0
            for i in range(self.num_bits - 1):
                total += j * int(self.question[-(i + 1)])
                j *= 2
            msb = self.question[0]
            if msb == "0":
                self.correct_answer = total
            else:
                if self.question == "10000000":
                    self.correct_answer = 0
                else:
                    self.correct_answer = -total
            self.plausible_answers.append(self.correct_answer)

        else:
            if self.question == 0:
                msb = random.choice(["0", "1"])  # there can be -ve or +ve 0 in sign and magnitude
            elif self.question > 0:
                msb = "0"
            else:
                msb = "1"
            j = 2 ** (self.num_bits - 2)
            total = msb
            temp = abs(int(self.question))
            for i in range(self.num_bits - 1):
                if temp >= j:
                    total += "1"
                    temp -= j
                else:
                    total += "0"
                j /= 2
            self.correct_answer = total

    def generate_plausible_answers(self):
        if self.question_type == "dtsm":
            bit_index = -1
            for i in range(2):
                exclude = [bit_index]
                while True:
                    bit_index = random.randint(0, self.num_bits - 1)
                    if bit_index not in exclude:  # excludes the number that has already been used so plausible answers
                        # doesnt have duplicates
                        break
                temp = list(self.correct_answer)  # passing mutable objects calls by reference?
                if temp[bit_index] == "0":
                    temp[bit_index] = "1"
                else:
                    temp[bit_index] = "0"
                t = "".join(temp)
                self.plausible_answers.append(t)
        else:
            num = 0
            for i in range(2):
                exclude = [num]
                while True:
                    num = random.randint(-(2**self.num_bits), (self.num_bits))
                    if num not in exclude:
                        break
                temp = int(self.correct_answer) + num
                self.plausible_answers.append(temp)
        random.shuffle(self.plausible_answers)



class HexToDec(Question):  # hexidecimal to binary
    def __init__(self):
        super().__init__()  # Call the parent constructor
        self.types = ["htd,dth"]
        self.type = ""
        self.num_bits = 8
        self.num_hex_chars = self.num_bits/4
        self.question_phrase = ""
        self.chars = {  '0': 0, '1': 1, '2': 2, '3': 3,
                        '4': 4, '5': 5, '6': 6, '7': 7,
                        '8': 8, '9': 9, 'A': 10, 'B': 11,
                        'C': 12, 'D': 13, 'E': 14, 'F': 15}

    def generate_question(self):
        bits = ""
        self.type = random.choice(self.types)
        if self.type == "htd":
            for i in range(int(self.num_hex_chars)):
                bits = bits + random.choice(self.chars)
        else:
            bits = random.randint(0, 2 ** self.num_bits - 1)
        self.question = bits

    def generate_question_phrase(self):
        if self.type == "htb":
            self.question_phrase = f"convert this hexidecimal number{self.question} to unsigned binary"
        else:
            self.question_phrase = f"convert this unsigned binary number{self.question} to hexidecimal"

    def generate_correct_answer(self):
        key_list = list(self.chars.keys())
        val_list = list(self.chars.values())
        self.correct_answer = ""
        if self.type == "htd":
            j = 1
            decimal = 0
            for i in range(int(self.num_hex_chars)):
                char = self.question[-(i + 1)]
                position = key_list.index(char)
                val = val_list[position]
                decimal += j * val
                j *= 16
            self.correct_answer = decimal
        else:
            j = 16 ** (self.num_hex_chars - 1)
            hexadecimal = ""
            decimal = int(self.question)
            #################################

            self.correct_answer = hexadecimal

        self.plausible_answers.append(self.correct_answer)

    def generate_plausible_answers(self):
        pass



