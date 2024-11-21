import bcrypt
from json_data_store import details

class User:
    def __init__(self):
        self.name = ""
        self.username = ""
        self.password = ""
        self.details = details

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
        return bcrypt.checkpw(string, self.details[self.username]["hashed_password"])

    def save_details(self):
        self.details[self.username] = {
            "name": self.name,
            "hashed_password": self.hash_password(self.password),
            "signed_in": True
        }

    def sign_in(self):
        self.get_username()
        while self.username not in self.details.keys():
            print("username incorrect")
            self.get_username()
        self.get_password()
        while not self.check_password():
            print("password incorrect")
            self.get_password()
        self.details[self.username]["signed_in"] = True
        print("username and password found. Successful sign-in")



    def sign_out(self):
        if self.username == "":
            print("not signed in")
        else:
            self.details[self.username]["signed_in"] = False

    def check_signed_in(self):
        if self.username in self.details.keys:
            return self.details[self.username]["signed_in"]
        else:
            return False

    def sign_up(self):
        self.name = input("name: ")
        self.get_username()
        self.get_password()
        self.save_details()
        print("details saved, signed up")
