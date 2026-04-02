"""
TSP Performance Analysis
Run experiments with different parameters and visualize results
"""

import random
import time
from typing import List, Dict
from tsp_data import TSPDataset, create_sample_dataset, load_sample_dataset
from tsp_ga import GeneticAlgorithmTSP


class TSPExperiment:
    """Run and analyze TSP experiments"""
    
    def __init__(self, dataset: TSPDataset):
        self.dataset = dataset
        self.results = []
    
    def run_single_experiment(self, 
                             population_size: int = 100,
                             elite_size: int = 20,
                             mutation_rate: float = 0.02,
                             generations: int = 200,
                             seed: int = None,
                             verbose: bool = False) -> Dict:
        """Run a single experiment"""
        
        if seed is not None:
            random.seed(seed)
        
        ga = GeneticAlgorithmTSP(
            dataset=self.dataset,
            population_size=population_size,
            elite_size=elite_size,
            mutation_rate=mutation_rate
        )
        
        start_time = time.time()
        best_solution, best_fitness = ga.evolve(generations=generations, verbose=verbose)
        end_time = time.time()
        
        return {
            'population_size': population_size,
            'elite_size': elite_size,
            'mutation_rate': mutation_rate,
            'generations': generations,
            'seed': seed,
            'best_fitness': best_fitness,
            'best_solution': best_solution,
            'time': end_time - start_time,
            'history': ga.history
        }
    
    def run_multiple_trials(self, 
                          n_trials: int = 5,
                          population_size: int = 100,
                          elite_size: int = 20,
                          mutation_rate: float = 0.02,
                          generations: int = 200) -> Dict:
        """Run multiple trials with different random seeds"""
        
        print(f"\nRunning {n_trials} trials with:")
        print(f"  Population: {population_size}, Elite: {elite_size}")
        print(f"  Mutation Rate: {mutation_rate}, Generations: {generations}")
        print("-" * 60)
        
        results = []
        
        for trial in range(n_trials):
            print(f"\nTrial {trial + 1}/{n_trials}:")
            result = self.run_single_experiment(
                population_size=population_size,
                elite_size=elite_size,
                mutation_rate=mutation_rate,
                generations=generations,
                seed=trial * 1000,
                verbose=False
            )
            
            results.append(result)
            print(f"  Best fitness: {result['best_fitness']:.2f}")
            print(f"  Time: {result['time']:.2f}s")
        
        # Calculate statistics
        fitnesses = [r['best_fitness'] for r in results]
        times = [r['time'] for r in results]
        
        stats = {
            'n_trials': n_trials,
            'best': min(fitnesses),
            'worst': max(fitnesses),
            'average': sum(fitnesses) / len(fitnesses),
            'avg_time': sum(times) / len(times),
            'results': results
        }
        
        print("\n" + "=" * 60)
        print("Statistics:")
        print(f"  Best: {stats['best']:.2f}")
        print(f"  Worst: {stats['worst']:.2f}")
        print(f"  Average: {stats['average']:.2f}")
        print(f"  Avg Time: {stats['avg_time']:.2f}s")
        print("=" * 60)
        
        return stats
    
    def compare_parameters(self):
        """Compare different parameter settings"""
        
        print("\n" + "=" * 60)
        print("Comparing Different Parameter Settings")
        print("=" * 60)
        
        # Test different population sizes
        print("\n--- Effect of Population Size ---")
        for pop_size in [50, 100, 200]:
            result = self.run_single_experiment(
                population_size=pop_size,
                elite_size=int(pop_size * 0.2),
                mutation_rate=0.02,
                generations=100,
                seed=42
            )
            print(f"Pop={pop_size:3d}: Fitness={result['best_fitness']:.2f}, Time={result['time']:.2f}s")
        
        # Test different mutation rates
        print("\n--- Effect of Mutation Rate ---")
        for mut_rate in [0.01, 0.02, 0.05, 0.10]:
            result = self.run_single_experiment(
                population_size=100,
                elite_size=20,
                mutation_rate=mut_rate,
                generations=100,
                seed=42
            )
            print(f"Mutation={mut_rate:.2f}: Fitness={result['best_fitness']:.2f}, Time={result['time']:.2f}s")
        
        # Test different elite sizes
        print("\n--- Effect of Elite Size ---")
        for elite in [10, 20, 30, 40]:
            result = self.run_single_experiment(
                population_size=100,
                elite_size=elite,
                mutation_rate=0.02,
                generations=100,
                seed=42
            )
            print(f"Elite={elite:2d}: Fitness={result['best_fitness']:.2f}, Time={result['time']:.2f}s")


def main():
    """Run TSP analysis experiments"""
    
    print("=" * 60)
    print("TSP Genetic Algorithm - Performance Analysis")
    print("=" * 60)
    
    # Choose dataset
    print("\nAvailable datasets:")
    print("1. Random 15-city dataset")
    print("2. Burma14 (14 cities)")
    print("3. Ulysses16 (16 cities)")
    
    choice = input("\nSelect dataset (1-3) or Enter for default: ").strip()
    
    if choice == '1':
        dataset = create_sample_dataset(15)
        print(f"\nUsing random 15-city dataset")
    elif choice == '2':
        dataset = load_sample_dataset("burma14")
        print(f"\nUsing Burma14 dataset (optimal: ~30.87)")
    elif choice == '3':
        dataset = load_sample_dataset("ulysses16")
        print(f"\nUsing Ulysses16 dataset")
    else:
        dataset = create_sample_dataset(10)
        print(f"\nUsing default random 10-city dataset")
    
    experiment = TSPExperiment(dataset)
    
    # Run multiple trials
    print("\n" + "=" * 60)
    print("Experiment 1: Multiple Trials with Same Parameters")
    print("=" * 60)
    
    stats = experiment.run_multiple_trials(
        n_trials=5,
        population_size=100,
        elite_size=20,
        mutation_rate=0.02,
        generations=200
    )
    
    # Compare parameters
    print("\n" + "=" * 60)
    print("Experiment 2: Parameter Comparison")
    print("=" * 60)
    
    experiment.compare_parameters()
    
    # Best configuration
    print("\n" + "=" * 60)
    print("Experiment 3: Best Configuration (Long Run)")
    print("=" * 60)
    
    print("\nRunning with optimized parameters...")
    best_result = experiment.run_single_experiment(
        population_size=150,
        elite_size=30,
        mutation_rate=0.02,
        generations=500,
        seed=42,
        verbose=True
    )
    
    print(f"\nFinal Best Solution:")
    print(f"  Tour: {best_result['best_solution']}")
    print(f"  Length: {best_result['best_fitness']:.2f}")
    print(f"  Time: {best_result['time']:.2f}s")
    
    # Show convergence
    print("\nConvergence (every 50 generations):")
    history = best_result['history']
    for i in range(0, len(history), 50):
        h = history[i]
        print(f"  Gen {h['generation']:3d}: Best={h['best']:.2f}, Avg={h['average']:.2f}")


if __name__ == "__main__":
    main()
