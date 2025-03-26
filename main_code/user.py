import bcrypt
import json
from main_code.priority_queue import Queue
class User:
    def __init__(self):
        self.signed_in = None
        self.name = ""
        self.username = ""
        self.password = ""
        self.details_dict = {}
        self.queue = Queue()

    def get_details(self):
        with open("details.json", mode="r", encoding="utf-8") as read_file:
            self.details_dict = json.load(read_file)
    def get_queue(self):
        self.queue.items = self.details_dict[self.username]["question_queue"]

    def hash_password(self, password):
        string = password.encode('utf-8')  # converts password to byte string eg b"{password}"
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(string, salt)

    def check_password(self, username, password):
        string = password.encode('utf-8')
        return bcrypt.checkpw(string, self.details_dict[username]["hashed_password"].encode('utf-8'))

    def save_details_dict_to_json(self):
        with open("details.json", mode="w", encoding="utf-8") as write_file:
            json.dump(self.details_dict, write_file, indent=4)

    def find_high_score(self, game_type):
        correct_scores = self.details_dict[self.username][game_type].get("correct", [])  # Get correct scores list
        if len(correct_scores) == 0:
            return 0
        highest_score = correct_scores[0]
        for score in correct_scores:
            if score > highest_score:
                highest_score = score

        return highest_score

    def sign_in(self, username, password):
        if username not in self.details_dict.keys() or not self.check_password(username, password):
            return False
        else:
            self.username = username
            self.password = password
            self.details_dict[self.username]["signed_in"] = True
            self.name = self.details_dict[self.username]["name"]
            self.signed_in = True
            return True

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

    def sign_up(self, name, username, password):
        self.name = name
        self.username = username
        self.password = password
        self.signed_in = True
        self.details_dict[username] = {
            "name": name,
            "hashed_password": self.hash_password(password).decode("utf-8"),
            "signed_in": True,
            "queue":[],
            "unsigned binary to decimal": {"correct": [], "incorrect": []},
            "decimal to unsigned binary": {"correct": [], "incorrect": []},
            "sign and magnitude binary to decimal": {"correct": [], "incorrect": []},
            "decimal to sign and magnitude binary": {"correct": [], "incorrect": []},
            "two's complement binary to decimal": {"correct": [], "incorrect": []},
            "decimal to two's complement binary": {"correct": [], "incorrect": []},
            "hexadecimal to decimal": {"correct": [], "incorrect": []},
            "decimal to hexadecimal": {"correct": [], "incorrect": []}
        }
