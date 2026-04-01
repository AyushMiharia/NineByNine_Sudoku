"""
Min-Conflicts Local Search Solver (Box-Swap Variant)
Author: Ayush
Status: Complete (upgraded in PR2)
  - PR1: Basic box-swap structure
  - PR2: Sideways moves with probability, stale detection for early
          restart, optimized conflict counting, fully integrated
"""

import random


class MinConflictsSolver:
    NAME = "Min-Conflicts (Local Search)"

    def __init__(self, max_iters=200000, max_restarts=20):
        self.max_iters = max_iters
        self.max_restarts = max_restarts
        self.nodes_expanded = 0
        self.backtracks = 0
        self.constraint_checks = 0
        self.iterations_used = 0
        self.restarts_used = 0

    def solve(self, board):
        self.nodes_expanded = 0
        self.backtracks = 0
        self.constraint_checks = 0
        self.iterations_used = 0
        self.restarts_used = 0

        fixed = set()
        for r in range(board.SIZE):
            for c in range(board.SIZE):
                if not board.is_empty(r, c):
                    fixed.add((r, c))

        for restart in range(self.max_restarts):
            self.restarts_used = restart + 1

            # Clear non-fixed cells
            for r in range(9):
                for c in range(9):
                    if (r, c) not in fixed:
                        board.clear(r, c)

            self._init_boxes(board, fixed)

            if self._repair(board, fixed):
                return True
            self.backtracks += 1

        return False

    def _init_boxes(self, board, fixed):
        """Fill each 3x3 box with a valid permutation of missing values."""
        for br in range(0, 9, 3):
            for bc in range(0, 9, 3):
                used, empty = set(), []
                for r in range(br, br+3):
                    for c in range(bc, bc+3):
                        if (r, c) in fixed:
                            used.add(board.get(r, c))
                        else:
                            empty.append((r, c))
                avail = list(set(range(1, 10)) - used)
                random.shuffle(avail)
                for i, (r, c) in enumerate(empty):
                    board.set(r, c, avail[i])

    def _rc_conflicts(self, board, r, c):
        """Count row + column conflicts (boxes always valid by construction)."""
        v = board.get(r, c)
        if v == 0: return 0
        self.constraint_checks += 1
        ct = 0
        for i in range(9):
            if i != c and board.get(r, i) == v: ct += 1
            if i != r and board.get(i, c) == v: ct += 1
        return ct

    def _total_conflicts(self, board):
        t = 0
        for r in range(9):
            for c in range(9):
                t += self._rc_conflicts(board, r, c)
        return t // 2

    def _repair(self, board, fixed):
        """Swap-based repair with sideways moves and stale detection."""
        stale = 0
        best_total = self._total_conflicts(board)

        for it in range(self.max_iters):
            self.iterations_used += 1

            if best_total == 0:
                return True

            # Pick a random box
            br, bc = random.choice([0, 3, 6]), random.choice([0, 3, 6])
            swappable = [(r, c) for r in range(br, br+3) for c in range(bc, bc+3) if (r, c) not in fixed]

            if len(swappable) < 2:
                continue

            c1, c2 = random.sample(swappable, 2)
            r1, col1 = c1
            r2, col2 = c2
            v1, v2 = board.get(r1, col1), board.get(r2, col2)
            if v1 == v2:
                continue

            self.nodes_expanded += 1

            old = self._rc_conflicts(board, r1, col1) + self._rc_conflicts(board, r2, col2)
            board.set(r1, col1, v2)
            board.set(r2, col2, v1)
            new = self._rc_conflicts(board, r1, col1) + self._rc_conflicts(board, r2, col2)

            delta = new - old

            if delta < 0:
                # Improvement — keep
                best_total += delta
                stale = 0
            elif delta == 0 and random.random() < 0.3:
                # Sideways move with 30% probability to escape plateaus
                stale += 1
            else:
                # Undo
                board.set(r1, col1, v1)
                board.set(r2, col2, v2)
                stale += 1

            # Stale detection — restart early if stuck
            if stale > 5000:
                break

        return self._total_conflicts(board) == 0

    def get_metrics(self):
        return {
            "nodes_expanded": self.nodes_expanded,
            "backtracks": self.backtracks,
            "constraint_checks": self.constraint_checks,
            "iterations": self.iterations_used,
            "restarts": self.restarts_used,
        }
