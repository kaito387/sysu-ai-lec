"""
Maze Solver using Blind Search Algorithms
Implements: BFS, DFS, DLS, IDS, and Bidirectional Search
"""

from collections import deque
from typing import List, Tuple, Optional, Set


class MazeSolver:
    def __init__(self, maze: List[List[int]]):
        """
        Initialize maze solver
        Args:
            maze: 2D grid where 0=passable, 1=wall, 'S'=start, 'E'=end
        """
        self.maze = maze
        self.rows = len(maze)
        self.cols = len(maze[0]) if maze else 0
        self.start = None
        self.end = None
        
        # Find start and end positions
        for i in range(self.rows):
            for j in range(self.cols):
                if maze[i][j] == 'S':
                    self.start = (i, j)
                elif maze[i][j] == 'E':
                    self.end = (i, j)
    
    def get_neighbors(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Get valid neighboring positions (up, down, left, right)"""
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        neighbors = []
        
        for dx, dy in directions:
            nx, ny = pos[0] + dx, pos[1] + dy
            if (0 <= nx < self.rows and 0 <= ny < self.cols and 
                self.maze[nx][ny] != 1):
                neighbors.append((nx, ny))
        
        return neighbors
    
    def bfs(self) -> Optional[List[Tuple[int, int]]]:
        """Breadth-First Search"""
        if not self.start or not self.end:
            return None
        
        queue = deque([(self.start, [self.start])])
        visited = {self.start}
        
        while queue:
            pos, path = queue.popleft()
            
            if pos == self.end:
                return path
            
            for neighbor in self.get_neighbors(pos):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        
        return None
    
    def dfs(self) -> Optional[List[Tuple[int, int]]]:
        """Depth-First Search"""
        if not self.start or not self.end:
            return None
        
        stack = [(self.start, [self.start])]
        visited = {self.start}
        
        while stack:
            pos, path = stack.pop()
            
            if pos == self.end:
                return path
            
            for neighbor in self.get_neighbors(pos):
                if neighbor not in visited:
                    visited.add(neighbor)
                    stack.append((neighbor, path + [neighbor]))
        
        return None
    
    def dls(self, limit: int) -> Optional[List[Tuple[int, int]]]:
        """Depth-Limited Search"""
        if not self.start or not self.end:
            return None
        
        def dls_recursive(pos: Tuple[int, int], path: List[Tuple[int, int]], 
                         visited: Set[Tuple[int, int]], depth: int) -> Optional[List[Tuple[int, int]]]:
            if pos == self.end:
                return path
            
            if depth >= limit:
                return None
            
            for neighbor in self.get_neighbors(pos):
                if neighbor not in visited:
                    visited.add(neighbor)
                    result = dls_recursive(neighbor, path + [neighbor], visited, depth + 1)
                    if result:
                        return result
                    visited.remove(neighbor)
            
            return None
        
        return dls_recursive(self.start, [self.start], {self.start}, 0)
    
    def ids(self, max_depth: int = 50) -> Optional[List[Tuple[int, int]]]:
        """Iterative Deepening Search"""
        for depth in range(max_depth):
            result = self.dls(depth)
            if result:
                return result
        return None
    
    def bidirectional_search(self) -> Optional[List[Tuple[int, int]]]:
        """Bidirectional Search"""
        if not self.start or not self.end:
            return None
        
        # Forward search from start
        forward_queue = deque([(self.start, [self.start])])
        forward_visited = {self.start: [self.start]}
        
        # Backward search from end
        backward_queue = deque([(self.end, [self.end])])
        backward_visited = {self.end: [self.end]}
        
        while forward_queue and backward_queue:
            # Forward step
            if forward_queue:
                pos, path = forward_queue.popleft()
                
                # Check if we met the backward search
                if pos in backward_visited:
                    backward_path = backward_visited[pos]
                    return path + backward_path[-2::-1]
                
                for neighbor in self.get_neighbors(pos):
                    if neighbor not in forward_visited:
                        new_path = path + [neighbor]
                        forward_visited[neighbor] = new_path
                        forward_queue.append((neighbor, new_path))
            
            # Backward step
            if backward_queue:
                pos, path = backward_queue.popleft()
                
                # Check if we met the forward search
                if pos in forward_visited:
                    forward_path = forward_visited[pos]
                    return forward_path + path[-2::-1]
                
                for neighbor in self.get_neighbors(pos):
                    if neighbor not in backward_visited:
                        new_path = path + [neighbor]
                        backward_visited[neighbor] = new_path
                        backward_queue.append((neighbor, new_path))
        
        return None
    
    def visualize_path(self, path: Optional[List[Tuple[int, int]]]) -> str:
        """Visualize the maze with the solution path"""
        if not path:
            return "No path found!"
        
        # Create a copy of maze for visualization
        visual = []
        for row in self.maze:
            visual.append([str(cell) if cell in [0, 1] else cell for cell in row])
        
        # Mark the path
        for pos in path:
            if pos != self.start and pos != self.end:
                visual[pos[0]][pos[1]] = '*'
        
        # Convert to string
        result = []
        for row in visual:
            result.append(' '.join(str(cell) for cell in row))
        
        return '\n'.join(result)


def test_maze_solver():
    """Test maze solver with sample mazes"""
    
    # Sample maze 1: Simple maze
    maze1 = [
        ['S', 0, 1, 0, 0],
        [0, 0, 1, 0, 1],
        [1, 0, 0, 0, 1],
        [0, 0, 1, 0, 0],
        [0, 1, 0, 0, 'E']
    ]
    
    print("=" * 50)
    print("MAZE 1:")
    print("=" * 50)
    
    solver = MazeSolver(maze1)
    
    algorithms = [
        ("BFS", solver.bfs),
        ("DFS", solver.dfs),
        ("IDS", solver.ids),
        ("Bidirectional", solver.bidirectional_search),
    ]
    
    for name, algorithm in algorithms:
        print(f"\n{name}:")
        path = algorithm()
        if path:
            print(f"Path length: {len(path)}")
            print(f"Path: {' -> '.join([str(p) for p in path])}")
            print("\nVisualization:")
            print(solver.visualize_path(path))
        else:
            print("No path found!")
    
    # Sample maze 2: More complex
    maze2 = [
        ['S', 0, 0, 1, 0, 0, 0],
        [1, 1, 0, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 1, 0],
        [0, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 0],
        [1, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 'E']
    ]
    
    print("\n" + "=" * 50)
    print("MAZE 2:")
    print("=" * 50)
    
    solver2 = MazeSolver(maze2)
    
    for name, algorithm in algorithms:
        print(f"\n{name}:")
        path = algorithm()
        if path:
            print(f"Path length: {len(path)}")
            print(f"Path: {' -> '.join([str(p) for p in path[:5]])} ... {' -> '.join([str(p) for p in path[-3:]])}")
        else:
            print("No path found!")


if __name__ == "__main__":
    test_maze_solver()
