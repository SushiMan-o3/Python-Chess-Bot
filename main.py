from __future__ import annotations
from typing import Optional, Tuple, List
import chess
import time
import random

from engine import get_best_move
import utils

class ChessGame:
    def __init__(self, board: Optional[chess.Board] = None):
        """Initialize the chess game with a new board or a given board."""
        if board is None:
            self.board = chess.Board()
        else:
            self.board = board
        


if __name__ == "__main__":
    pass