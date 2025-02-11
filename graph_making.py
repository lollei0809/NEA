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
SCALING = 2.0


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

        self.figure, self.ax = plt.subplots(figsize=(WIDTH / (100 * SCALING), HEIGHT / (100 * SCALING)))

        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=False)

        self.back_btn = tk.Button(self, text="Back", command=self.app.go_to_graphs)

    def get_details(self):
        with open("details.json", mode="r", encoding="utf-8") as read_file:
            self.details_dict = json.load(read_file)

    def convert_to_pd(self):
        data_list = []

        for username, user_data in self.details_dict.items():
            for category, scores in user_data.items():
                if isinstance(scores, dict) and "correct" in scores and "incorrect" in scores:
                    for i, correct_value in enumerate(scores["correct"]):
                        data_list.append({
                            "Username": username,
                            "Attempt": i + 1,
                            "Category": category,
                            "Type": "Correct",
                            "Score": correct_value
                        })
                    for i, incorrect_value in enumerate(scores["incorrect"]):
                        data_list.append({
                            "Username": username,
                            "Attempt": i + 1,
                            "Category": category,
                            "Type": "Incorrect",
                            "Score": incorrect_value
                        })

        self.df = pd.DataFrame(data_list)

    def draw_1_user_1_category(self):
        filtered_df = self.df[(self.df["Category"] == self.category) & (self.df["Username"] == self.username1)]
        self.ax.clear()
        sns.barplot(data=filtered_df, x="Attempt", y="Score", hue="Type", ax=self.ax)
        self.ax.set_title(f"Correct vs Incorrect for {self.user1_data.get('name', self.username1)} for {self.category}")
        self.ax.set_xlabel("Attempt")
        self.ax.set_ylabel("Score")
        # self.ax.tick_params(axis='x', rotation=45)
        self.ax.legend(title="Answer Type")
        self.canvas.draw()
        self.back_btn.pack()

    def draw_1_user_all_categories(self):
        pass

    def draw_2_users_1_category(self):
        pass

    def draw_2_users_all_categories(self):
        filtered_df = self.df[((self.df["Username"] == self.username1) | (self.df["Username"] == self.username2)) & (
                    self.df["Type"] == "Correct")]
        #here i want to average the correct and incorrect on each attempt to get rid of those black lines

        print(filtered_df)
        self.ax.clear()
        sns.barplot(data=filtered_df, x="Category", y="Score", hue="Username", ax=self.ax)
        self.ax.set_title(
            f"scores for {self.user1_data.get('name', self.username1)} and {self.user1_data.get('name', self.username2)}")
        self.ax.set_xlabel("Attempt")
        self.ax.set_ylabel("Score")
        self.ax.tick_params(axis='x', rotation=45)
        self.ax.legend(title="Answer Type")
        self.canvas.draw()
        self.back_btn.pack()


if __name__ == '__main__':
    root = tk.Tk()
    sns.set(font_scale=0.5)
    sns.set_theme()
    graph_frame = GraphFrame(root, width=WIDTH, height=HEIGHT)
    graph_frame.grid()
    graph_frame.username1 = "lolly123"
    graph_frame.category = "unsigned binary to decimal"
    graph_frame.get_details()
    graph_frame.convert_to_pd()
    graph_frame.draw_1_user_1_category()

    root.mainloop()
