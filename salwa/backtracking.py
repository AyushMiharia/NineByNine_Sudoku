"""
Plain Backtracking Solver
Author: Salwa
Status: COMPLETE

Standard depth-first backtracking for Sudoku.
Serves as the baseline for performance comparison.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from common.constraints import is_valid_placement


class BacktrackingSolver:

    NAME = "Plain Backtracking"

    def __init__(self):
        self.nodes_expanded = 0
        self.backtracks = 0
        self.constraint_checks = 0

    def solve(self, board):
        self.nodes_expanded = 0
        self.backtracks = 0
        self.constraint_checks = 0
        return self._backtrack(board)

    def _backtrack(self, board):
        empty = board.get_empty_cells()
        if not empty:
            return True

        row, col = empty[0]
        self.nodes_expanded += 1

        for value in range(1, 10):
            self.constraint_checks += 1
            if is_valid_placement(board, row, col, value):
                board.set(row, col, value)
                if self._backtrack(board):
                    return True
                board.clear(row, col)
                self.backtracks += 1

        return False

    def get_metrics(self):
        return {
            "nodes_expanded": self.nodes_expanded,
            "backtracks": self.backtracks,
            "constraint_checks": self.constraint_checks,
        }
