"""
Domain Tracking for Sudoku CSP
Author: Anjali
Status: COMPLETE

Manages the domain (set of possible values) for each cell.
Supports initialization, pruning, cloning, and MRV selection.
Used by the Forward Checking solver.
"""

class DomainTracker:

    def __init__(self, board):
        self.size = board.SIZE
        self.domains = {}
        self._init_domains(board)

    def _init_domains(self, board):
        for r in range(self.size):
            for c in range(self.size):
                if board.is_empty(r, c):
                    used = set()
                    used.update(board.get_row(r))
                    used.update(board.get_col(c))
                    used.update(board.get_box(r, c))
                    used.discard(board.EMPTY)
                    self.domains[(r, c)] = set(range(1, 10)) - used
                else:
                    self.domains[(r, c)] = {board.get(r, c)}

    def get_domain(self, row, col):
        return self.domains.get((row, col), set())

    def set_domain(self, row, col, values):
        self.domains[(row, col)] = set(values)

    def clone(self):
        new_tracker = DomainTracker.__new__(DomainTracker)
        new_tracker.size = self.size
        new_tracker.domains = {k: set(v) for k, v in self.domains.items()}
        return new_tracker

    def get_mrv_cell(self, board):
        """Return the empty cell with the smallest domain."""
        best_cell = None
        min_size = float("inf")

        for r in range(self.size):
            for c in range(self.size):
                if board.is_empty(r, c):
                    domain_size = len(self.domains.get((r, c), set()))
                    if domain_size < min_size:
                        min_size = domain_size
                        best_cell = (r, c)
                        if min_size <= 1:
                            return best_cell

        return best_cell
