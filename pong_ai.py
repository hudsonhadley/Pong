from settings import WINDOW_SIZE
from random import randint
from settings import PADDLE_SPEED
from math import sqrt


# Description:
#    Easy AI moves in the current direction of the ball on the y coordinate
#    in other words it naively assumes the ball won't hit the top or bottom and
#    simply moves up and down to match its position.
# INPUTS:
#    ball_history -- a list of ball coordinates from most to least recent
#                    this list always includes at least 2 coordinates.
#    paddle_coord -- x,y coordinates of the front middle of the AIs paddle
#    paddle       -- a reference to the paddle on which to call moveUP/moveDown
def easy_ai(ball_history, paddle_coord, paddle):
    # get the ball's current location (first item in ball_history)
    ball_coord = ball_history[0]
    # if the ball is currently above the middle of the paddle, move up
    if ball_coord.y < paddle_coord.y:
        paddle.moveUp()
    # if the ball is below the middle of the paddle, move down
    elif ball_coord.y > paddle_coord.y:
        paddle.moveDown()
    # if the paddle is on the same level as the ball don't move
    else:
        pass


def predict_ball_y(ball_history, paddle):
    last = ball_history[1]
    current = ball_history[0]

    m = (current.y - last.y) / (current.x - last.x)

    predicted_y = m * (WINDOW_SIZE.width - paddle.width - current.x) + current.y
    bounces = predicted_y // WINDOW_SIZE.height
    predicted_y %= WINDOW_SIZE.height

    if bounces % 2 == 1:
        predicted_y = WINDOW_SIZE.height - predicted_y

    return predicted_y


# Description:
#    
# INPUTS:
#    ball_history -- a list of ball coordinates from most to least recent
#                    this list always includes at least 2 coordinates.
#    paddle_coord -- x,y coordinates of the front middle of the AIs paddle
#    paddle       -- a reference to the paddle on which to call moveUP/moveDown
def moderate_ai(ball_history, paddle_coord, paddle):
    # NOTE: YOUR IMPLEMENTATION GOES HERE
    current = ball_history[0]

    offset = int(abs(paddle_coord.x - current.x)) // 4
    predicted_y = predict_ball_y(ball_history, paddle) + randint(-offset, offset)

    if current.x < int(WINDOW_SIZE.width * 0.8):
        if paddle_coord.y - current.y > PADDLE_SPEED:
            paddle.moveUp()

        # if the ball is below the middle of the paddle, move down
        elif current.y - paddle_coord.y > PADDLE_SPEED:
            paddle.moveDown()

        # if the paddle is on the same level as the ball don't move
        else:
            pass

    else:
        if paddle_coord.y - predicted_y > PADDLE_SPEED + offset:
            paddle.moveUp()

        # if the ball is below the middle of the paddle, move down
        elif predicted_y - paddle_coord.y > PADDLE_SPEED + offset:
            paddle.moveDown()

        # if the paddle is on the same level as the ball don't move
        else:
            pass


# Description:
#
# INPUTS:
#    ball_history -- a list of ball coordinates from most to least recent
#                    this list always includes at least 2 coordinates.
#    paddle_coord -- x,y coordinates of the front middle of the AIs paddle
#    paddle       -- a reference to the paddle on which to call moveUP/moveDown
def hard_ai(ball_history, paddle_coord, paddle):
    # NOTE: YOUR IMPLEMENTATION GOES HERE

    # If it's moving backwards, bring it back to the middle
    if ball_history[0].x < ball_history[1].x:
        if WINDOW_SIZE.height // 2 - paddle_coord.y > PADDLE_SPEED:
            paddle.moveDown()

        elif paddle_coord.y - WINDOW_SIZE.height // 2 > PADDLE_SPEED:
            paddle.moveUp()

    else:
        predicted_y = predict_ball_y(ball_history, paddle)

        if paddle_coord.y - predicted_y > PADDLE_SPEED:
            paddle.moveUp()

        # if the ball is below the middle of the paddle, move down
        elif predicted_y - paddle_coord.y > PADDLE_SPEED:
            paddle.moveDown()

        # if the paddle is on the same level as the ball don't move
        else:
            pass


def distance(p1, p2):
    return sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)
