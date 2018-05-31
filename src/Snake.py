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

CONST_WINDOW_H = 0
CONST_WINDOW_W = 0

CONST_GRID_SIZE_X = 0
CONST_GRID_SIZE_Y = 0

CONST_GRID_LENGTH_X = 0
CONST_GRID_LENGTH_Y = 0

CONST_HEAD_PATH = "..\img\head.png"
CONST_BODY_PATH = "..\img\/body.png"
CONST_TAIL_PATH = "..\img\/tail.png"
CONST_LASER_PATH = "..\img\/laser.png"


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
    speed = 100

    # Corpo da cobra
    bodies = []

    def __init__(self, window_w, window_h, size_grid_x, size_grid_y):
        # Constants
        global CONST_GRID_SIZE_X
        global CONST_GRID_SIZE_Y
        CONST_GRID_SIZE_X = size_grid_x
        CONST_GRID_SIZE_Y = size_grid_y

        global CONST_GRID_LENGTH_X
        global CONST_GRID_LENGTH_Y
        CONST_GRID_LENGTH_X = window_w / size_grid_x
        CONST_GRID_LENGTH_Y = window_h / size_grid_y

        global CONST_WINDOW_H
        global CONST_WINDOW_W
        CONST_WINDOW_H = window_h
        CONST_WINDOW_W = window_w

        # Initializations
        # Creating snake's parts and initializating it's positions and headings
        start_pos_grid = [int(size_grid_x / 2), int(size_grid_y / 2)]
        self.head = Body(Sprite(CONST_HEAD_PATH, 4), CONST_UP, start_pos_grid)

        body_pos_grid = [start_pos_grid[X], start_pos_grid[Y] + 1]
        body = Body(Sprite(CONST_BODY_PATH, 8), CONST_UP, body_pos_grid)
        self.bodies.append(body)

        tail_pos_grid = [body_pos_grid[X], body_pos_grid[Y] + 1]
        self.tail = Body(Sprite(CONST_TAIL_PATH, 4), CONST_UP, tail_pos_grid)

        # Self explanatory
        self.keyboard = Keyboard()

        # Flags
        self.direction_input_got = False
        self.increase_size_flag = False
        self.shot_flag = False

        # Time variables
        self.current_time = 0
        self.last_move = 0
        self.last_append = 0
        self.last_shot = 0

        # Shots variables
        self.shots = []
        self.shot_cadence = 200

    def run(self, total_time):
        self.current_time = total_time

        self.get_input()
        # Checks if the necessary time has already passed
        if self.current_time - self.last_move >= self.speed:
            self.check_borders()
            self.move()

            self.last_move = self.current_time  # Updates last move
            self.direction_input_got = False  # Allowed to get the next input
        # TODO: interactions()
        self.increase_size()
        self.shot()

    def get_input(self):
        if not self.direction_input_got:
            # Directionals
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

            # Temporary key to increase size
            if self.keyboard.key_pressed("k"):
                if self.current_time - self.last_append >= 500:
                    self.increase_size_flag = True
                    self.last_append = self.current_time

        # Shot key
        if self.keyboard.key_pressed("space"):
            self.shot_flag = True

    def check_borders(self):
        if self.head.pos_grid[X] < 0:
            self.head.pos_grid[X] = 20
            self.head.pos_pixel = to_pixel(self.head.pos_grid)
        elif self.head.pos_grid[X] >= CONST_GRID_SIZE_X:
            self.head.pos_grid[X] = -1
            self.head.pos_pixel = to_pixel(self.head.pos_grid)
        elif self.head.pos_grid[Y] < 0:
            self.head.pos_grid[Y] = 20
            self.head.pos_pixel = to_pixel(self.head.pos_grid)
        elif self.head.pos_grid[Y] >= CONST_GRID_SIZE_Y:
            self.head.pos_grid[Y] = -1
            self.head.pos_pixel = to_pixel(self.head.pos_grid)

    def move(self):
        # Updates tail position
        self.tail.set_position(self.bodies[len(self.bodies) - 1].sprite.x,
                               self.bodies[len(self.bodies) - 1].sprite.y)

        # Updates bodies positions
        for i in range(len(self.bodies) - 1, -1, -1):
            if i == 0:  # If it's the neck (i.e. first body part after head)
                self.bodies[i].set_position(self.head.sprite.x, self.head.sprite.y)
            else:  # Rest of the body
                self.bodies[i].set_position(self.bodies[i - 1].sprite.x, self.bodies[i - 1].sprite.y)

        # Updates head position and changes the frame to the appropriate one
        if self.head.direction == CONST_UP:
            self.head.set_curr_frame(CONST_UP)
            self.head.pos_grid[Y] -= 1
        elif self.head.direction == CONST_DOWN:
            self.head.set_curr_frame(CONST_DOWN)
            self.head.pos_grid[Y] += 1
        elif self.head.direction == CONST_LEFT:
            self.head.set_curr_frame(CONST_LEFT)
            self.head.pos_grid[X] -= 1
        elif self.head.direction == CONST_RIGHT:
            self.head.set_curr_frame(CONST_RIGHT)
            self.head.pos_grid[X] += 1
        self.head.pos_pixel = to_pixel(self.head.pos_grid)

        self.head.set_position(self.head.pos_pixel[X], self.head.pos_pixel[Y])

        # Updates tail direction and changes the frame to the appropriate one
        frame = self.bodies[len(self.bodies) - 1].direction
        self.tail.set_curr_frame(frame)
        self.tail.direction = self.bodies[len(self.bodies) - 1].direction

        # Updates bodies directions and changes the frames to the appropriate ones
        for i in range(len(self.bodies) - 1, -1, -1):
            # If it's the neck (i.e. first body part after head)
            if i == 0:
                frame = self.decide_frame(self.bodies[i].direction, self.head.direction)
                self.bodies[i].set_curr_frame(frame)
                self.bodies[i].direction = self.head.direction
            # Rest of the body
            else:
                frame = self.decide_frame(self.bodies[i].direction, self.bodies[i - 1].direction)
                self.bodies[i].set_curr_frame(frame)
                self.bodies[i].direction = self.bodies[i - 1].direction

    def shot(self):
        if self.shot_flag and self.current_time - self.last_shot >= self.shot_cadence:
            # Create shot sprite
            new_shot = Laser(self.head, self.current_time)
            self.shots.append(new_shot)
            # Create it in front of the head
            self.shot_flag = False
            self.last_shot = self.current_time

        # Move shots
        for i in range(len(self.shots)):
            self.shots[i].run(self.current_time)

        # Shots cleaning
        for i in range(len(self.shots)):
            if self.shots[i].sprite.x >= CONST_WINDOW_W:
                pass

    def draw(self):
        # Draw head
        self.head.draw()
        # Draw bodies
        for i in range(len(self.bodies)):
            self.bodies[i].draw()
        # Draw tail
        self.tail.draw()
        # Draw shots
        for i in range(len(self.shots)):
            self.shots[i].draw()

    def increase_size(self):
        # TODO improve it
        if self.increase_size_flag:
            self.bodies.append(Body(Sprite(CONST_BODY_PATH, 8), CONST_UP, self.head.pos_grid))

            self.increase_size_flag = False

    def get_size(self):
        return len(self.bodies)

    @staticmethod
    def decide_frame(curr, next):
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

    def set_position(self, x, y):
        self.sprite.set_position(x, y)

    def set_curr_frame(self, frame):
        self.sprite.set_curr_frame(frame)

    def draw(self):
        self.sprite.draw()


