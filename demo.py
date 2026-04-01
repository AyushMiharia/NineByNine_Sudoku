#!/usr/bin/env python3
"""
NineByNine AI - Progress Report 2 Demo
Runs all 4 solvers on easy and hard puzzles.
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from common.board import SudokuBoard
from common.generator import SAMPLE_PUZZLES
from ayush.runner import StrategyRunner


def main():
    print("=" * 60)
    print("  NineByNine AI - Progress Report 2 Demo")
    print("  CS 5100 - Foundations of AI")
    print("=" * 60)

    runner = StrategyRunner()

    for name, grid in SAMPLE_PUZZLES.items():
        print(f"\n{'─' * 60}")
        print(f"  {name.upper()} PUZZLE")
        print(f"{'─' * 60}")
        board = SudokuBoard(grid)
        board.save_original()
        print(board)
        print()
        collector = runner.run_all(board)
        collector.print_comparison()

    print(f"\n{'─' * 60}")
    print("  GENERATED MEDIUM PUZZLE")
    print(f"{'─' * 60}")
    from common.generator import generate_puzzle
    board, _ = generate_puzzle("medium")
    print(board)
    print()
    collector = runner.run_all(board)
    collector.print_comparison()


if __name__ == "__main__":
    main()
