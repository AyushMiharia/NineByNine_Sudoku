"""
Strategy Runner - Orchestrates Solver Comparison
Author: Ayush
Status: IN PROGRESS - basic runner done, UI integration pending

Runs available solvers on the same board and collects metrics.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from common.board import SudokuBoard
from salwa.backtracking import BacktrackingSolver
from salwa.mrv_solver import MRVSolver
from anjali.forward_checking import ForwardCheckingSolver
from anjali.metrics import MetricsCollector


class StrategyRunner:

    def __init__(self):
        self.collector = MetricsCollector()
        self.solvers = [
            BacktrackingSolver(),
            MRVSolver(),
            ForwardCheckingSolver(),
            # MinConflictsSolver — will be added once optimized
        ]

    def run_all(self, original_board):
        """Run all solvers on clones of the given board."""
        self.collector = MetricsCollector()

        print("Running solver comparison...")
        print(original_board)
        print()

        for solver in self.solvers:
            board_copy = original_board.clone()
            name = solver.NAME

            self.collector.start_timer()
            solved = solver.solve(board_copy)
            elapsed = self.collector.stop_timer()

            self.collector.record(name, solved, elapsed, solver.get_metrics())
            status = "Solved" if solved else "Failed"
            print(f"  {name}: {status} in {elapsed:.6f}s")

        return self.collector


# TODO (Ayush):
# - Add MinConflictsSolver once swap optimization is done
# - Build interactive React frontend with solver selection
# - Add hint system using MRV to pick next best cell
# - Result page with algorithm explanation and metrics display
