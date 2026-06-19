import chess
import random

# Material value evaluation metrics
PIECE_VALUES = {
    chess.PAWN: 10,
    chess.KNIGHT: 30,
    chess.BISHOP: 30,
    chess.ROOK: 50,
    chess.QUEEN: 90,
    chess.KING: 900
}

def evaluate_board(board):
    """
    Evaluates the score of the current board state.
    Positive scores favor White; Negative scores favor Black.
    """
    if board.is_checkmate():
        if board.turn == chess.WHITE:
            return -9999  # Black wins
        else:
            return 9999   # White wins
    if board.is_stalemate() or board.is_insufficient_material():
        return 0

    score = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            value = PIECE_VALUES[piece.piece_type]
            if piece.color == chess.WHITE:
                score += value
            else:
                score -= value
    return score

def alpha_beta(board, depth, alpha, beta, maximizing_player):
    """
    Core Minimax Algorithm enhanced with Alpha-Beta Pruning.
    """
    if depth == 0 or board.is_game_over():
        return evaluate_board(board), None

    legal_moves = list(board.legal_moves)
    # Simple move ordering optimization: evaluate captures first
    legal_moves.sort(key=lambda move: board.is_capture(move), reverse=True)

    best_move = None

    if maximizing_player:
        max_eval = float('-inf')
        for move in legal_moves:
            board.push(move)
            evaluation, _ = alpha_beta(board, depth - 1, alpha, beta, False)
            board.pop()
            
            if evaluation > max_eval:
                max_eval = evaluation
                best_move = move
                
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break  # Beta cutoff (Pruning)
        return max_eval, best_move

    else:
        min_eval = float('inf')
        for move in legal_moves:
            board.push(move)
            evaluation, _ = alpha_beta(board, depth - 1, alpha, beta, True)
            board.pop()
            
            if evaluation < min_eval:
                min_eval = evaluation
                best_move = move
                
            beta = min(beta, evaluation)
            if beta <= alpha:
                break  # Alpha cutoff (Pruning)
        return min_eval, best_move

def play_game():
    """
    Launches a text-based game console loop where you play against the AI.
    """
    board = chess.Board()
    print("Welcome to Alpha-Beta Chess AI!")
    print(board)
    print("-" * 20)

    # Human player is White, AI is Black
    while not board.is_game_over():
        if board.turn == chess.WHITE:
            # Human turn
            print("Your turn (White). Enter your move in standard UCI format (e.g., e2e4):")
            move_str = input("Move: ").strip()
            try:
                move = chess.Move.from_uci(move_str)
                if move in board.legal_moves:
                    board.push(move)
                else:
                    print("Illegal move! Try again.")
                    continue
            except ValueError:
                print("Invalid format. Use UCI format like 'g1f3'.")
                continue
        else:
            # AI Turn
            print("\nAI is calculating its move using Alpha-Beta Pruning...")
            # Depth 3 balancing speed and tactical competence
            _, ai_move = alpha_beta(board, depth=3, alpha=float('-inf'), beta=float('inf'), maximizing_player=False)
            if ai_move:
                board.push(ai_move)
                print(f"AI played: {ai_move.uci()}")
            else:
                break

        print("\n", board)
        print("-" * 20)

    print("Game Over. Result:", board.result())

if __name__ == "__main__":
    play_game()
