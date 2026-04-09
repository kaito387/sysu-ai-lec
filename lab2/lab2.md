---
title: "人工智能实验报告"
subtitle: "中山大学计算机学院本科生实验报告"
author:
  - "课程名称：Artificial Intelligence"
  - "学号：24344064"
  - "姓名：廖海涛"
date: "Thu Apr 9, 2026"
---

# 实验题目

<!-- 在此填写实验题目 -->
- 2.2 利用启发式搜索解决 15-Puzzle 问题
- 2.4 利用遗传算法求解 TSP 问题

# 实验内容

## 1. 算法原理

<!-- 描述算法的基本原理和思想 -->
### 1.1. 启发式搜索解决 15-Puzzle 问题

启发式搜索是一种基于启发式函数的搜索算法, 通过评估每个状态的启发式值来指导搜索过程. 在 15-Puzzle 问题中, 启发式函数通常是当前状态与目标状态之间的距离, 如曼哈顿距离或错位数. 启发式搜索通过优先扩展启发式值较小的节点, 从而更快地找到解决方案.

- 当启发式函数 $f^*$ 是真实函数 $f$ 的下界时, 启发式搜索算法能够保证找到最优解.
- 当启发式函数 $f^*$ 过于乐观时, 可能会导致搜索过程过于深入某些错误分支, 从而增加搜索时间.
- 当启发式函数 $f^*$ 过于悲观时, 可能会导致搜索过程过于广泛, 从而增加搜索时间.

### 1.2. 遗传算法求解 TSP 问题

遗传算法是一种基于自然选择和遗传学原理的优化算法, 通过模拟生物进化过程来寻找问题的最优解. 在 TSP 问题中, 遗传算法通过编码路径为染色体, 使用选择、交叉和变异等操作来生成新的解.

- 选择操作通过评估每个染色体的适应度来选择下一代的父母染色体, 适应度通常与路径长度成反比.
- 交叉操作通过组合两个父母染色体来生成新的子代染色体, 常用的交叉方法包括部分映射交叉 (PMX) 和顺序交叉 (OX).
- 变异操作通过随机改变染色体中的某些基因来引入多样性, 常用的变异方法包括交换变异和插入变异. 本次实验使用翻转变异.
- 遗传算法通过不断迭代选择、交叉和变异来优化解, 直到满足终止条件, 如达到最大迭代次数或找到满意的解.

## 2. 关键代码展示（可选）

### 2.1. 启发式搜索解决 15-Puzzle 问题

```python
def ida_star(initial: PuzzleState,
             goal: PuzzleState,
             heuristic_func
            ) -> Optional[PuzzleState]:
    """IDA* Search Algorithm"""
    
    def search(path: List[PuzzleState],
               g: int,
               threshold: int,
               nodes_expanded: List[int]
              ) -> Tuple[Optional[PuzzleState], int]:
        # Threshold is the f-cost limit for this iteration
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
        # Update threshold for next iteration
        threshold = new_threshold
```

### 2.2. 遗传算法求解 TSP 问题

```python
def pmx_crossover(self,
                  parent1: List[int],
                  parent2: List[int]
                ) -> Tuple[List[int], List[int]]:
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
```

```python
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
```

```python
def evolve(self, generations: int, verbose: bool = True):
    """Run the genetic algorithm"""
    
    # Create initial population
    self.create_initial_population()
    
    for generation in range(generations):
        # Evaluate fitness
        fitness_scores = [(ind, self.calculate_fitness(ind))
                          for ind in self.population]
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
            print(
              f"Generation {generation}: ",
              f"Best={self.best_fitness:.2f}, "
              f"Average={avg_fitness:.2f}"
            )
        
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
```

# 实验结果及分析

## 1. 实验结果展示示例

### 1.1. 启发式搜索解决 15-Puzzle 问题

