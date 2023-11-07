import pygame
import time
import random
import sys
from BattleOfShields import Game
from GameComponents import *
from Player import *

# intialization
pygame.init()
clock = pygame.time.Clock()
fps = 60

# set mode
width = 500
height = 700
screen = pygame.display.set_mode((width, height))

# colors
Brightred = (238, 75, 43)
Burntred = (233, 116, 81)
back_color = (226, 175, 205)
pink = (255, 92, 245)
# fonts
font = pygame.font.Font("freesansbold.ttf", 32)


# images for background
menu_img = pygame.image.load("images/back.jpg").convert_alpha()
menu_back_img = pygame.transform.scale(menu_img, (width, height)).convert_alpha()
# logo
logo_ig = pygame.image.load("images/logo.png").convert_alpha()
logo_img = pygame.transform.scale(logo_ig, (300, 300))
# menu instances
menu_state = "menu"
player_move = random.randint(1, 2)


# button class objects
play_b = Button(screen, "images/play.png", 210, 350)

exit_b = Button(screen, "images/back_icon.png", 210, 450)

u = 0
u1 = 0
u3 = 0
n = 6

# image for place for active player
place = pygame.image.load("images/place.png").convert_alpha()

# place = pygame.transform.scale(place_img, (120, 120))


# loading music for game

# background music
# pygame.mixer.music.load("backgroundsound.mp3")
# pygame.mixer.music.play(-1)

# player selection sound
player_selection = pygame.mixer.Sound("music/playersound.mp3")


win_sound = pygame.mixer.Sound("music/winsound.wav")

# loss
loss_sound = pygame.mixer.Sound("music/deathsound.mp3")


# game loop
runing = True
while runing:
    screen.fill(back_color)
    # events
    if menu_state != "play":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runing = False
        # make object of class to play the game
        game = Game(n)

        # game variable
        show_img_l = False
        show_card = True
        player_won = player_lost = False

        # player original position
        px = 220
        py = 560
        speed = 0
        possible_move = [-1]

        if menu_state == "menu":
            # draw the back, logo, play, exit button
            screen.blit(menu_back_img, (0, 0))
            # screen.fill(coler)
            screen.blit(logo_img, (100, 125))
            play_b.draw()
            exit_b.draw()
            if play_b.clicked():
                menu_state = "play"

            if exit_b.clicked():
                runing = False

            # player class for player methods
            player = Player(screen, 2)
            # player_no = random.randint(0, 1)
            player_move = (0, 0)

            # when game started then its give some time to shield to apear at middle point
            game_ready_point = True

            # choose the mode variable
            player_vs_player = player_vs_computer = False

    else:
        sqr = Square(screen, 106, 120, n)
        sqr_lst = sqr.draw_square(possible_move)
        # if there is first move of the game
        if game_ready_point:
            # intialize everything for one time
            px = 220
            py = 560
            possible_move = [-1]

        # position of player
        position = game.get_position()

        # all possible moves
        possible_move = game.get_possible_move(position)

        # creating bombs in possible moves
        game.create_bomb(possible_move)

        # showing static (which are not active players) shield
        for i in range(2):
            for j in range(3):
                if player_move != (i, j):
                    if (i, j) in player.won_move:
                        player.draw_player(player.get_position((i, j)), 40, i)
                    else:
                        player.draw_player(player.get_position((i, j)), 570, i)

            # game end check update
            if player_won or player_lost:
                game_end = True
                show_card = False
                velocity = 0.8
                speed += velocity
            else:
                game_end = False

        # events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runing = False

            if event.type == pygame.MOUSEBUTTONUP:
                pos = event.pos
                for i in range(n * 4):
                    if sqr_lst[i].collidepoint(pos):
                        if i in possible_move:
                            p_x, p_y = sqr_lst[i].topleft
                            px, py = p_x + 5, p_y + 5
                            speed = 0

        for user_input in range(n * 4):
            if sqr_lst[user_input].collidepoint((px, py)):
                u = game.board[user_input]

                # showing the value of user_input in board
                game.take_user_input(user_input)

                # if player win
                if game.winner(user_input):
                    show_img_w = False
                    player_won = True
                    # player_lost = True

                # if lost
                if game.loser(user_input):
                    show_img_l = True
                    player_lost = True

                if show_card:
                    if show_img_l:
                        sqr.show_won_lost_card("images/red.png", user_input)
                    else:
                        sqr.show_won_lost_card("images/green.png", user_input)

            if game_end:
                pygame.time.delay(12)
                if player_won:
                    player.draw_player(220, 50, player_move[0])
                    if speed >= 3 and speed <= 5:
                        # make object of class to play the game
                        game = Game(n)
                        # game variable
                        show_img_l = False
                        show_card = True
                        player_won = player_lost = False

                        # player original position
                        px = 220
                        py = 560
                        speed = 0
                        possible_move = [-1]

                        won_list = player.won_next_move(player_move)
                        if won_list[0]:
                            menu_state = "menu"
                            # player is won the game then
                            win_sound.play()
                            time.sleep(1.2)

                        else:
                            player_move = won_list[1]
                            # sound for next player
                            player_selection.play()

                elif player_lost:
                    # player_move
                    player.draw_player(
                        player.get_position(player_move), 570, player_move[0]
                    )

                    #  if speed <= 1:
                    # loss_sound.play()

                    if speed >= 3 and speed <= 5:
                        # make object of class to play the game
                        game = Game(n)

                        # game variable
                        show_img_l = False
                        show_card = True
                        player_won = player_lost = False

                        # player original position
                        px = 220
                        py = 560
                        speed = 0
                        possible_move = [-1]

                        # take move from player class
                        next_move = player.lost_next_move(player_move)
                        player_move = next_move

                        # sound for next player
                        player_selection.play()

            else:
                if game_ready_point:
                    player.draw_player(px, py, player_move[0])
                    px = 220
                    py = 560
                    game_ready_point = False

                else:
                    player.draw_player(px, py, player_move[0])

    pygame.display.update()
    clock.tick(fps)

pygame.quit()
sys.exit()
