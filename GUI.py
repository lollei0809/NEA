from pygame_game import WIDTH, HEIGHT, load_image, load_sound, GameObject, Spaceship, Bullet, Answer, Game, TextBox
from tkinter_page import App, ChoiceFrame, LogInFrame, SignInFrame, SignUpFrame, SettingsFrame
from controller import ControlGame
from questions import Question, UnsignedQuestion, SignAndMagnitude, HexToDec
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
        self.pygame = Game()
        if self.tkinter.color != "":
            self.pygame.set_color(self.tkinter.color)
        if self.tkinter.sound != "":
            self.pygame.set_sound(self.tkinter.sound)
        self.run_question()
        self.pygame.main_loop()

    def run_question(self):
        self.controller.gen_question()
        self.pygame.set_question(self.controller.question.question_phrase)
        self.pygame.set_answers(self.controller.question.plausible_answers,self.controller.question.correct_answer)


if __name__ == '__main__':
    game_controller = ControlGame()
    gui = GUI(game_controller)
    gui.run_tk()
    gui.run_pyg()
