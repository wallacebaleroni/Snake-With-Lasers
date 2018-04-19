from PPlay.keyboard import *
from PPlay.sprite import *
from src.Body import *

# Directions constraints
CONST_UP = 1
CONST_DOWN = 2
CONST_LEFT = 3
CONST_RIGHT = 4

CONST_SPRITE_W = 25
CONST_SPRITE_H = 25

X = 0
Y = 1

global CONST_GRID_SIZE_X
global CONST_GRID_SIZE_Y

global CONST_GRID_LENGHT_X
global CONST_GRID_LENGHT_Y


class Snake:
    # Objetos do PPlay/janela
    window_w = None
    window_h = None
    sprite = None
    keyboard = None

    # Variaveis de espaco
    direction = CONST_RIGHT
    speed = 100
    pos_grid = []
    pos_pixel = []

    # Corpo da cobra
    head = None
    bodies = []
    tail = None

    # Controle de tempo
    total_time = 0
    last_move = 0
    last_append = 0

    def __init__(self, window_w, window_h, size_grid_x, size_grid_y):
        CONST_GRID_SIZE_X = size_grid_x
        CONST_GRID_SIZE_Y = size_grid_y

        LENGHT_GRID_X = window_w / size_grid_x
        LENGHT_GRID_Y = window_h / size_grid_y

        self.pos_grid = [int(size_grid_x / 2), int(size_grid_y / 2)]

        self.pos_pixel = self.to_pixel(self.pos_grid)

        self.window_h = window_h
        self.window_w = window_w

        self.sprite = Sprite("img\snake_temp.png", 1)
        self.sprite.set_total_duration(1000)

        self.bodies.append(Body(CONST_RIGHT, 50, 50))
        self.keyboard = Keyboard()

    def run(self, total_time):
        self.get_input()
        self.total_time = total_time
        self.move()

    def move(self):
        self.check_border()

        if self.total_time - self.last_move >= self.speed:
            if self.direction == CONST_UP:
                self.pos_grid[Y] -= 1
                self.pos_pixel[Y] -= CONST_GRID_LENGHT_Y
            elif self.direction == CONST_DOWN:
                self.pos_grid[Y] += 1
                self.pos_pixel[Y] += CONST_GRID_LENGHT_Y
            elif self.direction == CONST_LEFT:
                self.pos_grid[X] -= 1
                self.pos_pixel[X] -= CONST_GRID_LENGHT_X
            elif self.direction == CONST_RIGHT:
                self.pos_pixel[X] += CONST_GRID_LENGHT_X
                self.pos_grid[X] += 1

            self.last_move = self.total_time

        self.sprite.set_position(self.pos_pixel[X], self.pos_pixel[Y])

    def check_border(self):
        if self.pos_pixel[X] <= 0:
            self.direction = CONST_RIGHT
        elif self.pos_pixel[X] + CONST_SPRITE_W >= self.window_w:
            self.direction = CONST_LEFT
        elif self.pos_pixel[Y] <= 0:
            self.direction = CONST_DOWN
        elif self.pos_pixel[Y] + CONST_SPRITE_H >= self.window_h:
            self.direction = CONST_UP

    def get_input(self):
        if self.keyboard.key_pressed("w"):
            self.direction = CONST_UP
        elif self.keyboard.key_pressed("s"):
            self.direction = CONST_DOWN
        elif self.keyboard.key_pressed("a"):
            self.direction = CONST_LEFT
        elif self.keyboard.key_pressed("d"):
            self.direction = CONST_RIGHT
        elif self.keyboard.key_pressed("k"):
            if self.total_time - self.last_append >= 1000:
                self.increase_size()
                self.last_append = self.total_time

    def draw(self):
        self.sprite.draw()

    def update(self):
        self.sprite.update()

    def increase_size(self):
        # Pegar posicao do rabo e colocar ali mais um corpo
        self.bodies.append(Body(CONST_RIGHT, 50, 50))

    def get_size(self):
        return len(self.bodies)

    def to_pixel(self, pos_grid):
        return [pos_grid[X] * CONST_GRID_LENGHT_X, pos_grid[Y] * CONST_GRID_LENGHT_Y]

    def to_grid(self, pos_pixel):
        return [pos_pixel[X] / CONST_GRID_LENGHT_X, pos_pixel[Y] / CONST_GRID_LENGHT_Y]
