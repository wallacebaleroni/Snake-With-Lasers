from PPlay.window import *
from src.Snake import *
# ------------- ALTERACOES PRA AULA ------------------
from PPlay.sprite import *
# ----------------------------------------------------

CONST_WINDOW_SIZE_X = 400
CONST_WINDOW_SIZE_Y = 400

GRID_SIZE_X = 20
GRID_SIZE_Y = 20


def main():
    game_window = Window(CONST_WINDOW_SIZE_X, CONST_WINDOW_SIZE_Y)
    game_window.set_title("Snake With Lasers")

    snake = Snake(CONST_WINDOW_SIZE_X, CONST_WINDOW_SIZE_Y, GRID_SIZE_X, GRID_SIZE_Y)

    # ------------- ALTERACOES PRA AULA ------------------
    game_objects = []
    # head
    game_objects.append(Sprite("../img/head.png", 1))
    # tail
    game_objects.append(Sprite("../img/tail.png", 1))
    # laser comum
    game_objects.append(Sprite("../img/laser.png", 1))
    # laser forte
    game_objects.append(Sprite("../img/slaser.png", 1))
    # bloco
    game_objects.append(Sprite("../img/block.png", 1))
    # power up
    game_objects.append(Sprite("../img/pup.png", 1))
    # parede
    game_objects.append(Sprite("../img/wall.png", 1))

    for sprite in game_objects:
        sprite.set_position((game_objects.index(sprite) + 1) * 20, 0)
    # ----------------------------------------------------

    # Game loop
    while True:
        # snake.run(game_window.total_time)

        game_window.set_background_color((0, 0, 0))
        snake.draw()

        # ------------- ALTERACOES PRA AULA ------------------
        for sprite in game_objects:
            sprite.draw()
        # ----------------------------------------------------

        game_window.update()
        snake.update()


main()
