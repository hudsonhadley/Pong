import pygame
from settings import WINDOW_SIZE, PADDLE_SPEED


class Paddle(pygame.sprite.Sprite):
    def __init__(self, fg_color, bg_color, width, height):
        super().__init__()
        # store width and height as percent of window
        self.width = width / WINDOW_SIZE.width
        self.height = height / WINDOW_SIZE.height

        # store foreground and background colors
        self.fg_color = fg_color
        self.bg_color = bg_color

        # describe the appearance of the background
        self.image = pygame.Surface([width, height])
        self.image.fill(bg_color)
        self.image.set_colorkey(bg_color)

        # draw this paddle on top of the background
        pygame.draw.rect(self.image, fg_color, [0, 0, width, height])
        self.rect = self.image.get_rect()

    def moveUp(self):
        # move in the desired direction
        self.rect.y -= PADDLE_SPEED

        # make sure you haven't gone too far
        if self.rect.y < 0:
            self.rect.y = 0

    def moveDown(self):
        # move in the desired direction
        self.rect.y += PADDLE_SPEED

        # make sure you haven't gone too far
        if self.rect.y > WINDOW_SIZE.height * (1 - self.height):
            self.rect.y = int(WINDOW_SIZE.height * (1 - self.height))
