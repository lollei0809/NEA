import pytest
from questions import UnsignedQuestion
import random

class TestUnsignedQuestion:
    @pytest.fixture
    def unsigned_question(self):
        random.seed(12345678)
        test_question = UnsignedQuestion()
        test_question.generate_question()
        test_question.generate_question_phrase()
        test_question.generate_correct_answer()
        test_question.generate_plausible_answers()
        return test_question

    def test_UQ_setup(self, unsigned_question): #to check any changes to the functions don't affect the questions
                                                # and answers that have been generated by the origional algorithms
                                                #separate into different test functions
        print(unsigned_question)
        random.seed(12345678)
        assert unsigned_question.correct_answer == '01110101'
        assert unsigned_question.num_bits == 8
        assert unsigned_question.question == 117
        assert unsigned_question.question_phrase == "convert this decimal number 117 to unsigned binary"
        assert unsigned_question.question_type == "dtb"

        #check algorithms are generating correct answers


"""
    def test_UQ


    def test_correct_answer(self, unsigned_question):
        if unsigned_question.question_type == type[1]:
            assert unsigned_question.question >= 0 and unsigned_question <= 255
        if unsigned_question.question_type == type[0]:
            assert len(unsigned_question.question) == 8
            for i in range(unsigned_question.num_bits):
                assert unsigned_question.question[i] in ["0","1"]

    def test_plausible_answers(self, unsigned_question):
        assert len(unsigned_question.plausible_answers) == 3
        assert unsigned_question.plausible_answers #check for duplicates
"""
#boundry case and wrong cases
#concrete examples