import pygame
from abc import ABC, abstractmethod
from pygame import (
    K_LEFT,
    K_RIGHT,
    K_UP,
    K_DOWN,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    K_SPACE,
)

WIDTH = 1000
HEIGHT = 600


def load_image(name, size):
    destination = f"assets/sprites/{name}.png"
    image = pygame.image.load(destination)
    image = pygame.transform.scale(image, size)
    return image.convert_alpha()


class GameObject(ABC):
    def __init__(self, position, sprite, velocity):
        self.position = pygame.math.Vector2(position)
        self.sprite = sprite
        self.radius = sprite.get_width() / 2
        self.velocity = pygame.math.Vector2(velocity)

    def draw(self, surface):
        blit_position = self.position - pygame.math.Vector2(self.radius)
        surface.blit(self.sprite, blit_position)

    @abstractmethod
    def move(self):
        pass

    def collides_with(self, obj_2):
        distance = self.position.distance_to(obj_2.position)
        if distance < self.radius + obj_2.radius:
            return True
        else:
            return False


class Spaceship(GameObject):
    def __init__(self, position):
        super().__init__(position, load_image("rocket2", (50, 50)), pygame.math.Vector2((1, 0)))

    def move(self):
        self.position += self.velocity
        self.velocity *= 0.9 #applies friction

        # Constrain position within screen bounds
        self.position.x = max(0, min(self.position.x, WIDTH))
        self.position.y = max(0, min(self.position.y, HEIGHT))

        # Optional: Reset velocity to 0 if at boundary
        if self.position.x in (0, WIDTH):
            self.velocity.x = 0
        if self.position.y in (0, HEIGHT):
            self.velocity.y = 0

class Answer(GameObject):
    def __init__(self, position):
        super().__init__(position, load_image("asteroid", (100, 100)), pygame.math.Vector2((0, 0)))

    def move(self):
        self.position += self.velocity


class Bullet(GameObject):
    def __init__(self, position):
        super().__init__(position, load_image("bullet", (30, 30)), pygame.math.Vector2((0, -5)))
    def move(self):
        self.position += self.velocity






class Game:
    def __init__(self):
        self.initialise_pygame()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.background = load_image("red", (WIDTH, HEIGHT))  # user input can change color of backgroud:
        # needs set up frame to input username password and settings like colors and sounds
        self.spaceship = Spaceship((WIDTH / 2, 550))
        self.answers = [Answer((WIDTH / 2, 100))]
        self.bullets = []

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
                # close with the x or esc
                quit()
            if event.type == KEYDOWN and event.key == K_SPACE:
                self.bullets.append(Bullet(self.spaceship.position))

        # update player on the basis of pressed keys
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT] and self.spaceship.position:
            self.spaceship.velocity += (-1, 0)
        if pressed_keys[K_RIGHT]:
            self.spaceship.velocity += (1, 0)
        if pressed_keys[K_UP]:
            self.spaceship.velocity += (0, -1)
        if pressed_keys[K_DOWN]:
            self.spaceship.velocity += (0, 1)

    def process_game_logic(self):
        self.spaceship.move()
        for bullet in self.bullets:
            bullet.move()
            if bullet.position.y < 200:
                bullet = None
        for answer in self.answers:
            answer.move()

    def draw_game_elements(self):
        self.screen.blit(self.background, (0, 0))
        self.spaceship.draw(self.screen)
        for bullet in self.bullets:
            bullet.draw(self.screen)
        for answer in self.answers:
            answer.draw(self.screen)
        self.clock.tick(100)
        pygame.display.flip()


if __name__ == "__main__":
    game = Game()
    game.main_loop()
