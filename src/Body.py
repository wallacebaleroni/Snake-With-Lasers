# Directions constraints
CONST_UP = 0
CONST_RIGHT = 1
CONST_DOWN = 2
CONST_LEFT = 3

CONST_HEAD = 1
CONST_BODY = 2
CONST_TAIL = 3


class Body:
    curve = False
    pos_x = 0
    pos_y = 0

    def __init__(self, pos_x, pos_y):
        self.direction = direction
        self.pos_x = pos_x
        self.pos_y = pos_y