```plain
Initial State:
 5  1  2  4
 9  6  3  8
13 15 10 11
14  .  7 12

--- A* with Manhattan Distance ---
Nodes expanded: 24
Solution found! Moves: 14
Time: 0.0009s
Path: Up -> Right -> Down -> Left -> Left -> Up -> Up -> Up -> Right -> Right ->
Down -> Down -> Right -> Down

--- A* with Misplaced Tiles ---
Nodes expanded: 63
Solution found! Moves: 14
Time: 0.0019s
Path: Up -> Right -> Down -> Left -> Left -> Up -> Up -> Up -> Right -> Right ->
Down -> Down -> Right -> Down

--- A* with Linear Conflict ---
Nodes expanded: 22
Solution found! Moves: 14
Time: 0.0054s
Path: Up -> Right -> Down -> Left -> Left -> Up -> Up -> Up -> Right -> Right ->
Down -> Down -> Right -> Down

--- IDA* with Manhattan Distance ---
Nodes expanded: 14
Solution found! Moves: 14
Time: 0.0004s
Path: Up -> Right -> Down -> Left -> Left -> Up -> Up -> Up -> Right -> Right ->
Down -> Down -> Right -> Down
```

### 1.2. 遗传算法求解 TSP 问题

```plain
Using: Burma14 dataset
Final Best Solution:
  Tour: [11, 6, 12, 7, 10, 8, 9, 0, 1, 13, 2, 3, 4, 5]
  Length: 3323.00
  Time: 1.20s

Convergence (every 100 generations):
  Gen   0: Best=4849.00, Avg=6689.66
  Gen 100: Best=3323.00, Avg=3416.57
  Gen 200: Best=3323.00, Avg=3500.76
  Gen 300: Best=3323.00, Avg=3465.38

Using: Ulysses16 dataset
Final Best Solution:
  Tour: [1, 2, 15, 9, 8, 10, 4, 14, 5, 6, 11, 12, 13, 0, 7, 3]
  Length: 6859.00
  Time: 2.13s

Convergence (every 100 generations):
  Gen   0: Best=9506.00, Avg=13025.97
  Gen 100: Best=6859.00, Avg=6977.75
  Gen 200: Best=6859.00, Avg=6916.93
  Gen 300: Best=6859.00, Avg=6922.03
  Gen 400: Best=6859.00, Avg=6921.49
  Gen 500: Best=6859.00, Avg=6932.64

Using: Ulysses22 dataset
Final Best Solution:
  Tour: [6, 11, 12, 13, 0, 7, 17, 3, 21, 16, 1, 2, 15, 20, 19,
  18, 9, 8, 10, 4, 14, 5]
  Length: 7013.00
  Time: 1.48s

Convergence (every 100 generations):
  Gen   0: Best=11224.00, Avg=16528.08
  Gen 100: Best=7013.00, Avg=7149.11
  Gen 200: Best=7013.00, Avg=7138.22
  Gen 300: Best=7013.00, Avg=7138.31
```

三个简单数据集均成功找到最优解（可见 TSPLIB95）, 且在 300 代内收敛.

对于较大的数据集：

```plain
--- Running on dj38.tsp ---
Generation 0: Best=20910.85, Avg=27704.52
Generation 50: Best=6856.39, Avg=7292.95
Generation 100: Best=6659.91, Avg=6991.32
Generation 150: Best=6659.91, Avg=6999.85
Generation 200: Best=6659.91, Avg=6990.40
Generation 250: Best=6659.91, Avg=6995.48
Generation 300: Best=6659.91, Avg=6964.24

Best solution: [23, 27, 26, 30, 35, 33, 32, 37, 36, 34, 31, 29, 28, 20,
13, 9, 0, 1, 3, 2, 4, 5, 6, 7, 8, 11, 10, 16, 18, 17, 15, 12, 14, 19,
22, 25, 24, 21]
Best fitness: 6659.91
Time: 24.29s
```

已经接近最优解 6656, 差距为 3.91, 可能需要使用其他算法微调路径才能找到最优解.

