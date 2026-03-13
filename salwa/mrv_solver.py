"""
Backtracking + MRV (Minimum Remaining Values) Solver
Author: Salwa
Status: IN PROGRESS - core logic complete, optimization pending

Enhances plain backtracking by choosing the empty cell with the
fewest legal values remaining (most constrained variable heuristic).
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from common.constraints import is_valid_placement, get_legal_values


class MRVSolver:

    NAME = "Backtracking + MRV"

    def __init__(self):
        self.nodes_expanded = 0
        self.backtracks = 0
        self.constraint_checks = 0

    def solve(self, board):
        self.nodes_expanded = 0
        self.backtracks = 0
        self.constraint_checks = 0
        return self._backtrack(board)

    def _select_mrv_cell(self, board):
        """Select the empty cell with the minimum remaining legal values."""
        empty_cells = board.get_empty_cells()
        if not empty_cells:
            return None, set()

        best_cell = None
        best_values = None
        min_count = float("inf")

        for row, col in empty_cells:
            legal = get_legal_values(board, row, col)
            self.constraint_checks += 1
            if len(legal) < min_count:
                min_count = len(legal)
                best_cell = (row, col)
                best_values = legal
                if min_count <= 1:
                    break  # Can't do better

        return best_cell, best_values

    def _backtrack(self, board):
        cell, legal_values = self._select_mrv_cell(board)

        if cell is None:
            return board.is_complete()

        row, col = cell
        self.nodes_expanded += 1

        if not legal_values:
            return False

        for value in legal_values:
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


# TODO (Salwa):
# - Add degree heuristic as tiebreaker for MRV
# - Investigate LCV (Least Constraining Value) ordering
# - Profile performance on expert-level puzzles
