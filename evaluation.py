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

# --- Add an endgame king table (simple example) ---
KING_EG_TABLE = [
    -50,-40,-30,-20,-20,-30,-40,-50,
    -30,-20,-10,  0,  0,-10,-20,-30,
    -30,-10, 20, 30, 30, 20,-10,-30,
    -30,-10, 30, 40, 40, 30,-10,-30,
    -30,-10, 30, 40, 40, 30,-10,-30,
    -30,-10, 20, 30, 30, 20,-10,-30,
    -30,-30,  0,  0,  0,  0,-30,-30,
    -50,-30,-30,-30,-30,-30,-30,-50
]

# Phase weights: higher = more midgame
PHASE_WEIGHTS = {
    chess.PAWN: 0,
    chess.KNIGHT: 1,
    chess.BISHOP: 1,
    chess.ROOK: 2,
    chess.QUEEN: 4,
    chess.KING: 0
}
MAX_PHASE = 24  # typical (2Q=8,4R=8,4B=4,4N=4)

def _game_phase(board: chess.Board) -> float:
    phase = 0
    for pt, w in PHASE_WEIGHTS.items():
        phase += w * (len(board.pieces(pt, chess.WHITE)) + len(board.pieces(pt, chess.BLACK)))
    return min(phase, MAX_PHASE) / MAX_PHASE  # 1.0 = midgame, 0.0 = endgame

def _file_of(square: int) -> int:
    return chess.square_file(square)

def _rank_of(square: int) -> int:
    return chess.square_rank(square)

def _pawn_structure(board: chess.Board, color: bool) -> int:
    """Return pawn structure score for one side (positive is good for that side)."""
    pawns = board.pieces(chess.PAWN, color)
    if not pawns:
        return 0

    score = 0
    files = [0]*8
    for sq in pawns:
        files[_file_of(sq)] += 1

    # doubled pawns
    for fcount in files:
        if fcount >= 2:
            score -= 15 * (fcount - 1)

    # isolated pawns
    for f in range(8):
        if files[f] > 0:
            left = files[f-1] if f-1 >= 0 else 0
            right = files[f+1] if f+1 <= 7 else 0
            if left == 0 and right == 0:
                score -= 10 * files[f]

    # passed pawns (simple)
    enemy_pawns = board.pieces(chess.PAWN, not color)
    enemy_by_file = {f: [] for f in range(8)}
    for esq in enemy_pawns:
        enemy_by_file[_file_of(esq)].append(esq)

    for sq in pawns:
        f = _file_of(sq)
        r = _rank_of(sq)
        # check enemy pawns in same/adjacent files that are in front
        ahead = []
        for nf in (f-1, f, f+1):
            if 0 <= nf <= 7:
                ahead.extend(enemy_by_file[nf])
        is_passed = True
        for esq in ahead:
            er = _rank_of(esq)
            if color == chess.WHITE:
                if er > r:  # enemy pawn ahead (toward rank 7)
                    is_passed = False
                    break
            else:
                if er < r:
                    is_passed = False
                    break
        if is_passed:
            # bonus increases as pawn advances
            advance = r if color == chess.WHITE else (7 - r)
            score += 12 + 6 * advance

    return score

def _rook_activity(board: chess.Board, color: bool) -> int:
    score = 0
    rooks = board.pieces(chess.ROOK, color)
    if not rooks:
        return 0

    my_pawns = board.pieces(chess.PAWN, color)
    opp_pawns = board.pieces(chess.PAWN, not color)

    my_pawn_files = set(_file_of(sq) for sq in my_pawns)
    opp_pawn_files = set(_file_of(sq) for sq in opp_pawns)

    for r_sq in rooks:
        f = _file_of(r_sq)
        # open / semi-open file
        if f not in my_pawn_files:
            score += 12  # semi-open
            if f not in opp_pawn_files:
                score += 10  # open

        # 7th rank activity
        rank = _rank_of(r_sq)
        if color == chess.WHITE and rank == 6:
            score += 20
        if color == chess.BLACK and rank == 1:
            score += 20

    return score

def _mobility(board: chess.Board) -> int:
    """Mobility difference (white - black)."""
    turn = board.turn

    board.turn = chess.WHITE
    white_moves = board.legal_moves.count()

    board.turn = chess.BLACK
    black_moves = board.legal_moves.count()

    board.turn = turn
    return white_moves - black_moves

def evaluate(board: chess.Board) -> float:
    # Game over?
    outcome = board.outcome()
    if outcome is not None:
        if outcome.winner is None:
            return 0
        return CHECKMATE if outcome.winner == chess.WHITE else -CHECKMATE

    phase = _game_phase(board)  # 1.0 MG, 0.0 EG

    score = 0

    # Material + PST (with king blended MG/EG)
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is None:
            continue

        pt = piece.piece_type
        base = PIECE_VALUES[pt]

        if piece.color == chess.WHITE:
            score += base
            if pt == chess.KING:
                mg = PIECE_SQUARE_TABLES[chess.KING][square]
                eg = KING_EG_TABLE[square]
                score += phase * mg + (1 - phase) * eg
            else:
                score += PIECE_SQUARE_TABLES[pt][square]
        else:
            score -= base
            msq = chess.square_mirror(square)
            if pt == chess.KING:
                mg = PIECE_SQUARE_TABLES[chess.KING][msq]
                eg = KING_EG_TABLE[msq]
                score -= phase * mg + (1 - phase) * eg
            else:
                score -= PIECE_SQUARE_TABLES[pt][msq]

    # Check bonus/penalty (small)
    if board.is_check():
        score += 30 if board.turn == chess.BLACK else -30  # if black to move and in check, good for white

    # Bishop pair only
    if len(board.pieces(chess.BISHOP, chess.WHITE)) >= 2:
        score += 40
    if len(board.pieces(chess.BISHOP, chess.BLACK)) >= 2:
        score -= 40

    # Pawn structure
    score += _pawn_structure(board, chess.WHITE)
    score -= _pawn_structure(board, chess.BLACK)

    # Rook activity
    score += _rook_activity(board, chess.WHITE)
    score -= _rook_activity(board, chess.BLACK)

    # Mobility (scale down so it doesn't dominate)
    score += 2 * _mobility(board)

    # Castling rights: keep small (they're a proxy)
    if board.has_kingside_castling_rights(chess.WHITE) or board.has_queenside_castling_rights(chess.WHITE):
        score += 10
    if board.has_kingside_castling_rights(chess.BLACK) or board.has_queenside_castling_rights(chess.BLACK):
        score -= 10

    return score


