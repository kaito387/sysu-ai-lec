"""
Genetic Algorithm for TSP
Implements: Selection, PMX Crossover, Inversion Mutation
"""

import random
from typing import List, Tuple
from tsp_data import TSPDataset
import time


class GeneticAlgorithmTSP:
    """Genetic Algorithm for solving TSP"""
    
    def __init__(self, 
                 dataset: TSPDataset,
                 population_size: int = 100,
                 elite_size: int = 20,
                 mutation_rate: float = 0.01,
                 tournament_size: int = 5):
        """
        Initialize GA
        
        Args:
            dataset: TSP dataset
            population_size: Size of population
            elite_size: Number of elite individuals to keep
            mutation_rate: Probability of mutation
            tournament_size: Size of tournament for selection
        """
        self.dataset = dataset
        self.n_cities = dataset.dimension
        self.population_size = population_size
        self.elite_size = elite_size
        self.mutation_rate = mutation_rate
        self.tournament_size = tournament_size
        
        # Pre-compute distance matrix for efficiency
        self.distance_matrix = dataset.get_distance_matrix()
        
        self.population = []
        self.best_solution = None
        self.best_fitness = float('inf')
        self.history = []
    
    def calculate_fitness(self, individual: List[int]) -> float:
        """Calculate fitness (tour length) - lower is better"""
        total_distance = 0
        
        for i in range(len(individual)):
            city1 = individual[i]
            city2 = individual[(i + 1) % len(individual)]
            total_distance += self.distance_matrix[city1][city2]
        
        return total_distance
    
    def create_initial_population(self):
        """Create initial random population"""
        self.population = []
        
        for _ in range(self.population_size):
            individual = list(range(self.n_cities))
            random.shuffle(individual)
            self.population.append(individual)
    
    def tournament_selection(self, population: List[List[int]]) -> List[int]:
        """Select individual using tournament selection"""
        tournament = random.sample(population, self.tournament_size)
        return min(tournament, key=lambda x: self.calculate_fitness(x))
    
    def pmx_crossover(self, parent1: List[int], parent2: List[int]) -> Tuple[List[int], List[int]]:
        """
        Partial Mapped Crossover (PMX)
        """
        size = len(parent1)
        
        # Choose two random crossover points
        cx_point1 = random.randint(0, size - 1)
        cx_point2 = random.randint(0, size - 1)
        
        if cx_point1 > cx_point2:
            cx_point1, cx_point2 = cx_point2, cx_point1
        
        # Initialize offspring
        offspring1 = [-1] * size
        offspring2 = [-1] * size
        
        # Copy the segment between crossover points
        offspring1[cx_point1:cx_point2+1] = parent1[cx_point1:cx_point2+1]
        offspring2[cx_point1:cx_point2+1] = parent2[cx_point1:cx_point2+1]
        
        # Create mapping
        def fill_offspring(offspring, parent_donor, parent_source, start, end):
            for i in range(size):
                if i < start or i > end:
                    value = parent_donor[i]
                    
                    # If value already in offspring, find replacement
                    while value in offspring[start:end+1]:
                        idx = parent_source.index(value)
                        value = parent_donor[idx]
                    
                    offspring[i] = value
        
        fill_offspring(offspring1, parent2, parent1, cx_point1, cx_point2)
        fill_offspring(offspring2, parent1, parent2, cx_point1, cx_point2)
        
        return offspring1, offspring2
    
    def inversion_mutation(self, individual: List[int]) -> List[int]:
        """
        Inversion Mutation: Reverse a random segment
        """
        if random.random() < self.mutation_rate:
            mutated = individual[:]
            
            # Choose two random points
            pos1 = random.randint(0, len(mutated) - 1)
            pos2 = random.randint(0, len(mutated) - 1)
            
            if pos1 > pos2:
                pos1, pos2 = pos2, pos1
            
            # Reverse the segment
            mutated[pos1:pos2+1] = reversed(mutated[pos1:pos2+1])
            
            return mutated
        
        return individual
    
    def evolve(self, generations: int, verbose: bool = True):
        """Run the genetic algorithm"""
        
        # Create initial population
        self.create_initial_population()
        
        for generation in range(generations):
            # Evaluate fitness
            fitness_scores = [(ind, self.calculate_fitness(ind)) for ind in self.population]
            fitness_scores.sort(key=lambda x: x[1])
            
            # Update best solution
            if fitness_scores[0][1] < self.best_fitness:
                self.best_solution = fitness_scores[0][0][:]
                self.best_fitness = fitness_scores[0][1]
            
            # Record history
            avg_fitness = sum(f for _, f in fitness_scores) / len(fitness_scores)
            self.history.append({
                'generation': generation,
                'best': fitness_scores[0][1],
                'average': avg_fitness,
                'worst': fitness_scores[-1][1]
            })
            
            if verbose and generation % 10 == 0:
                print(f"Generation {generation}: Best={self.best_fitness:.2f}, Avg={avg_fitness:.2f}")
            
            # Create next generation
            new_population = []
            
            # Elitism: keep best individuals
            for i in range(self.elite_size):
                new_population.append(fitness_scores[i][0])
            
            # Create offspring
            while len(new_population) < self.population_size:
                # Selection
                parent1 = self.tournament_selection(self.population)
                parent2 = self.tournament_selection(self.population)
                
                # Crossover
                offspring1, offspring2 = self.pmx_crossover(parent1, parent2)
                
                # Mutation
                offspring1 = self.inversion_mutation(offspring1)
                offspring2 = self.inversion_mutation(offspring2)
                
                new_population.append(offspring1)
                if len(new_population) < self.population_size:
                    new_population.append(offspring2)
            
            self.population = new_population
        
        # Final evaluation
        fitness_scores = [(ind, self.calculate_fitness(ind)) for ind in self.population]
        fitness_scores.sort(key=lambda x: x[1])
        
        if fitness_scores[0][1] < self.best_fitness:
            self.best_solution = fitness_scores[0][0][:]
            self.best_fitness = fitness_scores[0][1]
        
        return self.best_solution, self.best_fitness


