import pygame

# import threading module to allow the AI to process in parallel
from threading import Thread

# import deque to store ball history from most recent to most dated
from collections import deque

# import paddle and ball sprites from other files
from paddle import Paddle
from ball import Ball

# import constants from the settings file
from settings import Point
from settings import SCORE_COOLDOWN
from settings import BLACK, GREEN
from settings import WINDOW_SIZE, PADDLE_SIZE, BALL_SIZE, NET_SIZE, FONT_SIZE

# import desired artificial intelligence as ai
from pong_ai import moderate_ai as game_ai

pygame.init()

# create the game window and make it fullscreen
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("COMP 155 | Pong")

# add paddles and ball to the window and position them
paddleA = Paddle(GREEN, BLACK, PADDLE_SIZE.width, PADDLE_SIZE.height)
paddleA.rect.x = BALL_SIZE.width - 1
paddleA.rect.y = (WINDOW_SIZE.height - PADDLE_SIZE.height) // 2

paddleB = Paddle(GREEN, BLACK, PADDLE_SIZE.width, PADDLE_SIZE.height)
paddleB.rect.x = WINDOW_SIZE.width - PADDLE_SIZE.width - BALL_SIZE.width + 1
paddleB.rect.y = (WINDOW_SIZE.height - PADDLE_SIZE.height) // 2

ball = Ball(GREEN, BLACK, BALL_SIZE.width, BALL_SIZE.height)
ball.rect.x = (WINDOW_SIZE.width // 2 - BALL_SIZE.width)
ball.rect.y = (WINDOW_SIZE.height // 2 - BALL_SIZE.height)



# Create a sprite group containing all of our game sprites
core_sprites = pygame.sprite.Group()
core_sprites.add(paddleA)
core_sprites.add(paddleB)
core_sprites.add(ball)

# prepare the main game loop
playing = True

# define a game clock to control how fast the game updates
clock = pygame.time.Clock()

# initialize player scores
scoreA = 0
scoreB = 0
last_score = pygame.time.get_ticks()

# initialize AI variables
t = None  # thread for handling AI decision-making
ball_history = deque()  # all ball coordinates since last paddle/point bounce

# define the main game loop
while playing:
    # handle different events that can occur
    for event in pygame.event.get():  # Check user-generated events
        if event.type == pygame.QUIT:  # if the user tried to quit
            playing = False  # exit after finishing this loop

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:  # pressing X closes the game
                playing = False

            elif event.key == pygame.K_ESCAPE:  # pressing ESC closes game too
                playing = False

    # separately handle control keys that may be held
    # in the single player version the player can use UP/DOWN or W/S
    keys = pygame.key.get_pressed()

    if keys[pygame.K_w] or keys[pygame.K_UP]:  # check the UP/W key
        paddleA.moveUp()

    if keys[pygame.K_s] or keys[pygame.K_DOWN]:  # check the DOWN/S key
        paddleA.moveDown()

    # give the AI an opportunity make its move
    if (t is None or not t.is_alive()) and len(ball_history) > 1:
        pdl_coord = Point(paddleB.rect.x, paddleB.rect.y + PADDLE_SIZE.height / 2)

        t = Thread(target=game_ai, args=(ball_history, pdl_coord, paddleB))
        t.start()

    # Game Logic
    core_sprites.update()

    # Check if the ball has collided with the right-hand window border
    if ball.rect.x >= WINDOW_SIZE.width - BALL_SIZE.width:

        # check if enough time has passed and if so score a point
        if (pygame.time.get_ticks() - last_score) > SCORE_COOLDOWN:
            last_score = pygame.time.get_ticks()
            scoreA += 1

        ball.velocity[0] *= -1
        ball_history.clear()  # reset history after each score

    # Check if the ball has collided with the left-hand window border
    if ball.rect.x <= 0:

        # check if enough time has passed and if so score a point
        if (pygame.time.get_ticks() - last_score) > SCORE_COOLDOWN:
            last_score = pygame.time.get_ticks()
            scoreB += 1

        ball.velocity[0] *= -1
        ball_history.clear()  # reset history after each score

    # Check if the ball has collided with the bottom of the screen
    if ball.rect.y >= WINDOW_SIZE.height - BALL_SIZE.height:
        ball.velocity[1] *= -1

    # Check if the ball has collided with the top of the screen
    if ball.rect.y < 0:
        ball.velocity[1] *= -1

    # Detect collisions between the ball and the paddles
    if pygame.sprite.collide_mask(ball, paddleA) or \
            pygame.sprite.collide_mask(ball, paddleB):
        ball.bounce()
        ball_history.clear()  # reset history after each hit

    # Update ball location history, so it can be provided to the AI
    coord = Point(ball.rect.x + BALL_SIZE.width / 2, ball.rect.y + BALL_SIZE.height / 2)
    ball_history.appendleft(coord)

    # Rendering Logic
    screen.fill(BLACK)

    # draw a line from point a to point b c pixels wide
    pygame.draw.line(screen, GREEN,
                     [WINDOW_SIZE.width // 2, 0],
                     [WINDOW_SIZE.width // 2, WINDOW_SIZE.height],
                     NET_SIZE.width)

    # redraw updated versions of each sprite on the screen
    core_sprites.draw(screen)

    # Display scores:
    # define the font that will be used for the scores
    font = pygame.font.Font(None, FONT_SIZE)

    # render scores using this font
    scoreboardA = font.render(str(scoreA), 1, GREEN)
    scoreboardB = font.render(str(scoreB), 1, GREEN)

    # position scores on the screen above each side
    screen.blit(scoreboardA,
                (WINDOW_SIZE.width // 4 - FONT_SIZE // 2,
                 int(0.02 * WINDOW_SIZE.height)))

    screen.blit(scoreboardB,
                ((3 * WINDOW_SIZE.width) // 4 - FONT_SIZE // 2,
                 int(0.02 * WINDOW_SIZE.height)))

    # update the screen with everything that has been drawn
    pygame.display.flip()

    # use the clock to cap-out at 60 frames per second
    clock.tick(60)

# if we reach this point the game is over, perform clean up and exit
pygame.quit()
