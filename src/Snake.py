from PPlay.keyboard import *
from PPlay.sprite import *
from src.Body import *

# Directions constraints
CONST_UP = 0
CONST_RIGHT = 1
CONST_DOWN = 2
CONST_LEFT = 3

CONST_DOWN_RIGHT = 4
CONST_DOWN_LEFT = 5
CONST_UP_LEFT = 6
CONST_UP_RIGHT = 7

CONST_SPRITE_W = 25
CONST_SPRITE_H = 25

X = 0
Y = 1

CONST_GRID_SIZE_X = 0
CONST_GRID_SIZE_Y = 0

CONST_GRID_LENGTH_X = 0
CONST_GRID_LENGTH_Y = 0

CONST_HEAD_PATH = "..\img\head.png"
CONST_BODY_PATH = "..\img\/body.png"
CONST_TAIL_PATH = "..\img\/tail.png"


def to_grid(pos_pixel):
    return [pos_pixel[X] / CONST_GRID_LENGTH_X, pos_pixel[Y] / CONST_GRID_LENGTH_Y]


def to_pixel(pos_grid):
    return [pos_grid[X] * CONST_GRID_LENGTH_X, pos_grid[Y] * CONST_GRID_LENGTH_Y]


class Snake:
    # Objetos do PPlay/janela
    window_w = None
    window_h = None
    head = None
    keyboard = None

    # Variaveis de espaco
    speed = 200

    # Corpo da cobra
    bodies = []

    # Controle de tempo
    total_time = 0
    last_move = 0
    last_append = 0

    def __init__(self, window_w, window_h, size_grid_x, size_grid_y):
        global CONST_GRID_SIZE_X
        global CONST_GRID_SIZE_Y
        CONST_GRID_SIZE_X = size_grid_x
        CONST_GRID_SIZE_Y = size_grid_y

        global CONST_GRID_LENGTH_X
        global CONST_GRID_LENGTH_Y
        CONST_GRID_LENGTH_X = window_w / size_grid_x
        CONST_GRID_LENGTH_Y = window_h / size_grid_y

        self.window_h = window_h
        self.window_w = window_w

        start_pos_grid = [int(size_grid_x / 2), int(size_grid_y / 2)]
        self.head = Body(Sprite(CONST_HEAD_PATH, 4), CONST_UP, start_pos_grid)

        body_pos_grid = [start_pos_grid[X], start_pos_grid[Y] + 1]
        body = Body(Sprite(CONST_BODY_PATH, 8), CONST_UP, body_pos_grid)
        self.bodies.append(body)

        tail_pos_grid = [body_pos_grid[X], body_pos_grid[Y] + 1]
        self.tail = Body(Sprite(CONST_TAIL_PATH, 4), CONST_UP, tail_pos_grid)

        self.keyboard = Keyboard()

        self.direction_input_got = False

    def run(self, total_time):
        self.get_input()
        self.total_time = total_time
        self.move()

    def move(self):
        if self.total_time - self.last_move >= self.speed:
            self.check_border()
            self.move_body()
            self.move_head()
            self.update_bodies_frames()

            self.last_move = self.total_time

            # Able to get the next input
            self.direction_input_got = False

    def move_head(self):
        # Changes frame to the appropriate one and moves in the grid
        if self.head.direction == CONST_UP:
            self.head.sprite.set_curr_frame(CONST_UP)
            self.head.pos_grid[Y] -= 1
            self.head.pos_pixel[Y] -= CONST_GRID_LENGTH_Y
        elif self.head.direction == CONST_DOWN:
            self.head.sprite.set_curr_frame(CONST_DOWN)
            self.head.pos_grid[Y] += 1
            self.head.pos_pixel[Y] += CONST_GRID_LENGTH_Y
        elif self.head.direction == CONST_LEFT:
            self.head.sprite.set_curr_frame(CONST_LEFT)
            self.head.pos_grid[X] -= 1
            self.head.pos_pixel[X] -= CONST_GRID_LENGTH_X
        elif self.head.direction == CONST_RIGHT:
            self.head.sprite.set_curr_frame(CONST_RIGHT)
            self.head.pos_pixel[X] += CONST_GRID_LENGTH_X
            self.head.pos_grid[X] += 1

        self.head.sprite.set_position(self.head.pos_pixel[X], self.head.pos_pixel[Y])

    def move_body(self):
        # Updates tail position
        self.tail.sprite.set_position(self.bodies[len(self.bodies) - 1].sprite.x,
                                      self.bodies[len(self.bodies) - 1].sprite.y)

        # Updates bodies position
        for i in range(len(self.bodies) - 1, -1, -1):
            if i == 0:
                # It's the neck
                self.bodies[i].sprite.set_position(self.head.sprite.x, self.head.sprite.y)
            else:
                # Rest of the body
                self.bodies[i].sprite.set_position(self.bodies[i - 1].sprite.x, self.bodies[i - 1].sprite.y)

    def update_bodies_frames(self):
        # Updates tail direction and frame
        frame = self.bodies[len(self.bodies) - 1].direction
        self.tail.sprite.set_curr_frame(frame)
        self.tail.direction = self.bodies[len(self.bodies) - 1].direction

        # Updates bodies directions and frames
        for i in range(len(self.bodies) - 1, -1, -1):
            if i == 0:
                # It's the neck
                frame = self.decide_frame(self.bodies[i].direction, self.head.direction)
                print("curr:" + str(self.bodies[i].direction), "next: " + str(self.head.direction), "frame: " + str(frame))
                self.bodies[i].sprite.set_curr_frame(frame)
                self.bodies[i].direction = self.head.direction
            else:
                frame = self.decide_frame(self.bodies[i].direction, self.bodies[i - 1].direction)
                self.bodies[i].sprite.set_curr_frame(frame)
                self.bodies[i].direction = self.bodies[i - 1].direction

    def check_border(self):
        if self.head.pos_grid[X] < 0:
            self.head.pos_grid[X] = 20
            self.head.pos_pixel = to_pixel(self.head.pos_grid)
        elif self.head.pos_grid[X] >= CONST_GRID_SIZE_X:
            self.head.pos_grid[X] = 0
            self.head.pos_pixel = to_pixel(self.head.pos_grid)
        elif self.head.pos_grid[Y] < 0:
            self.head.pos_grid[Y] = 20
            self.head.pos_pixel = to_pixel(self.head.pos_grid)
        elif self.head.pos_grid[Y] >= CONST_GRID_SIZE_Y:
            self.head.pos_grid[Y] = 0
            self.head.pos_pixel = to_pixel(self.head.pos_grid)

    def get_input(self):
        if not self.direction_input_got:
            if self.keyboard.key_pressed("w") and self.head.direction != CONST_DOWN:
                self.direction_input_got = True
                self.head.direction = CONST_UP
            elif self.keyboard.key_pressed("s") and self.head.direction != CONST_UP:
                self.direction_input_got = True
                self.head.direction = CONST_DOWN
            elif self.keyboard.key_pressed("a") and self.head.direction != CONST_RIGHT:
                self.direction_input_got = True
                self.head.direction = CONST_LEFT
            elif self.keyboard.key_pressed("d") and self.head.direction != CONST_LEFT:
                self.direction_input_got = True
                self.head.direction = CONST_RIGHT

            if self.keyboard.key_pressed("k"):
                self.direction_input_got = True
                if self.total_time - self.last_append >= 500:
                    self.increase_size()
                    self.last_append = self.total_time

    def draw(self):
        self.head.sprite.draw()
        for i in range(len(self.bodies)):
            self.bodies[i].sprite.draw()
        self.tail.sprite.draw()

    def increase_size(self):
        # TODO improve it
        self.bodies.append(Body(Sprite(CONST_BODY_PATH, 8), CONST_UP, self.head.pos_grid))

    def get_size(self):
        return len(self.bodies)

    def decide_frame(self, curr, next):
        if curr == next:
            return curr
        elif (curr == CONST_UP and next == CONST_RIGHT
                or curr == CONST_LEFT and next == CONST_DOWN):
            return CONST_DOWN_RIGHT
        elif (curr == CONST_RIGHT and next == CONST_DOWN
              or curr == CONST_UP and next == CONST_LEFT):
            return CONST_DOWN_LEFT
        elif (curr == CONST_RIGHT and next == CONST_UP
              or curr == CONST_DOWN and next == CONST_LEFT):
            return CONST_UP_LEFT
        elif (curr == CONST_DOWN and next == CONST_RIGHT
              or curr == CONST_LEFT and next == CONST_UP):
            return CONST_UP_RIGHT


class Body:
    sprite = None
    direction = None
    pos_grid = []
    pos_pixel = []

    def __init__(self, sprite, direction, pos_grid):
        self.sprite = sprite
        self.direction = direction
        self.pos_grid = pos_grid
        self.pos_pixel = to_pixel(pos_grid)

        self.sprite.set_position(self.pos_pixel[X], self.pos_pixel[Y])
