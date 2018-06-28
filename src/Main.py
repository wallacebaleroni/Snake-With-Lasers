import time

from PPlay.window import *
from PPlay.gameimage import *
from PPlay.mouse import *

from Snake import *

CONST_WINDOW_SIZE_X = 400
CONST_WINDOW_SIZE_Y = 400

CONST_GRID_SIZE_X = 20
CONST_GRID_SIZE_Y = 20

CONST_RUNNING = -1
CONST_NEXT_LEVEL = 1
CONST_DEAD = 2
CONST_QUIT = 3

CONST_MENU_BACKGROUND_PATH = "..\img\menu\/background.png"
CONST_MENU_PLAY_PATH = "..\img\menu\play.png"
CONST_MENU_RANKING_PATH = "..\img\menu\/ranking.png"
CONST_MENU_QUIT_PATH = "..\img\menu\quit.png"
CONST_RANKING_BACKGROUND_PATH = "..\img\menu\/ranking_background.png"
CONST_RANKING_BACK_PATH = "..\img\menu\/back.png"
CONST_GAME_OVER_PATH = "..\img\game_over.png"
CONST_YOU_WON_PATH = "..\img\you_won.png"


def main_menu():
    game_window = Window(CONST_WINDOW_SIZE_X, CONST_WINDOW_SIZE_Y)
    game_window.set_title("Snake With Lasers")

    background = GameImage(CONST_MENU_BACKGROUND_PATH)
    play_button = Sprite(CONST_MENU_PLAY_PATH, 2)
    ranking_button = Sprite(CONST_MENU_RANKING_PATH, 2)
    quit_button = Sprite(CONST_MENU_QUIT_PATH, 2)

    play_button.set_position(133, 160)
    ranking_button.set_position(111, 230)
    quit_button.set_position(144, 300)

    play_button.set_curr_frame(0)
    ranking_button.set_curr_frame(0)
    quit_button.set_curr_frame(0)

    mouse_input = Mouse()

    click_cooldown_time = 750
    last_click = 0
    just_clicked = False
    block_click = False

    while True:
        if mouse_input.is_over_object(play_button):
            play_button.set_curr_frame(1)
            if mouse_input.is_button_pressed(1):
                game()
        else:
            play_button.set_curr_frame(0)
        if mouse_input.is_over_object(ranking_button):
            ranking_button.set_curr_frame(1)
            if mouse_input.is_button_pressed(1):
                menu_ranking()
                just_clicked = True
                block_click = True
        else:
            ranking_button.set_curr_frame(0)
        if mouse_input.is_over_object(quit_button):
            quit_button.set_curr_frame(1)
            if mouse_input.is_button_pressed(1) and not block_click:
                return
        else:
            quit_button.set_curr_frame(0)

        background.draw()
        play_button.draw()
        ranking_button.draw()
        quit_button.draw()

        game_window.update()

        total_time = game_window.total_time
        if just_clicked:
            last_click = total_time
            just_clicked = False
        if block_click:
            if total_time - last_click > click_cooldown_time:
                block_click = False


def game():
    game_window = Window(CONST_WINDOW_SIZE_X, CONST_WINDOW_SIZE_Y)
    game_window.set_title("Snake With Lasers")

    current_level = 1
    score = 0

    snake = Snake(CONST_WINDOW_SIZE_X, CONST_WINDOW_SIZE_Y, CONST_GRID_SIZE_X, CONST_GRID_SIZE_Y, current_level, score)

    # Game loop
    while True:
        game_over = snake.run(game_window.total_time)
        if game_over == CONST_RUNNING:
            pass
        elif game_over == CONST_DEAD:
            set_ranking(score)
        elif game_over == CONST_QUIT:
            break
        else:
            score = game_over
            current_level += 1
            if current_level > 5:
                set_ranking(score)
            else:
                snake = Snake(CONST_WINDOW_SIZE_X, CONST_WINDOW_SIZE_Y, CONST_GRID_SIZE_X, CONST_GRID_SIZE_Y, current_level, score)

        # Draw
        if current_level > 5:
            # Draws the you won message
            draw_you_won()
        elif game_over != CONST_DEAD:
            # Draws background
            game_window.set_background_color((0, 0, 0))
            # Draws snake
            snake.draw()
            # Draws score
            score = snake.get_score()
            game_window.draw_text("Score: " + str(score), 5, 4, color=(255, 255, 255))
            # Draws level
            game_window.draw_text("Level " + str(current_level), CONST_WINDOW_SIZE_X / 2 - 20, 4, color=(255, 255, 255))
            # Draws power-ups time left
            sl_timeout = snake.get_laser_timeout()
            if sl_timeout != 0:
                game_window.draw_text("Super Laser: " + str(int(sl_timeout / 1000)), CONST_WINDOW_SIZE_X - 85, 4,
                                      color=(255, 255, 255))
            sp_timeout = snake.get_speed_timeout()
            if sp_timeout != 0:
                game_window.draw_text("Slow Speed: " + str(int(sp_timeout / 1000)), CONST_WINDOW_SIZE_X - 155, 4,
                                      color=(255, 255, 255))
        else:
            # Draws the game over message
            draw_game_over()

        game_window.update()

        # Waits a little to show the message
        if game_over == CONST_DEAD or current_level > 5:
            time.sleep(2.5)
            break


def set_ranking(score):
    ranking_file = open("ranking.txt", "r")

    # Puts the ranking in a list
    ranking = []
    while True:
        line = ranking_file.readline()
        if line == "":
            break
        ranking.append(int(line))
    ranking_file.close()

    # Puts the new score in the ranking
    if score not in ranking:
        ranking.append(score)
    ranking.sort(reverse=True)

    # Rewrites to the ranking file the 5 biggest
    ranking_file = open("ranking.txt", "w")
    i = 0   
    while i < 5 and i < len(ranking):
        ranking_file.write(str(ranking[i]) + "\n")
        i += 1

    ranking_file.close()


def menu_ranking():
    game_window = Window(CONST_WINDOW_SIZE_X, CONST_WINDOW_SIZE_Y)
    game_window.set_title("Snake With Lasers")

    background = GameImage(CONST_RANKING_BACKGROUND_PATH)

    back_button = Sprite(CONST_RANKING_BACK_PATH, 2)
    back_button.set_position(141, 300)

    back_button.set_curr_frame(0)

    mouse_input = Mouse()

    while True:
        if mouse_input.is_over_object(back_button):
            back_button.set_curr_frame(1)
            if mouse_input.is_button_pressed(1):
                return
        else:
            back_button.set_curr_frame(0)

        background.draw()
        back_button.draw()

        ranking = get_ranking()
        for i in range(len(ranking)):
            game_window.draw_text(str(i + 1) + ".    " + str(ranking[i]), 100, 120 + i * 35, color=(34, 177, 76), font_name="Arial", size=20)

        game_window.update()


def get_ranking():
    ranking_file = open("ranking.txt", "r")

    ranking = []
    while True:
        line = ranking_file.readline()
        if line == "":
            break
        ranking.append(int(line))
    ranking_file.close()

    return ranking


def draw_game_over():
    game_over_image = GameImage(CONST_GAME_OVER_PATH)
    game_over_image.set_position(102, 190)
    game_over_image.draw()


def draw_you_won():
    you_won_image = GameImage(CONST_YOU_WON_PATH)
    you_won_image.set_position(124, 190)
    you_won_image.draw()


main_menu()
