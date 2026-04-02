"""
Chinese Chess AI using Minimax with Alpha-Beta Pruning
"""

from chess_engine import ChessBoard, ChessPiece
from copy import deepcopy
from typing import Tuple, Optional
import random


class ChessAI:
    """AI for Chinese Chess using Minimax with Alpha-Beta pruning"""
    
    # Piece values
    PIECE_VALUES = {
        ChessPiece.JIANG: 10000,
        ChessPiece.CHE: 600,
        ChessPiece.MA: 300,
        ChessPiece.PAO: 300,
        ChessPiece.SHI: 200,
        ChessPiece.XIANG: 200,
        ChessPiece.BING: 100,
    }
    
    def __init__(self, max_depth: int = 3):
        self.max_depth = max_depth
        self.nodes_evaluated = 0
    
    def evaluate_board(self, board: ChessBoard, is_red_maximizing: bool) -> int:
        """
        Evaluate board position
        Positive score favors red, negative favors black
        """
        score = 0
        
        # Material count
        for row in range(10):
            for col in range(9):
                piece = board.get_piece(row, col)
                if piece:
                    value = self.PIECE_VALUES.get(piece.type, 0)
                    
                    # Add positional bonus for advanced pawns
                    if piece.type == ChessPiece.BING:
                        if piece.is_red and row < 5:  # Crossed river
                            value += 50
                        elif not piece.is_red and row >= 5:
                            value += 50
                    
                    # Add position value
                    if piece.is_red:
                        score += value
                    else:
                        score -= value
        
        # Mobility (number of legal moves)
        red_moves = len(board.get_all_legal_moves(True))
        black_moves = len(board.get_all_legal_moves(False))
        score += (red_moves - black_moves) * 5
        
        # Return from perspective of maximizing player
        return score if is_red_maximizing else -score
    
    def minimax_alpha_beta(self, board: ChessBoard, depth: int, alpha: float, 
                          beta: float, is_maximizing: bool, 
                          is_red_turn: bool) -> Tuple[int, Optional[Tuple]]:
        """
        Minimax algorithm with alpha-beta pruning
        
        Args:
            board: Current board state
            depth: Remaining search depth
            alpha: Best value for maximizer
            beta: Best value for minimizer
            is_maximizing: True if maximizing player's turn
            is_red_turn: True if it's red's turn
        
        Returns:
            (score, best_move)
        """
        self.nodes_evaluated += 1
        
        # Terminal conditions
        if depth == 0:
            return self.evaluate_board(board, is_red_turn), None
        
        legal_moves = board.get_all_legal_moves(is_red_turn)
        
        # No legal moves (checkmate/stalemate)
        if not legal_moves:
            return -10000 if is_maximizing else 10000, None
        
        best_move = None
        
        if is_maximizing:
            max_eval = float('-inf')
            
            for move in legal_moves:
                # Make move
                from_pos, to_pos = move
                old_board = deepcopy(board)
                board.make_move(from_pos, to_pos)
                
                # Recursive call
                eval_score, _ = self.minimax_alpha_beta(
                    board, depth - 1, alpha, beta, False, not is_red_turn
                )
                
                # Undo move
                board.board = old_board.board
                board.red_turn = old_board.red_turn
                
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
                
                # Alpha-beta pruning
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break  # Beta cutoff
            
            return max_eval, best_move
        
        else:
            min_eval = float('inf')
            
            for move in legal_moves:
                # Make move
                from_pos, to_pos = move
                old_board = deepcopy(board)
                board.make_move(from_pos, to_pos)
                
                # Recursive call
                eval_score, _ = self.minimax_alpha_beta(
                    board, depth - 1, alpha, beta, True, not is_red_turn
                )
                
                # Undo move
                board.board = old_board.board
                board.red_turn = old_board.red_turn
                
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
                
                # Alpha-beta pruning
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break  # Alpha cutoff
            
            return min_eval, best_move
    
    def get_best_move(self, board: ChessBoard, is_red: bool) -> Optional[Tuple]:
        """Get the best move for the current position"""
        self.nodes_evaluated = 0
        
        score, best_move = self.minimax_alpha_beta(
            deepcopy(board), 
            self.max_depth,
            float('-inf'),
            float('inf'),
            True,
            is_red
        )
        
        print(f"Nodes evaluated: {self.nodes_evaluated}, Score: {score}")
        
        return best_move


class RandomAI:
    """Simple random move AI for testing"""
    
    def get_best_move(self, board: ChessBoard, is_red: bool) -> Optional[Tuple]:
        """Pick a random legal move"""
        legal_moves = board.get_all_legal_moves(is_red)
        if legal_moves:
            return random.choice(legal_moves)
        return None


def test_ai():
    """Test the chess AI"""
    print("Testing Chinese Chess AI with Alpha-Beta Pruning")
    print("=" * 60)
    
    board = ChessBoard()
    print("Initial board:")
    print(board)
    
    # Create AIs
    red_ai = ChessAI(max_depth=3)
    black_ai = RandomAI()  # Use random AI for black to speed up testing
    
    move_count = 0
    max_moves = 10  # Limit moves for testing
    
    while move_count < max_moves:
        move_count += 1
        print(f"\n--- Move {move_count} ---")
        
        if board.red_turn:
            print("Red's turn (AI):")
            move = red_ai.get_best_move(board, True)
        else:
            print("Black's turn (Random):")
            move = black_ai.get_best_move(board, False)
        
        if not move:
            print("No legal moves! Game over.")
            break
        
        from_pos, to_pos = move
        print(f"Move: {from_pos} -> {to_pos}")
        
        board.make_move(from_pos, to_pos)
        print(board)
        
        # Check for king capture (game over)
        kings = {'red': False, 'black': False}
        for row in range(10):
            for col in range(9):
                piece = board.get_piece(row, col)
                if piece and piece.type == ChessPiece.JIANG:
                    if piece.is_red:
                        kings['red'] = True
                    else:
                        kings['black'] = True
        
        if not kings['red']:
            print("\nBlack wins!")
            break
        if not kings['black']:
            print("\nRed wins!")
            break
    
    print(f"\nTest completed after {move_count} moves.")


if __name__ == "__main__":
    test_ai()
