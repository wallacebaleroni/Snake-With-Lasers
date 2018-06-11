from PPlay.keyboard import *
from PPlay.sprite import *
from PPlay.collision import *

import random

# Constraints
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

CONST_RUNNING = 0
CONST_NEXT_LEVEL = 1
CONST_DEAD = 2

CONST_PLUS_ONE = 1
CONST_SPEED_DOWN = 2

X = 0
Y = 1

CONST_WINDOW_H = 0
CONST_WINDOW_W = 0

CONST_GRID_SIZE_X = 0
CONST_GRID_SIZE_Y = 0

CONST_GRID_LENGTH_X = 0
CONST_GRID_LENGTH_Y = 0

CONST_WALL_PATH = "..\img\wall.png"
CONST_HEAD_PATH = "..\img\head.png"
CONST_BODY_PATH = "..\img\/body.png"
CONST_TAIL_PATH = "..\img\/tail.png"
CONST_LASER_PATH = "..\img\/laser.png"
CONST_SUPER_LASER_PATH = "..\img\/slaser.png"
CONST_BLOCK_PATH = "..\img\/block.png"
CONST_POWER_UP_PATH = "..\img\/pup.png"


class Snake:
    def __init__(self, window_w, window_h, size_grid_x, size_grid_y, current_level):
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

        # Creates walls
        self.walls = []
        for i in range(size_grid_x):
            for j in range(size_grid_y):
                if i != 0 and i != size_grid_y - 1:
                    if j != 0 and j != size_grid_x - 1:
                        continue
                new_wall = Wall(i, j)
                self.walls.append(new_wall)

        # Creating snake's parts and initializing it's positions and headings
        start_pos_grid = [int(size_grid_x / 2), int(size_grid_y / 2)]
        self.head = Body(Sprite(CONST_HEAD_PATH, 4), CONST_UP, start_pos_grid)

        self.bodies = []
        body_pos_grid = [start_pos_grid[X], start_pos_grid[Y] + 1]
        body = Body(Sprite(CONST_BODY_PATH, 8), CONST_UP, body_pos_grid)
        self.bodies.append(body)

        tail_pos_grid = [body_pos_grid[X], body_pos_grid[Y] + 1]
        self.tail = Body(Sprite(CONST_TAIL_PATH, 4), CONST_UP, tail_pos_grid)

        # Snake speed
        self.speed = 200 * (current_level * 100)

        # Self explanatory
        self.keyboard = Keyboard()

        # Flags
        self.direction_input_got = False
        self.laser_flag = False

        # Time variables
        self.current_time = 0
        self.last_move = 0
        self.last_append = 0
        self.last_laser = 0
        self.last_spawn = 0
        self.s_laser_start = 0
        self.s_laser_timeout = 10000
        # TODO: fazer o da velocidade

        # Blocks variables
        self.blocks = []
        self.block_spawn_time = 2000

        # Lasers variables
        self.lasers = []
        self.laser_cadence = 400
        self.s_laser_cadence = 800
        self.s_laser_active = False

        # Score
        self.current_level = current_level
        self.score = 0


        # Game Over flag
        self.game_over = CONST_RUNNING

    def run(self, total_time):
        self.current_time = total_time

        self.get_input()
        # Checks if the necessary time has already passed
        if self.current_time - self.last_move >= self.speed:
            self.move()
            self.check_borders()
            self.check_collision()
            self.check_wall()

            # Updates last move
            self.last_move = self.current_time
            # Allowed to get the next input
            self.direction_input_got = False
        self.interactions()
        self.spawn_blocks()
        self.laser()

        # return self.game_over

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

        # Laser key
        if self.keyboard.key_pressed("space"):
            self.laser_flag = True

    def check_borders(self):
        if self.head.pos_grid[X] < 0:
            self.head.pos_grid[X] = 19
            self.head.pos_pixel = to_pixel(self.head.pos_grid)
        elif self.head.pos_grid[X] >= CONST_GRID_SIZE_X:
            self.head.pos_grid[X] = -1
            self.head.pos_pixel = to_pixel(self.head.pos_grid)
        elif self.head.pos_grid[Y] < 0:
            self.head.pos_grid[Y] = 19
            self.head.pos_pixel = to_pixel(self.head.pos_grid)
        elif self.head.pos_grid[Y] >= CONST_GRID_SIZE_Y:
            self.head.pos_grid[Y] = -1
            self.head.pos_pixel = to_pixel(self.head.pos_grid)

    def check_collision(self):
        for body in self.bodies:
            if self.head.pos_grid == body.pos_grid:
                self.game_over = CONST_DEAD
                print("Self Hit!")

    def check_wall(self):
        for wall in self.walls:
            if Collision.collided(self.head.sprite, wall.sprite):
                self.game_over = CONST_DEAD
                print("Wall Hit!")

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
                frame = decide_bodies_frames(self.bodies[i].direction, self.head.direction)
                self.bodies[i].set_curr_frame(frame)
                self.bodies[i].direction = self.head.direction
            # Rest of the body
            else:
                frame = decide_bodies_frames(self.bodies[i].direction, self.bodies[i - 1].direction)
                self.bodies[i].set_curr_frame(frame)
                self.bodies[i].direction = self.bodies[i - 1].direction

    def interactions(self):
        # Checks interaction with blocks
        for block in self.blocks:
            if self.head.pos_grid == block.pos_grid:
                # Snake will eat it
                if block.destroyed:
                    # TODO: fazer o da velocidade
                    if block.power_up:
                        self.s_laser_active = True
                        self.s_laser_start = self.current_time
                    else:
                        self.increase_size()
                    self.blocks.remove(block)
                # Snake dies
                else:
                    self.game_over = CONST_DEAD
                    print("Block Hit!")

        # Check timeouts
        if self.s_laser_active and (self.current_time - self.s_laser_start >= self.s_laser_timeout):
            self.s_laser_active = False
        # TODO: fazer o da velocidade

    def increase_size(self):
        # Increase score
        self.score += self.current_level * 10

        # Get tail position then shift it
        tail_pos_grid = [self.tail.pos_grid[X], self.tail.pos_grid[Y]]
        tail_direction = self.tail.direction
        self.tail.move_back()

        # Put new body where the tail was
        sprite = Sprite(CONST_BODY_PATH, 8)
        sprite.set_curr_frame(tail_direction)
        new_body = Body(sprite, tail_direction, tail_pos_grid)
        self.bodies.append(new_body)

    def spawn_blocks(self):
        if self.current_time - self.last_spawn >= self.block_spawn_time:
            valid = False
            # Generates a random valid position
            rand_pos_x = 0
            rand_pos_y = 0
            while not valid:
                valid = True
                # Chooses a random coordinate
                rand_pos_x = random.randint(0, CONST_GRID_LENGTH_X - 1)
                rand_pos_y = random.randint(0, CONST_GRID_LENGTH_Y - 1)

                # Checks if it's not on the walls
                if (rand_pos_x == 0 or rand_pos_x == CONST_GRID_SIZE_X - 1
                        or rand_pos_y == 0 or rand_pos_y == CONST_GRID_SIZE_Y - 1):
                    valid = False

                # Checks if it's not in the line of movement of the snake
                snake_direction = self.head.direction
                snake_pos_x = self.head.pos_grid[X]
                snake_pos_y = self.head.pos_grid[Y]
                if snake_direction == CONST_UP and rand_pos_x == snake_pos_x and rand_pos_y <= snake_pos_y:
                    valid = False
                if snake_direction == CONST_DOWN and rand_pos_x == snake_pos_x and rand_pos_y >= snake_pos_y:
                    valid = False
                if snake_direction == CONST_LEFT and rand_pos_y == snake_pos_y and rand_pos_x <= snake_pos_x:
                    valid = False
                if snake_direction == CONST_RIGHT and rand_pos_y == snake_pos_y and rand_pos_x >= snake_pos_x:
                    valid = False

                # Checks if it isn't over the snake's body
                for body in self.bodies:
                    if body.pos_grid[X] == rand_pos_x and body.pos_grid[Y] == rand_pos_y and valid:
                        valid = False

                # Checks if it ins't over another block
                for block in self.blocks:
                    if block.pos_grid[X] == rand_pos_x and block.pos_grid[Y] == rand_pos_y and valid:
                        valid = False

            # 25% chance of being a power up
            power_up = False
            if random.randint(0, 3) == 0:
                power_up = True

            # Creates the block
            new_block = Block([rand_pos_x, rand_pos_y], power_up)
            self.blocks.append(new_block)

            self.last_spawn = self.current_time

    def laser(self):
        # Checks the need of creating a laser
        cadence = self.s_laser_cadence if self.s_laser_active else self.laser_cadence
        if self.laser_flag and self.current_time - self.last_laser >= cadence:
            # Create laser sprite
            new_laser = Laser(self.head, self.current_time, self.s_laser_active)
            self.lasers.append(new_laser)
            # Create it in front of the head
            self.laser_flag = False
            self.last_laser = self.current_time

        # Move lasers
        for laser in self.lasers:
            laser.run(self.current_time)

        # Check block hits
        for laser in self.lasers:
            for block in self.blocks:
                if not block.destroyed:
                    if Collision.collided(laser.sprite, block.sprite):
                        self.lasers.remove(laser)
                        block.destroy()

        # Check wall hits
        for laser in self.lasers:
            for wall in self.walls:
                if Collision.collided(laser.sprite, wall.sprite):
                    self.lasers.remove(laser)
                    if laser.s_laser:
                        wall.hit()
                        if wall.health == 0:
                            self.walls.remove(wall)

        # Lasers cleaning
        for laser in self.lasers:
            if (laser.sprite.x >= CONST_WINDOW_W or laser.sprite.x <= 0 or
                    laser.sprite.y >= CONST_WINDOW_H or laser.sprite.y <= 0):
                self.lasers.remove(laser)

    def draw(self):
        # Draw walls
        for wall in self.walls:
            wall.draw()
        # Draw head
        self.head.draw()
        # Draw bodies
        for body in self.bodies:
            body.draw()
        # Draw tail
        self.tail.draw()
        # Draw blocks
        for block in self.blocks:
            block.draw()
        # Draw lasers
        for laser in self.lasers:
            laser.draw()

    def get_score(self):
        return self.score

    # TODO: fazer o da velocidade
    def get_laser_timeout(self):
        return self.current_time - self.s_laser_start


