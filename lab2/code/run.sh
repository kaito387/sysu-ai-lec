#!/bin/bash
# 快速启动脚本 - AI Lab 2

echo "======================================================================"
echo "人工智能实验 Lab 2 - 搜索算法"
echo "======================================================================"
echo ""
echo "选择要运行的任务："
echo ""
echo "1. 任务 2.1 - 迷宫求解（BFS/DFS/IDS 等）"
echo "2. 任务 2.2 - 15-Puzzle 求解（A*/IDA*）⭐ 要求提交"
echo "3. 任务 2.3 - 中国象棋 AI（Minimax + Alpha-Beta）"
echo "4. 任务 2.4 - TSP 遗传算法 ⭐ 要求提交"
echo "5. 任务 2.4 - TSP 性能分析"
echo "6. 运行所有验证测试"
echo "0. 退出"
echo ""
read -p "请输入选项 (0-6): " choice

case $choice in
    1)
        echo ""
        echo "运行任务 2.1: 迷宫求解..."
        cd maze && python3 maze_solver.py
        ;;
    2)
        echo ""
        echo "运行任务 2.2: 15-Puzzle 求解..."
        cd puzzle && python3 puzzle_solver.py
        ;;
    3)
        echo ""
        echo "运行任务 2.3: 中国象棋 AI..."
        cd chess && python3 chess_game.py
        ;;
    4)
        echo ""
        echo "运行任务 2.4: TSP 遗传算法..."
        cd tsp && python3 tsp_ga.py
        ;;
    5)
        echo ""
        echo "运行任务 2.4: TSP 性能分析..."
        cd tsp && python3 tsp_analysis.py
        ;;
    6)
        echo ""
        echo "运行所有验证测试..."
        python3 test_all.py
        ;;
    0)
        echo "退出"
        exit 0
        ;;
    *)
        echo "无效选项"
        exit 1
        ;;
esac

echo ""
echo "======================================================================"
echo "运行完成！"
echo "======================================================================"
