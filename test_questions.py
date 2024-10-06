import pytest
from questions import UnsignedQuestion


class TestUnsignedQuestion:
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
        types = ["dtb","btd"]
        assert unsigned_question.question_type in types


    def test_question(self, unsigned_question):
        if unsigned_question.question_type == type[0]:
            assert unsigned_question.question >= 0 and unsigned_question <= 255
        if unsigned_question.question_type == type[1]:
            assert True

    def test_correct_answer(self, unsigned_question):
        assert True


    def test_plausible_answers(self, unsigned_question):
        assert True

