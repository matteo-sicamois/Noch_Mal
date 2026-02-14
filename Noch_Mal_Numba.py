import numpy as np
from numba import njit
from numba.typed import List
import random
import time

colors = {0: '\x1b[0m', 1: '\x1b[92m', 2: '\x1b[95m', 3: '\x1b[91m', 4: '\x1b[94m', 5: '\x1b[93m', 'NORMAL': '\x1b[0m', 'GREEN': '\x1b[92m', 'PINK': '\x1b[95m', 'RED': '\x1b[91m', 'BLUE': '\x1b[94m', 'YELLOW': '\x1b[93m' }

@njit
def get_hash(x):
    h = 0
    for i in x:
        h = h*31 + (i+2)
    return h

@njit
def insertion_sort(tup, val):
    res = List()
    inserted = False
    plc_hldr_count = tup.count(-1)
    for x in tup:
        if x != -1:
            if val < x and not inserted:
                res.append(val)
                inserted = True
            res.append(x)
    if not inserted:
        res.append(val)
    for _ in range(plc_hldr_count-1):
        res.append(-1)
    return res

class NochMal:
    def __init__(self):               #0, 1, 2, 3, 4, 5, 6  7  8  9 10 11 12 13 14
        self.board = np.array([[1, 1, 1, 5, 5, 5, 5, 1, 4, 4, 4, 2, 5, 5, 1],
                                      [2, 1, 5, 1, 5, 5, 2, 2, 3, 4, 4, 2, 2, 1, 1],
                                      [4, 1, 3, 1, 1, 1, 1, 3, 3, 3, 5, 5, 2, 1, 1],
                                      [4, 3, 3, 2, 2, 2, 4, 4, 1, 1, 5, 5, 2, 3, 4],
                                      [3, 1, 2, 2, 2, 3, 4, 4, 2, 2, 2, 3, 3, 3, 3],
                                      [3, 4, 4, 3, 3, 3, 3, 5, 5, 2, 3, 4, 4, 4, 2],
                                      [5, 5, 4, 4, 4, 4, 3, 5, 5, 1, 1, 1, 1, 2, 2]], dtype = np.int8)
                                      #Green = 1 Pink = 2 Red = 3 Blue = 4 Yellow = 5
                                      #A  B  C  D  E  F  G  H  I  J  K  L  M  N  O
        self.stars = [(0,7),(0,11),(1,2),(1,4),(1,9),(2,0),(2,6),(3,5),(3,13),(5,1),(5,3),(5,8),(5,10),(5,14),(6,12)]
        self.valid = np.zeros((7,15), dtype=np.int8)
        self.valid[:,7] = -1
        self.color_dices = np.array([])
        self.num_dices = np.array([])
        self.roll_dices()
        self.h, self.w = self.board.shape
        self.score_table = np.array([5,4,4,3,3,2,2,1,2,2,3,3,4,4,5])
        self.num_rounds = 30


    def roll_dices(self):
        self.num_dices = np.random.randint(1,6,size=2, dtype=np.int8)
        self.color_dices = np.random.randint(1, 6, size=2, dtype=np.int8)

    @staticmethod
    @njit
    def find_moves(start: np.ndarray, n: list, board: np.ndarray):
        start = list(start)
        n.sort()
        possible_moves = List()
        h, w = board.shape
        flat_board = board.reshape(-1)
        visited = set()
        for x in start:
            x = x[0] * w + x[1]
            starting_node = [-1 if i != 0 else x for i in range(n[-1])]
            stack = [List(starting_node)]
            target = flat_board[x]
            while stack:
                current_move = stack.pop()
                if get_hash(current_move) not in visited:
                    visited.add(get_hash(current_move))
                    if len(current_move) - current_move.count(-1) == n[-1]:
                        possible_moves.append(current_move)
                    else:
                        if len(current_move)- current_move.count(-1) in n:
                            possible_moves.append(current_move)
                        for sqr in current_move:
                            if sqr != -1:
                                if sqr % w != w - 1:
                                    if flat_board[sqr + 1] == target and sqr + 1 not in current_move:
                                        stack.append(insertion_sort(current_move, sqr + 1))
                                if sqr % w != 0:
                                    if flat_board[sqr - 1] == target and sqr - 1 not in current_move:
                                        stack.append(insertion_sort(current_move, sqr - 1))
                                if sqr // w != 0:
                                    if flat_board[sqr - w] == target and sqr - w not in current_move:
                                        stack.append(insertion_sort(current_move, sqr - w))
                                if sqr // w != h - 1:
                                    if flat_board[sqr + w] == target and sqr + w not in current_move:
                                        stack.append(insertion_sort(current_move, sqr +w))

        return [[(square // w, square % w) for square in move] for move in possible_moves]


    def get_possible_moves(self):
        possible_moves = [[]]
        possible_moves += self.find_moves(np.argwhere(((self.board == self.color_dices[0]) | (self.board == self.color_dices[1])) & self.valid),list(self.num_dices),self.board)

        return possible_moves


    def make_move(self,move):
        for square in move:
            r, c = square
            if square in self.stars:
                self.stars.remove(square)
            self.board[r][c] = 0
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.h and 0 <= nc < self.w:
                    self.valid[nr][nc] = -1
        return move


    def get_score(self):
        score = 0
        score += ((self.board.sum(axis=0) == 0) * self.score_table).sum()
        score += (5-len(np.intersect1d(self.board, np.arange(1,6))))*5
        score -= 2*len(self.stars)
        return score


    def print_board(self):
        print("  ", end="")
        for i in range(15):
            if i in [7,8]: print(" ", end="")
            print(f"{i:^2}", end=' ')
        print()
        for r,i in enumerate(self.board):
            print(r, end=" ")
            for c,j in enumerate(i):
                if c in [7+1,7]:
                    print(" ", end="")
                if j == 0:
                    print("[]", end="")
                else: print(f"{colors[j]}{'██' if (r,c) not in self.stars else '◀▶'}", end='')
                print(f" {colors[0]}",end='')
            print()


def user_input(game,possible_moves:set):
    def format_move(move):
        return frozenset([(int(m.split(",")[0]), int(m.split(",")[1])) for m in move.split()])

    move = format_move(input("Enter move: "))
    while move not in possible_moves:
        move = format_move(input("Move not valid, enter move: "))
    return move

def random_move(game, possible_moves):
    return random.choice(possible_moves[1:]) if len(possible_moves)>1 else possible_moves[0]

def check_star(game, possible_moves:set):
    return max(possible_moves, key= lambda x:(len(set(x).intersection(game.stars)), len(x)))

def check_columns(game:NochMal, possible_moves):
    def value_columns(x):
        values = {}
        for square in x:
            values.setdefault(square, game.board[square[0]][square[1]])
            game.board[square[0]][square[1]] = 0
        score =  np.sum(np.sum(game.board.astype(bool), axis=0)**0.01)
        for square in x:
            game.board[square[0]][square[1]] = values[square]
        return score
    return max(possible_moves, key= lambda x:(len(set(x).intersection(game.stars)), -value_columns(x), len(x)))


def play_and_print(game, strategy):
    for i in range(game.num_rounds):
        game.print_board()
        print("numbers: ", game.num_dices)
        print("colors: ", end='')
        for c in game.color_dices:
            print(f"{colors[c]}██", end=' ')
        print(colors[0])
        possible_moves = game.get_possible_moves()
        move = strategy(game, possible_moves)
        if strategy != user_input:
            print(f"possible moves:{[list(move) for move in possible_moves]}\nmove :{[square for square in move]}")
        game.make_move(move)
        game.roll_dices()
    game.print_board()
    print("Game Over")
    score = game.get_score()
    print(f"Score: {score}")
    return score

def play_no_print(strategy, n):
    total_score = 0
    for simulation in range(n):
        game = NochMal()
        for i in range(game.num_rounds):
            game.roll_dices()
            possible_moves = game.get_possible_moves()
            game.make_move(strategy(game, possible_moves))
        total_score += (game.get_score())

    return total_score/n


def main(c1=None,c2=None,c3=None,c4=None):
    game = NochMal()
    print("Welcome to Noch Mal")
    if c1 is None:
        c1 = int(input("Who wants to play? You -> 0 or Computer -> 1\n>"))
    if c1 == 0:
        strategy = user_input
        play_and_print(game, strategy)
    elif c1 == 1:
        if c2 is None:
            c2 = int(input("Choose a strategy: Random -> 0 or Check for stars -> 1 or Columns -> 2\n>"))
        if c2 == 0:strategy = random_move
        elif c2 == 1: strategy = check_star
        elif c2 == 2: strategy = check_columns
        if c3 is None:
            c3 = int(input("Show moves or get average score? Show moves -> 0 average score -> 1\n>"))
        if c3 == 0:
            play_and_print(game, strategy)
        elif c3 == 1:
            if c4 is None:
                c4 = int(input('How many times to simulate the game?\n>'))
            start = time.perf_counter()
            print(f"Average score:{play_no_print(strategy, c4)}, Total time: {time.perf_counter()-start:.2f}")
            print()



if __name__ == "__main__":
    main()
    #c1 you or computer
    #c2 strategy
    #c3 show or average
    #c4 number of games