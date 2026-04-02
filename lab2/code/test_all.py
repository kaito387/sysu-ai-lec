#!/usr/bin/env python3
"""
Quick verification script to test all implementations
"""

import sys
import os

def test_maze():
    """Test maze solver"""
    print("\n" + "="*60)
    print("Testing Task 2.1: Maze Solver")
    print("="*60)
    
    sys.path.insert(0, 'maze')
    from maze_solver import MazeSolver
    
    maze = [
        ['S', 0, 1, 0],
        [0, 0, 1, 0],
        [1, 0, 0, 0],
        [0, 0, 1, 'E']
    ]
    
    solver = MazeSolver(maze)
    path = solver.bfs()
    
    if path:
        print(f"✓ BFS found path with {len(path)} steps")
        return True
    else:
        print("✗ BFS failed")
        return False


def test_puzzle():
    """Test 15-puzzle solver"""
    print("\n" + "="*60)
    print("Testing Task 2.2: 15-Puzzle Solver")
    print("="*60)
    
    sys.path.insert(0, 'puzzle')
    from puzzle_solver import PuzzleState, a_star, manhattan_distance
    
    # Easy puzzle
    board = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 0, 15]
    ]
    
    goal_board = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 15, 0]
    ]
    
    initial = PuzzleState(board)
    goal = PuzzleState(goal_board)
    
    result = a_star(initial, goal, manhattan_distance)
    
    if result:
        path = result.get_path()
        print(f"✓ A* found solution with {len(path)} moves")
        return True
    else:
        print("✗ A* failed")
        return False


def test_chess():
    """Test chess engine"""
    print("\n" + "="*60)
    print("Testing Task 2.3: Chinese Chess AI")
    print("="*60)
    
    sys.path.insert(0, 'chess')
    from chess_engine import ChessBoard
    from chess_ai import ChessAI
    
    board = ChessBoard()
    ai = ChessAI(max_depth=2)
    
    move = ai.get_best_move(board, True)
    
    if move:
        print(f"✓ AI found move: {move}")
        return True
    else:
        print("✗ AI failed")
        return False


def test_tsp():
    """Test TSP genetic algorithm"""
    print("\n" + "="*60)
    print("Testing Task 2.4: TSP Genetic Algorithm")
    print("="*60)
    
    sys.path.insert(0, 'tsp')
    from tsp_data import create_sample_dataset
    from tsp_ga import GeneticAlgorithmTSP
    
    dataset = create_sample_dataset(8)
    ga = GeneticAlgorithmTSP(
        dataset=dataset,
        population_size=30,
        elite_size=5,
        mutation_rate=0.02
    )
    
    best_solution, best_fitness = ga.evolve(generations=20, verbose=False)
    
    if best_solution and best_fitness < float('inf'):
        print(f"✓ GA found solution with fitness: {best_fitness:.2f}")
        return True
    else:
        print("✗ GA failed")
        return False


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("AI Lab 2 - Verification Script")
    print("="*60)
    
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    results = []
    
    try:
        results.append(("Maze Solver", test_maze()))
    except Exception as e:
        print(f"✗ Maze test error: {e}")
        results.append(("Maze Solver", False))
    
    try:
        results.append(("15-Puzzle", test_puzzle()))
    except Exception as e:
        print(f"✗ Puzzle test error: {e}")
        results.append(("15-Puzzle", False))
    
    try:
        results.append(("Chess AI", test_chess()))
    except Exception as e:
        print(f"✗ Chess test error: {e}")
        results.append(("Chess AI", False))
    
    try:
        results.append(("TSP GA", test_tsp()))
    except Exception as e:
        print(f"✗ TSP test error: {e}")
        results.append(("TSP GA", False))
    
    # Summary
    print("\n" + "="*60)
    print("Summary")
    print("="*60)
    
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status} - {name}")
    
    all_passed = all(result[1] for result in results)
    
    print("\n" + "="*60)
    if all_passed:
        print("✓ All tests passed!")
    else:
        print("✗ Some tests failed")
    print("="*60)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
