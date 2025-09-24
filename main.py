from __future__ import annotations
import chess

from engine import get_best_move

def start():
    board = chess.Board()

    while True:
        try:
            received = input()
        except EOFError:
            break

        if received == "uci":
            print("id name SushimsEngine")
            print("id author Sushim Malla")
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
                fen_index = tokens.index("fen") + 1
                fen_parts = []
                for part in tokens[fen_index:]:
                    if part == "moves":
                        break
                    fen_parts.append(part)
                fen = " ".join(fen_parts)
                board.set_fen(fen)

                if "moves" in tokens:
                    moves_index = tokens.index("moves") + 1 + len(fen_parts)
                    for move_str in tokens[moves_index:]:
                        board.push_uci(move_str)

        elif received == "ucinewgame":
            board = chess.Board()

        elif received.startswith("go"):
            move = get_best_move(board, depth=5, maximizing_player=board.turn)
            print(f"bestmove {move.uci()}")

        elif received == "quit":
            break

if __name__ == "__main__":
    start()
