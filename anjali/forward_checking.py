"""
MRV + Forward Checking + AC-3 Arc Consistency
Author: Anjali
Status: Complete (upgraded in PR2)
  - PR1: Basic forward checking
  - PR2: Added AC-3 arc consistency propagation
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from anjali.domains import DomainTracker
from collections import deque


class ForwardCheckingSolver:
    NAME = "MRV + Forward Checking"

    def __init__(self, use_ac3=True):
        self.use_ac3 = use_ac3
        self.nodes_expanded = 0
        self.backtracks = 0
        self.constraint_checks = 0
        self.arc_revisions = 0

    def solve(self, board):
        self.nodes_expanded = 0
        self.backtracks = 0
        self.constraint_checks = 0
        self.arc_revisions = 0
        domains = DomainTracker(board)

        # Run initial AC-3 before search begins
        if self.use_ac3:
            if not self._ac3(board, domains):
                return False

        return self._bt(board, domains)

    def _bt(self, board, domains):
        if not board.get_empty_cells():
            return True

        cell = domains.get_mrv_cell(board)
        if cell is None:
            return True

        r, c = cell
        dom = domains.get_domain(r, c)
        if not dom:
            return False

        self.nodes_expanded += 1

        for v in sorted(dom):
            self.constraint_checks += 1
            saved = domains.clone()

            board.set(r, c, v)
            domains.set_domain(r, c, {v})

            if self._forward_check(board, domains, r, c, v):
                # Run AC-3 after forward check for deeper propagation
                ac3_ok = True
                if self.use_ac3:
                    ac3_ok = self._ac3_from(board, domains, r, c)

                if ac3_ok and self._bt(board, domains):
                    return True

            board.clear(r, c)
            domains = saved
            self.backtracks += 1

        return False

    def _forward_check(self, board, domains, row, col, value):
        """Prune value from all neighbors' domains."""
        for nr, nc in board.get_neighbors(row, col):
            if board.is_empty(nr, nc):
                self.constraint_checks += 1
                d = domains.get_domain(nr, nc)
                if value in d:
                    d.discard(value)
                    domains.set_domain(nr, nc, d)
                    if len(d) == 0:
                        return False
        return True

    def _ac3(self, board, domains):
        """
        Full AC-3: enforce arc consistency across all arcs.
        An arc (Xi, Xj) is consistent if for every value in Xi's domain,
        there exists some value in Xj's domain that satisfies the constraint.
        """
        queue = deque()
        # Initialize queue with all arcs
        for r in range(9):
            for c in range(9):
                if board.is_empty(r, c):
                    for nr, nc in board.get_neighbors(r, c):
                        if board.is_empty(nr, nc):
                            queue.append(((r, c), (nr, nc)))

        return self._process_ac3_queue(board, domains, queue)

    def _ac3_from(self, board, domains, row, col):
        """
        Targeted AC-3: only enqueue arcs affected by the assignment at (row, col).
        """
        queue = deque()
        for nr, nc in board.get_neighbors(row, col):
            if board.is_empty(nr, nc):
                for nnr, nnc in board.get_neighbors(nr, nc):
                    if board.is_empty(nnr, nnc) and (nnr, nnc) != (row, col):
                        queue.append(((nr, nc), (nnr, nnc)))

        return self._process_ac3_queue(board, domains, queue)

    def _process_ac3_queue(self, board, domains, queue):
        """Process the AC-3 queue. Returns False if any domain is wiped out."""
        while queue:
            (r1, c1), (r2, c2) = queue.popleft()
            self.arc_revisions += 1

            if self._revise(domains, r1, c1, r2, c2):
                d = domains.get_domain(r1, c1)
                if len(d) == 0:
                    return False
                # If domain shrunk, re-check all neighbors of (r1, c1)
                for nr, nc in board.get_neighbors(r1, c1):
                    if board.is_empty(nr, nc) and (nr, nc) != (r2, c2):
                        queue.append(((nr, nc), (r1, c1)))

        return True

    def _revise(self, domains, r1, c1, r2, c2):
        """
        Remove values from domain of (r1,c1) that have no support in (r2,c2).
        Returns True if domain was revised.
        """
        revised = False
        d1 = domains.get_domain(r1, c1)
        d2 = domains.get_domain(r2, c2)

        to_remove = set()
        for val in d1:
            self.constraint_checks += 1
            # val is supported if d2 has at least one value != val
            if d2 == {val}:  # Only unsupported if d2 has ONLY this value
                to_remove.add(val)

        if to_remove:
            d1 -= to_remove
            domains.set_domain(r1, c1, d1)
            revised = True

        return revised

    def get_metrics(self):
        return {
            "nodes_expanded": self.nodes_expanded,
            "backtracks": self.backtracks,
            "constraint_checks": self.constraint_checks,
            "arc_revisions": self.arc_revisions,
        }
