import math, time
from tqdm import tqdm 
import numpy as np


class eggychess:
    def __init__(self):
        # 3x3 board where each cell can hold a piece: 0 for empty, 1 for small, 2 for medium, 3 for big
        # Player 1's pieces are positive, Player 2's pieces are negative (e.g., 3 = big for player 1, -3 = big for player 2)
        self.board = np.zeros((3, 3))
        # self.board = np.array([1, 1, 1, 1, 1, 1, -1, -1, -1]) # testing purpose
        self.current_player = 1  # Player 1 starts
        self.win_conditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]

        self.num_pieces = [0, 3, 3, 2, 2, 3, 3]

    def reset(self):
        self.board = np.zeros(9)
        self.num_pieces = [0, 3, 3, 2, 2, 3, 3]
        return board, self.num_pieces

    def can_place_piece(self, index, piece):
        # Check if the move is valid: the spot is either empty or has a smaller piece from the opponent
        if self.board[index] == 0:
            return True
        # player:
        elif self.current_player == 1 and self.board[index] < 0 and abs(self.board[index]) < piece and self.num_pieces[
            piece * self.current_player] > 0:
            return True
        # AI:
        elif self.current_player == -1 and self.board[index] > 0 and self.board[index] < piece and self.num_pieces[
            piece * self.current_player] > 0:
            return True
        return False

    def place_piece(self, index, piece):
        self.board[index] = piece * self.current_player  # Place the piece
        self.num_pieces[piece * self.current_player] -= 1

    def remove_piece(self, index, piece, previous_state):
        self.board[index] = previous_state
        self.num_pieces[piece * self.current_player] -= 1

    def generate_possible_moves(self):
        possible_moves = []
        for index in range(9):
            for size in range(3):
                if self.can_place_piece(index, size):
                    possible_moves.append(size * self.current_player)
        return possible_moves

    def check_win_fullBoard(self):
        player_count = np.sum(self.board > 0)
        ai_count = np.sum(self.board < 0)

        return player_count > ai_count

    def check_win(self):  # need fixing
        for condition in self.win_conditions:
            if all(x > 0 for x in self.board[condition]):
                return 1 # player wins
            elif all(x > 0 for x in self.board[condition]):
                return -1 # ai wins

        if np.any(self.board != 0):  # board is full
            if (len(self.generate_possible_moves()) > 0):
                return False # ongoing
            else:
                self.check_win_fullBoard() # True if player wins, False otherwise
        else:
            return 0 # ongoing

    def heuristic_evaluation(self, depth):
        player_score = np.sum(self.board[self.board > 0])
        ai_score = np.sum(self.board[self.board < 0])

        return (ai_score - player_score) / (depth + 1)

    def minimax(self, depth, alpha, beta, max_depth=5):
        if self.check_win():


    def aiMove():
        pass


env = eggychess()
