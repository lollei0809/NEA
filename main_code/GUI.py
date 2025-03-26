from pygame_game import Game
from tkinter_page import App
from controller import ControlGame
from typing import Optional


class GUI:
    def __init__(self, controller):
        self.controller: Optional[ControlGame] = controller
        self.tkinter: Optional[App] = None
        self.pygame: Optional[Game] = None

    def run_tk(self):
        self.tkinter = App(self.controller)
        self.tkinter.mainloop()

    def run_pyg(self):
        self.tkinter.close()
        self.pygame = Game(self.controller)
        if self.tkinter.color != "":
            self.pygame.set_color(self.tkinter.color)
        if self.tkinter.sound != "":
            self.pygame.set_sound(self.tkinter.sound)
        self.pygame.main_loop()

if __name__ == '__main__':
    game_controller = ControlGame()
    gui = GUI(game_controller)
    gui.run_tk()
    gui.run_pyg()
