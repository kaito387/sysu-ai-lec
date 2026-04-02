"""
Chinese Chess Game Interface
Supports Human vs AI and AI vs AI modes
"""

from chess_engine import ChessBoard
from chess_ai import ChessAI, RandomAI


class ChessGame:
    """Game controller for Chinese Chess"""
    
    def __init__(self):
        self.board = ChessBoard()
        self.red_player = None  # 'human', 'ai', or 'random'
        self.black_player = None
        self.red_ai = None
        self.black_ai = None
    
    def setup_game(self, red_player: str = 'human', black_player: str = 'ai', ai_depth: int = 3):
        """
        Setup game mode
        
        Args:
            red_player: 'human', 'ai', or 'random'
            black_player: 'human', 'ai', or 'random'
            ai_depth: Search depth for AI
        """
        self.red_player = red_player
        self.black_player = black_player
        
        if red_player == 'ai':
            self.red_ai = ChessAI(max_depth=ai_depth)
        elif red_player == 'random':
            self.red_ai = RandomAI()
        
        if black_player == 'ai':
            self.black_ai = ChessAI(max_depth=ai_depth)
        elif black_player == 'random':
            self.black_ai = RandomAI()
    
    def parse_move(self, move_str: str):
        """Parse move string like '9,4 to 8,4' or '94 84'"""
        move_str = move_str.replace('to', ' ').replace(',', ' ')
        parts = move_str.split()
        
        if len(parts) >= 4:
            from_row = int(parts[0])
            from_col = int(parts[1])
            to_row = int(parts[2])
            to_col = int(parts[3])
            return (from_row, from_col), (to_row, to_col)
        elif len(parts) >= 2:
            from_str = parts[0]
            to_str = parts[1]
            if len(from_str) == 2 and len(to_str) == 2:
                from_row = int(from_str[0])
                from_col = int(from_str[1])
                to_row = int(to_str[0])
                to_col = int(to_str[1])
                return (from_row, from_col), (to_row, to_col)
        
        return None
    
    def play_turn(self):
        """Play one turn"""
        print(f"\n{'Red' if self.board.red_turn else 'Black'}'s turn")
        
        current_player = self.red_player if self.board.red_turn else self.black_player
        current_ai = self.red_ai if self.board.red_turn else self.black_ai
        
        if current_player == 'human':
            # Human player
            while True:
                try:
                    move_input = input("Enter move (e.g., '9,4 to 8,4' or '94 84') or 'quit': ")
                    
                    if move_input.lower() == 'quit':
                        return False
                    
                    move = self.parse_move(move_input)
                    if move:
                        from_pos, to_pos = move
                        if self.board.make_move(from_pos, to_pos):
                            print(f"Move executed: {from_pos} -> {to_pos}")
                            break
                        else:
                            print("Invalid move! Try again.")
                    else:
                        print("Invalid format! Use '9,4 to 8,4' or '94 84'")
                except Exception as e:
                    print(f"Error: {e}")
        
        else:
            # AI player
            print("AI is thinking...")
            move = current_ai.get_best_move(self.board, self.board.red_turn)
            
            if move:
                from_pos, to_pos = move
                self.board.make_move(from_pos, to_pos)
                print(f"AI move: {from_pos} -> {to_pos}")
            else:
                print("No legal moves available!")
                return False
        
        return True
    
    def check_game_over(self):
        """Check if game is over"""
        kings = {'red': False, 'black': False}
        
        for row in range(10):
            for col in range(9):
                piece = self.board.get_piece(row, col)
                if piece and piece.type == 'K':
                    if piece.is_red:
                        kings['red'] = True
                    else:
                        kings['black'] = True
        
        if not kings['red']:
            return 'black'
        if not kings['black']:
            return 'red'
        
        # Check if current player has no legal moves
        if not self.board.get_all_legal_moves(self.board.red_turn):
            return 'black' if self.board.red_turn else 'red'
        
        return None
    
    def play(self, max_moves: int = 100):
        """Play the game"""
        print("=" * 60)
        print(f"Chinese Chess Game: {self.red_player.upper()} (Red) vs {self.black_player.upper()} (Black)")
        print("=" * 60)
        
        move_count = 0
        
        while move_count < max_moves:
            print(f"\n--- Move {move_count + 1} ---")
            print(self.board)
            
            if not self.play_turn():
                break
            
            winner = self.check_game_over()
            if winner:
                print("\n" + "=" * 60)
                print(self.board)
                print(f"\nGame Over! {winner.upper()} wins!")
                print("=" * 60)
                break
            
            move_count += 1
        
        if move_count >= max_moves:
            print(f"\nGame ended after {max_moves} moves (draw).")


def main():
    """Main entry point"""
    print("\nChinese Chess Game")
    print("=" * 60)
    print("\nGame Modes:")
    print("1. Human (Red) vs AI (Black)")
    print("2. AI (Red) vs AI (Black)")
    print("3. Human (Red) vs Random AI (Black)")
    print("4. AI (Red) vs Random AI (Black) - Fast Demo")
    
    choice = input("\nSelect mode (1-4): ").strip()
    
    game = ChessGame()
    
    if choice == '1':
        game.setup_game('human', 'ai', ai_depth=3)
        game.play()
    elif choice == '2':
        game.setup_game('ai', 'ai', ai_depth=2)  # Lower depth for faster play
        game.play(max_moves=30)
    elif choice == '3':
        game.setup_game('human', 'random')
        game.play()
    elif choice == '4':
        game.setup_game('ai', 'random', ai_depth=3)
        game.play(max_moves=20)
    else:
        print("Invalid choice!")


if __name__ == "__main__":
    main()
