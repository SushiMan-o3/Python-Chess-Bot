import chess

PIECE_VALUES = {
        chess.PAWN: 100,
        chess.KNIGHT: 320,
        chess.BISHOP: 330,
        chess.ROOK: 500,
        chess.QUEEN: 900,
        chess.KING: 0
    }

COLOR_MULTIPLIER = {
        chess.WHITE: 1,
        chess.BLACK: -1
    }


def evaluate(board: chess.Board) -> float:
    """
    Evaluates a given position using its piece-values. 
    """
    eval = 0

    if board.outcome() is not None:
        if board.outcome().result == "1-0":
            return 10000
        
        if board.outcome().result == "0-1":
            return -10000
    
    if (
        board.is_stalemate()
        or board.is_insufficient_material()
        or board.can_claim_fifty_moves()
        or board.can_claim_threefold_repetition()
    ):
        return 0


    # evaluate based on material
    for square, piece in board.piece_map().items():
        if piece.color == chess.WHITE:
            eval += PIECE_VALUES[piece.piece_type]
        else:
            eval -= PIECE_VALUES[piece.piece_type]

    # award points based on check, capture and attack

    return eval


