import random
from abc import ABC, abstractmethod


class Question(ABC):
    """abstract base class which other question classes inherit from
    most methods have property making them virtual/abstract methods that the subclasses will overwrite
    """
    def __init__(self, type_acr):
        """
        
        Parameters
        ----------
        type_acr: acronym for the type of question wanted:eg dtub= decimal to unsigned binary
        """
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

    @abstractmethod
    def generate_question(self):
        pass

    @abstractmethod
    def generate_correct_answer(self):
        pass

    @abstractmethod
    def generate_plausible_answers(self):
        pass

    def check_answer(self):
        """
        
        Returns
        -------
        bool: is the user answer correct

        """
        return self.user_answer == self.correct_answer

    def run(self):
        """
        runs the methods needed to create a question, question phrase, answer and plausible answers
        Returns
        -------
        None
        """
        self.generate_question()
        self.generate_question_phrase()
        self.generate_correct_answer()
        self.generate_plausible_answers()


class UnsignedQuestion(Question):
    """
    subclass of Question that allows for the conversion between 8 bit unsigned binary and decimal numbers
    allowed types is a class attribute that can be called even if no instance of the class has been made and it
    describes the type the answer should be. eg: dtub = decimal(integer)--> unsigned binary(string) and vice versa 
    """
    allowed_types = {"dtub":"str", "ubtd":"int"}
    def __init__(self, type_acr):
        """
        calls parent constructor with the type acronym eg: dtub
        """
        super().__init__(type_acr)
        self.num_bits = 8

    def generate_question(self):
        """ creates a question int or string
        checks the question type.
        if decimal to unsigned binary(dtub), creates a random number between 0 and 255
        if ubtd creates a random string of 0s and 1s, 8 bits long
        Attributes:
        -----------
        self.question is updated to hold the question string or int created
        """
        bits = ""
        if self.question_type == "dtub":
            self.question = random.randint(0, 2 ** self.num_bits - 1)
        else:
            for i in range(self.num_bits):
                bits = bits + str(random.choice([0, 1]))
            self.question = bits

    def generate_question_phrase(self):
        """creates a sentence with the question str/int inside
        Attributes
        ----------
        self.question phrase holds the question sentence that has been chosen based on the question type
        """
        self.question_phrases = [f"convert this decimal number {self.question} to unsigned binary",
                                 f"convert this unsigned binary number {self.question} to decimal"]
        if isinstance(self.question, int):
            self.question_phrase = self.question_phrases[0]
        else:
            self.question_phrase = self.question_phrases[1]

    def generate_correct_answer(self):
        """ converts the question into an answer
        if question is decimal, repeatedly removes decreasing powers of two and appends them to a string of 1s and 0s
        if question is unsigned binary, adds the value of each bit to an integer variable
        Attributes
        ----------
        self.correct_answer holds the result of converting the question
        self.plausible_answers is a list holding the correct answer as 2 incorrect answers will be added

        """
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
        """ creates 2 incorrect but similar answers and appends them to the plausible answers
        plausible_answers_set is used to prevent duplicates
        if the question is decimal, a random bit in the answer is flipped to create a similar but distinct plausible answer
        if the question is an unsigned binary string, a small offset is added
        Attributes
        -------
        self.plausible_answers is now a list with 1 correct and 2 incorrect answersnd is shuffeled to change the order
         of the items

        """
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
    """ allows for conversion between a sign and magnitude and decimal numbers
    """
    allowed_types = {"smtd":"int", "dtsm":"str"}
    def __init__(self,type_acr):
        super().__init__(type_acr)  # Call the parent constructor
        self.num_bits = 8

    def generate_question(self):
        """
        if the question is decimal, it generates a decimal number from -127 to 128
        if the question is unisgned binary, it generates random 8 bit sequence
        Attributes
        ----------
        self.question now holds the 8 bit unsigned binary or an integer
        """
        bits = ""
        if self.question_type == "dtsm":
            self.question = random.randint(int(-1 * (((2 ** self.num_bits) / 2) - 1)), (2 ** self.num_bits) / 2)

        else:
            for i in range(self.num_bits):
                bits = bits + str(random.choice([0, 1]))
                self.question = bits

    def generate_question_phrase(self):
        """
        creates a sentence holding the question number
        Attributes
        ----------
        self.question_phrase holds a string with the sentence and question number

        """
        if self.question_type == "smtd":
            self.question_phrase = f"convert this sign and magnitude binary number {self.question} to decimal"
        else:
            self.question_phrase = f"convert this decimal number {self.question} to sign and magnitude binary"

    def generate_correct_answer(self):
        """ converts the question from sign and magnitude binary to decimal or vice versa
        if the question is sign and magnitude, it sums the right 7 bits values and checks if the msb is 1 or 0. accounts
         for -0
        if the question is decimal, it assigns the msb according to the sign of the number (either 1 or 0 if decimal is
        0) and then converts the absolute value of the question to binary and adds on the msb
        Attributes
        ----------
        self.correct_answer now holds the calculated string or integer
        self.plausible_answers is a list with the correct answer inside

        """
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
        """ creates 2 incorrect but similar answers and appends them to the plausible answers
        plausible_answers_set is used to prevent duplicates
        if the question is decimal, a random bit in the answer is flipped to create a similar but distinct plausible answer
        if the question is an sign and magnitude binary string, a small offset is added
        Attributes
        -------
        self.plausible_answers is now a list with 1 correct and 2 incorrect answers and is shuffeled to change the order
         of the items
        """
        plausible_answers_set = {self.correct_answer}

        if self.question_type == "dtsm":
            while len(plausible_answers_set) < 3:
                bit_index = random.randint(0, self.num_bits - 1)
                temp = list(self.correct_answer)
                temp[bit_index] = "1" if temp[bit_index] == "0" else "0"
                plausible_answer = "".join(temp)
                plausible_answers_set.add(plausible_answer)
        else:
            while len(plausible_answers_set) < 3:
                plausible_answer = 128 #out of range
                while plausible_answer < -127 or plausible_answer > 127:
                    offset = random.randint(-1 * abs(int(self.correct_answer)) // 2, abs(int(self.correct_answer)) // 2)
                    plausible_answer = int(self.correct_answer) + offset
                plausible_answers_set.add(plausible_answer)

        self.plausible_answers = list(plausible_answers_set)
        random.shuffle(self.plausible_answers)

class HexToDec(Question):
    """
    allows for hexidecimal numbers to be converted to decimal and vice versa
    """
    allowed_types = {"htd":"int", "dth":"str"}
    def __init__(self,type_acr):
        super().__init__(type_acr)  # Call the parent constructor
        self.type = type_acr
        self.num_bits = 8
        self.num_hex_chars = self.num_bits / 4
        self.chars = {'0': 0, '1': 1, '2': 2, '3': 3,
                      '4': 4, '5': 5, '6': 6, '7': 7,
                      '8': 8, '9': 9, 'A': 10, 'B': 11,
                      'C': 12, 'D': 13, 'E': 14, 'F': 15}
        self.key_list = list(self.chars.keys())
        self.val_list = list(self.chars.values())

    def generate_question(self):
        """
        if the question is hexidecimal,2 random choices from the keys list of all the hex characters: 0-F
        if the question is decimal, random number from 0-128 is calculated
        Attributes
        -------
        self.question holds the new question string or int that was calculated
        """
        digits = ""
        if self.type == "htd":
            for i in range(int(self.num_hex_chars)):
                digits += random.choice(self.key_list)
        else:
            digits = random.randint(0, 2 ** self.num_bits - 1)
        self.question = digits

    def generate_question_phrase(self):
        """
        creates a sentence holding the question number
        Attributes
        ----------
        self.question_phrase holds a string with the sentence and question number

        """
        if self.type == "htd":
            self.question_phrase = f"convert this hexidecimal number {self.question} to decimal"
        else:
            self.question_phrase = f"convert this decimal number {self.question} to hexidecimal"

    def generate_correct_answer(self):
        """ converts the question from hexidecimal to decimal or vice versa
        if the question is hex, it multiplies each digit by its respective power of 16 and adds it to a total.
        if the question is decimal, if 0, the answer is "00" otherwise, the
        Attributes
        ----------
        self.correct_answer now holds the calculated string or integer
        self.plausible_answers is a list with the correct answer inside

        """
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
            hexadecimal = ""
            decimal = int(self.question)
            if decimal == 0:
                hexadecimal = "00"
            while decimal > 0:
                remainder = decimal % 16
                hexadecimal = str(self.key_list[remainder]) + hexadecimal
                decimal //= 16
            self.correct_answer = hexadecimal

        self.plausible_answers.append(self.correct_answer)

    def generate_plausible_answers(self):
        """ creates 2 incorrect but similar answers and appends them to the plausible answers
        plausible_answers_set is used to prevent duplicates
        if the question is decimal, one of the chars in the hex is replaced
        if the question is a hex, an offset is added to the decjmal
        Attributes
        -------
        self.plausible_answers is now a list with 1 correct and 2 incorrect answers and is shuffeled to change the order
         of the items
        """
        plausible_answers_set = {self.correct_answer}#prevent duplicates

        if self.question_type == "dth":
            while len(plausible_answers_set) < 3:
                temp = self.correct_answer
                if len(temp) < 2:
                    raise ValueError("temp must have at least two characters")
                i = random.randint(0, len(temp) - 1)
                temp = temp.replace(temp[i], random.choice(self.key_list))
                plausible_answers_set.add(temp)

        else:
            while len(plausible_answers_set) < 3:
                plausible_answer = 256#out of range of two digit hex
                while plausible_answer < 0 or plausible_answer > 255:
                    offset = random.randint(-1 * int(self.correct_answer) // 2, int(self.correct_answer) // 2)
                    plausible_answer = int(self.correct_answer) + offset
                plausible_answers_set.add(plausible_answer)

        self.plausible_answers = list(plausible_answers_set)
        random.shuffle(self.plausible_answers)