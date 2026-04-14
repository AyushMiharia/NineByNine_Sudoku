#!/usr/bin/env python3
"""Quick terminal demo: sample puzzles + one generated board."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from common.board import SudokuBoard
from common.generator import SAMPLE_PUZZLES, generate_puzzle
from ayush.runner import StrategyRunner


def main():
    print("NineByNine / CS 5100 demo")
    print("-" * 40)

    runner = StrategyRunner()

    for name, grid in SAMPLE_PUZZLES.items():
        print(f"\n{name.upper()}")
        board = SudokuBoard(grid)
        board.save_original()
        print(board)
        print()
        runner.run_all(board).print_comparison()

    print("\nRandom medium")
    board, _ = generate_puzzle("medium")
    print(board)
    print()
    runner.run_all(board).print_comparison()


if __name__ == "__main__":
    main()
