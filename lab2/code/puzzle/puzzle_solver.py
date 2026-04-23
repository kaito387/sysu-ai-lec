"""
15-Puzzle Solver using Heuristic Search Algorithms
Implements: A* and IDA* with multiple heuristics
"""

import heapq
from typing import List, Tuple, Optional, Set
import time


class PuzzleState:
    """Represents a state of the 15-puzzle"""
    
    def __init__(self, board: List[List[int]], parent=None, move: str = ""):
        self.board = [row[:] for row in board]  # Deep copy
        self.parent = parent
        self.move = move
        self.g = 0 if parent is None else parent.g + 1
        self.h = 0
        self.f = 0
        
        # Find blank position
        self.blank_pos = None
        for i in range(4):
            for j in range(4):
                if board[i][j] == 0:
                    self.blank_pos = (i, j)
                    break
    
    def __lt__(self, other):
        return self.f < other.f
    
    def __eq__(self, other):
        return self.board == other.board
    
    def __hash__(self):
        return hash(str(self.board))
    
    def get_neighbors(self) -> List['PuzzleState']:
        """Generate all possible next states"""
        neighbors = []
        i, j = self.blank_pos
        
        # Possible moves: up, down, left, right
        moves = [
            ((-1, 0), "Up"),
            ((1, 0), "Down"),
            ((0, -1), "Left"),
            ((0, 1), "Right")
        ]
        
        for (di, dj), move_name in moves:
            ni, nj = i + di, j + dj
            if 0 <= ni < 4 and 0 <= nj < 4:
                # Create new board
                new_board = [row[:] for row in self.board]
                new_board[i][j], new_board[ni][nj] = new_board[ni][nj], new_board[i][j]
                neighbors.append(PuzzleState(new_board, self, move_name))
        
        return neighbors
    
    def get_path(self) -> List[str]:
        """Get the path from initial state to this state"""
        path = []
        current = self
        while current.parent:
            path.append(current.move)
            current = current.parent
        return path[::-1]
    
    def __str__(self):
        lines = []
        for row in self.board:
            lines.append(' '.join(f'{x:2d}' if x != 0 else ' .' for x in row))
        return '\n'.join(lines)


def manhattan_distance(state: PuzzleState, goal: PuzzleState) -> int:
    """Calculate Manhattan distance heuristic"""
    distance = 0
    goal_positions = {}
    
    # Build goal position map
    for i in range(4):
        for j in range(4):
            if goal.board[i][j] != 0:
                goal_positions[goal.board[i][j]] = (i, j)
    
    # Calculate distances
    for i in range(4):
        for j in range(4):
            if state.board[i][j] != 0:
                value = state.board[i][j]
                goal_i, goal_j = goal_positions[value]
                distance += abs(i - goal_i) + abs(j - goal_j)
    
    return distance


def misplaced_tiles(state: PuzzleState, goal: PuzzleState) -> int:
    """Calculate number of misplaced tiles heuristic"""
    count = 0
    for i in range(4):
        for j in range(4):
            if state.board[i][j] != 0 and state.board[i][j] != goal.board[i][j]:
                count += 1
    return count


def linear_conflict(state: PuzzleState, goal: PuzzleState) -> int:
    """Manhattan distance + linear conflict heuristic"""
    md = manhattan_distance(state, goal)
    # conflict means two tiles are in the same row/column and both are in their goal row/column but reversed order, which adds 2 moves to resolve
    
    # Add linear conflicts
    conflicts = 0
    
    # Row conflicts
    for i in range(4):
        for j in range(4):
            if state.board[i][j] == 0:
                continue
            for k in range(j + 1, 4):
                if state.board[i][k] == 0:
                    continue
                
                # Check if both tiles belong to same row in goal
                val_j = state.board[i][j]
                val_k = state.board[i][k]
                
                # Find goal positions
                goal_j_pos = None
                goal_k_pos = None
                for gi in range(4):
                    for gj in range(4):
                        if goal.board[gi][gj] == val_j:
                            goal_j_pos = (gi, gj)
                        if goal.board[gi][gj] == val_k:
                            goal_k_pos = (gi, gj)
                
                if goal_j_pos and goal_k_pos:
                    if goal_j_pos[0] == i and goal_k_pos[0] == i:
                        if goal_j_pos[1] > goal_k_pos[1]:
                            conflicts += 1
    
    # Column conflicts
    for j in range(4):
        for i in range(4):
            if state.board[i][j] == 0:
                continue
            for k in range(i + 1, 4):
                if state.board[k][j] == 0:
                    continue
                
                val_i = state.board[i][j]
                val_k = state.board[k][j]
                
                # Find goal positions
                goal_i_pos = None
                goal_k_pos = None
                for gi in range(4):
                    for gj in range(4):
                        if goal.board[gi][gj] == val_i:
                            goal_i_pos = (gi, gj)
                        if goal.board[gi][gj] == val_k:
                            goal_k_pos = (gi, gj)
                
                if goal_i_pos and goal_k_pos:
                    if goal_i_pos[1] == j and goal_k_pos[1] == j:
                        if goal_i_pos[0] > goal_k_pos[0]:
                            conflicts += 1
    
    return md + 2 * conflicts


