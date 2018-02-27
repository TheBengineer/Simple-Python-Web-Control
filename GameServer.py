import time

from threading import Thread
from threading import Lock


class Game(Thread):
    """
    This class holds the server side game logic. (Aka game state)
    """

    def __init__(self):
        Thread.__init__(self)
        self.board = [[" "] * 3 for i in range(3)]
        self.board[1][1] = "X"
        self.board[0][1] = "O"
        self.lock = Lock()  # This allows the data to be safe even when accessed by multiple threads.
        self.game_start_time = time.time()
        self.game_time = 0
        self.go = True
        print self.draw_board()

    def draw_board(self):
        with self.lock:
            return '\n--+---+--\n'.join(["{} | {} | {}".format(*i) for i in self.board])

    def reset_board(self):
        with self.lock:
            self.board = [[" "] * 3 for i in range(3)]

    def check_win(self, player):
        ways_to_win = [
            [[0, 0], [0, 1], [0, 2]],  # Vertical
            [[1, 0], [1, 1], [1, 2]],
            [[2, 0], [2, 1], [2, 2]],

            [[0, 0], [1, 1], [2, 2]],
            [[2, 0], [1, 1], [0, 2]],  # Cross

            [[0, 0], [1, 0], [2, 0]],
            [[0, 1], [1, 1], [2, 1]],
            [[0, 2], [1, 2], [2, 2]],  # Horizontal
        ]
        with self.lock:
            for i in ways_to_win:
                if sum([1 if self.board[x][y] == player else 0 for x, y in i]) == 3:
                    return True
            return False

    def check_board_full(self):
        with self.lock:
            for i in self.board:
                for j in i:
                    if j == " ":
                        return False
        return True

    def check_cell_open(self, x, y):
        with self.lock:  # checks out the lock and returns it when access is done
            if not 2 >= x >= 0:
                raise IndexError("Tried to access out of bounds board cell: x{}".format(x))
            if not 2 >= y >= 0:
                raise IndexError("Tried to access out of bounds board cell: y{}".format(y))
            if self.board[x][y] == " ":
                return True
            else:
                return False

    def play_cell(self, cell, player):
        try:
            x, y = cell
        except:
            raise ValueError("Invalid cell coordinated:", cell)
        if not 2 >= x >= 0:
            raise IndexError("Tried to access out of bounds board cell: x{}".format(x))
        if not 2 >= y >= 0:
            raise IndexError("Tried to access out of bounds board cell: y{}".format(y))
        if not player == "X" and not player == "O":
            raise ValueError("Not a valid player:", player)
        if self.check_cell_open(x, y):
            with self.lock:
                self.board[x][y] = player
        if self.check_win("X"):
            print "X wins"
            self.reset_board()
        if self.check_win("O"):
            print "O wins"
            self.reset_board()
        print self.draw_board()

    def run(self):
        while self.go:  # Game server mainloop
            self.game_time = time.time() - self.game_start_time
            time.sleep(.1)
