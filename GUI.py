import pygame

def load_image(name):
    destination = f"assets/sprites/{name}.png"
    image = pygame.image.load(destination)
    return image.convert_alpha()

class GameObject:
    def __init__(self, position, sprite, velocity):
        self.position = pygame.math.Vector2(position)
        self.sprite = sprite
        self.radius = sprite.get_width()/2
        self.velocity = pygame.math.Vector2(velocity)

    def draw(self, surface):
        blit_position = self.position - pygame.math.Vector2(self.radius)
        surface.blit(self.sprite, blit_position)

    def move(self):
        self.position += self.velocity

    def collides_with(self, obj_2):
        distance = self.position.distance_to(obj_2.position)
        if distance < self.radius + obj_2.radius:
            return True
        else:
            return False

class Game:
    def __init__(self):
        self.initialise_pygame()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.background = load_image("blue") # user input can change color of backgroud:
        #needs set up frame to input username password and settings like colors and sounds
        self.spaceship = GameObject(
            (400, 300), load_image("rocket2"), (0, 0)
        )
        self.asteroid = GameObject(
            (400, 300), load_image("rocket2"), (1, 0)
        )

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
        self.spaceship.move()
        self.asteroid.move()

    def draw_game_elements(self):
        self.screen.blit(self.background, (0, 0))
        self.spaceship.draw(self.screen)
        self.asteroid.draw(self.screen)
        self.clock.tick(100)
        pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.main_loop()
