from getpass import getpass  # when using getpass you must edit the configurations to emulate terminal in output console
import bcrypt
from game import GamePlay
import json_data_store
class User:
    def __init__(self):
        self.name = ""
        self.username = ""
        self.password = ""
        self.hashed_password = ""


    def get_username_password(self):
        self.username = input("username: ")
        self.password = getpass("password(hidden whilst typing): ")

    def hash_password(self, password):
        string = password.encode('utf-8')
        salt = bcrypt.gensalt()
        self.hashed_password = bcrypt.hashpw(string, salt)

    def check_password(self):
        return bcrypt.checkpw(json_datga_store.details[self.username]["password"].encode('utf-8'), self.hashed_password)

    def save_details(self):
        json_datga_store.details[self.username] = {
            "name": self.name,
            "password": self.password,
        }

    def sign_in(self):
        self.get_username_password()
        self.hash_password(self.password)
        while not self.check_password():
            print("username or password incorrect")
            self.get_username_password()
            self.hash_password(self.password)
        print("username and password found. Successful sign-in")

    def sign_up(self):
        self.name = input("name: ")
        self.get_username_password()
        self.hash_password(self.password)
        self.save_details()
        print("details saved, signed up")
