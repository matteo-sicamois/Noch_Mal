#Noch mal
#Rules:
# You roll for dices, 2 for colors and 2 for numbers.
# You then have to choose 2 of the dices and select the corresponding amount of squares of that color.
# The squares have to be either in the highlighted column or adjacent to an already occupied square.
# They all have to touch each others (no diagonals)
import copy
# Completing a column gives a determinate number of points (see score_table of NochMal class)
# Completing a color gives 5 points
# Each non-collected star (the rhombuses) removes 2 points at the end of the self.
# The self ends after 30 rounds

#To select the squares write their coordinates separated by a comma. Separate each square with a space.

#Example:
# numbers: [2,5] colors: [red, yellow]
#Enter move: 5,7 5,8

import random
import itertools
from copy import deepcopy

class colors:
    PINK = TWO = '\033[95m'
    BLUE = FOUR = '\033[94m'
    GREEN = ONE = '\033[92m'
    YELLOW = FIVE = '\033[93m'
    RED = THREE = '\033[91m'
    NORMAL = '\033[0m'

color_list = ['\033[0m','\033[92m','\033[95m','\033[91m','\033[94m','\033[93m']

def visualize_move(board,move):
    print("  ", end="")
    for i in range(len(board[0])):
        print(f"{i:^2}", end=' ')
    print()
    for i_x, x in enumerate(board):
        print(i_x, end=" ")
        for i_y,y in enumerate(x):
            if (i_x, i_y) in move:
                print(f"{colors.NORMAL}██", end='')
            elif y == 0:
                print("[]", end="")
            elif y == 1:
                print(f"{colors.ONE}██", end='')
            elif y == 2:
                print(f"{colors.TWO}██", end='')
            elif y == 3:
                print(f"{colors.THREE}██", end='')
            elif y == 4:
                print(f"{colors.FOUR}██", end='')
            elif y == 5:
                print(f"{colors.FIVE}██", end='')
            print(f" {colors.NORMAL}", end='')
        print()

class NochMal:
    def __init__(self):
        #              A  B  C  D  E  F  G  H  I  J  K  L  M  N  O
        self.board = [[1, 1, 1, 5, 5, 5, 5, 1.0, 4, 4, 4, 2.0, 5, 5, 1],
                      [2, 1, 5, 1, 5, 5, 2, 2, 3, 4, 4, 2, 2, 1, 1],
                      [4.0, 1, 3, 1, 1, 1, 1.0, 3, 3, 3, 5, 5, 2, 1, 1],
                      [4, 3, 3, 2, 2, 2, 4, 4, 1, 1, 5, 5, 2, 3.0, 4],
                      [3, 1, 2, 2, 2, 3, 4, 4, 2, 2, 2, 3, 3, 3, 3],
                      [3, 4.0, 4, 3.0, 3, 3, 3, 5, 5, 2, 3.0, 4, 4, 4, 2.0],
                      [5, 5, 4, 4, 4, 4, 3, 5, 5, 1, 1, 1, 1.0, 2, 2]]
                      #Green = 1 Pink = 2 Red = 3 Blue = 4 Yellow = 5
        #              A  B  C  D  E  F  G  H  I  J  K  L  M  N  O
        self.hight_board = len(self.board)
        self.width_board = len(self.board[0])
        self.turn = 0
        self.score = 0
        self.color_dices = []
        self.num_dices = []
        self.columns_done = []
        self.colors_done = []
        self.start_column = 7
        self.total_rounds = 30
        self.score_table = {0:5,1:3,2:3,3:3,4:2,5:2,6:2,7:1,8:2,9:2,10:2,11:3,12:3,13:3,14:5}
        self.stars = [(0,7),(0,11),(1,2),(1,9),(2,0),(2,6)]


        self.is_game_over = False

        self.roll_dices()

    def roll_dices(self):
        self.color_dices = []
        self.num_dices = []
        self.color_dices.append(random.randint(1, 5))
        self.color_dices.append(random.randint(1, 5))
        self.num_dices.append(random.randint(1, 5))
        self.num_dices.append(random.randint(1, 5))

    @staticmethod
    def copy_board(board):
        return [row.copy() for row in board]

    def get_possible_moves(self):
        possible_moves = set()
        possible_moves.add(frozenset())

        def has_neighbor(board,row,col,target):
            for d in (-1, 1):
                try:
                    if board[row + d][col] == target and row + d >= 0:
                        return True
                    if board[row][col + d] == target and col + d >= 0:
                        return True
                except IndexError: pass
            return False

        def find_start(board):
            start = []
            for i_row,row in enumerate(board):
                    for i_col, col in enumerate(row):
                        valid = True
                        if board[i_row][i_col] != color:
                            valid = False
                        if valid and i_col != self.start_column and not has_neighbor(board,i_row,i_col,0):
                            valid = False
                        if valid:
                            start.append((i_row, i_col))
            return start

        def build_stack(start:list):
            def elaborate(move):
                if len(move) == number:
                    return move
                squares = set(itertools.chain(*[
                    [(min(a[0] + 1, self.hight_board - 1), a[1]), (max(a[0] - 1, 0), a[1]),
                 (a[0], min(a[1] + 1, self.width_board - 1)), (a[0], max(a[1] - 1, 0))] for a in move])) - set(move)
                squares = [square for square in squares if self.board[square[0]][square[1]] == color]
                for square in squares:
                    stack.append(move+[square])
                return None

            stack = [start]
            while stack:
                move = stack.pop(-1)
                if elaborate(move):
                    possible_moves.add(frozenset(move))

        for color in  self.color_dices:
            for number in self.num_dices:
                for start in find_start(self.board):
                    build_stack([start])

        return possible_moves

    def make_move(self, move):
        for square in move:
            self.board[square[0]][square[1]] = 0

    def update_state(self):
        for color in range(1,6):
            if color not in list(itertools.chain(*self.board))+ self.colors_done:
                self.colors_done.append(color)
        for n,column in enumerate(zip(*self.board)):
            if sum(column) == 0 and n not in self.columns_done:
                self.columns_done.append(n)
        if len(self.colors_done) == 2:
            self.is_game_over = True
        if self.turn == self.total_rounds:
            self.is_game_over = True

    def is_game_over(self):
        return self.is_game_over

    def get_game_score(self):
        score = 0
        for n in self.columns_done: score += self.score_table[n]
        score += len(self.colors_done) * 5
        for c in list(itertools.chain.from_iterable(self.board)):
            if type(c) == float: score -= 2
        return score

    def print_board(self):
        print("  ", end="")
        for i in range(self.width_board):
            if i in [self.start_column,self.start_column+1]: print(" ", end="")
            print(f"{i:^2}", end=' ')
        print()
        for n,i in enumerate(self.board):
            print(n, end=" ")
            for n,j in enumerate(i):
                if n in [self.start_column+1,self.start_column]:
                    print(" ", end="")
                if j == 0:
                    print("[]", end="")
                if j == 1:
                    print(f"{colors.ONE}{'██' if type(j) == int else '◀▶'}", end='')
                elif j == 2:
                    print(f"{colors.TWO}{'██' if type(j) == int else '◀▶'}", end='')
                elif j == 3:
                    print(f"{colors.THREE}{'██' if type(j) == int else '◀▶'}", end='')
                elif j == 4:
                    print(f"{colors.FOUR}{'██' if type(j) == int else '◀▶'}", end='')
                elif j == 5:
                    print(f"{colors.FIVE}{'██' if type(j) == int else '◀▶'}", end='')
                print(f" {colors.NORMAL}",end='')
            print()

