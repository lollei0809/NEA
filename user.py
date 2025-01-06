import bcrypt
import json


class User:
    def __init__(self):
        self.signed_in = None
        self.name = ""
        self.username = ""
        self.password = ""
        self.details_dict = {}

    def get_details(self):
        with open("details.json", mode="r", encoding="utf-8") as read_file:
            self.details_dict = json.load(read_file)

    def get_username(self):
        self.username = input("username: ")

    def get_password(self):
        self.password = input("password: ")

    def hash_password(self, password):
        string = password.encode('utf-8')  # converts password to byte string eg b"{password}"
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(string, salt)

    def check_password(self):
        string = self.password.encode('utf-8')
        return bcrypt.checkpw(string, self.details_dict[self.username]["hashed_password"].encode('utf-8'))

    def save_details_dict_to_json(self):
        with open("details.json", mode="w", encoding="utf-8") as write_file:
            json.dump(self.details_dict, write_file, indent=4)




    def sign_in(self):
        self.get_username()
        while self.username not in self.details_dict.keys():
            print("username incorrect")
            self.get_username()
        self.get_password()
        while not self.check_password():
            print("password incorrect")
            self.get_password()
        self.details_dict[self.username]["signed_in"] = True
        self.name = self.details_dict[self.username]["name"]
        print("username and password found. Successful sign-in")
        self.signed_in = True

    def sign_out(self):
        if self.username == "":
            print("not signed in")
        else:
            self.details_dict[self.username]["signed_in"] = False
        self.name = ""
        self.username = ""
        self.password = ""
        self.signed_in = False

    def check_signed_in(self):
        if self.username in self.details_dict.keys():
            return self.details_dict[self.username]["signed_in"]
        else:
            return False

    def sign_up(self):
        self.signed_in = True
        self.details_dict[self.username] = {
            "name": self.name,
            "hashed_password": self.hash_password(self.password).decode("utf-8"),
            "signed_in": True,
            "unsigned binary to decimal": {"correct": [0], "incorrect": [0]},
            "decimal to unsigned binary": {"correct": [0], "incorrect": [0]},
            "sign and magnitude binary to decimal": {"correct": [0], "incorrect": [0]},
            "decimal to sign and magnitude binary": {"correct": [0], "incorrect": [0]},
            "hexadecimal to decimal": {"correct": [0], "incorrect": [0]},
            "decimal to hexadecimal": {"correct": [0], "incorrect": [0]}
        }