```plain
Summary for qa194.tsp:
Run 1: Best fitness = 10262.33
Run 2: Best fitness = 10658.54
Run 3: Best fitness = 10263.63
Run 4: Best fitness = 10186.06
Run 5: Best fitness = 10268.96
Best solution across runs: [92, 95, 94, 91, 96, 104, 105, 117, 121, 140, 146, 150, 154, 161, 157, 158, 151, 152, 156, 153, 149, 143, 138, 137, 141, 136, 124, 125, 118, 113, 112, 108, 101, 86, 79, 75, 70, 24, 22, 12, 13, 10, 6, 3, 2, 1, 0, 5, 7, 15, 35, 58, 61, 81, 88, 62, 19, 64, 84, 85, 97, 89, 93, 98, 100, 103, 110, 129, 126, 131, 133, 139, 145, 148, 144, 155, 160, 162, 163, 168, 175, 181, 193, 189, 186, 182, 185, 178, 171, 173, 172, 174, 183, 188, 191, 190, 187, 192, 184, 179, 177, 180, 176, 167, 164, 166, 169, 170, 165, 159, 147, 142, 134, 135, 130, 128, 132, 127, 123, 122, 119, 120, 116, 115, 114, 111, 109, 107, 106, 99, 83, 87, 82, 80, 78, 76, 67, 65, 72, 66, 60, 57, 50, 46, 42, 55, 52, 51, 47, 53, 54, 48, 49, 41, 43, 45, 40, 39, 37, 34, 30, 31, 29, 18, 14, 4, 8, 9, 11, 26, 33, 38, 36, 21, 28, 44, 56, 63, 69, 59, 32, 27, 17, 20, 16, 23, 25, 68, 73, 71, 74, 77, 90, 102]
Best fitness 10186.06
```

由于遗传算法是随机化算法，这里运行了 5 次, 最好的结果是 10186.06, 理论最优解是 9352.00, 差距为 834.06.

## 2. 评测指标展示及分析

### 2.1. 启发式搜索解决 15-Puzzle 问题

| algorithm | heuristic function | moves | time (ms) |
|:----:|:----:|:----:|:----:|
| A* | Manhattan Distance | 14 | 0.9 |
| A* | Misplaced Tiles | 14 | 1.9 |
| A* | Linear Conflict | 14 | 5.4 |
| IDA* | Manhattan Distance | 14 | 0.4 |

- A* with Manhattan Distance 和 IDA* with Manhattan Distance 都成功找到最优解, 但 IDA* 的节点扩展数量更少, 时间更短.

### 2.2. 遗传算法求解 TSP 问题

| dataset | best length | time (s) | convergence generation |
|:----:|:----:|:----:|:----:|
| Burma14 | 3323.00 | 1.20 | 20 |
| Ulysses16 | 6859.00 | 2.13 | 20 |
| Ulysses22 | 7013.00 | 1.48 | 90 |

<!-- 在此分析评测指标 -->
- 在不同数据集上，算法均能找到最优解，但是需要设置不同的参数。
- 在 Burma14 数据集上，算法采用了 `population=200, elite_size=30, mutation_rate=0.1, generations=300` 的参数设置，成功在 20 代内找到最优解，耗时 1.20 秒。
- 在 Ulysses16 数据集上，算法采用了 `population=200, elite_size=50, mutation_rate=0.2, generations=500` 的参数设置，成功在 20 代内找到最优解，耗时 2.13 秒。
- 在 Ulysses22 数据集上，算法采用了 `population=200, elite_size=30, mutation_rate=0.2, generations=300` 的参数设置，成功在 90 代内找到最优解，耗时 1.48 秒。

| dataset | best length | time (s) | iteration generation |
|:----:|:----:|:----:|:----:|
| dj38.tsp | 6659.91 | 24.29 | 300 |
| qa194.tsp | 10186.06 | 236.78 | 500 |

其中参数设置为：

```python
settings = {
        "dj38.tsp": {
          "population": 2000, 
          "elite_size": 20, 
          "mutation_rate": 0.3, 
          "tournament_size": 8, 
          "generations": 301
        },
        "qa194.tsp": {
          "population": 2000, 
          "elite_size": 30, 
          "mutation_rate": 0.3, 
          "tournament_size": 10, 
          "generations": 501
        }
    }
```

---

# 参考资料

- [TSP 的已知最优解](https://gitee.com/masx200/tsp-lib-test-data/blob/master/TSP%E7%9A%84%E5%B7%B2%E7%9F%A5%E6%9C%80%E4%BC%98%E8%A7%A3.txt)
- [TSPLib Dataset](https://github.com/coin-or/jorlib/tree/master/jorlib-core/src/test/resources/tspLib/tsp)
- [Linear Conflict Heuristic](https://cdn.aaai.org/AAAI/1996/AAAI96-178.pdf)

