from main_code.user import User
import pytest

details_file = "test_details.json"

@pytest.fixture
def user():
    """thjis fixture creates a new user before each test."""
    u = User()
    u.details_dict = {}
    return u


def test_signup(user):
    """puts the user in the details dict with the correct username etc"""
    user.sign_up("John Doe", "john123", "password123")
    assert "john123" in user.details_dict
    assert user.details_dict["john123"]["name"] == "John Doe"
    assert user.signed_in is True


def test_password_hashing(user):
    """Test password hashing and checking"""
    password = "password123"
    user.sign_up("Alice", "alice123", password)
    assert user.check_password("alice123", password) is True


def test_signin_correct(user):
    """tests signing in with correct username and password works"""
    user.sign_up("John Doe", "johnd", "password123")
    assert user.sign_in("johnd", "password123") is True


def test_signin_incorrect(user):
    """tests signing in with wrong usermane/password doesnt work """
    user.sign_up("John Doe", "johnd", "password123")
    assert user.sign_in("johnd", "wrongpass") is False
    assert user.sign_in("wronguser", "password123") is False


def test_signout(user):
    """tests signing out."""
    user.sign_up("John Doe", "johnd", "password123")
    assert user.name == "John Doe"
    user.sign_out()
    assert user.signed_in is False
    assert user.name == ""



def test_check_signed_in(user):
    """tests checking if a user is signed in."""
    user.sign_up("John Doe", "johnd", "password123")
    assert user.check_signed_in() is True
    user.sign_out()
    assert user.check_signed_in() is False


def test_save_and_load_details(user):
    """tests saving and loading details from the json file"""
    user.sign_up("John Doe", "john123", "password123")
    user.save_details_dict_to_json()

    new_user = User()
    new_user.get_details()
    assert "john123" in new_user.details_dict
    assert new_user.details_dict["john123"]["name"] == "John Doe"


def test_find_high_score():
    """tests finding the highest score in a game type with multiple scores"""
    user = User()
    user.sign_up("lolly","ll","asdf")
    assert user.find_high_score("unsigned binary to decimal") == 0
    user.details_dict["ll"]["unsigned binary to decimal"]["correct"] = [1,5,7,2,6,11,3,9,]
    assert user.find_high_score("unsigned binary to decimal")==11

