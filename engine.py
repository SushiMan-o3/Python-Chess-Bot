import chess
from evaluation import evaluate
from typing import Tuple
import utils

def get_best_move(board: chess.Board, depth: int, maximizing_player: int) -> chess.Move:
    """
    Get the best move for the current player using a simple evaluation function.
    """
    def _helper(board: chess.Board, depth: int, maximizing_player: int) -> Tuple[int, chess.Move]:
        """
        Helper that finds best move. Used for recurisve purposes. 
        """
        # TODO Base Cases
        if board.is_checkmate():
            return 
        
        if board.is_variant_draw():
            return 
        
        best_move = None
        best_score = None
        
        for move in board.legal_moves:
            board.push_san(move)
            evaluation_of_board = evaluate(board)

            # TODO All recursive calls
            if maximizing_player == chess.BLACK:
                # make recursive call here with depth -1
                _helper(board, depth-1, chess.WHITE)
                pass
            else:
                # make recursive call here
                _helper(board, depth-1, chess.BLACK)
                pass
            
            board.pop()
        
        return best_score, best_move
    
    return _helper(board, depth, maximizing_player)[1]