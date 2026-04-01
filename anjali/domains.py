"""
Domain Tracking for Forward Checking
Author: Anjali
Status: Complete (since PR1)
"""


class DomainTracker:
    def __init__(self, board):
        self.size = board.SIZE
        self.domains = {}
        for r in range(9):
            for c in range(9):
                if board.is_empty(r, c):
                    used = set(board.get_row(r)) | set(board.get_col(c)) | set(board.get_box(r, c))
                    used.discard(0)
                    self.domains[(r, c)] = set(range(1, 10)) - used
                else:
                    self.domains[(r, c)] = {board.get(r, c)}

    def get_domain(self, r, c): return self.domains.get((r, c), set())
    def set_domain(self, r, c, vals): self.domains[(r, c)] = set(vals)

    def clone(self):
        t = DomainTracker.__new__(DomainTracker)
        t.size = self.size
        t.domains = {k: set(v) for k, v in self.domains.items()}
        return t

    def get_mrv_cell(self, board):
        best, mn = None, float("inf")
        for r in range(9):
            for c in range(9):
                if board.is_empty(r, c):
                    sz = len(self.domains.get((r, c), set()))
                    if sz < mn:
                        mn = sz; best = (r, c)
                        if mn <= 1: return best
        return best
