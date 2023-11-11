import pygame


# clas for players movements
class Player:
    def __init__(self, screen, player_no):
        self.player_no = player_no
        self.won_move = set()
        self.lost_move = set()
        self.screen = screen
        # players
        self.player_img = []

        for member in range(self.player_no):
            p1_img = pygame.image.load(f"images/player{member+1}.png").convert_alpha()

            player_img = pygame.transform.scale(p1_img, (60, 60))

            self.player_img.append(player_img)

    def draw_player(self, x, y, turn):
        self.screen.blit(self.player_img[turn], (x, y))

    def is_winner(self):
        # check if there is a winner then retuen true
        # by checking winners moves

        for moves in self.won_move:
            if moves[1] == 2:
                return True
        return False

    # next moves
    def lost_next_move(self, current_move):
        # list for opposite players won moves
        oppo_move = set()
        # check if there is a winner move in game
        if len(self.won_move) > 0:
            for move in self.won_move:
                if move[0] != current_move[0]:
                    oppo_move.add(move)
                    self.lost_move.add(move)

            if len(oppo_move) > 0:
                # finding max move from opposition  winning moves
                max_move = max(oppo_move)
                if max_move[1] == 0:
                    return (max_move[0], 1)
                else:
                    return (max_move[0], 2)
        # if there is no opposition wining move then return first move
        if current_move[0] == 0:
            return (1, 0)
        else:
            return (0, 0)

    def won_next_move(self, current_move):
        # first of all add this move into winner's set
        # we need to check winner after adding moves in current move

        self.won_move.add(current_move)
        # checking if there is any winner or not
        if not self.is_winner():
            if current_move[1] == 0:
                next_move = (current_move[0], 1)
            else:
                next_move = (current_move[0], 2)
        else:
            next_move = (0, 2)

        return [self.is_winner(), next_move]

    @staticmethod
    def get_position(move):
        # give the horizontal position for shields.
        if move[0] == 0:
            return 80 - move[1] * 30

        else:
            return 362 + move[1] * 30


# class for rendering the text for players
class RenderingFont:
    def __init__(self, screen, size):
        self.screen = screen
        self.font = pygame.font.Font("freesansbold.ttf", size)

    def show_the_message(self, message, dimension):
        text = self.font.render(message, True, (255, 255, 255))
        self.screen.blit(text, dimension)
