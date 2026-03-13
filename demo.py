#!/usr/bin/env python3
"""
Progress Demo - Run available solvers on a sample puzzle.
Shows current working state of the project.

Usage: python demo.py
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from common.board import SudokuBoard
from common.generator import SAMPLE_PUZZLES
from ayush.runner import StrategyRunner


def main():
    print("=" * 50)
    print("  NineByNine AI - Progress Demo")
    print("  CS 5100 - Foundations of AI")
    print("=" * 50)

    # Run on easy puzzle
    print("\n--- EASY PUZZLE ---")
    board = SudokuBoard(SAMPLE_PUZZLES["easy"])
    board.save_original()

    runner = StrategyRunner()
    collector = runner.run_all(board)

    print("\nResults:")
    for r in collector.get_comparison_table():
        print(f"  {r['Solver']:<28} {r['Solved']:<6} {r['Time (s)']:>12}  Nodes: {r['Nodes']}")

    fastest = collector.get_fastest()
    if fastest:
        print(f"\n  Fastest: {fastest.solver_name} ({fastest.execution_time:.6f}s)")

    print("\n--- HARD PUZZLE ---")
    board2 = SudokuBoard(SAMPLE_PUZZLES["hard"])
    board2.save_original()

    runner2 = StrategyRunner()
    collector2 = runner2.run_all(board2)

    print("\nResults:")
    for r in collector2.get_comparison_table():
        print(f"  {r['Solver']:<28} {r['Solved']:<6} {r['Time (s)']:>12}  Nodes: {r['Nodes']}")


if __name__ == "__main__":
    main()
