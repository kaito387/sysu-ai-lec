# AI Lab 2 - Search Algorithms Implementation

实验报告：人工智能搜索算法实验

## 项目概述

本实验实现了 4 个人工智能搜索算法任务：

1. **任务 2.1**: 利用盲目搜索解决迷宫问题（BFS, DFS, DLS, IDS, 双向搜索）
2. **任务 2.2**: 利用启发式搜索解决 15-Puzzle 问题（A*, IDA*）⭐ **要求提交**
3. **任务 2.3**: 利用博弈树搜索实现象棋 AI（Minimax + Alpha-Beta 剪枝）
4. **任务 2.4**: 利用遗传算法求解 TSP 问题（PMX 交叉，倒置变异）⭐ **要求提交**

## 目录结构

```
code/
├── maze/              # 任务 2.1: 迷宫求解
│   └── maze_solver.py
├── puzzle/            # 任务 2.2: 15-Puzzle 求解 ⭐
│   └── puzzle_solver.py
├── chess/             # 任务 2.3: 中国象棋 AI
│   ├── chess_engine.py
│   ├── chess_ai.py
│   └── chess_game.py
└── tsp/               # 任务 2.4: TSP 遗传算法 ⭐
    ├── tsp_data.py
    ├── tsp_ga.py
    └── tsp_analysis.py
```

## 环境要求

- Python 3.8+
- 无需额外依赖库（仅使用标准库）

## 运行说明

### 任务 2.1: 迷宫求解

实现了 5 种盲目搜索算法：
- BFS（宽度优先搜索）
- DFS（深度优先搜索）
- DLS（深度受限搜索）
- IDS（迭代加深搜索）
- 双向搜索

**运行方式：**
```bash
cd code/maze
python3 maze_solver.py
```

**功能：**
- 测试多种搜索算法
- 可视化路径
- 比较不同算法的性能

---

### 任务 2.2: 15-Puzzle 求解 ⭐

实现了启发式搜索算法：
- A* 搜索（支持多种启发函数）
  - Manhattan Distance（曼哈顿距离）
  - Misplaced Tiles（错位方块数）
  - Linear Conflict（线性冲突）
- IDA* 搜索（迭代加深 A*）

**运行方式：**
```bash
cd code/puzzle
python3 puzzle_solver.py
```

**特点：**
- 多种启发函数对比
- 节点扩展数统计
- 性能分析（时间、步数）

**示例输出：**
```
--- A* with Manhattan Distance ---
Nodes expanded: 4
Solution found! Moves: 3
Time: 0.0002s
Path: Down -> Right -> Down
```

---

### 任务 2.3: 中国象棋 AI

实现了完整的中国象棋引擎和 AI：
- 完整的象棋规则（将/士/象/马/车/炮/兵）
- Minimax 算法 + Alpha-Beta 剪枝
- 棋局评估函数
- 多种对弈模式

**运行方式：**
```bash
cd code/chess

# 测试棋盘和规则
python3 chess_engine.py

# 测试 AI
python3 chess_ai.py

# 运行游戏
python3 chess_game.py
```

**游戏模式：**
1. 人类 vs AI
2. AI vs AI
3. 人类 vs 随机 AI
4. AI vs 随机 AI（快速演示）

**输入格式：**
- 移动棋子：`9,4 to 8,4` 或 `94 84`
- 退出：`quit`

---

### 任务 2.4: TSP 遗传算法 ⭐

实现了完整的遗传算法求解 TSP：
- PMX（部分映射交叉）
- 倒置变异
- 锦标赛选择
- 精英保留策略

**数据集：**
- Burma14（14 城市，最优解 ≈ 30.87）
- Ulysses16（16 城市）
- 自定义随机数据集

**运行方式：**

1. **基本测试：**
```bash
cd code/tsp
python3 tsp_ga.py
```

2. **性能分析（推荐）：**
```bash
python3 tsp_analysis.py
```

**分析功能：**
- 多次试验统计（不同随机种子）
- 参数对比（种群大小、变异率、精英数）
- 收敛曲线
- 最优解搜索

**示例输出：**
```
--- Test 2: Burma14 (14 cities) ---
Generation 0: Best=5076.00, Avg=6682.86
Generation 100: Best=3448.00, Avg=3453.90
Generation 200: Best=3448.00, Avg=3460.18

Best fitness: 3448.00
Time: 0.18s
```

---

## 实验结果总结

### 2.1 迷宫求解
- BFS 和 IDS 找到最短路径
- DFS 较快但不保证最优
- 双向搜索在大迷宫中效率更高

### 2.2 15-Puzzle
- Manhattan Distance 启发函数最优
- A* 扩展节点少，效率高
- IDA* 空间复杂度更低

### 2.3 象棋 AI
- Alpha-Beta 剪枝显著减少搜索节点
- 深度 3 可以做出合理决策
- 评估函数考虑子力价值和位置

### 2.4 TSP 遗传算法
- 种群大小 100-200 效果较好
- 变异率 0.02 平衡探索和利用
- 精英保留策略加速收敛
- 多次运行取最优解

## 技术细节

### 盲目搜索（任务 2.1）
- 使用队列（BFS）和栈（DFS）
- 迭代加深避免深度限制选择困难
- 双向搜索从两端同时搜索

### 启发式搜索（任务 2.2）
- 优先队列管理待扩展节点
- 可采纳启发函数保证最优解
- IDA* 使用深度优先降低空间复杂度

### 博弈树搜索（任务 2.3）
- Minimax 递归搜索
- Alpha-Beta 剪枝提前终止分支
- 评估函数：子力价值 + 移动能力

### 遗传算法（任务 2.4）
- 排列编码表示路径
- PMX 交叉保持合法性
- 倒置变异探索邻域
- 锦标赛选择保持多样性

## 作者信息

- 实验名称：人工智能搜索算法实验
- 实验编号：Lab 2
- 完成日期：2025 年 4 月

## 许可证

本项目仅用于学习和教学目的。
