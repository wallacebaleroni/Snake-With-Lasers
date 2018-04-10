from PPlay.window import *
from src.Snake import *

CONST_WINDOW_SIZE_X = 400
CONST_WINDOW_SIZE_Y = 400


def main():
    game_window = Window(CONST_WINDOW_SIZE_X, CONST_WINDOW_SIZE_Y)
    game_window.set_title("Snake With Lasers")

    snake = Snake(CONST_WINDOW_SIZE_X, CONST_WINDOW_SIZE_Y)

    # Game loop
    while True:
        snake.run()

        game_window.set_background_color((0, 0, 0))
        snake.draw()

        game_window.update()
        snake.update()


main()
