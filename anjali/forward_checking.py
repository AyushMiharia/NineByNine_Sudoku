"""
MRV + Forward Checking Solver
Author: Anjali
Status: IN PROGRESS - solver functional, arc consistency planned

Combines MRV variable selection with forward checking.
After each assignment, prunes inconsistent values from neighbors.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from anjali.domains import DomainTracker


class ForwardCheckingSolver:

    NAME = "MRV + Forward Checking"

    def __init__(self):
        self.nodes_expanded = 0
        self.backtracks = 0
        self.constraint_checks = 0

    def solve(self, board):
        self.nodes_expanded = 0
        self.backtracks = 0
        self.constraint_checks = 0
        domains = DomainTracker(board)
        return self._backtrack(board, domains)

    def _backtrack(self, board, domains):
        if not board.get_empty_cells():
            return True

        cell = domains.get_mrv_cell(board)
        if cell is None:
            return True

        row, col = cell
        domain = domains.get_domain(row, col)

        if not domain:
            return False

        self.nodes_expanded += 1

        for value in sorted(domain):
            self.constraint_checks += 1

            saved_domains = domains.clone()

            board.set(row, col, value)
            domains.set_domain(row, col, {value})

            if self._forward_check(board, domains, row, col, value):
                if self._backtrack(board, domains):
                    return True

            board.clear(row, col)
            domains = saved_domains
            self.backtracks += 1

        return False

    def _forward_check(self, board, domains, row, col, value):
        """Prune value from all neighbors' domains."""
        neighbors = board.get_neighbors(row, col)

        for nr, nc in neighbors:
            if board.is_empty(nr, nc):
                self.constraint_checks += 1
                neighbor_domain = domains.get_domain(nr, nc)

                if value in neighbor_domain:
                    neighbor_domain.discard(value)
                    domains.set_domain(nr, nc, neighbor_domain)

                    if len(neighbor_domain) == 0:
                        return False  # Domain wipeout

        return True

    def get_metrics(self):
        return {
            "nodes_expanded": self.nodes_expanded,
            "backtracks": self.backtracks,
            "constraint_checks": self.constraint_checks,
        }


# TODO (Anjali):
# - Implement AC-3 arc consistency as additional propagation
# - Add metrics visualization/charting
# - Integrate with comparison framework