def test_genetic_algorithm():
    """Test the genetic algorithm"""
    from tsp_data import create_sample_dataset, load_sample_dataset
    
    print("Testing Genetic Algorithm for TSP")
    print("=" * 60)
    
    # Test with small random dataset
    print("\n--- Test 1: Random 10-city problem ---")
    dataset = create_sample_dataset(10)
    
    ga = GeneticAlgorithmTSP(
        dataset=dataset,
        population_size=50,
        elite_size=10,
        mutation_rate=0.02,
        tournament_size=5
    )
    
    start_time = time.time()
    best_solution, best_fitness = ga.evolve(generations=100, verbose=True)
    end_time = time.time()
    
    print(f"\nBest solution: {best_solution}")
    print(f"Best fitness: {best_fitness:.2f}")
    print(f"Time: {end_time - start_time:.2f}s")
    
    # Test with Burma14
    print("\n\n--- Test 2: Burma14 (14 cities) ---")
    dataset2 = load_sample_dataset("burma14")
    
    ga2 = GeneticAlgorithmTSP(
        dataset=dataset2,
        population_size=100,
        elite_size=20,
        mutation_rate=0.02,
        tournament_size=5
    )
    
    start_time = time.time()
    best_solution2, best_fitness2 = ga2.evolve(generations=200, verbose=True)
    end_time = time.time()
    
    print(f"\nBest solution: {best_solution2}")
    print(f"Best fitness: {best_fitness2:.2f}")
    print(f"Time: {end_time - start_time:.2f}s")
    print(f"\nNote: Optimal tour length for Burma14 is 30.87 (known)")


if __name__ == "__main__":
    test_genetic_algorithm()