class Laser:
    def __init__(self, head: Body, current_time):
        # Initializations
        self.sprite = Sprite(CONST_LASER_PATH, 8)
        self.direction = head.direction

        # Sets apropriate frame
        if self.direction == CONST_UP:
            self.sprite.set_curr_frame(CONST_UP)
        elif self.direction == CONST_DOWN:
            self.sprite.set_curr_frame(CONST_DOWN)
        elif self.direction == CONST_LEFT:
            self.sprite.set_curr_frame(CONST_LEFT)
        elif self.direction == CONST_RIGHT:
            self.sprite.set_curr_frame(CONST_RIGHT)

        # Initial position is after the head
        if self.direction == CONST_UP:
            self.pos_grid = [head.pos_grid[X], head.pos_grid[Y] - 1]
        elif self.direction == CONST_DOWN:
            self.pos_grid = [head.pos_grid[X], head.pos_grid[Y] + 1]
        elif self.direction == CONST_LEFT:
            self.pos_grid = [head.pos_grid[X] - 1, head.pos_grid[Y]]
        elif self.direction == CONST_RIGHT:
            self.pos_grid = [head.pos_grid[X] + 1, head.pos_grid[Y]]
        self.pos_pixel = to_pixel(self.pos_grid)

        self.sprite.set_position(self.pos_pixel[X], self.pos_pixel[Y])

        # Time control
        self.total_time = current_time
        self.current_time = 0
        self.delta_time = 0

        # Self explanatory
        self.speed = 0.3

    def run(self, current_time):
        self.delta_time = current_time - self.total_time
        self.total_time = current_time

        self.move()
        self.update_frames()

    def move(self):
        # Moves the shot depending on it's direction
        if self.direction == CONST_UP:
            self.sprite.set_position(self.sprite.x, self.sprite.y - self.speed * self.delta_time)
        elif self.direction == CONST_DOWN:
            self.sprite.set_position(self.sprite.x, self.sprite.y + self.speed * self.delta_time)
        elif self.direction == CONST_LEFT:
            self.sprite.set_position(self.sprite.x - self.speed * self.delta_time, self.sprite.y)
        elif self.direction == CONST_RIGHT:
            self.sprite.set_position(self.sprite.x + self.speed * self.delta_time, self.sprite.y)

    def update_frames(self):
        curr_frame = self.sprite.get_curr_frame()
        if curr_frame > 3:
            self.sprite.set_curr_frame(curr_frame - 4)
        else:
            self.sprite.set_curr_frame(curr_frame + 4)

    def draw(self):
        self.sprite.draw()
