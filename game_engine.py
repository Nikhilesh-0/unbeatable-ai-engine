import math

class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]
        self.current_winner = None

    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def empty_squares(self):
        return ' ' in self.board

    def num_empty_squares(self):
        return self.board.count(' ')

    def make_move(self, square, letter):
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def winner(self, square, letter):
        # Check row
        row_ind = square // 3
        row = self.board[row_ind*3 : (row_ind + 1) * 3]
        if all([spot == letter for spot in row]): return True
        
        # Check column
        col_ind = square % 3
        column = [self.board[col_ind+i*3] for i in range(3)]
        if all([spot == letter for spot in column]): return True
        
        # Check diagonals
        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]] 
            if all([spot == letter for spot in diagonal1]): return True
            diagonal2 = [self.board[i] for i in [2, 4, 6]] 
            if all([spot == letter for spot in diagonal2]): return True
        return False

def minimax(position, depth, alpha, beta, maximizing_player):
    # BASE CASE
    if position.current_winner == 'O': 
        return {'position': None, 'score': 1 * (position.num_empty_squares() + 1)}
    if position.current_winner == 'X': 
        return {'position': None, 'score': -1 * (position.num_empty_squares() + 1)}
    if not position.empty_squares():   
        return {'position': None, 'score': 0}

    if maximizing_player:
        max_eval = {'position': None, 'score': -math.inf}
        for move in position.available_moves():
            position.make_move(move, 'O')
            sim_score = minimax(position, depth + 1, alpha, beta, False)
            position.board[move] = ' '
            position.current_winner = None
            
            sim_score['position'] = move
            if sim_score['score'] > max_eval['score']:
                max_eval = sim_score
            
            # Alpha-Beta Pruning
            alpha = max(alpha, sim_score['score'])
            if beta <= alpha:
                break
        return max_eval

    else:
        min_eval = {'position': None, 'score': math.inf}
        for move in position.available_moves():
            position.make_move(move, 'X')
            sim_score = minimax(position, depth + 1, alpha, beta, True)
            position.board[move] = ' '
            position.current_winner = None
            
            sim_score['position'] = move
            if sim_score['score'] < min_eval['score']:
                min_eval = sim_score
            
            # Alpha-Beta Pruning
            beta = min(beta, sim_score['score'])
            if beta <= alpha:
                break
        return min_eval