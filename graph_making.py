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
        self.filtered_df = None

        # Create a Matplotlib figure

        self.figure, self.ax = plt.subplots(figsize=(WIDTH/100, HEIGHT/100))

        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=False)

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
                            "Username": username,  # Add username to the entry
                            "Attempt": i + 1,
                            "Category": category,
                            "Type": "Incorrect",
                            "Score": incorrect_value
                        })

        self.df = pd.DataFrame(data_list)
        self.filtered_df = self.df[(self.df["Category"] == self.category) & (self.df["Username"] == self.username1)]

    def draw_graph(self):
        self.ax.clear()  # Clear previous graph

        sns.barplot(data=self.filtered_df, x="Attempt", y="Score", hue="Type", ax=self.ax)
        self.ax.set_title(f"Correct vs Incorrect for {self.user1_data.get('name', self.username1)}")
        self.ax.set_xlabel("Attempt")
        self.ax.set_ylabel("Score")
        # self.ax.tick_params(axis='x', rotation=45)
        self.ax.legend(title="Answer Type")
        self.canvas.draw()  # Refresh canvas


# Example usage
if __name__ == '__main__':
    root = tk.Tk()
    sns.set_theme()

    graph_frame = GraphFrame(root, width=WIDTH, height=HEIGHT)
    graph_frame.pack(fill=tk.BOTH, expand=True)

    graph_frame.username1 = "lolly123"
    graph_frame.category = "unsigned binary to decimal"
    graph_frame.get_details()
    graph_frame.convert_to_pd()
    graph_frame.draw_graph()

    root.mainloop()
