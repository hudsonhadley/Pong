import pygame
from random import randint
from settings import BALL_DELTA_X, BALL_DELTA_Y
from settings import BOUNCE_COOLDOWN, BALL_ACCELERATION

class Ball(pygame.sprite.Sprite):
    def __init__(self, fg_color, bg_color, width, height):
        super().__init__()
        # track number of bounces to accelerate ball over time
        self.bounces = 0
        self.last_bounce = pygame.time.get_ticks()


        # describe the appearance of the background
        self.image = pygame.Surface([width,height])
        self.image.fill(bg_color)
        self.image.set_colorkey(bg_color)


        # draw the ball (a rectangle) over the background
        pygame.draw.rect(self.image, fg_color, [0, 0, width, height])


        self.velocity = [randint(*BALL_DELTA_X), randint(*BALL_DELTA_Y)]
        self.rect = self.image.get_rect()



    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]



    def bounce(self):
        if (pygame.time.get_ticks() - self.last_bounce) > BOUNCE_COOLDOWN:
            self.last_bounce = pygame.time.get_ticks()

            # increment the number of times the ball has bounced
            self.bounces += 1

            # change the direction of the ball
            self.velocity[0] *= -1

            # accelerate the ball based to total number of bounces
            self.velocity[0] += int(BALL_ACCELERATION * self.bounces)
            self.velocity[1] = randint(*BALL_DELTA_Y)
