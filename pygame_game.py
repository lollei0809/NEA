import random
import pygame
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
from pygame.mixer import Sound

WIDTH = 1000
HEIGHT = 600



def load_image(name, size):
    destination = f"assets/sprites/{name}.png"
    image = pygame.image.load(destination)
    image = pygame.transform.scale(image, size)
    return image.convert_alpha()
def load_sound(name):
    path = f"assets/sounds/{name}.wav"
    return Sound(path)

class GameObject():
    def __init__(self, position, sprite, velocity):
        self.position = pygame.math.Vector2(position)
        self.sprite = sprite
        self.radius = sprite.get_width() / 2
        self.velocity = pygame.math.Vector2(velocity)

    def draw(self, surface):
        blit_position = self.position - pygame.math.Vector2(self.radius)
        surface.blit(self.sprite, blit_position)

    def move(self):
        self.position += self.velocity

    def collides_with(self, obj_2):
        distance = self.position.distance_to(obj_2.position)
        if distance <= self.radius + obj_2.radius:
            return True
        else:
            return False


class Spaceship(GameObject):
    def __init__(self, position):
        super().__init__(position, load_image("rocket", (50, 50)), pygame.math.Vector2((1, 0)))
        self.shoot_sound = load_sound("click")

    def move(self):
        super().move()
        self.velocity *= 0.9  # applies friction
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
        super().__init__(position, load_image("asteroid", (100, 100)), pygame.math.Vector2((0, 0.5)))
        self.correct = False


class Bullet(GameObject):
    def __init__(self, position):
        super().__init__(position, load_image("bullet", (30, 30)), pygame.math.Vector2((0, -10)))

    def move(self):
        super().move()
        # if hits top of screen remove from bullet list
        if self.position.y <= -5:
            game.bullets.remove(self)

class TextBox:
    def __init__(self, text, position, font_size=24, color=(255, 255, 255)):
        self.text = text
        self.position = position
        self.font_size = font_size
        self.color = color
        self.font = pygame.font.Font(None, font_size)
        self.size = self.font.size(self.text)


    def draw(self, surface):
        # Render the text without the rectangle
        rendered_text = self.font.render(self.text, True, self.color)
        surface.blit(rendered_text, self.position)
    def update_text(self, new_text):
        self.text = new_text

class Game:
    def __init__(self):
        self.correct = 0
        self.incorrect = 0
        self.percentage = 0
        self.initialise_pygame()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.background = load_image("red", (WIDTH, HEIGHT))#default red
        self.spaceship = Spaceship((WIDTH / 2, 550))
        self.answers = [[Answer((WIDTH / 4, 0)), Answer((WIDTH / 2, 0)), Answer((3 * WIDTH / 4, 0))]]
        self.bullets = []

        self.correct_box = TextBox("correct: 0",(0, HEIGHT-20))
        self.incorrect_box = TextBox("incorrect: 1",(220,HEIGHT-20))
        self.instruction_box = TextBox("question here",(0, 0))

        self.paused = False
        self.pause_button = TextBox("Pause",(WIDTH-50,0))
        self.level = 0
        self.game_over = False

        self.gameover_sound = load_sound("game_over")
        self.play_sound = True



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
            if event.type == QUIT or (event.type == pygame.KEYDOWN and event.key == K_ESCAPE):
                # close with the x or esc
                quit()
            if event.type == KEYDOWN and event.key == K_SPACE:
                self.spaceship.shoot_sound.play()
                bullet_position = list(self.spaceship.position)
                bullet_position[1] -= 40
                self.bullets.append(Bullet(tuple(bullet_position)))
            if event.type == pygame.MOUSEBUTTONDOWN:
                x_min,y_min = self.pause_button.position
                x_max = x_min + self.pause_button.size[0]
                y_max = y_min+self.pause_button.size[1]
                if x_max > event.pos[0] > x_min and y_max > event.pos[1] > y_min:
                    self.paused = not self.paused



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
        if not self.paused:
            self.pause_button.text = "pause"
            self.spaceship.move()
            for bullet in self.bullets:
                bullet.move()
            for trio in self.answers:
                for answer in trio:
                    answer.move()
            self.check_collisions()

            self.correct_box.update_text(f"correct: {self.correct}")
            self.incorrect_box.update_text(f"incorrect: {self.incorrect}")
        else:
            self.pause_button.text = "Play"

        if self.correct >= (self.level+10):
            self.level += 10
            for trio in self.answers:
                for answer in trio:
                    answer.velocity += (0, 0.1)

        for trio in self.answers:
            if len(trio)!=0:
                if trio[0].position.y == HEIGHT-20:
                    self.answers.append([Answer((random.randint(0,333), 0)),
                                         Answer((random.randint(333,666), 0)),
                                         Answer((random.randint(666,1000), 0))
                                         ])
            else:
                self.game_over=True

    def draw_game_elements(self):
        if self.game_over:
            if self.play_sound:
                self.play_sound = False
                self.gameover_sound.play()
            self.screen.fill((0, 0, 0))
            gameover_text = TextBox("GAME OVER",(200,200),100,(255,0,0))
            self.calc_percent()
            percentage_text = TextBox(f"percentage correct: {self.percentage}%",(200,300),24,(0,255,0))
            self.correct_box.position, self.correct_box.font_size, self.correct_box.color =(200,350),24,(0,255,0)
            gameover_text.draw(self.screen)
            percentage_text.draw(self.screen)
            self.correct_box.draw(self.screen)
        else:
            self.screen.blit(self.background, (0, 0))
            self.spaceship.draw(self.screen)
            for bullet in self.bullets:
                bullet.draw(self.screen)
            for trio in self.answers:
                for answer in trio:
                    answer.draw(self.screen)

            self.correct_box.draw(self.screen)
            self.incorrect_box.draw(self.screen)
            self.instruction_box.draw(self.screen)
            self.pause_button.draw(self.screen)

            self.clock.tick(100)
        pygame.display.flip()

    def check_collisions(self):
        # check bullet and answer
        for bullet in self.bullets[:]:  # copy of the list to avoid errors
            for trio in self.answers[:]:
                for answer in trio:
                    if bullet.collides_with(answer):
                        self.bullets.remove(bullet)
                        trio.remove(answer)
                        if answer.correct:
                            self.correct += 1
                            self.correct_box.text_color = (0,255,0)
                        else:
                            self.incorrect += 1
                            self.correct_box.text_color = (255, 0, 0)
                        break
        # check correct answer and bottom
        for trio in self.answers[:]:
            if len(trio)!=0:
                if trio[0].position.y >= HEIGHT + 50:
                    for answer in trio:
                        if answer.correct:
                            self.game_over = True

                    self.answers.remove(trio)

                    print("GAME OVER reached bottom")
                    print(self.correct)
            else:
                self.game_over=True

    def set_color(self, color="red"):
        self.background = load_image(color, (WIDTH, HEIGHT))

    def set_sound(self, sound="click"):
        self.spaceship.shoot_sound = load_sound(sound)

    def calc_percent(self):
        self.percentage = round(self.correct / (self.correct + self.incorrect), 1)


if __name__ == "__main__":
    game = Game()
    game.main_loop()
