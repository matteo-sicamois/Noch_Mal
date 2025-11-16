#Noch mal
import copy
import random
import itertools

class colors:
    PINK = TWO = '\033[95m'
    BLUE = FOUR = '\033[94m'
    GREEN = ONE = '\033[92m'
    YELLOW = FIVE = '\033[93m'
    RED = THREE = '\033[91m'
    NORMAL = '\033[0m'

color_list = ['\033[0m','\033[92m','\033[95m','\033[91m','\033[94m','\033[93m']

class Node:
    def __init__(self, value):
        self.value = value
        self.children = []

def print_board_debug(board):
    for row in board:
        print(*row, sep=' ')

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
        self.board = [[1, 1, 1, 5, 5, 5, 5, 1.0, 4, 4, 4, 2.0, 5, 5, 5],
                      [2, 1, 5, 1, 5, 5, 2, 2, 3, 4, 4, 2, 2, 1, 1],
                      [4.0, 1, 3, 1, 1, 1, 1.0, 3, 3, 3, 5, 5, 2, 1, 1],
                      [4, 3, 3, 2, 2, 2, 4, 4, 1, 1, 5, 5, 2, 3.0, 4],
                      [3, 1, 2, 2, 2, 3, 4, 4, 2, 2, 2, 3, 3, 3, 3],
                      [3, 4.0, 4, 3.0, 3, 3, 3, 5, 5, 2, 3.0, 4, 4, 4, 2.0],
                      [5, 5, 4, 4, 4, 4, 3, 5, 5, 1, 1, 1, 1.0, 2, 2]]
                      #Green = 1 Pink = 2 Red = 3 Blue = 4 Yellow = 5
        #              A  B  C  D  E  F  G  H  I  J  K  L  M  N  O
        self.turn = 0
        self.score = 0
        self.color_dices = []
        self.num_dices = []
        self.columns_done = []
        self.colors_done = []
        self.start_column = 7
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

        def get_move_notation(board,target):
            move = []
            for i_row, row in enumerate(board):
                for i_col, item in enumerate(row):
                    if item == target: move.append((i_row,i_col))
            return frozenset(move)

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

        def build_tree(board,max_depth, current_depth=0):
            node = Node(board)
            if current_depth == max_depth:
                possible_moves.add(get_move_notation(board,-1))
                return node
            row = 0
            while row < len(board):
                col = 0
                while col < len(board[0]):
                    if board[row][col] == color and has_neighbor(board, row, col, -1):
                        board_copy = copy.deepcopy(board)
                        board_copy[row][col] = -1
                        child_node = build_tree(board_copy, max_depth, current_depth + 1)
                        node.children.append(child_node)
                    col += 1
                row += 1
            return node

        def visualize_tree(node, indent_level=0): #stolen
            """
            Recursively prints a simple visualization of the game tree.
            """
            # 1. Create indentation strings
            # The 'tree_indent' is for the "Node" line
            # The 'board_indent' is for the board lines, indented one level further
            tree_indent = "  " * indent_level
            board_indent = "  " * (indent_level + 1)

            # 2. Print this node's information
            if indent_level > 0:
                print(f"{tree_indent}└── Node (Depth {indent_level})")
            else:
                print(f"Root Node (Depth 0)")

            # 3. Print this node's board, nicely formatted
            if not node.value:
                print(f"{board_indent}[Empty Board]")
            else:
                # Find max width for cell alignment (e.g., -1 vs 0)
                try:
                    # Handle potential empty boards or non-number data
                    max_w = max(len(str(cell)) for row in node.value for cell in row)
                    if max_w == 0: max_w = 1
                except (ValueError, TypeError):
                    max_w = 1  # Default width

                for row in node.value:
                    # Format each cell to be the same width (rjust)
                    formatted_row = [str(cell).rjust(max_w) for cell in row]
                    print(f"{board_indent}| {' '.join(formatted_row)} |")

            # 4. Recurse for all children
            for child in node.children:
                visualize_tree(child, indent_level + 1) #s

        for color in  self.color_dices:
            for number in self.num_dices:
                for start in find_start(self.board):
                    board_copy = copy.deepcopy(self.board)
                    board_copy[start[0]][start[1]] = -1
                    tree= build_tree(board_copy,number-1,0)
                    #visualize_tree(root,0)

        return possible_moves

    def make_move(self, move):#[(5,0),(6,0),(5,1)]
        for square in move:
            self.board[square[0]][square[1]] = 0

    def update_state(self):
        for color in range(1,6):
            if color not in list(itertools.chain.from_iterable(self.board)) + self.colors_done:
                self.colors_done.append(color)
        for n,column in enumerate(zip(*self.board)):
            if column.count(0) == len(column) and n not in self.columns_done:
                self.columns_done.append(n)
        if len(self.colors_done) == 2:
            self.is_game_over = True
        if self.turn == 30:
            self.is_game_over = True

    def get_game_state(self):
        pass

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
        for i in range(len(self.board[0])):
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

def play(game):

    def format_move(move):
        return frozenset([(int(m.split(",")[0]), int(m.split(",")[1])) for m in move.split()])

    while not game.is_game_over:
        game.print_board()
        print("numbers: ", game.num_dices)
        print("colors: ", end='')
        for c in game.color_dices:
            print(f"{color_list[c]}██", end=' ')
        print(color_list[0])
        move = format_move(input("Enter move: "))
        while move not in game.get_possible_moves():
            move = format_move(input("Move not valid, enter move: "))
        game.make_move(move)
        game.turn += 1
        game.update_state()
        game.roll_dices()
    game.print_board()
    print("Game Over")
    print(f"Score: {game.get_game_score()}")
    print(f"Colors: {game.colors_done} Columns {game.columns_done}")

def computer_player(game):
    while not game.is_game_over:
        game.make_move(check_star(game))
        game.turn += 1
        game.update_state()
        game.roll_dices()
    return game.get_game_score()

def random_move(game):
    return random.choice(list((game.get_possible_moves())))

def check_star(game):
    for move in game.get_possible_moves():
        for square in move:
            if type(game.board[square[0]][square[1]]) == float:
                return move
    return random.choice(list((game.get_possible_moves())))

def play_random(i):
    total_score = 0
    for _ in range(i):
        game = NochMal()
        total_score += computer_player(game)
    return total_score/i



 #-16.662
#play(NochMal())







