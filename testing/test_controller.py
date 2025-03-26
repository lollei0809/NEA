import pytest
from main_code.controller import ControlGame
from main_code.user import User
from main_code.questions import UnsignedQuestion, SignAndMagnitude, HexToDec, TwosComplement


def test_get_question_type():
    """test if ControlGame method correctly sets question type"""
    controller = ControlGame()
    controller.get_question_type("decimal to hexadecimal")
    assert controller.type == "decimal to hexadecimal"
    assert controller.type_acr == "dth"

    controller.get_question_type("invalid type")  # Shouldnt change type
    assert controller.type == "decimal to hexadecimal"
    assert controller.type_acr == "dth"


def test_gen_question():
    """test if ControlGame() generates correct question objects"""
    controller = ControlGame()
    controller.get_question_type("decimal to unsigned binary")
    controller.gen_question()
    assert isinstance(controller.question, UnsignedQuestion)

    controller.get_question_type("decimal to sign and magnitude binary")
    controller.gen_question()
    assert isinstance(controller.question, SignAndMagnitude)

    controller.get_question_type("decimal to two's complement binary")
    controller.gen_question()
    assert isinstance(controller.question, TwosComplement)

    controller.get_question_type("decimal to hexadecimal")
    controller.gen_question()
    assert isinstance(controller.question, HexToDec)


def test_set_answer():
    """Test if user answer is set correctly."""
    controller = ControlGame()
    controller.get_question_type("decimal to unsigned binary")
    controller.gen_question()
    controller.set_answer("10101010")
    assert controller.question.user_answer == "10101010"


def test_update_scores():
    """Test if ControlGame updates scores correctly."""
    controller = ControlGame()
    controller.get_question_type("decimal to unsigned binary")
    controller.gen_question()
    controller.question.correct_answer = "10101010"
    controller.set_answer("10101010")
    result = controller.update_scores()
    assert result == "correct"
    assert controller.correct == 1

    controller.set_answer("00000000")
    result = controller.update_scores()
    assert result == "incorrect"
    assert controller.incorrect == 1


def test_calc_average_correct():
    """Test if average correct calculation is accurate."""
    controller = ControlGame()
    controller.user = User()
    controller.user.username = "username"
    controller.user.details_dict = {"username": {
        "name": "name",
        "hashed_password": "password",
        "signed_in": True,
        "unsigned binary to decimal": {"correct": [], "incorrect": []},
        "decimal to unsigned binary": {"correct": [1], "incorrect": [1]},
        "sign and magnitude binary to decimal": {"correct": [0], "incorrect": [0]},
        "decimal to sign and magnitude binary": {"correct": [], "incorrect": []},
        "two's complement binary to decimal": {"correct": [], "incorrect": []},
        "decimal to two's complement binary": {"correct": [], "incorrect": []},
        "hexadecimal to decimal": {"correct": [], "incorrect": []},
        "decimal to hexadecimal": {"correct": [3, 5], "incorrect": [2, 3]}
    }}
    assert controller.calc_average_correct("unsigned binary to decimal") == 0.5
    assert controller.calc_average_correct("decimal to unsigned binary") == 0.5
    assert controller.calc_average_correct("sign and magnitude binary to decimal") == 0.5
    assert controller.calc_average_correct("decimal to hexadecimal") == 0.62




def test_recommend_question():
    controller = ControlGame()
    controller.user = User()
    controller.user.username = "username"

    controller.user.details_dict = {"username": {
        "name": "name",
        "hashed_password": "password",
        "signed_in": True,
        "question_queue": [],
        "unsigned binary to decimal": {"correct": [], "incorrect": []},
        "decimal to unsigned binary": {"correct": [], "incorrect": []},
        "sign and magnitude binary to decimal": {"correct": [], "incorrect": []},
        "decimal to sign and magnitude binary": {"correct": [], "incorrect": []},
        "two's complement binary to decimal": {"correct": [], "incorrect": []},
        "decimal to two's complement binary": {"correct": [], "incorrect": []},
        "hexadecimal to decimal": {"correct": [], "incorrect": []},
        "decimal to hexadecimal": {"correct": [], "incorrect": []}
    }}
    controller.recommend_question()
    assert controller.user.queue.size() == (8 * 3) - 1

    controller.user.details_dict = {"username": {
        "name": "name",
        "hashed_password": "password",
        "signed_in": True,
        "question_queue": [],
        "unsigned binary to decimal": {"correct": [99], "incorrect": [1]},
        "decimal to unsigned binary": {"correct": [99], "incorrect": [1]},
        "sign and magnitude binary to decimal": {"correct": [99], "incorrect": [1]},
        "decimal to sign and magnitude binary": {"correct": [99], "incorrect": [1]},
        "two's complement binary to decimal": {"correct": [99], "incorrect": [1]},
        "decimal to two's complement binary": {"correct": [99], "incorrect": [1]},
        "hexadecimal to decimal": {"correct": [99], "incorrect": [1]},
        "decimal to hexadecimal": {"correct": [99], "incorrect": [1]}
    }}
    controller.recommend_question()
    assert controller.user.queue.size() == (8 * 1) - 1

    controller.user.details_dict = {"username": {
        "name": "name",
        "hashed_password": "password",
        "signed_in": True,
        "question_queue": [],
        "unsigned binary to decimal": {"correct": [0], "incorrect": [0]},  # 3
        "decimal to unsigned binary": {"correct": [20], "incorrect": [80]},  # 5
        "sign and magnitude binary to decimal": {"correct": [40], "incorrect": [60]},  # 4
        "decimal to sign and magnitude binary": {"correct": [60], "incorrect": [40]},  # 3
        "two's complement binary to decimal": {"correct": [80], "incorrect": [20]},  # 2
        "decimal to two's complement binary": {"correct": [], "incorrect": []},  # 3
        "hexadecimal to decimal": {"correct": [], "incorrect": []},
        "decimal to hexadecimal": {"correct": [], "incorrect": []}
    }}
    controller.recommend_question()
    assert controller.user.queue.size() == 25
