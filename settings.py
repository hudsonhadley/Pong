from collections import namedtuple

import pygetwindow

# Define the concept of an x, y point
Point = namedtuple('Point', ('x', 'y'))

# Define the concept of a rgb color
Color = namedtuple('Color', ('r', 'g', 'b'))

# Define the concept of a width, height size
Size = namedtuple('Size', ('width', 'height'))

# Deine the concept of an integer range (inclusive)
Range = namedtuple('Range', ('min', 'max'))


# --- COLOR CONSTANTS ---
BLACK = Color(0, 0, 0)
WHITE = Color(255, 255, 255)
GREEN = Color(0, 255, 0)


# --- SIZE CONSTANTS ---
# Width and height of the display window in pixels
WINDOW_SIZE = Size(1064, 576)


# Width and height of each paddle in pixels
PADDLE_SIZE = Size(int(0.008 * WINDOW_SIZE.width),
                   int(0.175 * WINDOW_SIZE.height))


# Width and height of the ball in pixels
BALL_SIZE = Size(int(0.012 * WINDOW_SIZE.width),
                 int(0.012 * WINDOW_SIZE.width))


# Width and height of the "net" in pixels
NET_SIZE = Size(int(0.008 * WINDOW_SIZE.width), WINDOW_SIZE.height)
FONT_SIZE = int(0.15 * WINDOW_SIZE.height)



# --- SPEED AND RULE CONSTANTS ---
# Number of pixels the paddle moves up or down each time it is moved
PADDLE_SPEED = int(0.010 * WINDOW_SIZE.height)


# Minimum and maximum number of pixels the ball moves left/right per frame
BALL_DELTA_X = Range(int(0.005 * WINDOW_SIZE.width),
                     int(0.010 * WINDOW_SIZE.width))


# Minimum and maximum number of pixels the ball moves up/down per frame
BALL_DELTA_Y = Range(int(0.016 * WINDOW_SIZE.height) * -1,
                     int(0.016 * WINDOW_SIZE.height))


SCORE_COOLDOWN = 500  # minimum milliseconds between points scored
BOUNCE_COOLDOWN = 500  # minimum milliseconds between bounces
BALL_ACCELERATION = 0.1  # added to ball delta x after each second of game time
