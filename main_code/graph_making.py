import json
import seaborn as sns
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

matplotlib.use("TkAgg")
WIDTH = 700
HEIGHT = 400
PADX = 10
PADY = 10
SCALING = 2
class GraphFrame(tk.Frame):
    def __init__(self, app, width, height):
        super().__init__(app, width=width, height=height)
        self.settings = {'padx': PADX, 'pady': PADY}
        self.app = app
        self.details_dict = {}
        self.username1 = ""
        self.user1_data = {}
        self.username2 = ""
        self.user2_data = {}
        self.category = ""
        self.df = None

        self.figure, self.ax = plt.subplots(figsize=(WIDTH / (50 * SCALING), HEIGHT / (50 * SCALING)))

        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=False)

        self.back_btn = tk.Button(self, text="Back", command=self.app.go_to_graphs)
        self.types = {"unsigned binary to decimal": "ubtd",
                      "decimal to unsigned binary": "dtub",
                      "sign and magnitude binary to decimal": "smtd",
                      "decimal to sign and magnitude binary": "dtsm",
                      "two's complement binary to decimal": "tctd",
                      "decimal to two's complement binary": "dttc",
                      "hexadecimal to decimal": "htd",
                      "decimal to hexadecimal": "dth"}

    def get_details(self):
        with open("details.json", mode="r", encoding="utf-8") as read_file:
            self.details_dict = json.load(read_file)

    def convert_to_pd(self):
        data_list = []

        for username, user_data in self.details_dict.items():
            for category, scores in user_data.items():
                if isinstance(scores, dict) and "correct" in scores and "incorrect" in scores:
                    i = 1
                    for correct_value in scores["correct"]:
                        data_list.append({
                            "Username": username,
                            "Attempt": i,
                            "Category": category,
                            "Type": "Correct",
                            "Score": correct_value
                        })
                        i += 1

                    j = 1
                    for incorrect_value in scores["incorrect"]:
                        data_list.append({
                            "Username": username,
                            "Attempt": j,
                            "Category": category,
                            "Type": "Incorrect",
                            "Score": incorrect_value
                        })
                        j += 1
                self.df = pd.DataFrame(data_list)

    def draw_1_user_1_category(self):
        filtered_df = self.df[(self.df["Category"] == self.category) & (self.df["Username"] == self.username1)]
        self.ax.clear()
        sns.barplot(data=filtered_df, x="Attempt", y="Score", hue="Type", ax=self.ax)
        self.ax.set_title(f"scores for {self.user1_data.get('name', self.username1)} for {self.category}")
        self.ax.set_xlabel("Attempt")
        self.ax.set_ylabel("Score")
        # self.ax.tick_params(axis='x', rotation=45)
        self.ax.legend(title="Answer Type")
        self.figure.tight_layout()
        self.canvas.draw()
        self.back_btn.pack()

    def draw_1_user_all_categories(self):
        filtered_df = self.df[(self.df["Username"] == self.username1)]
        filtered_df["Category"] = filtered_df["Category"].map(self.types)#to show the acronyms not the words so it isnt overcrowded
        self.ax.clear()
        sns.barplot(data=filtered_df, x="Category", y="Score", hue="Type", ax=self.ax)
        self.ax.set_title(
            f"scores for {self.user1_data.get('name', self.username1)}  ")
        self.ax.set_xlabel("Category")
        self.ax.set_ylabel("Score")#
        self.ax.legend(title="Answer Type")
        self.figure.tight_layout()
        self.canvas.draw()
        self.back_btn.pack()


    def draw_2_users_1_category(self):
        filtered_df = self.df[((self.df["Username"] == self.username1) | (self.df["Username"] == self.username2)) & (
                self.df["Category"] == self.category)]
        self.ax.clear()
        sns.barplot(data=filtered_df, x="Username", y="Score", hue="Type", ax=self.ax)
        self.ax.set_title(f"Correct vs Incorrect for {self.user1_data.get('name', self.username1)} and {self.user2_data.get('name', self.username2)} for {self.category}")
        self.ax.set_xlabel("Username")
        self.ax.set_ylabel("Score")
        self.ax.legend(title="Answer Type")
        self.figure.tight_layout()
        self.canvas.draw()
        self.back_btn.pack()