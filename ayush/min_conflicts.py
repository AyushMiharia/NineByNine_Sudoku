"""
Min-Conflicts Local Search Solver
Author: Ayush
Status: IN PROGRESS - basic structure complete, swap optimization planned

A local search approach that fills the board randomly and iteratively
repairs conflicts by swapping values within 3x3 boxes.
"""

import random


class MinConflictsSolver:

    NAME = "Min-Conflicts (Local Search)"

    def __init__(self, max_iterations=50000, max_restarts=10):
        self.max_iterations = max_iterations
        self.max_restarts = max_restarts
        self.nodes_expanded = 0
        self.backtracks = 0  # restarts
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

            # Clear non-fixed
            for r in range(board.SIZE):
                for c in range(board.SIZE):
                    if (r, c) not in fixed:
                        board.clear(r, c)

            self._init_boxes(board, fixed)

            if self._repair_loop(board, fixed):
                return True

            self.backtracks += 1

        return False

    def _init_boxes(self, board, fixed):
        """Fill each 3x3 box with a valid permutation of missing values."""
        for box_r in range(0, 9, 3):
            for box_c in range(0, 9, 3):
                used = set()
                empty_cells = []
                for r in range(box_r, box_r + 3):
                    for c in range(box_c, box_c + 3):
                        if (r, c) in fixed:
                            used.add(board.get(r, c))
                        else:
                            empty_cells.append((r, c))

                available = list(set(range(1, 10)) - used)
                random.shuffle(available)
                for i, (r, c) in enumerate(empty_cells):
                    board.set(r, c, available[i])

    def _count_rc_conflicts(self, board, row, col):
        """Count row + column conflicts (boxes always valid)."""
        val = board.get(row, col)
        if val == 0:
            return 0
        conflicts = 0
        self.constraint_checks += 1
        for c in range(9):
            if c != col and board.get(row, c) == val:
                conflicts += 1
        for r in range(9):
            if r != row and board.get(r, col) == val:
                conflicts += 1
        return conflicts

    def _repair_loop(self, board, fixed):
        """Core swap-based repair loop."""
        # TODO: implement stale detection and adaptive restart
        for iteration in range(self.max_iterations):
            self.iterations_used += 1

            # Check if solved
            total = 0
            for r in range(9):
                for c in range(9):
                    total += self._count_rc_conflicts(board, r, c)
            if total == 0:
                return True

            # Pick random box and try a swap
            box_r = random.choice([0, 3, 6])
            box_c = random.choice([0, 3, 6])

            swappable = []
            for r in range(box_r, box_r + 3):
                for c in range(box_c, box_c + 3):
                    if (r, c) not in fixed:
                        swappable.append((r, c))

            if len(swappable) < 2:
                continue

            c1, c2 = random.sample(swappable, 2)
            r1, col1 = c1
            r2, col2 = c2
            self.nodes_expanded += 1

            v1, v2 = board.get(r1, col1), board.get(r2, col2)
            if v1 == v2:
                continue

            old = self._count_rc_conflicts(board, r1, col1) + self._count_rc_conflicts(board, r2, col2)
            board.set(r1, col1, v2)
            board.set(r2, col2, v1)
            new = self._count_rc_conflicts(board, r1, col1) + self._count_rc_conflicts(board, r2, col2)

            if new >= old:
                # Undo swap if not improving
                board.set(r1, col1, v1)
                board.set(r2, col2, v2)

        return False

    def get_metrics(self):
        return {
            "nodes_expanded": self.nodes_expanded,
            "backtracks": self.backtracks,
            "constraint_checks": self.constraint_checks,
        }


# TODO (Ayush):
# - Add sideways moves with probability to escape plateaus
# - Add stale detection for early restart
# - Optimize total_conflicts with incremental updates
# - Integrate with React frontend
