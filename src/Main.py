from PPlay.window import *
from src.Snake import *

CONST_WINDOW_SIZE_X = 400
CONST_WINDOW_SIZE_Y = 400

CONST_GRID_SIZE_X = 20
CONST_GRID_SIZE_Y = 20

CONST_RUNNING = 0
CONST_NEXT_LEVEL = 1
CONST_DEAD = 2


def main():
    game_window = Window(CONST_WINDOW_SIZE_X, CONST_WINDOW_SIZE_Y)
    game_window.set_title("Snake With Lasers")

    current_level = 1

    snake = Snake(CONST_WINDOW_SIZE_X, CONST_WINDOW_SIZE_Y, CONST_GRID_SIZE_X, CONST_GRID_SIZE_Y, current_level)

    # Game loop
    while True:
        game_over = snake.run(game_window.total_time)
        if game_over == CONST_NEXT_LEVEL:
            current_level += 1
            snake = Snake(CONST_WINDOW_SIZE_X, CONST_WINDOW_SIZE_Y, CONST_GRID_SIZE_X, CONST_GRID_SIZE_Y, current_level)
        elif game_over == CONST_DEAD:
            break

        game_window.set_background_color((0, 0, 0))
        snake.draw()

        # Draw HUD
        score = snake.get_score()
        game_window.draw_text("Score: " + str(score), 10, 5)
        game_window.draw_text("Level " + str(current_level), CONST_GRID_SIZE_X / 2 - 20, 5)
        sl_timeout = snake.get_laser_timeout()
        if sl_timeout != 0:
            game_window.draw_text("Super Laser: " + str(sl_timeout), CONST_GRID_SIZE_X - 50, 5)
        # TODO: fazer o da velocidade

        game_window.update()


main()
