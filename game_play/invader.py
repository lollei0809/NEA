import pygame
import random
from pygame import (
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    K_SPACE,
)

# constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
PLAYER_SPEED = 10
MAX_BULLETS = 50


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('../assets/sprites/rocket.png')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.9))
        self.direction = 0

    def shoot(self):
        bullet = Bullet(self.rect.center)
        return bullet

    def update(self):
        if 0 < self.rect.left + PLAYER_SPEED * self.direction and self.rect.right + PLAYER_SPEED * self.direction < SCREEN_WIDTH:
            self.rect.move_ip((PLAYER_SPEED * self.direction, 0))


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        # create a surface to show the object
        self.surf = pygame.Surface((5, 20))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(center=pos)

    def update(self):
        self.rect.move_ip(0, -5)
        if self.rect.bottom < 0:
            self.kill()

class Answer(pygame.sprite.Sprite):
    def __init__(self,x_val):
        super().__init__()
        self.image = pygame.image.load('../assets/sprites/asteroid.png')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(center=(x_val, 0))

    def update(self):
        self.rect.move_ip((0, 1))
        if self.rect.bottom > SCREEN_HEIGHT:
            self.kill()


class SpaceInvaders:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        self.clock = pygame.time.Clock()

        self.player = Player()

        self.bullets = pygame.sprite.Group()
        self.answers = pygame.sprite.Group()
        self.sprites = pygame.sprite.Group(self.player)

        self.running = True
        self.frame_count = 0
        self.xvals = [0, 100, 200]

    def main_loop(self):
        while self.running:
            self._handle_input()
            self._process_game_logic()
            self._draw()
        pygame.quit()

    def _handle_input(self):
        for event in pygame.event.get():
            # Quit conditions
            if (event.type == QUIT or
                    event.type == KEYDOWN and event.key == K_ESCAPE):
                self.running = False
            if event.type == KEYDOWN and event.key == K_SPACE and len(self.bullets) < MAX_BULLETS:
                self.bullets.add(self.player.shoot())

        # update player on the basis of pressed keys
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT] and self.player.rect.right < SCREEN_WIDTH:
            self.player.direction = -1
        if pressed_keys[K_RIGHT]:
            self.player.direction = 1



    def _process_game_logic(self):
        self.clock.tick(60)
        self.sprites.update()

        #check if bullet meets answer
        # for bullet in self.bullets:
        #     if bullet.rect.colliderect(self.answer):
        #         bullet.kill()
        #         self.answer.kill()

        # Spawn new answers periodically
        self.frame_count += 1

        if self.frame_count % 480 == 0:
            for i in range (3):
                answer = Answer(self.xvals[i])
                self.answers.add(answer)
                self.sprites.add(answer)

        # Handle collisions
        #for bullet in self.bullets:
        #    for answer in self.answers:
        collision = pygame.sprite.groupcollide(self.bullets, self.answers, True,True)
        if collision:
            print("collision")
            # bullet.kill()
            # answer.kill()

    def _draw(self):
        self.screen.fill((0, 0, 0))
        for sprite in self.sprites:
            self.screen.blit(sprite.image if hasattr(sprite, 'image') else sprite.surf, sprite.rect)
        pygame.display.flip()


if __name__ == "__main__":
    game = SpaceInvaders()
    game.main_loop()
