import tkinter as tk
from tkinter import ttk
from controller import ControlGame
from user import User
from typing import Optional
import time
from graph_making import GraphFrame

WIDTH = 700
HEIGHT = 400
PADX = 10
PADY = 10
class App(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.tk.call("tk", "scaling", 2.0)

        self.controller = controller

        self.password = ""
        self.username = ""
        self.name = ""

        self.num_users = 0

        self.color = ""
        self.sound = ""

        self.settings = {'padx': PADX, 'pady': PADY}
        self.title("settings page")

        # Set a fixed window size
        self.geometry(f"{WIDTH}x{HEIGHT}")  # Width x Height
        self.resizable(True, True)

        # Frames
        self.choice_frame = ChoiceFrame(self, width=WIDTH, height=HEIGHT)
        self.sign_in_frame = SignInFrame(self, width=WIDTH, height=HEIGHT)
        self.sign_up_frame = SignUpFrame(self, width=WIDTH, height=HEIGHT)
        self.settings_frame = SettingsFrame(self, width=WIDTH, height=HEIGHT)
        self.question_frame = QuestionFrame(self, width=WIDTH, height=HEIGHT)
        self.tutorial_frame = TutorialFrame(self, width=WIDTH, height=HEIGHT)
        self.graph_settings_frame = GraphSettingsFrame(self, width=WIDTH, height=HEIGHT)
        self.graph_frame = GraphFrame(self, width=WIDTH, height=HEIGHT)

        self.go_to_choice()

    def forget_frames(self):
        self.choice_frame.grid_forget()
        self.sign_in_frame.grid_forget()
        self.sign_up_frame.grid_forget()
        self.tutorial_frame.grid_forget()
        self.question_frame.grid_forget()
        self.settings_frame.grid_forget()
        self.graph_frame.grid_forget()
        self.graph_settings_frame.grid_forget()

    def go_to_sign_in(self):
        self.forget_frames()
        self.sign_in_frame.grid()
        self.sign_in_frame.place_widgets()

    def go_to_sign_up(self):
        self.forget_frames()
        self.sign_up_frame.grid()
        self.sign_up_frame.place_widgets()

    def go_to_choice(self):
        self.forget_frames()
        self.choice_frame.grid()
        self.choice_frame.place_widgets()

    def go_to_settings(self):
        self.forget_frames()
        self.settings_frame.grid()
        self.settings_frame.place_widgets()

    def go_to_question(self):
        self.forget_frames()
        self.question_frame.grid()
        self.question_frame.place_widgets()

    def go_to_tut(self):
        type = self.question_frame.question_drop.get()
        self.controller.get_question_type(type)
        print(f"controller q type and acr: {self.controller.type} {self.controller.type_acr}")
        self.forget_frames()
        self.tutorial_frame.grid()
        self.tutorial_frame.place_widgets()

    def go_to_graphs(self):
        self.forget_frames()
        self.graph_settings_frame.grid()
        self.graph_settings_frame.place_widgets()

    def show_graph(self):
        self.forget_frames()
        self.graph_frame.grid()
        ################
        self.graph_frame.grid(row=0, column=0, sticky="nsew")
        self.graph_frame.username1 = self.graph_settings_frame.username1.get()
        self.graph_frame.username2 = self.graph_settings_frame.username2.get()
        self.graph_frame.category = self.graph_settings_frame.type_drop.get()
        self.graph_frame.get_details()
        self.graph_frame.convert_to_pd()
        self.graph_frame.draw_graph()
        #######################
    def check_details(self):
        username = self.sign_in_frame.username.get()
        password = self.sign_in_frame.password.get()

        if self.controller.define_user(option="sign in", name=None, username=username,
                                       password=password):  # if the user is found
            self.sign_in_frame.try_again_txt.grid_forget()
            self.sign_in_frame.success_txt.grid(row=4, column=0, columnspan=2, sticky="W", **self.settings, )
            self.sign_in_frame.next_btn.grid(row=3, column=2, **self.settings)
        else:
            self.sign_in_frame.try_again_txt.grid(row=4, column=0, columnspan=2, sticky="W", **self.settings, )
            # display this on frame and resubmit next_btn press

    def add_user(self):
        name = self.sign_up_frame.name.get()
        username = self.sign_up_frame.username.get()
        password = self.sign_up_frame.password.get()

        self.controller.define_user(option="sign up", name=name, username=username, password=password)
        print(self.controller.user.details_dict)

        self.sign_up_frame.success_txt.grid(row=4, column=0, columnspan=2, sticky="W", **self.settings, )
        self.sign_up_frame.next_btn.grid(row=3, column=2, **self.settings)

    def change_color(self, color):
        print(f"Changing color to {color}")  # Placeholder for changing background in pygame
        self.color = color

    def change_sound(self, sound):
        print(f"Changing sound to {sound}")  # Placeholder for changing sound in pygame
        self.sound = sound

    def recommend(self):
        self.controller.recommend = True
        self.question_frame.question_drop.grid_forget()

    def close(self):
        self.quit()


class ChoiceFrame(tk.Frame):
    def __init__(self, app, width, height):
        super().__init__(app, width=width, height=height)
        self.settings = {'padx': PADX, 'pady': PADX}
        self.app = app

        self.sign_in_btn = tk.Button(self, text="Sign In", command=self.app.go_to_sign_in)
        self.sign_up_btn = tk.Button(self, text="Sign Up", command=self.app.go_to_sign_up)
        self.graph_btn = tk.Button(self, text="Graphs", command=self.app.go_to_graphs)

        self.place_widgets()

    def place_widgets(self):
        self.sign_in_btn.grid(row=0, column=0, sticky="w", **self.settings)
        self.sign_up_btn.grid(row=0, column=1, sticky="w", **self.settings)
        self.graph_btn.grid(row=0, column=2, sticky="w", **self.settings)


class LogInFrame(tk.Frame):
    def __init__(self, app, width, height):
        super().__init__(app, width=width, height=height)
        self.app = app
        self.settings = {'padx': PADX, 'pady': PADY}
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.username_txt = tk.Label(self, text="username")
        self.password_txt = tk.Label(self, text="Password")
        self.username_entry = tk.Entry(self, width=50, textvariable=self.username)
        self.password_entry = tk.Entry(self, width=50, show="*", textvariable=self.password)
        self.back_btn = tk.Button(self, text="Back", command=self.app.go_to_choice)
        self.next_btn = tk.Button(self, text="Next", command=self.app.go_to_settings)
        self.success_txt = tk.Label(self, text="successfully signed in/up", foreground="green")

    def place_widgets(self):
        self.username_txt.grid(row=1, column=0, sticky="W", **self.settings)
        self.username_entry.grid(row=1, column=1, columnspan=2, **self.settings)
        self.password_txt.grid(row=2, column=0, sticky="W", **self.settings)
        self.password_entry.grid(row=2, column=1, columnspan=2, **self.settings)
        self.back_btn.grid(row=3, column=0, **self.settings)


class SignInFrame(LogInFrame):
    def __init__(self, app, width, height):
        super().__init__(app, width=width, height=height)
        self.check_btn = tk.Button(self, text="check details", command=self.app.check_details)
        self.try_again_txt = tk.Label(self, text="Username or password incorrect.", foreground="red")

    def place_widgets(self):
        super().place_widgets()
        self.check_btn.grid(row=3, column=1, **self.settings)


class SignUpFrame(LogInFrame):
    def __init__(self, app, width, height):
        super().__init__(app, width=width, height=height)
        self.name = tk.StringVar()
        self.name_txt = tk.Label(self, text="Name")
        self.name_entry = tk.Entry(self, width=50, textvariable=self.name)
        self.add_btn = tk.Button(self, text="add details", command=self.app.add_user)

    def place_widgets(self):
        super().place_widgets()
        self.name_txt.grid(row=0, column=0, sticky="W", **self.settings)
        self.name_entry.grid(row=0, column=1, columnspan=2, **self.settings)
        self.add_btn.grid(row=3, column=1, **self.settings)


class SettingsFrame(tk.Frame):
    def __init__(self, app, width, height):
        super().__init__(app, width=width, height=height)
        self.settings = {'padx': PADX, 'pady': PADY}
        self.app = app

        self.red_btn = tk.Button(self, text="Red", command=lambda: self.app.change_color("red"), bg="red", fg="white")
        self.yellow_btn = tk.Button(self, text="yellow", command=lambda: self.app.change_color("yellow"), bg="yellow",
                                    fg="black")
        self.green_btn = tk.Button(self, text="Green", command=lambda: self.app.change_color("green"), bg="green",
                                   fg="white")
        self.blue_btn = tk.Button(self, text="Blue", command=lambda: self.app.change_color("blue"), bg="blue",
                                  fg="white")
        self.purple_btn = tk.Button(self, text="purple", command=lambda: self.app.change_color("purple"), bg="purple",
                                    fg="white")

        self.cannon_btn = tk.Button(self, text="cannon noise", command=lambda: self.app.change_sound("cannon"))
        self.click_btn = tk.Button(self, text="click noise", command=lambda: self.app.change_sound("click"))
        self.boing_btn = tk.Button(self, text="boing noise", command=lambda: self.app.change_sound("boing"))

        self.back_btn = tk.Button(self, text="Back", command=self.app.go_to_choice)
        self.next_btn = tk.Button(self, text="next", command=self.app.go_to_question)

    def place_widgets(self):
        self.red_btn.grid(row=0, column=0, **self.settings)
        self.yellow_btn.grid(row=0, column=1, **self.settings)
        self.green_btn.grid(row=0, column=2, **self.settings)
        self.blue_btn.grid(row=0, column=3, **self.settings)
        self.purple_btn.grid(row=0, column=4, **self.settings)

        self.cannon_btn.grid(row=1, column=1, **self.settings)
        self.click_btn.grid(row=1, column=2, **self.settings)
        self.boing_btn.grid(row=1, column=3, **self.settings)

        self.back_btn.grid(row=2, column=0, **self.settings)
        self.next_btn.grid(row=2, column=4, **self.settings)


class QuestionFrame(tk.Frame):
    def __init__(self, app, width, height):
        super().__init__(app, width=width, height=height)
        self.settings = {'padx': PADX, 'pady': PADY}
        self.app = app
        self.text = tk.Label(self, text="Would you like to choose your own question or have one recomended for you")
        self.recommend_btn = tk.Button(self, text="recommend", command=lambda: self.app.recommend())

        self.choose_btn = tk.Button(self, text="choose",
                                    command=lambda: self.question_drop.grid(row=2, column=0,
                                                                            **self.settings))
        values = []
        for key in self.app.controller.types.keys():
            values.append(key)
        self.question_drop = tk.ttk.Combobox(self, values=values, width=36)
        self.question_drop["state"] = "readonly"

        self.back_btn = tk.Button(self, text="Back", command=self.app.go_to_settings)
        self.next_btn = tk.Button(self, text="next", command=self.app.go_to_tut)

    def place_widgets(self):
        self.text.grid(row=0, column=0, sticky="w", columnspan=2, **self.settings)
        self.recommend_btn.grid(row=1, column=0, sticky="w", **self.settings)
        self.choose_btn.grid(row=1, column=1, sticky="w", **self.app.settings)

        self.back_btn.grid(row=3, column=0, sticky="w", **self.settings)
        self.next_btn.grid(row=3, column=1, sticky="w", **self.settings)


class TutorialFrame(tk.Frame):
    def __init__(self, app, width, height):
        super().__init__(app, width=width, height=height)
        self.settings = {'padx': PADX, 'pady': PADY}
        self.app = app

        self.tut_txt = tk.Message(self, text="binary game tutorial!\nAIMS:\nshoot down the correct answer before it "
                                             "reaches the bottom of the screen to increase the 'correct' score."
                                             "MOVEMENT:\nuse the arrow "
                                             "keys to move the spaceship around and the space bar to shoot"
                                             "\nWATCHOUT:\nif you shoot down both incorrect answers or let the correct "
                                             "answer reach the bottom, GAME OVER.  ")  # message text or label: message for non editable multiline text

        self.back_btn = tk.Button(self, text="Back", command=self.app.go_to_question)
        self.play_btn = tk.Button(self, text="PLAY!", command=self.app.close, bg="green")

    def place_widgets(self):
        self.tut_txt.grid(row=1, column=1, columnspan=2, **self.settings)
        self.back_btn.grid(row=2, column=1, **self.settings)
        self.play_btn.grid(row=2, column=3, **self.settings)


class GraphSettingsFrame(tk.Frame):
    def __init__(self, app, width, height):
        super().__init__(app, width=width, height=height)
        self.settings = {'padx': PADX, 'pady': PADY}
        self.app = app
        self.users_text = tk.Label(self, text="compare multiple users' high scores, or 1 user's high scores over time?")
        self.type_text = tk.Label(self, text="select a specific question type or leave blank to compare all")
        self.username1 = tk.StringVar()
        self.username2 = tk.StringVar()
        self.username1_entry = tk.Entry(self, width=50, textvariable=self.username1)
        self.username2_entry = tk.Entry(self, width=50, textvariable=self.username2)

        self.one_user_btn = tk.Button(self, text="1 user", command=lambda: self.grid1())
        self.two_users_btn = tk.Button(self, text="multiple users", command=lambda: self.grid2())

        values = []
        for key in self.app.controller.types.keys():
            values.append(key)
        self.type_drop = tk.ttk.Combobox(self, values=values, width=36)
        self.type_drop["state"] = "readonly"

        self.back_btn = tk.Button(self, text="Back", command=self.app.go_to_choice)
        self.go_btn = tk.Button(self, text="GO!", command=self.app.show_graph, bg="green")

    def place_widgets(self):
        self.users_text.grid(row=0, column=0, sticky="w", columnspan=2, **self.settings)
        self.one_user_btn.grid(row=1, column=0, sticky="w", **self.settings)
        self.two_users_btn.grid(row=1, column=1, sticky="w", **self.settings)
        self.type_text.grid(row=4, column=0, sticky="w", columnspan=2, **self.settings)
        self.type_drop.grid(row=5, column=0, **self.settings)
        self.back_btn.grid(row=6, column=0, sticky="w", **self.settings)
        self.go_btn.grid(row=6, column=1, sticky="w", **self.settings)

    def grid1(self):
        self.app.num_users = 1
        self.username2_entry.grid_forget()
        self.username1_entry.grid(row=2, column=0, sticky="w", columnspan=2, **self.settings)

    def grid2(self):
        self.app.num_users = 2
        self.username1_entry.grid(row=2, column=0, sticky="w", columnspan=2, **self.settings)
        self.username2_entry.grid(row=3, column=0, sticky="w", columnspan=2, **self.settings)


if __name__ == '__main__':
    controller = ControlGame()
    tk_app = App(controller)
    tk_app.mainloop()
