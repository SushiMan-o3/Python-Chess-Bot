import chess
import utils
import random

PIECE_VALUES = {
        chess.PAWN: 100,
        chess.KNIGHT: 320,
        chess.BISHOP: 330,
        chess.ROOK: 500,
        chess.QUEEN: 900,
        chess.KING: 0
    }

def evaluate(board: chess.Board) -> float:
    """
    Evaluates a given position using its piece-values. 
    """
    eval = 0

    # evaluate based on material
    for square, piece in board.piece_map().items():
        if piece.color == chess.WHITE:
            eval += PIECE_VALUES[piece.piece_type]
        else:
            eval -= PIECE_VALUES[piece.piece_type]

    if board.has_kingside_castling_rights(chess.WHITE) or board.has_queenside_castling_rights(chess.WHITE):
        eval += 300
    
    if board.has_kingside_castling_rights(chess.BLACK) or board.has_queenside_castling_rights(chess.BLACK):
        eval -= 300

    return random.choice(board.legal_moves)


