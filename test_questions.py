import pytest
from questions import UnsignedQuestion
import random

class TestUnsignedQuestion:
    @pytest.fixture
    random.seed(12345678)  # first time you generate numbers they are repeated when you reset the seed.

    @pytest.fixture
    def unsigned_question(self):
        test_question = UnsignedQuestion()
        test_question.generate_question()
        test_question.generate_question_phrase()
        test_question.generate_correct_answer()
        test_question.generate_plausible_answers()
        return test_question

    def test_UQ_setup(self, unsigned_question):
        assert unsigned_question.num_bits == 8

    def test_question_type(self, unsigned_question):
        types = ["dtb", "btd"]
        assert unsigned_question.question_type in types

    def test_question(self, unsigned_question):
        if unsigned_question.question_type == type[0]:
            assert unsigned_question.question >= 0 and unsigned_question <= 255
        if unsigned_question.question_type == type[1]:
            assert len(unsigned_question.question) == 8
            for i in range(unsigned_question.num_bits):
                assert unsigned_question.question[i] in ["0","1"]


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


#boundry case and wrong cases
#concrete examples