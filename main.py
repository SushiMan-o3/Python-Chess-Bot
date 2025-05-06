from __future__ import annotations
import chess

from engine import get_best_move
import utils

def start():
    board = chess.Board()

    while True:
        try:
            received = input()
        except EOFError:
            break

        if received == "uci":
            print("id name SimpleEngine")
            print("id author YourName")
            print("uciok")
        elif received == "isready":
            print("readyok")
        elif received.startswith("position"):
            tokens = received.split()
            if "startpos" in tokens:
                board.set_fen(chess.STARTING_FEN)
                if "moves" in tokens:
                    moves_index = tokens.index("moves") + 1
                    for move_str in tokens[moves_index:]:
                        board.push_uci(move_str)
            elif "fen" in tokens:
                # optional: handle FEN setup here later
                pass
        elif received == "ucinewgame":
            board = chess.Board()
        elif received.startswith("go"):
            move = get_best_move(board, depth=3, maximizing_player=chess.WHITE if board.turn else chess.BLACK)
            print(f"bestmove {move.uci()}")
        elif received == "quit":
            break


if __name__ == "__main__":
    start()