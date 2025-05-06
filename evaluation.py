import chess
import utils

PIECE_VALUES = {
        chess.PAWN: 1.00,
        chess.KNIGHT: 3.20,
        chess.BISHOP: 3.30,
        chess.ROOK: 5.00,
        chess.QUEEN: 9.00,
        chess.KING: 0
    }

def evaluate(board: chess.Board) -> float:
    """
    Evaluates a given position using its piece-values. 
    """
    eval = 0

    for square, piece in board.piece_map().items():
        if piece.color == chess.WHITE:
            eval += PIECE_VALUES[piece.piece_type]
        else:
            eval -= PIECE_VALUES[piece.piece_type]

    return eval


