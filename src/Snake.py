from PPlay.keyboard import *
from PPlay.sprite import *
from src.Body import *

CONST_UP = 1
CONST_DOWN = 2
CONST_LEFT = 3
CONST_RIGHT = 4

CONST_SPRITE_W = 25
CONST_SPRITE_H = 25


class Snake:
    sprite = None
    keyboard = None
    window_h = None
    window_w = None

    bodies = []
    direction = CONST_RIGHT
    speed = 0.03
    pos_x = 0
    pos_y = 0

    def __init__(self, window_h, window_w, pos_x=50, pos_y=50):
        self.pos_x = pos_x
        self.pos_y = pos_y

        self.window_h = window_h
        self.window_w = window_w

        self.sprite = Sprite("img\snake_temp.png", 1)
        self.sprite.set_total_duration(1000)

        self.bodies.append(Body(CONST_RIGHT, 50, 50))
        self.keyboard = Keyboard()

    def run(self):
        self.get_input()
        self.move()

    def move(self):
        self.check_border()

        if self.direction == CONST_UP:
            self.pos_y -= self.speed
        elif self.direction == CONST_DOWN:
            self.pos_y += self.speed
        elif self.direction == CONST_LEFT:
            self.pos_x -= self.speed
        elif self.direction == CONST_RIGHT:
            self.pos_x += self.speed

        self.sprite.set_position(self.pos_x, self.pos_y)

    def check_border(self):
        if self.pos_x <= 0:
            self.direction = CONST_RIGHT
        elif self.pos_x + CONST_SPRITE_W >= self.window_w:
            self.direction = CONST_LEFT
        elif self.pos_y <= 0:
            self.direction = CONST_DOWN
        elif self.pos_y + CONST_SPRITE_H >= self.window_h:
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

    def draw(self):
        self.sprite.draw()

    def update(self):
        self.sprite.update()

    def increase_size(self):
        self.bodies.append(Body(CONST_RIGHT, 50, 50))

    def get_size(self):
        return len(self.bodies)
