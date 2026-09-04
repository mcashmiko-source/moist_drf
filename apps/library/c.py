import chess

# Starting position
board = chess.Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

print(f"Total legal moves: {len(list(board.legal_moves))}\n")

# Show each move with the resulting FEN position
for move in board.legal_moves:
    # Make the move on a copy of the board
    new_board = board.copy()
    new_board.push(move)
    
    # Get the move in SAN notation and the resulting FEN
    san_move = board.san(move)
    fen_after = new_board.fen()
    
    print(f"Move: {san_move:>6} -> FEN: {fen_after}")