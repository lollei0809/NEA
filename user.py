from getpass import getpass  # when using getpass you must edit the configurations to emulate terminal in output console
import bcrypt
import json_data_store
details = {  # will be converted to json
    "jane123": {"name": "Jane Doe",
                "hashed_password": b'$2b$12$Rg1AfE9GqoGU5fs6biZmf.IWf188pRLVFr40tKqGXwIJzTrIoM1GW',#asdf
                "signed_in": False,
                "unsigned_high_score": 5,
                },
            }
class User:
    def __init__(self):
        self.name = ""
        self.username = ""
        self.password = ""


    def get_username_password(self):
        self.username = input("username: ")
        self.password = getpass("password(hidden whilst typing): ")

    def hash_password(self, password):
        string = password.encode('utf-8')#converts password to byte string eg b"{password}"
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(string, salt)

    def check_password(self):
        return bcrypt.checkpw(self.password.encode('utf-8'), details[self.username]["hashed_password"])

    def save_details(self):
        details[self.username] = {
            "name": self.name,
            "hashed_password": self.hash_password(self.password),
            "signed_in": True
        }

    def sign_in(self):
        self.get_username_password()
        while not self.check_password():
            print("username or password incorrect")
            self.get_username_password()
        details[self.username]["signed_in"] = True
        print("username and password found. Successful sign-in")

    def sign_out(self):
        details[self.username]["signed_in"] = False
    def check_signed_in(self):
        return details[self.username]["signed_in"]
    def sign_up(self):
        self.name = input("name: ")
        self.get_username_password()
        self.save_details()
        print("details saved, signed up")

