import random
from abc import ABC, abstractmethod


class Question(ABC):  # abstract base class which other question objects inherit from
    def __init__(self, type_acr):
        self.plausible_answers = []
        self.correct_answer = ""
        self.user_answer = ""
        self.question = ""
        self.question_phrase = ""
        self.question_phrases = []
        self.question_type = type_acr

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

    def check_answer(self):
        return self.user_answer == self.correct_answer

    def run(self):
        self.generate_question()
        self.generate_question_phrase()
        self.generate_correct_answer()
        self.generate_plausible_answers()


class UnsignedQuestion(Question):
    allowed_types = {"dtub":"str", "ubtd":"int"}#class attribute can be called even if no instance of the class
    #type for the answer

    def __init__(self, type_acr):
        super().__init__(type_acr)  # Call the parent constructor
        self.num_bits = 8
        # self.allowed_types = ["dtub", "ubtd"]

    def generate_question(self):
        bits = ""
        if self.question_type == "dtub":
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
        if self.question_type == "dtub":
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
        plausible_answers_set = {self.correct_answer}#prevent duplicates

        if self.question_type == "dtub":#flips a random bit in the binary
            while len(plausible_answers_set) < 3:
                bit_index = random.randint(0, self.num_bits - 1)
                temp = list(self.correct_answer)
                temp[bit_index] = "1" if temp[bit_index] == "0" else "0"
                plausible_answer = "".join(temp)
                plausible_answers_set.add(plausible_answer)#will ignore if it is a duplicate
        else:
            while len(plausible_answers_set) < 3:
                plausible_answer = 256#out of range
                while plausible_answer < 0 or plausible_answer > 255:
                    offset = random.randint(-1 * int(self.correct_answer) // 2, int(self.correct_answer) // 2)
                    plausible_answer = int(self.correct_answer) + offset
                plausible_answers_set.add(plausible_answer)

        self.plausible_answers = list(plausible_answers_set)
        random.shuffle(self.plausible_answers)


class SignAndMagnitude(Question):
    allowed_types = {"smtd":"int", "dtsm":"str"}
    def __init__(self,type_acr):
        super().__init__(type_acr)  # Call the parent constructor
        self.num_bits = 8

    def generate_question(self):
        bits = ""
        if self.question_type == "dtsm":
            self.question = random.randint(int(-1 * (((2 ** self.num_bits) / 2) - 1)), (2 ** self.num_bits) / 2)
            # ^ generates decimal numbers eg. for 8 bits, -127 to 128
        else:
            for i in range(self.num_bits):
                bits = bits + str(random.choice([0, 1]))
                self.question = bits

    def generate_question_phrase(self):
        if self.question_type == "smtd":
            self.question_phrase = f"convert this sign and magnitude binary number {self.question} to decimal"
        else:
            self.question_phrase = f"convert this decimal number {self.question} to sign and magnitude binary"

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

        else:
            if self.question == 0:
                msb = random.choice(["0", "1"])  # there can be -ve or +ve 0 in sign and magnitude
            elif int(self.question) > 0:
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
        self.plausible_answers.append(self.correct_answer)

    def generate_plausible_answers(self):
        plausible_answers_set = {self.correct_answer} #prevent duplicates

        if self.question_type == "dtsm": #flips a random bit in the binary
            while len(plausible_answers_set) < 3:
                bit_index = random.randint(0, self.num_bits - 1)
                temp = list(self.correct_answer)
                temp[bit_index] = "1" if temp[bit_index] == "0" else "0"
                plausible_answer = "".join(temp)
                plausible_answers_set.add(plausible_answer)#will ignore if it is a duplicate
        else:#
            while len(plausible_answers_set) < 3:
                plausible_answer = 128 #out of range
                while plausible_answer < -127 or plausible_answer > 127:
                    offset = random.randint(-1 * abs(int(self.correct_answer)) // 2, abs(int(self.correct_answer)) // 2)
                    plausible_answer = int(self.correct_answer) + offset
                plausible_answers_set.add(plausible_answer)

        self.plausible_answers = list(plausible_answers_set)
        random.shuffle(self.plausible_answers)

class HexToDec(Question):  # hexidecimal to binary
    allowed_types = {"htd":"int", "dth":"str"}
    def __init__(self,type_acr):
        super().__init__(type_acr)  # Call the parent constructor
        self.type = ""
        self.num_bits = 8
        self.num_hex_chars = self.num_bits / 4
        self.chars = {'0': 0, '1': 1, '2': 2, '3': 3,
                      '4': 4, '5': 5, '6': 6, '7': 7,
                      '8': 8, '9': 9, 'A': 10, 'B': 11,
                      'C': 12, 'D': 13, 'E': 14, 'F': 15}
        self.key_list = list(self.chars.keys())
        self.val_list = list(self.chars.values())

    def generate_question(self):
        digits = ""
        if self.type == "htd":
            for i in range(int(self.num_hex_chars)):
                digits = digits + random.choice(self.key_list)
        else:
            digits = random.randint(0, 2 ** self.num_bits - 1)
        self.question = digits

    def generate_question_phrase(self):
        if self.type == "htd":
            self.question_phrase = f"convert this hexidecimal number {self.question} to decimal"
        else:
            self.question_phrase = f"convert this decimal number {self.question} to hexidecimal"

    def generate_correct_answer(self):

        self.correct_answer = ""
        if self.type == "htd":
            j = 1
            decimal = 0
            for i in range(int(self.num_hex_chars)):
                char = self.question[-(i + 1)]
                position = self.key_list.index(char)
                val = self.val_list[position]
                decimal += j * val
                j *= 16
            self.correct_answer = decimal
        else:
            j = 16 ** (self.num_hex_chars - 1)
            hexadecimal = ""
            decimal = int(self.question)
            while decimal > 0:
                remainder = decimal % 16
                hexadecimal = str(self.key_list[remainder]) + hexadecimal
                decimal //= 16
                j /= 16
            self.correct_answer = hexadecimal

        self.plausible_answers.append(int(self.correct_answer))

    def generate_plausible_answers(self):
        plausible_answers_set = {self.correct_answer}#prevent duplicates

        if self.question_type == "dth":
            while len(plausible_answers_set) < 3:
                hexdigits = ""
                for i in range(int(self.num_hex_chars)):
                    hexdigits += random.choice(self.key_list)
                plausible_answers_set.add(str(hexdigits))
        else:
            while len(plausible_answers_set) < 3:
                plausible_answer = 256#out of range of two digit hex
                while plausible_answer < 0 or plausible_answer > 255:
                    offset = random.randint(-1 * int(self.correct_answer) // 2, int(self.correct_answer) // 2)
                    plausible_answer = int(self.correct_answer) + offset
                plausible_answers_set.add(plausible_answer)

        self.plausible_answers = list(plausible_answers_set)
        random.shuffle(self.plausible_answers)