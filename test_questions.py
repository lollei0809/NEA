import pytest
from questions import UnsignedQuestion


class TestUnsignedQuestion:
    @pytest.fixture
    def unsigned_question(self):
        test_question = UnsignedQuestion()
        test_question.generate_question_type()
        test_question.generate_question()
        test_question.generate_correct_answer()
        test_question.generate_plausible_answers()
        return test_question

    def test_UQ_setup(self, unsigned_question):
        assert unsigned_question.num_bits == 8

    def test_generate_question_type(self, unsigned_question):
        types = [f"convert this denery number {self.question} to unsigned binary",
                 f"convert this unsigned binary number {self.question} to denery"]
        assert unsigned_question.question_type in types

    def test_question(self, unsigned_question):
        if unsigned_question.question_type == type[0]:
            assert unsigned_question.question >= 0 and unsigned_question.question <= 255
        if unsigned_question.question_type == type[1]:
            assert True
