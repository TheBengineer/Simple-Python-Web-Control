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
        self.lock = Lock()  # This allows the data to be safe even when accessed by multiple threads.
        self.game_start_time = time.time()
        self.game_time = 0
        self.go = True
        self.print_board()

    def print_board(self):
        with self.lock:
            print '\n--+---+--\n'.join(["{} | {} | {}".format(*i) for i in self.board])

    def check_win(self):
        pass

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
        if not player == "X" or player == "O":
            raise ValueError("Not a valid player:", player)
        self.board[x][y] = player:

    def run(self):
        while self.go:  # Game server mainloop
            self.game_time = time.time() - self.game_start_time
            time.sleep(.1)