def a_star(initial: PuzzleState, goal: PuzzleState, heuristic_func) -> Optional[PuzzleState]:
    """A* Search Algorithm"""
    
    initial.h = heuristic_func(initial, goal)
    initial.f = initial.g + initial.h
    
    open_set = [initial]
    closed_set = set()
    nodes_expanded = 0
    
    while open_set:
        current = heapq.heappop(open_set)
        nodes_expanded += 1
        
        if current.board == goal.board:
            print(f"Nodes expanded: {nodes_expanded}")
            return current
        
        closed_set.add(hash(str(current.board)))
        
        for neighbor in current.get_neighbors():
            if hash(str(neighbor.board)) in closed_set:
                continue
            
            neighbor.h = heuristic_func(neighbor, goal)
            neighbor.f = neighbor.g + neighbor.h
            
            heapq.heappush(open_set, neighbor)
    
    return None


def ida_star(initial: PuzzleState, goal: PuzzleState, heuristic_func) -> Optional[PuzzleState]:
    """IDA* Search Algorithm"""
    
    def search(path: List[PuzzleState], g: int, threshold: int, nodes_expanded: List[int]) -> Tuple[Optional[PuzzleState], int]:
        current = path[-1]
        current.h = heuristic_func(current, goal)
        f = g + current.h
        
        if f > threshold:
            return None, f
        
        if current.board == goal.board:
            return current, -1
        
        min_threshold = float('inf')
        nodes_expanded[0] += 1
        
        for neighbor in current.get_neighbors():
            # Avoid going back to parent
            if len(path) > 1 and neighbor.board == path[-2].board:
                continue
            
            path.append(neighbor)
            result, new_threshold = search(path, g + 1, threshold, nodes_expanded)
            
            if result:
                return result, -1
            
            if new_threshold < min_threshold:
                min_threshold = new_threshold
            
            path.pop()
        
        return None, min_threshold
    
    threshold = heuristic_func(initial, goal)
    path = [initial]
    nodes_expanded = [0]
    
    while True:
        result, new_threshold = search(path, 0, threshold, nodes_expanded)
        
        if result:
            print(f"Nodes expanded: {nodes_expanded[0]}")
            return result
        
        if new_threshold == float('inf'):
            return None
        
        threshold = new_threshold


def test_puzzle_solver():
    """Test the puzzle solvers"""
    
    # Easy puzzle (few moves from goal)
    easy_board = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 0, 15]
    ]
    
    # Medium puzzle
    medium_board = [
        [1, 2, 3, 4],
        [5, 6, 0, 8],
        [9, 10, 7, 11],
        [13, 14, 15, 12]
    ]
    
    # Harder puzzle
    hard_board = [
        [5, 1, 2, 4],
        [9, 6, 3, 8],
        [13, 15, 10, 11],
        [14, 0, 7, 12]
    ]

    extreme_hard_board = [
        [0, 5, 15, 14],
        [7, 9, 6, 13],
        [1, 2, 12, 10],
        [8, 11, 4, 3]
    ]
    
    # Goal state
    goal_board = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 15, 0]
    ]
    
    test_cases = [
        ("Easy", easy_board),
        ("Medium", medium_board),
        ("Hard", hard_board),
        ("Extreme Hard", extreme_hard_board), # May take too long
    ]
    
    heuristics = [
        ("Manhattan Distance", manhattan_distance),
        ("Misplaced Tiles", misplaced_tiles),
        ("Linear Conflict", linear_conflict),
    ]
    
    for puzzle_name, board in test_cases:
        print("\n" + "=" * 60)
        print(f"{puzzle_name} Puzzle:")
        print("=" * 60)
        
        initial = PuzzleState(board)
        goal = PuzzleState(goal_board)
        
        print("\nInitial State:")
        print(initial)
        
        for heuristic_name, heuristic_func in heuristics:
            continue
            print(f"\n--- A* with {heuristic_name} ---")
            start_time = time.time()
            result = a_star(PuzzleState(board), goal, heuristic_func)
            end_time = time.time()
            
            if result:
                path = result.get_path()
                print(f"Solution found! Moves: {len(path)}")
                print(f"Time: {end_time - start_time:.4f}s")
                print(f"Path: {' -> '.join(path)}")
            else:
                print("No solution found")
        
        # Test IDA* with Manhattan distance (usually most efficient)
        print(f"\n--- IDA* with Manhattan Distance ---")
        start_time = time.time()
        result = ida_star(PuzzleState(board), goal, linear_conflict)
        end_time = time.time()
        
        if result:
            path = result.get_path()
            print(f"Solution found! Moves: {len(path)}")
            print(f"Time: {end_time - start_time:.4f}s")
            print(f"Path: {' -> '.join(path)}")
        else:
            print("No solution found")


if __name__ == "__main__":
    test_puzzle_solver()
