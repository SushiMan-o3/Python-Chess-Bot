import chess

PIECE_VALUES = {
        chess.PAWN: 100,
        chess.KNIGHT: 320,
        chess.BISHOP: 330,
        chess.ROOK: 500,
        chess.QUEEN: 900,
        chess.KING: 0
    }

# Piece square tables for white, not to use it for black
PIECE_SQUARE_TABLES = {
    chess.PAWN: [
         0,   0,   0,   0,   0,   0,   0,   0,
         5,  10,  10, -20, -20,  10,  10,   5,
         5,  -5, -10,   0,   0, -10,  -5,   5,
         0,   0,   0,  20,  20,   0,   0,   0,
         5,   5,  10,  25,  25,  10,   5,   5,
        10,  10,  20,  30,  30,  20,  10,  10,
        50,  50,  50,  50,  50,  50,  50,  50,
         0,   0,   0,   0,   0,   0,   0,   0
    ],
    chess.KNIGHT: [
        -50, -40, -30, -30, -30, -30, -40, -50,
        -40, -20,   0,   0,   0,   0, -20, -40,
        -30,   0,  10,  15,  15,  10,   0, -30,
        -30,   5,  15,  20,  20,  15,   5, -30,
        -30,   0,  15,  20,  20,  15,   0, -30,
        -30,   5,  10,  15,  15,  10,   5, -30,
        -40, -20,   0,   5,   5,   0, -20, -40,
        -50, -40, -30, -30, -30, -30, -40, -50
    ],
    chess.BISHOP: [
        -20, -10, -10, -10, -10, -10, -10, -20,
        -10,   0,   0,   0,   0,   0,   0, -10,
        -10,   0,   5,  10,  10,   5,   0, -10,
        -10,   5,   5,  10,  10,   5,   5, -10,
        -10,   0,  10,  10,  10,  10,   0, -10,
        -10,  10,  10,  10,  10,  10,  10, -10,
        -10,   5,   0,   0,   0,   0,   5, -10,
        -20, -10, -10, -10, -10, -10, -10, -20
    ],
    chess.ROOK: [
         0,   0,   0,   0,   0,   0,   0,   0,
         5,  10,  10,  10,  10,  10,  10,   5,
        -5,   0,   0,   0,   0,   0,   0,  -5,
        -5,   0,   0,   0,   0,   0,   0,  -5,
        -5,   0,   0,   0,   0,   0,   0,  -5,
        -5,   0,   0,   0,   0,   0,   0,  -5,
        -5,   0,   0,   0,   0,   0,   0,  -5,
         0,   0,   0,   5,   5,   0,   0,   0
    ],
    chess.QUEEN: [
        -20, -10, -10,  -5,  -5, -10, -10, -20,
        -10,   0,   0,   0,   0,   0,   0, -10,
        -10,   0,   5,   5,   5,   5,   0, -10,
         -5,   0,   5,   5,   5,   5,   0,  -5,
          0,   0,   5,   5,   5,   5,   0,  -5,
        -10,   5,   5,   5,   5,   5,   0, -10,
        -10,   0,   5,   0,   0,   0,   0, -10,
        -20, -10, -10,  -5,  -5, -10, -10, -20
    ],
    chess.KING: [
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -20, -30, -30, -40, -40, -30, -30, -20,
        -10, -20, -20, -20, -20, -20, -20, -10,
         20,  20,   0,   0,   0,   0,  20,  20,
         20,  30,  10,   0,   0,  10,  30,  20
    ]
}

CHECKMATE = 10000
    
def evaluate(board: chess.Board) -> float:
    """
    Evaluates a given position using its piece-values. 
    """
    eval = 0

    # Checks if the game is over
    if board.outcome() is not None:
        if board.outcome().winner is None:
            return 0
        
        if board.outcome().result == "1-0":
            return CHECKMATE
        
        if board.outcome().result == "0-1":
            return -CHECKMATE

    # Evaluate material and position based on piece-square tables
    for square in chess.SQUARES:
        piece = board.piece_at(square)

        if piece is not None:
            value = PIECE_VALUES[piece.piece_type]
            if piece.color == chess.WHITE:
                eval += value
                eval += PIECE_SQUARE_TABLES[piece.piece_type][square]
            else:
                eval -= value
                eval -= PIECE_SQUARE_TABLES[piece.piece_type][chess.square_mirror(square)]

    # Checks if the king is in check
    if board.is_check():
        if board.turn == chess.WHITE:
            eval -= 50
        else:
            eval += 50
        
    # Checks for king safety on both sides
    if board.has_kingside_castling_rights(chess.WHITE):
        eval += 30
    if board.has_queenside_castling_rights(chess.WHITE):
        eval += 30
    if board.has_kingside_castling_rights(chess.BLACK):
        eval -= 30
    if board.has_queenside_castling_rights(chess.BLACK):
        eval -= 30


    # Checks for bishop pair
    if len(board.pieces(chess.BISHOP, chess.WHITE)) >= 2:
        eval += 50
    if len(board.pieces(chess.BISHOP, chess.BLACK)) >= 2:
        eval -= 50

    # Checks for knight pair
    if len(board.pieces(chess.KNIGHT, chess.WHITE)) >= 2:
        eval += 50
    if len(board.pieces(chess.KNIGHT, chess.BLACK)) >= 2:
        eval -= 50

    # Checks for rook pair
    if len(board.pieces(chess.ROOK, chess.WHITE)) >= 2:
        eval += 50
    if len(board.pieces(chess.ROOK, chess.BLACK)) >= 2:
        eval -= 50

    # checks the mobility of each piece
    # Checks whether pawns are double or triple, isolated, protected, etc. 

    return eval


