from getpass import getpass  # when using getpass you must edit the configurations to emulate terminal in output console
import bcrypt


class User:
    def __init__(self):
        self.name = ""
        self.username = ""
        self.password = ""
        self.hashed_password = ""
        self.details = {
            "lolly123": {"password": "asdf",
                         "unsigned_high_score": 5,
                         },
            "john123": {"password": "qwerty",
                        "unsigned_high_score": 5,
                        }
        }

    def get_username_password(self):
        self.username = input("username: ")
        self.password = getpass("password(hidden whilst typing): ")

    def hash_password(self, password):
        string = password.encode('utf-8')
        salt = bcrypt.gensalt()
        self.hashed_password = bcrypt.hashpw(string, salt)

    def check_password(self):
        return self.hashed_password == self.hash_password(self.details[self.username]["password"])

    def save_details(self):
        self.details.update({self.username})

    def sign_in(self):
        while not self.check_password():
            self.get_username_password()
            self.hash_password(self.password)
        return "successful sign-in"

    def sign_up(self):
        self.name = input("name: ")
        self.get_username_password()
        self.hash_password(self.password)
        self.save_details()
        return "details saved, signed up"
