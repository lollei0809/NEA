import pygame

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
SCREEN_HEIGHT = 800
PLAYER_SPEED = 10
MAX_BULLETS = 5


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('Assets/Sprites/spaceship.png')
        self.image = pygame.transform.scale(self.image, (50, 20))
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.9))

    def shoot(self):
        bullet = Bullet(self.rect.center)
        return bullet

    def update(self, direction):
        if 0 < self.rect.left + PLAYER_SPEED * direction and self.rect.right + PLAYER_SPEED * direction < SCREEN_WIDTH:
            self.rect.move_ip((PLAYER_SPEED * direction, 0))


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        # create a surface to show the object
        self.surf = pygame.Surface((5, 20))
        self.surf.fill((255,255,255))
        self.rect = self.surf.get_rect(center=pos)

    def update(self):
        self.rect.move_ip((0, -5))
        if self.rect.bottom < 0:
            self.kill()


class SpaceInvaders:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        self.clock = pygame.time.Clock()

        self.player = Player()
        self.bullets = pygame.sprite.Group()
        self.running = True

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
            self.player.update(-1)
        if pressed_keys[K_RIGHT]:
            self.player.update(1)

    def _process_game_logic(self):
        self.clock.tick(60)
        self.bullets.update()

    def _draw(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.player.image, self.player.rect)
        for bullet in self.bullets:
            self.screen.blit(bullet.surf, bullet.rect)
        pygame.display.flip()


if __name__ == "__main__":
    game = SpaceInvaders()
    game.main_loop()
