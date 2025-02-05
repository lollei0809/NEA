from controller import ControlGame
import json
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt


class Graph:
    def __init__(self, controller):
        self.controller = controller
        self.details_dict = {}
        self.username1 = ""
        self.username2 = ""

    def get_details(self):
        with open("details.json", mode="r", encoding="utf-8") as read_file:
            self.details_dict = json.load(read_file)
        print(self.details_dict)

    def get_usernames(self):
        self.username1 = self.controller.graphuser1
        self.username2 = self.controller.graphuser1


if __name__ == '__main__':
    controller = ControlGame()
    graph = Graph(controller)
    graph.get_details()
