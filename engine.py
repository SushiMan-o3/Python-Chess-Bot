import chess
import math
from evaluation import PIECE_VALUES, CHECKMATE, evaluate
from typing import Tuple
from utils import list_of_sorted_moves
import json


def get_best_move(board: chess.Board, depth: int, maximizing_player: chess.Color) -> chess.Move:
    """
    Get the best move for the current player using a simple evaluation function.
    """
    original_player = maximizing_player
    original_depth = depth
    
    def _helper(board: chess.Board, depth: int, alpha, beta) -> Tuple[int, chess.Move]:
        """
        Helper that finds the best move using minimax with alpha-beta pruning. 
        """
        # base cases
        outcome = board.outcome()

        if outcome is not None:
            if outcome.winner is None:
                return 0, None
            
            depth_factor = original_depth - depth

            if outcome.winner == original_player:
                return CHECKMATE - depth_factor, None
            else:
                return -CHECKMATE + depth_factor, None

        if depth == 0:
            eval_of_pos = evaluate(board)
            if board.turn == original_player:
                return eval_of_pos, None
            else:
                return -eval_of_pos, None

        
        # Recursive step
        legal_moves = list_of_sorted_moves(board)
        best_move = legal_moves[0]
        
        if board.turn == original_player:
            best_score = float("-inf")
        else:
            best_score = float("inf")

    
        for move in legal_moves:
            board.push(move)
            score, _ = _helper(board, depth-1, alpha, beta)
            board.pop()

            if board.turn == original_player:
                if score > best_score:
                    best_score = score
                    best_move = move
                alpha = max(alpha, best_score)
            else:
                if score < best_score:
                    best_score = score
                    best_move = move
                beta = min(beta, best_score)
            
            if beta <= alpha:
                break  
        
        return best_score, best_move
    
    try:
        with open('opening_book.json', 'r') as file:
            opening_book = json.load(file)
            if board.fen() in opening_book:
                return opening_book[board.fen()]
    except FileNotFoundError:
        pass


    return _helper(board, depth, float("-inf"), float("inf"))[1]
