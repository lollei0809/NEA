import pygame

WIDTH = 1000
HEIGHT = 600
def load_image(name,size):
    destination = f"assets/sprites/{name}.png"
    image = pygame.image.load(destination)
    image = pygame.transform.scale(image, size)
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
class Spaceship(GameObject):
    def __init__(self,position):
        super().__init__(position, load_image("rocket2",(50,50)), pygame.math.Vector2(0))

class Answer(GameObject):
    def __init__(self,position):
        super().__init__(position, load_image("asteroid",(100,100)), pygame.math.Vector2(0))

class Bullet(GameObject):
    def __init__(self,position):
        super().__init__(position, load_image("bullet",(30,30)), pygame.math.Vector2(0))

class Game:
    def __init__(self):
        self.initialise_pygame()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        self.clock = pygame.time.Clock()
        self.background = load_image("red",(WIDTH,HEIGHT)) # user input can change color of backgroud:
        #needs set up frame to input username password and settings like colors and sounds
        self.spaceship = Spaceship((WIDTH/2, 550))
        self.answer = Answer((WIDTH/2, 100))
        self.bullet = Bullet((WIDTH/2, 300))
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

    def draw_game_elements(self):
        self.screen.blit(self.background, (0, 0))
        self.spaceship.draw(self.screen)
        self.bullet.draw(self.screen)
        self.answer.draw(self.screen)
        self.clock.tick(100)
        pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.main_loop()
