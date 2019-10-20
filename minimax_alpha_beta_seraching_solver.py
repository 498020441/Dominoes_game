import random
import copy
import math
from queue import PriorityQueue as PQ

def create_dominoes_game(rows, cols):
    if rows >= 0 and cols >= 0:
        return DominoesGame([[False for c in range(cols)] for r in range(rows)])
    return None


class DominoesGame(object):
    # Required
    def __init__(self, board):
        self.board = board
        self.rows = len(board)
        self.cols = len(board[0])

    def get_board(self):
        return self.board

    def reset(self):
        reset_board = create_dominoes_game(self.rows, self.cols)
        self.board = reset_board.board

    def is_legal_move(self, row, col, vertical):
        if vertical:
            if not self.board[row][col] and not self.board[row+1][col]:
                return True
            return False
        else:
            if not self.board[row][col] and not self.board[row][col+1]:
                return True
            return False

    def legal_moves(self, vertical):
        if vertical:
            for r in range(self.rows-1):
                for c in range(self.cols):
                    if not self.board[r][c] and not self.board[r+1][c]:
                        yield (r, c)
        elif not vertical:
            for r in range(self.rows):
                for c in range(self.cols-1):
                    if not self.board[r][c] and not self.board[r][c+1]:
                        yield (r, c)
        else:
            yield []

    def perform_move(self, row, col, vertical):
        if self.is_legal_move(row, col, vertical):
            if vertical:
                self.board[row][col] = True
                self.board[row+1][col] = True
            else:
                self.board[row][col] = True
                self.board[row][col+1] = True

    def game_over(self, vertical):
        if len(list(self.legal_moves(vertical))) > 0:
            return False
        return True

    def copy(self):
        board_copy = copy.deepcopy(self.board)
        return DominoesGame(board_copy)

    def successors(self, vertical):
        for loc in list(self.legal_moves(vertical)):
            domino_copy = self.copy()
            domino_copy.perform_move(loc[0], loc[1], vertical)
            yield loc, domino_copy

    def get_random_move(self, vertical):
        move_list = list(self.legal_moves(vertical))
        return random.choice(move_list)

    def get_best_move(self, vertical, limit):
        return self.max_player(limit, None, float('-inf'), float('inf'), vertical)

    def max_player(self, limit, position, alpha, beta, vertical):
        h_value = len(list(self.legal_moves(vertical))) - len((list(self.legal_moves(not vertical))))
        if limit == 0 or self.game_over(vertical):
            return position, h_value, 1
        num_leaf_node, max_eval = 0, float('-inf')
        for move, children_node in self.successors(vertical):
            state = list(children_node.min_player(limit - 1, move, alpha, beta, not vertical))
            num_leaf_node += state[2]
            if state[1] > max_eval:
                max_eval = state[1]
                position = move
            alpha = max(alpha, max_eval)
            if alpha >= beta:
                break
        return position, max_eval, num_leaf_node

    def min_player(self, limit, position, alpha, beta, vertical):
        h_value = len(list(self.legal_moves(not vertical))) - len((list(self.legal_moves(vertical))))
        if limit == 0 or self.game_over(vertical):
            return position, h_value, 1
        num_leaf_node, min_eval = 0, float('inf')
        for move, children_node in self.successors(vertical):
            state = list(children_node.max_player(limit-1, move, alpha, beta, not vertical))
            num_leaf_node += state[2]
            if state[1] < min_eval:
                min_eval = state[1]
                position = move
            beta = min(beta, min_eval)
            if beta <= alpha:
                break
        return position, min_eval, num_leaf_node