def decide_bodies_frames(curr, next):
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


def to_grid(pos_pixel):
    return [pos_pixel[X] / CONST_GRID_LENGTH_X, pos_pixel[Y] / CONST_GRID_LENGTH_Y]


def to_pixel(pos_grid):
    return [pos_grid[X] * CONST_GRID_LENGTH_X, pos_grid[Y] * CONST_GRID_LENGTH_Y]


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

    def move_back(self):
        if self.direction == CONST_UP:
            self.pos_grid[Y] += 1
        elif self.direction == CONST_DOWN:
            self.pos_grid[Y] -= 1
        elif self.direction == CONST_LEFT:
            self.pos_grid[X] += 1
        elif self.direction == CONST_RIGHT:
            self.pos_grid[X] -= 1
        self.pos_pixel = to_pixel(self.pos_grid)
        self.sprite.set_position(self.pos_pixel[X], self.pos_pixel[Y])

    def set_position(self, x, y):
        self.pos_pixel = [x, y]
        self.pos_grid = to_grid(self.pos_pixel)
        self.sprite.set_position(x, y)

    def set_curr_frame(self, frame):
        self.sprite.set_curr_frame(frame)

    def draw(self):
        self.sprite.draw()


class Laser:
    def __init__(self, head: Body, current_time, s_laser):
        # Initializations
        self.s_laser = s_laser
        if s_laser:
            self.sprite = Sprite(CONST_SUPER_LASER_PATH, 8)
        else:
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
        # Moves the laser depending on it's direction
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


class Block:
    def __init__(self, pos_grid, power_up):
        self.pos_grid = pos_grid
        self.pos_pixel = to_pixel(pos_grid)

        self.power_up = power_up
        if power_up:
            self.sprite = Sprite(CONST_POWER_UP_PATH, 2)
        else:
            self.sprite = Sprite(CONST_BLOCK_PATH, 2)
        self.sprite.set_position(self.pos_pixel[X], self.pos_pixel[Y])

        self.destroyed = False

        self.type = CONST_PLUS_ONE

    def draw(self):
        self.sprite.draw()

    def destroy(self):
        self.destroyed = True
        self.sprite.set_curr_frame(1)


class Wall:
    def __init__(self, pos_grid):
        self.pos_grid = pos_grid
        self.pos_pixel = to_pixel(pos_grid)

        self.sprite = Sprite(CONST_WALL_PATH, 1)
        self.sprite.set_position(self.pos_pixel[X], self.pos_pixel[Y])

        self.health = 3

    def hit(self):
        self.health -= 1
        # TODO: outros sprites da parede

    def draw(self):
        self.sprite.draw()