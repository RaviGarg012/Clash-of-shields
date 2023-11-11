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

# set mode for display
width = 500
height = 700
screen = pygame.display.set_mode((width, height))

# title icon and caption
pygame.display.set_caption("Clash Of Shields")
icon = pygame.image.load("images/icon.png")
pygame.display.set_icon(icon)

# colors
Brightred = (238, 75, 43)
Burntred = (233, 116, 81)
back_color = (226, 175, 205)
pink = (255, 92, 245)

# fonts oblject
font1 = RenderingFont(screen, 32)

font2 = RenderingFont(screen, 10)

font3 = RenderingFont(screen, 20)

# images for background
menu_img = pygame.image.load("images/back.jpg").convert_alpha()
menu_back_img = pygame.transform.scale(menu_img, (width, height)).convert_alpha()

game_back = pygame.image.load("images/game_back.jpg").convert_alpha()


# logo
logo_ig = pygame.image.load("images/logo.png").convert_alpha()
logo_img = pygame.transform.scale(logo_ig, (300, 300))

# menu instances
menu_state = "menu"

# button class objects
# play button
play_b = Button(screen, "images/play.png", 210, 350)

# exit button
exit_b = Button(screen, "images/back_icon.png", 210, 450)

# player vs player and player vs computer button
pvp = Button(screen, "images/PvP.png", 140, 410)

pvc = Button(screen, "images/PvC.png", 290, 410)

# raws in a column
n = 6

# loading music for game

# player selection sound
player_selection = pygame.mixer.Sound("music/playersound.mp3")

# win sound
win_sound = pygame.mixer.Sound("music/winsound.wav")
small_win_sound = pygame.mixer.Sound("music/smallwinsound.mp3")

# game loop
runing = True
while runing:
    screen.fill(back_color)
    # events
    if menu_state != "play":
        # draw the back, logo, play, exit button
        screen.blit(menu_back_img, (0, 0))
        # screen.fill(coler)
        screen.blit(logo_img, (100, 125))
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

        if menu_state == "menu":
            play_b.draw()
            exit_b.draw()
            if play_b.clicked():
                menu_state = "option"

            if exit_b.clicked():
                runing = False

            # player class for player methods
            player = Player(screen, 2)
            player_no = random.randint(0, 1)
            player_move = (player_no, 0)

            # computer move uniformly random
            computer_move = random.randint(0, 1)

            # waiting the computer to one move until the squares appear
            sec_for_computer = 0

            # when game started then its give some time to shield to apear at middle point
            game_ready_point = False

            # choose the mode variable
            player_vs_player = player_vs_computer = False

        elif menu_state == "option":
            # option of seleting a mode
            # font
            font1.show_the_message("Choose a mode", (135, 360))

            # drawing the pvp and pvc icon
            pvp.draw()
            pvc.draw()

            # user selection of mode
            if pvp.clicked():
                menu_state = "play"
                player_vs_player = True
            if pvc.clicked():
                player_vs_computer = True
                menu_state = "play"
    else:
        # game begins from here

        # game background screen
        screen.blit(game_back, (0, 0))

        sqr = Square(screen, 106, 120, n)

        # position of player
        position = game.get_position()

        # all possible moves
        possible_move = game.get_possible_move(position)

        sqr_lst = sqr.draw_square(possible_move)
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

        # game end check update and speed booster
        if player_won or player_lost:
            game_end = True
            show_card = False
            velocity = 1.6
            speed += velocity
        else:
            game_end = False

        # to handle the speed of computer and solow down it little bit
        sec_for_computer += clock.get_fps()

        # font name under the player's shields
        if player_vs_player:
            font2.show_the_message("Player 1", (60, 640))
            font2.show_the_message("Player 2", (402, 640))
        elif player_vs_computer:
            if computer_move == 0:
                font2.show_the_message("Computer", (60, 640))
                font2.show_the_message("You", (414, 640))
            else:
                font2.show_the_message("Computer", (402, 640))
                font2.show_the_message("You", (72, 640))
        # events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runing = False

            if event.type == pygame.MOUSEBUTTONUP:
                pos = event.pos
                if player_vs_player or (
                    player_vs_computer and player_move[0] != computer_move
                ):
                    for i in range(n * 4):
                        if sqr_lst[i].collidepoint(pos):
                            if i in possible_move:
                                p_x, p_y = sqr_lst[i].topleft
                                px, py = p_x + 5, p_y + 5
                                speed = 0

        # taking computer input
        if (
            player_vs_computer
            and player_move[0] == computer_move
            and not game_end
            and sec_for_computer / 620 >= 1
        ):
            pygame.time.wait(300)
            computer_turn = random.choice(possible_move)
            p_x, p_y = sqr_lst[computer_turn].topleft
            px, py = p_x + 5, p_y + 5
            speed = 0
            pygame.time.wait(300)
            sec_for_computer = 0

        for user_input in range(n * 4):
            if sqr_lst[user_input].collidepoint((px, py)):
                # placing the value of user_input in board
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
                    won_list = player.won_next_move(player_move)

                    # if any player won then showing the winner message
                    if won_list[0]:
                        if player_vs_player:
                            if player_move[0] == 0:
                                font3.show_the_message("Player1 Won!", (185, 20))
                            else:
                                font3.show_the_message("Player2 Won!", (185, 20))
                        elif player_vs_computer:
                            if player_move[0] == computer_move:
                                font3.show_the_message("Computer Won!", (175, 20))
                            else:
                                font3.show_the_message("You Won!", (205, 20))
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

                        if won_list[0]:
                            # menu_state = "menu"
                            # player is won the game then
                            win_sound.play()
                            time.sleep(10)

                        else:
                            player_move = won_list[1]
                            # sound for next player
                            pygame.time.delay(12)
                            small_win_sound.play()

                elif player_lost:
                    # player_move
                    player.draw_player(
                        player.get_position(player_move), 570, player_move[0]
                    )

                    if speed >= 3 and speed <= 5:
                        # make object of class to play the game
                        game = Game(n)

                        # game variables
                        show_img_l = False
                        show_card = True
                        player_won = player_lost = False
                        game_ready_point = True

                        # player original position
                        px = 220
                        py = 560
                        speed = 0

                        # waiting the computer a move
                        if player_vs_computer and player_move[0] != computer_move:
                            sec_for_computer = 0

                        # take move from player class
                        next_move = player.lost_next_move(player_move)
                        player_move = next_move

            else:
                player.draw_player(px, py, player_move[0])
                if game_ready_point:
                    # starting sound for player
                    player_selection.play()
                    game_ready_point = False

    pygame.display.update()
    clock.tick(fps)

pygame.quit()
sys.exit()
