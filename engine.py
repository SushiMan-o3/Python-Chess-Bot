import chess
from evaluation import PIECE_VALUES, CHECKMATE, evaluate
from typing import Tuple
import json


def get_best_move(board: chess.Board, depth: int, maximizing_player: chess.Color) -> chess.Move:
    """
    Get the best move for the current player using a simple evaluation function.
    """
    original_player = maximizing_player
    original_depth = depth
    
    def _helper(board: chess.Board, depth: int, alpha, beta, current_player: chess.Color) -> Tuple[int, chess.Move]:
        """
        Helper that finds best move. Used for recurisve purposes. 
        """
        if board.is_checkmate():
            if current_player == original_player:
                return -CHECKMATE + (original_depth - depth), None
            else:
                return CHECKMATE - (original_depth - depth), None
            
        if board.is_variant_draw():
            return 0, None
        
        if (
            board.is_stalemate()
            or board.is_insufficient_material()
            or board.can_claim_fifty_moves()
            or board.can_claim_threefold_repetition()
        ):
            return 0, None

        if depth == 0:
            eval_of_pos = evaluate(board)
            if current_player == original_player:
                return eval_of_pos, None
            else:
                return -eval_of_pos, None

        # sorts it based on captures and piece value to improve alpha beta pruning
        legal_moves = sorted(
            board.legal_moves,
            key=lambda move: (
                not board.is_capture(move),
                -PIECE_VALUES.get(board.piece_type_at(move.to_square), 0),
                PIECE_VALUES.get(board.piece_type_at(move.from_square), 0)
            )
        )


        if legal_moves == []:
            best_move = None
        else:
            best_move = legal_moves[0]
        

        if current_player == original_player:
            best_score = float("-inf")
        else:
            best_score = float("inf")

    
        for move in legal_moves:
            board.push(move)
            score, _ = _helper(board, depth-1, alpha, beta, not current_player)
            board.pop()

            if current_player == original_player:
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

    return _helper(board, depth, float("-inf"), float("inf"), maximizing_player)[1]