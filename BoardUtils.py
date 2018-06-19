import numpy as np


class BoardUtils:

    @staticmethod
    def blocks_every_line(board, opponent):
        return BoardUtils.blocks_column(board, opponent, 0) and \
               BoardUtils.blocks_column(board, opponent, 1) and \
               BoardUtils.blocks_column(board, opponent, 2) and \
               BoardUtils.blocks_row(board, opponent, 0) and \
               BoardUtils.blocks_row(board, opponent, 1) and \
               BoardUtils.blocks_row(board, opponent, 2) and \
               BoardUtils.blocks_diagonals(board, opponent)

    @staticmethod
    def blocks_row(board, opponent, row):
        for j in range(0, 3):
            if board[row][j] == opponent or board[row][j] == 'Tie':
                return True
        return False

    @staticmethod
    def blocks_column(board, opponent, col):
        for i in range(0, 3):
            if board[i][col] == opponent or board[i][col] == 'Tie':
                return True
        return False

    @staticmethod
    def blocks_diagonals(board, opponent):
        i = 0
        j = 2
        while i != 3:
            if board[i][j] == opponent or board[i][j] == 'Tie':
                return True
            i += 1
            j -= 1
        i = 0
        j = 0
        while i != 3:
            if board[i][j] == opponent or board[i][j] == 'Tie':
                return True
            i += 1
            j += 1
        return False

    @staticmethod
    def grid_to_2d_array(grid):
        arr = np.ndarray(shape=(3, 3), dtype=object)
        for i in range(0, 3):
            for j in range(0, 3):
                arr[i][j] = grid.itemAtPosition(i, j).widget().label.text()
        return arr

    @staticmethod
    def won_column(board, symbol, j):
        for i in range(0,3):
            if board[i][j] != symbol:
                return False
        return True

    @staticmethod
    def won_row(board, symbol, i):
        for j in range(0, 3):
            if board[i][j] != symbol:
                return False
        return True

    @staticmethod
    def won_left_diagonal(board, symbol):
        i = 0
        while i < 3:
            if board[i][i] != symbol:
                return False
            i += 1
        return True

    @staticmethod
    def won_right_diagonal(board, symbol):
        i = 0
        j = 2
        while i < 3:
            if board[i][j] != symbol:
                return False
            i += 1
            j -= 1
        return True

    @staticmethod
    def winner_move(board, symbol):
        if BoardUtils.won_left_diagonal(board, symbol):
            return 0, 0, 2, 2, 'diagonal left'
        if BoardUtils.won_right_diagonal(board, symbol):
            return 0, 2, 2, 0, 'diagonal right'
        if BoardUtils.won_column(board, symbol, 0):
            return 0, 0, 2, 0, 'col'
        if BoardUtils.won_column(board, symbol, 1):
            return 0, 1, 2, 1, 'col'
        if BoardUtils.won_column(board, symbol, 2):
            return 0, 2, 2, 2, 'col'
        if BoardUtils.won_row(board, symbol, 0):
            return 0, 0, 0, 2, 'row'
        if BoardUtils.won_row(board, symbol, 1):
            return 1, 0, 1, 2, 'row'
        if BoardUtils.won_row(board, symbol, 2):
            return 2, 0, 2, 2, 'row'
        return None

    @staticmethod
    def is_tie(board, p1, p2):
        if BoardUtils.blocks_every_line(board, p1) and BoardUtils.blocks_every_line(board, p2):
            return -1, -1, -1, -1
        return None

