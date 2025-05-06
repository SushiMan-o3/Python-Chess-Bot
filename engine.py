import chess
from evaluation import evaluate
from typing import Tuple
import json
import utils

def get_best_move(board: chess.Board, depth: int, maximizing_player: int) -> chess.Move:
    """
    Get the best move for the current player using a simple evaluation function.
    """
    original_player = maximizing_player
    original_depth = depth
    
    def _helper(board: chess.Board, depth: int, current_player: int) -> Tuple[int, chess.Move]:
        """
        Helper that finds best move. Used for recurisve purposes. 
        """
        eval_of_pos = evaluate(board)

        # TODO Base Cases
        if board.is_checkmate():
            if eval_of_pos > 0:
                return eval_of_pos - (original_depth - depth)
            else:
                return eval_of_pos + (original_depth - depth)
        if board.is_variant_draw():
            return 0, None
        
        if depth == 0:
            return eval_of_pos, None
        
        best_move = next(iter(board.legal_moves))

        if current_player == original_player:
            best_score = float("-inf")
        else:
            best_score = float("inf")

        
        for move in board.legal_moves:
            board.push(move)
            score, _ = _helper(board, depth-1, chess.WHITE)
    

            if current_player == original_player:
                if score > best_score:
                    best_score = score
                    best_move = move
            else:
                if score < best_score:
                    best_score = score
                    best_move = move
            
            board.pop()
        
        return best_score, best_move
    
    try:
        with open('opening_book.json', 'r') as file:
            opening_book = json.load(file)
            if board.fen in opening_book:
                return opening_book[board.fen]
    except FileNotFoundError:
        pass

    return _helper(board, depth, maximizing_player)[1]