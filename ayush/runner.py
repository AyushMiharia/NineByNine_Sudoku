"""Run all solvers on a board and collect timings."""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from common.board import SudokuBoard
from common.constraints import get_legal_values
from salwa.backtracking import BacktrackingSolver
from salwa.mrv_solver import MRVSolver
from anjali.forward_checking import ForwardCheckingSolver
from ayush.min_conflicts import MinConflictsSolver
from anjali.metrics import MetricsCollector


class StrategyRunner:
    def __init__(self):
        self.collector = MetricsCollector()
        self.solvers = [
            BacktrackingSolver(),
            MRVSolver(),
            ForwardCheckingSolver(),
            MinConflictsSolver(max_iters=200000, max_restarts=20),
        ]
        self.solved_boards = {}

    def run_all(self, board):
        self.collector = MetricsCollector()
        self.solved_boards = {}

        for solver in self.solvers:
            copy = board.clone()
            name = solver.NAME

            self.collector.start()
            solved = solver.solve(copy)
            elapsed = self.collector.stop()

            extra = {}
            if hasattr(solver, "iterations_used"):
                extra["iterations"] = solver.iterations_used
                extra["restarts"] = solver.restarts_used
            if hasattr(solver, "arc_revisions"):
                extra["arc_revisions"] = solver.arc_revisions

            self.collector.record(name, solved, elapsed, solver.get_metrics(), extra)

            if solved:
                self.solved_boards[name] = copy

            status = "Solved" if solved else "Failed"
            print(f"  {name:<32} {status} in {elapsed:.6f}s")

        return self.collector

    def get_hint(self, grid):
        board = SudokuBoard(grid)
        best, mn = None, float("inf")
        for r, c in board.get_empty_cells():
            lv = get_legal_values(board, r, c)
            if 0 < len(lv) < mn:
                mn = len(lv)
                best = (r, c, min(lv))
                if mn == 1: break
        return best