class PlayerClass():
    def __init__(self):
        self.game = NochMal()
        self.possible_moves = self.game.get_possible_moves()
        self.strategy = None

    def set_strategy(self, strategy):
        self.strategy = strategy

    def random_move(self):
        all = self.possible_moves
        if len(all) == 1:
            return all.pop()
        return random.choice([move for move in list(all) if move])

    def check_star(self):
        all_moves = list(self.possible_moves)
        star = sorted([move for move in all_moves if [square for square in move if type(self.game.board[square[0]][square[1]]) == float]], reverse=True)
        if len(star) != 0:
            return star[0]
        return random.choice(all_moves)

    def check_columns(self):
        all_moves = list(self.possible_moves)
        star = sorted(
            [move for move in all_moves if
             [square for square in move if type(self.game.board[square[0]][square[1]]) == float]],
            reverse=True)
        if len(star) != 0:
            all_moves = star
        b = self.game.copy_board(self.game.board)
        scores = {}
        for move in all_moves:
            for square in move:
                self.game.board[square[0]][square[1]] = 0
            scores[sum([sum(([bool(val) for val in col]))**0.01 for col in zip(*self.game.board)])] = move
            self.game.board = deepcopy(b)
        return scores[min(scores.keys())]

    def user_input(self):
        def format_move(move):
            return frozenset([(int(m.split(",")[0]), int(m.split(",")[1])) for m in move.split()])
        move = format_move(input("Enter move: "))
        while move not in self.possible_moves:
             move = format_move(input("Move not valid, enter move: "))
        return move

def play_and_print(player):
    while not player.game.is_game_over:
        player.game.print_board()
        print("numbers: ", player.game.num_dices)
        print("colors: ", end='')
        for c in player.game.color_dices:
            print(f"{color_list[c]}██", end=' ')
        print(color_list[0])
        move = player.strategy()
        if player.strategy != player.user_input:
            print(f"possible moves:{[list(move) for move in player.possible_moves]}\nmove :{[square for square in move]}")
        player.game.make_move(move)
        player.game.turn += 1
        player.game.update_state()
        player.game.roll_dices()
        player.possible_moves = player.game.get_possible_moves()
    player.game.print_board()
    print("Game Over")
    print(f"Score: {player.game.get_game_score()}")
    print(f"Colors: {player.game.colors_done} Columns {player.game.columns_done}")
    return player.game.get_game_score()

def play_no_print(player):
    while not player.game.is_game_over:
        player.game.make_move(player.strategy())
        player.game.turn += 1
        player.game.update_state()
        player.game.roll_dices()
        player.possible_moves = player.game.get_possible_moves()
    return player.game.get_game_score()

def play_repeat(i, player):
    total_score = 0
    for instance in range(i):
        player.game = NochMal()
        total_score += play_no_print(player)
    return total_score / i

def main():
    player = PlayerClass()
    print("Welcome to Noch Mal")
    choice = input("Who wants to play? You -> 0 or Computer -> 1\n>")
    if choice == "0":
        player.strategy = player.user_input
        play_and_print(player)
    elif choice == "1":
        strategy = input("Choose a strategy: Random -> 0 or Star -> 1 or Columns -> 2\n>")
        if strategy == "0": player.strategy = player.random_move
        elif strategy == "1": player.strategy = player.check_star
        elif strategy == "2": player.strategy = player.check_columns
        mode = input("Show moves or get average score? Show moves -> 0 average score -> 1\n>")
        if mode == "0": play_and_print(player)
        elif mode == "1": print(play_repeat(int(input("How many times to simulate the game?\n>")),player))

if __name__ == "__main__":
    main()


