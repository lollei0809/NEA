import pygame
from util import load_image

class Game:
    def __init__(self):
        self.initialise_pygame()
        self.screen = pygame.display.set_mode((800, 600))
        self.background = load_image("blue") # user input can change color of backgroud:
        #needs set up frame to input username password and settings like colors and sounds
    def main_loop(self):
        while True:
            self.handle_input()
            self.process_game_logic()
            self.draw_game_elements()

    def initialise_pygame(self):
        pygame.init()
        pygame.display.set_caption("Binary Game")

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                #close with the x or esc
                quit()

    def process_game_logic(self):
        pass

    def draw_game_elements(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()


if __name__ == "__main__":
    game = Game()
    game.main_loop()
