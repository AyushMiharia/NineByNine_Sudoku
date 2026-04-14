"""MRV backtracking for Sudoku (degree tie-break + LCV ordering)."""

import sys, os
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
        return self._bt(board)

    def _degree(self, board, row, col):
        """Unassigned neighbors (for tie-breaking)."""
        count = 0
        for nr, nc in board.get_neighbors(row, col):
            if board.is_empty(nr, nc):
                count += 1
        return count

    def _lcv_order(self, board, row, col, values):
        """Sort candidate values so we try the least constraining first."""
        def count_eliminated(val):
            total = 0
            for nr, nc in board.get_neighbors(row, col):
                if board.is_empty(nr, nc):
                    self.constraint_checks += 1
                    neighbor_legal = get_legal_values(board, nr, nc)
                    if val in neighbor_legal:
                        total += 1
            return total

        return sorted(values, key=count_eliminated)

    def _select_mrv(self, board):
        """Pick empty cell with smallest domain; ties -> higher degree."""
        empty_cells = board.get_empty_cells()
        if not empty_cells:
            return None, set()

        best_cell = None
        best_values = None
        min_count = float("inf")
        max_degree = -1

        for row, col in empty_cells:
            legal = get_legal_values(board, row, col)
            self.constraint_checks += 1
            lcount = len(legal)

            if lcount < min_count or (lcount == min_count and self._degree(board, row, col) > max_degree):
                min_count = lcount
                max_degree = self._degree(board, row, col)
                best_cell = (row, col)
                best_values = legal
                if min_count == 0:
                    break

        return best_cell, best_values

    def _bt(self, board):
        cell, vals = self._select_mrv(board)
        if cell is None:
            return board.is_complete()
        if not vals:
            return False
        r, c = cell
        self.nodes_expanded += 1

        ordered_vals = self._lcv_order(board, r, c, vals)

        for v in ordered_vals:
            self.constraint_checks += 1
            if is_valid_placement(board, r, c, v):
                board.set(r, c, v)
                if self._bt(board):
                    return True
                board.clear(r, c)
                self.backtracks += 1
        return False

    def get_metrics(self):
        return {"nodes_expanded": self.nodes_expanded, "backtracks": self.backtracks, "constraint_checks": self.constraint_checks}
