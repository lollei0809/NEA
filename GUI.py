from pygame_game import WIDTH, HEIGHT, load_image, load_sound, GameObject, Spaceship, Bullet, Answer, Game, TextBox
from tkinter_page import App, Choice, Log_in, Sign_in, Sign_up, Settings
from controller import ControlGame
from user import User
from questions import Question, UnsignedQuestion, SignAndMagnitude, HexToDec
from typing import Optional


class GUI:
    def __init__(self):
        self.controller = Optional[ControlGame] = None
        self.tkinter = Optional[App] = None
        self.pygame = Optional[Game] = None


    def run_tk(self):
        self.tkinter = App()
        self.tkinter.mainloop()


    def run_pyg(self):

        self.pygame = Game()
        if self.tkinter.color != "":
            self.pygame.set_color(self.tkinter.color)
        if self.tkinter.sound != "":
            self.pygame.set_sound(self.tkinter.sound)
        self.pygame.main_loop()

