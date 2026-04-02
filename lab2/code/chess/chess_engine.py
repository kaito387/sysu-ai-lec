"""
Chinese Chess (象棋) Engine
Implements game rules, board representation, and piece movements
"""

from typing import List, Tuple, Optional
from copy import deepcopy


class ChessPiece:
    """Represents a chess piece"""
    
    # Piece types
    JIANG = 'K'  # 将/帅 (King)
    SHI = 'A'     # 士/仕 (Advisor/Guard)
    XIANG = 'B'   # 象/相 (Bishop/Elephant)
    MA = 'N'      # 马 (Knight/Horse)
    CHE = 'R'     # 车/車 (Rook/Chariot)
    PAO = 'C'     # 炮/砲 (Cannon)
    BING = 'P'    # 兵/卒 (Pawn/Soldier)
    
    def __init__(self, piece_type: str, is_red: bool):
        self.type = piece_type
        self.is_red = is_red
    
    def __str__(self):
        # Red pieces: uppercase, Black pieces: lowercase
        return self.type if self.is_red else self.type.lower()
    
    def __repr__(self):
        return str(self)


class ChessBoard:
    """Chinese Chess Board (9x10)"""
    
    def __init__(self):
        self.board = [[None for _ in range(9)] for _ in range(10)]
        self.red_turn = True
        self.move_history = []
        self.setup_initial_position()
    
    def setup_initial_position(self):
        """Set up initial chess position"""
        # Black pieces (top, rows 0-4)
        self.board[0][4] = ChessPiece(ChessPiece.JIANG, False)
        self.board[0][3] = ChessPiece(ChessPiece.SHI, False)
        self.board[0][5] = ChessPiece(ChessPiece.SHI, False)
        self.board[0][2] = ChessPiece(ChessPiece.XIANG, False)
        self.board[0][6] = ChessPiece(ChessPiece.XIANG, False)
        self.board[0][1] = ChessPiece(ChessPiece.MA, False)
        self.board[0][7] = ChessPiece(ChessPiece.MA, False)
        self.board[0][0] = ChessPiece(ChessPiece.CHE, False)
        self.board[0][8] = ChessPiece(ChessPiece.CHE, False)
        self.board[2][1] = ChessPiece(ChessPiece.PAO, False)
        self.board[2][7] = ChessPiece(ChessPiece.PAO, False)
        self.board[3][0] = ChessPiece(ChessPiece.BING, False)
        self.board[3][2] = ChessPiece(ChessPiece.BING, False)
        self.board[3][4] = ChessPiece(ChessPiece.BING, False)
        self.board[3][6] = ChessPiece(ChessPiece.BING, False)
        self.board[3][8] = ChessPiece(ChessPiece.BING, False)
        
        # Red pieces (bottom, rows 5-9)
        self.board[9][4] = ChessPiece(ChessPiece.JIANG, True)
        self.board[9][3] = ChessPiece(ChessPiece.SHI, True)
        self.board[9][5] = ChessPiece(ChessPiece.SHI, True)
        self.board[9][2] = ChessPiece(ChessPiece.XIANG, True)
        self.board[9][6] = ChessPiece(ChessPiece.XIANG, True)
        self.board[9][1] = ChessPiece(ChessPiece.MA, True)
        self.board[9][7] = ChessPiece(ChessPiece.MA, True)
        self.board[9][0] = ChessPiece(ChessPiece.CHE, True)
        self.board[9][8] = ChessPiece(ChessPiece.CHE, True)
        self.board[7][1] = ChessPiece(ChessPiece.PAO, True)
        self.board[7][7] = ChessPiece(ChessPiece.PAO, True)
        self.board[6][0] = ChessPiece(ChessPiece.BING, True)
        self.board[6][2] = ChessPiece(ChessPiece.BING, True)
        self.board[6][4] = ChessPiece(ChessPiece.BING, True)
        self.board[6][6] = ChessPiece(ChessPiece.BING, True)
        self.board[6][8] = ChessPiece(ChessPiece.BING, True)
    
    def get_piece(self, row: int, col: int) -> Optional[ChessPiece]:
        """Get piece at position"""
        if 0 <= row < 10 and 0 <= col < 9:
            return self.board[row][col]
        return None
    
    def is_in_palace(self, row: int, col: int, is_red: bool) -> bool:
        """Check if position is in palace (九宫格)"""
        if is_red:
            return 7 <= row <= 9 and 3 <= col <= 5
        else:
            return 0 <= row <= 2 and 3 <= col <= 5
    
    def is_valid_move(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> bool:
        """Check if a move is valid"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        # Check bounds
        if not (0 <= to_row < 10 and 0 <= to_col < 9):
            return False
        
        piece = self.get_piece(from_row, from_col)
        if not piece:
            return False
        
        # Check turn
        if piece.is_red != self.red_turn:
            return False
        
        target = self.get_piece(to_row, to_col)
        # Can't capture own piece
        if target and target.is_red == piece.is_red:
            return False
        
        # Check piece-specific movement rules
        if piece.type == ChessPiece.JIANG:
            return self._is_valid_jiang_move(from_pos, to_pos, piece.is_red)
        elif piece.type == ChessPiece.SHI:
            return self._is_valid_shi_move(from_pos, to_pos, piece.is_red)
        elif piece.type == ChessPiece.XIANG:
            return self._is_valid_xiang_move(from_pos, to_pos, piece.is_red)
        elif piece.type == ChessPiece.MA:
            return self._is_valid_ma_move(from_pos, to_pos)
        elif piece.type == ChessPiece.CHE:
            return self._is_valid_che_move(from_pos, to_pos)
        elif piece.type == ChessPiece.PAO:
            return self._is_valid_pao_move(from_pos, to_pos)
        elif piece.type == ChessPiece.BING:
            return self._is_valid_bing_move(from_pos, to_pos, piece.is_red)
        
        return False
    
    def _is_valid_jiang_move(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int], is_red: bool) -> bool:
        """Validate Jiang (King) move: one step in palace"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        # Must stay in palace
        if not self.is_in_palace(to_row, to_col, is_red):
            return False
        
        # One step orthogonally
        return abs(from_row - to_row) + abs(from_col - to_col) == 1
    
    def _is_valid_shi_move(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int], is_red: bool) -> bool:
        """Validate Shi (Advisor) move: one step diagonally in palace"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        # Must stay in palace
        if not self.is_in_palace(to_row, to_col, is_red):
            return False
        
        # One step diagonally
        return abs(from_row - to_row) == 1 and abs(from_col - to_col) == 1
    
    def _is_valid_xiang_move(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int], is_red: bool) -> bool:
        """Validate Xiang (Elephant) move: two steps diagonally, can't cross river"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        # Can't cross river
        if is_red and to_row < 5:
            return False
        if not is_red and to_row > 4:
            return False
        
        # Two steps diagonally
        if abs(from_row - to_row) != 2 or abs(from_col - to_col) != 2:
            return False
        
        # Check blocking (elephant eye)
        mid_row = (from_row + to_row) // 2
        mid_col = (from_col + to_col) // 2
        return self.get_piece(mid_row, mid_col) is None
    
    def _is_valid_ma_move(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> bool:
        """Validate Ma (Horse) move: L-shape, check for blocking"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        dr = abs(from_row - to_row)
        dc = abs(from_col - to_col)
        
        # L-shape movement
        if not ((dr == 2 and dc == 1) or (dr == 1 and dc == 2)):
            return False
        
        # Check for blocking (马腿)
        if dr == 2:
            block_row = from_row + (1 if to_row > from_row else -1)
            return self.get_piece(block_row, from_col) is None
        else:
            block_col = from_col + (1 if to_col > from_col else -1)
            return self.get_piece(from_row, block_col) is None
    
    def _is_valid_che_move(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> bool:
        """Validate Che (Rook) move: straight line with no blocking"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        # Must be straight line
        if from_row != to_row and from_col != to_col:
            return False
        
        # Check for pieces in between
        if from_row == to_row:
            start, end = min(from_col, to_col), max(from_col, to_col)
            for col in range(start + 1, end):
                if self.get_piece(from_row, col):
                    return False
        else:
            start, end = min(from_row, to_row), max(from_row, to_row)
            for row in range(start + 1, end):
                if self.get_piece(row, from_col):
                    return False
        
        return True
    
    def _is_valid_pao_move(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> bool:
        """Validate Pao (Cannon) move: straight line, jump one piece to capture"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        # Must be straight line
        if from_row != to_row and from_col != to_col:
            return False
        
        target = self.get_piece(to_row, to_col)
        pieces_between = 0
        
        if from_row == to_row:
            start, end = min(from_col, to_col), max(from_col, to_col)
            for col in range(start + 1, end):
                if self.get_piece(from_row, col):
                    pieces_between += 1
        else:
            start, end = min(from_row, to_row), max(from_row, to_row)
            for row in range(start + 1, end):
                if self.get_piece(row, from_col):
                    pieces_between += 1
        
        # If capturing, must jump exactly one piece
        if target:
            return pieces_between == 1
        else:
            return pieces_between == 0
    
    def _is_valid_bing_move(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int], is_red: bool) -> bool:
        """Validate Bing (Pawn) move: forward before river, forward/sideways after"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        # One step only
        if abs(from_row - to_row) + abs(from_col - to_col) != 1:
            return False
        
        # Check direction and river crossing
        if is_red:
            # Red moves up (decreasing row)
            if to_row > from_row:  # Can't move backward
                return False
            # Before crossing river (row >= 5), can only move forward
            if from_row >= 5 and from_col != to_col:
                return False
        else:
            # Black moves down (increasing row)
            if to_row < from_row:  # Can't move backward
                return False
            # Before crossing river (row <= 4), can only move forward
            if from_row <= 4 and from_col != to_col:
                return False
        
        return True
    
    def make_move(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> bool:
        """Make a move if valid"""
        if not self.is_valid_move(from_pos, to_pos):
            return False
        
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        # Record move
        piece = self.board[from_row][from_col]
        captured = self.board[to_row][to_col]
        self.move_history.append((from_pos, to_pos, captured))
        
        # Execute move
        self.board[to_row][to_col] = piece
        self.board[from_row][from_col] = None
        
        # Switch turn
        self.red_turn = not self.red_turn
        
        return True
    
    def get_all_legal_moves(self, is_red: bool) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """Get all legal moves for a side"""
        moves = []
        
        for row in range(10):
            for col in range(9):
                piece = self.get_piece(row, col)
                if piece and piece.is_red == is_red:
                    # Try all possible destinations
                    for to_row in range(10):
                        for to_col in range(9):
                            if self.is_valid_move((row, col), (to_row, to_col)):
                                moves.append(((row, col), (to_row, to_col)))
        
        return moves
    
    def __str__(self):
        """Print board"""
        piece_names = {
            'K': '将', 'A': '士', 'B': '象', 'N': '马', 
            'R': '车', 'C': '炮', 'P': '兵',
            'k': '帅', 'a': '仕', 'b': '相', 'n': '馬',
            'r': '車', 'c': '砲', 'p': '卒'
        }
        
        lines = []
        lines.append("  0 1 2 3 4 5 6 7 8")
        for row in range(10):
            line = f"{row} "
            for col in range(9):
                piece = self.get_piece(row, col)
                if piece:
                    line += piece_names.get(str(piece), str(piece)) + " "
                else:
                    line += "· "
            lines.append(line)
        
        return '\n'.join(lines)


if __name__ == "__main__":
    board = ChessBoard()
    print("Initial Chinese Chess Board:")
    print(board)
    print(f"\nRed's turn: {board.red_turn}")
    print(f"Number of legal moves for Red: {len(board.get_all_legal_moves(True))}")
