import random

# class for game


class Game:
    def __init__(self, num_rows):
        # board
        self.board = [" " for _ in range(num_rows * 4)]
        self.num_rows = num_rows

        # creating storage for previous moves
        self.moves = set()

    @staticmethod
    def num_board(num_rows):
        n = num_rows
        board = [f"{i}" for i in range(n * 4)]
        rows = [board[j * 4 : (j + 1) * 4] for j in range(n)]
        for row in rows:
            print("| " + " | ".join(row) + " |")

        print("Take moves according to the this number board")

    # showing board after every move
    def show_board(self):
        n = self.num_rows
        rows = [self.board[i * 4 : (i + 1) * 4] for i in range(n)]
        for row in rows:
            print("| " + " | ".join(row) + " |")

    # position for latest move
    def get_position(self):
        n = self.num_rows
        # taking all move from board
        # if there is no move then give -1
        moves = [-1]
        # checking all the taken move
        spots = self.board
        for i in range(n * 4):
            if spots[i] != " " and spots[i] != "X":
                sp = int(spots[i])
                moves.append(sp)

        # removing -1 if there is any number in moves except -1
        numbers = [i for i in range(n * 4)]
        for move in moves:
            if move in numbers:
                moves.pop(0)
                break
        # getting smallest num in moves which is latest move
        latest_move = min(moves)
        return latest_move

    # getting all possible move
    def get_possible_move(self, position):
        n = self.num_rows
        # checking if possible move is -1 then return starting row
        if position == -1:
            row = [i for i in range((n - 1) * 4, n * 4)]
            return row

        # if position is (1,2,3.....8)
        # then return possible move
        # we move ahead only if position is not -1and is also not in forst row
        else:
            next_move = position - 4
            col = next_move % 4
            if col == 0:
                return [next_move, next_move + 1]
            elif col == 4 - 1:
                return [next_move - 1, next_move]
            else:
                return [next_move - 1, next_move, next_move + 1]

    # creating bomb

    def create_bomb(self, possible_moves):
        # choose random position and turn into this in bomb
        move = random.choice(possible_moves)
        if move not in self.moves:
            if self.board[move] == " ":
                self.board[move] = "X"
        for num in possible_moves:
            self.moves.add(num)

    def take_user_input(self, user_input):
        if self.board[user_input] == " ":
            self.board[user_input] = f"{user_input}"

    # winner function

    def winner(self, user_input):
        # 0th row means user at last row and he won
        row = user_input // 4
        if row == 0 and self.board[user_input] != "X":
            return True
        return False

    # loser function
    def loser(self, user_input):
        if self.board[user_input] == "X":
            return True
        return False


# play the game on command line
def play(game):
    # show num board
    game.num_board(game.num_rows)
    # infinite loop untill winner or looser diclare
    while True:
        game.show_board()
        print("*" * 15)
        # position of player
        position = game.get_position()
        # all possible moves
        possible_move = game.get_possible_move(position)
        # creating bombs in possible moves
        game.create_bomb(possible_move)

        # valid moves loop
        valid_move = False
        while not valid_move:
            try:
                user_input = int(input(f"Enter your move from {possible_move} : "))
                if user_input not in possible_move:
                    raise ValueError
                valid_move = True
            except ValueError:
                print(" Invalid move, Try again !")

        # showing the value of user_input in board
        game.take_user_input(user_input)
        print(game.moves)

        # if player win then break
        if game.winner(user_input):
            game.show_board()
            print("\n Congratulation you won !!\n")
            break

        # if player lost then break
        if game.loser(user_input):
            game.show_board()
            print("\n Sorry but you lost!!")
            break


if __name__ == "__main__":
    game = Game(6)
    play(game)
