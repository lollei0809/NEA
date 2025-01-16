import tkinter as tk
from controller import ControlGame
from user import User
from typing import Optional


class App(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.password = ""
        self.username = ""
        self.name = ""


        self.user: Optional[User] = None

        self.color = ""
        self.sound = ""

        self.settings = {'padx': 10, 'pady': 10}
        self.title("Binary Game")

        # Set a fixed window size
        self.geometry("400x300")  # Width x Height
        self.resizable(False, False)  # Prevent resizing

        # Frames
        self.choice_frame = ChoiceFrame(self, width=400, height=300)
        self.sign_in_frame = SignInFrame(self, width=400, height=300)
        self.sign_up_frame = SignUpFrame(self, width=400, height=300)
        self.settings_frame = SettingsFrame(self, width=400, height=300)
        self.tutorial_frame = TutorialFrame(self, width=400, height=300)

        self.pack_frames()

    def pack_frames(self):
        self.choice_frame.grid()

    def sign_in(self):
        self.choice_frame.grid_forget()
        self.sign_in_frame.grid()
        self.sign_in_frame.place_widgets()

    def sign_up(self):
        self.choice_frame.grid_forget()
        self.sign_up_frame.grid()
        self.sign_up_frame.place_widgets()

    def back_to_choice(self):
        self.sign_in_frame.grid_forget()
        self.sign_up_frame.grid_forget()
        self.settings_frame.grid_forget()
        self.choice_frame.grid()
        self.choice_frame.place_widgets()

    def back_to_settings(self):
        self.choice_frame.grid_forget()
        self.sign_in_frame.grid_forget()
        self.sign_up_frame.grid_forget()
        self.tutorial_frame.grid_forget()
        self.settings_frame.grid()
        self.settings_frame.place_widgets()

    def check_details(self):
        username = self.sign_in_frame.username.get()
        password = self.sign_in_frame.password.get()

        if self.controller.define_user(option="sign in", name=None, username=username, password=password):#if the user is found
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

    def go_to_settings(self):
        self.sign_in_frame.grid_forget()
        self.sign_up_frame.grid_forget()
        self.choice_frame.grid_forget()
        self.settings_frame.grid()
        self.settings_frame.place_widgets()

    def go_to_tut(self):
        self.sign_in_frame.grid_forget()
        self.sign_up_frame.grid_forget()
        self.choice_frame.grid_forget()
        self.settings_frame.grid_forget()
        self.tutorial_frame.grid()
        self.tutorial_frame.place_widgets()

    def change_color(self, color):
        print(f"Changing color to {color}")  # Placeholder for changing background in pygame
        self.color = color

    def change_sound(self, sound):
        print(f"Changing sound to {sound}")  # Placeholder for changing sound in pygame
        self.sound = sound

    def close(self):
        self.quit()


class ChoiceFrame(tk.Frame):
    def __init__(self, app, width, height):
        super().__init__(app, width=width, height=height)
        self.settings = {'padx': 10, 'pady': 10}
        self.app = app

        self.sign_in_btn = tk.Button(self, text="Sign In", command=self.app.sign_in)
        self.sign_up_btn = tk.Button(self, text="Sign Up", command=self.app.sign_up)

        self.place_widgets()

    def place_widgets(self):
        self.sign_in_btn.grid(row=0, column=0, **self.settings)
        self.sign_up_btn.grid(row=0, column=1, **self.settings)


class LogInFrame(tk.Frame):
    def __init__(self, app, width, height):
        super().__init__(app, width=width, height=height)
        self.app = app
        self.settings = {'padx': 10, 'pady': 10}
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.username_txt = tk.Label(self, text="username")
        self.password_txt = tk.Label(self, text="Password")
        self.username_entry = tk.Entry(self, width=50, textvariable=self.username)
        self.password_entry = tk.Entry(self, width=50, show="*", textvariable=self.password)
        self.back_btn = tk.Button(self, text="Back", command=self.app.back_to_choice)
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
        self.settings = {'padx': 10, 'pady': 10}
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

        self.back_btn = tk.Button(self, text="Back", command=self.app.back_to_choice)
        self.next_btn = tk.Button(self, text="next", command=self.app.go_to_tut)

    def place_widgets(self):
        self.red_btn.grid(row=0, column=0, **self.settings)
        self.yellow_btn.grid(row=0, column=1, **self.app.settings)
        self.green_btn.grid(row=0, column=2, **self.app.settings)
        self.blue_btn.grid(row=0, column=3, **self.settings)
        self.purple_btn.grid(row=0, column=4, **self.app.settings)

        self.cannon_btn.grid(row=1, column=1, **self.app.settings)
        self.click_btn.grid(row=1, column=2, **self.app.settings)
        self.boing_btn.grid(row=1, column=3, **self.app.settings)

        self.back_btn.grid(row=2, column=1, **self.settings)
        self.next_btn.grid(row=2, column=3, **self.settings)


class TutorialFrame(tk.Frame):
    def __init__(self, app, width, height):
        super().__init__(app, width=width, height=height)
        self.settings = {'padx': 10, 'pady': 10}
        self.app = app

        self.tut_txt = tk.Message(self, text="binary game tutorial!\nAIMS:\nshoot down the correct answer before it "
                                             "reaches the bottom of the screen to increase the 'correct' score. "
                                             "you have 2 chances to find the correct answer\nMOVEMENT:\nuse the arrow "
                                             "keys to move the spaceship around and the space bar to shoot"
                                             "\nWATCHOUT:\nif you shoot down both incorrect answers or let the correct "
                                             "answer reach the bottom, GAME OVER.  ")  # message text or label: message for non editable multiline text

        self.back_btn = tk.Button(self, text="Back", command=self.app.back_to_settings)
        self.play_btn = tk.Button(self, text="PLAY!", command=self.app.close, bg="green")

    def place_widgets(self):
        self.tut_txt.grid(row=1, column=1, columnspan=2, **self.settings)
        self.back_btn.grid(row=2, column=1, **self.settings)
        self.play_btn.grid(row=2, column=3, **self.settings)


if __name__ == '__main__':
    controller = ControlGame()
    tk_app = App(controller)
    tk_app.mainloop()
