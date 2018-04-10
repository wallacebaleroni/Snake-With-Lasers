CONST_UP = 1
CONST_DOWN = 2
CONST_LEFT = 3
CONST_RIGHT = 4


class Body:
    direction = CONST_UP
    curve = False
    pos_x = 0
    pos_y = 0

    def __init__(self, direction, pos_x, pos_y):
        self.direction = direction
        self.pos_x = pos_x
        self.pos_y = pos_y
