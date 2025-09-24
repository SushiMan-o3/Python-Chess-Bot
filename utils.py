import chess
from evaluation import PIECE_VALUES

def list_of_sorted_moves(board: chess.Board):
    """
    Sorts the legal moves based on captures and piece value to improve alpha-beta pruning.
    """
    return sorted(
        board.legal_moves,
        key=lambda move: (
            not board.is_capture(move),
            -PIECE_VALUES.get(board.piece_type_at(move.to_square), 0),
            PIECE_VALUES.get(board.piece_type_at(move.from_square), 0)
        )
    )