"""
Metrics Collection System
Author: Anjali
Status: IN PROGRESS - basic collection done, visualization pending

Collects and compares performance metrics across solvers.
"""

import time
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class SolverMetrics:
    solver_name: str
    solved: bool = False
    execution_time: float = 0.0
    nodes_expanded: int = 0
    backtracks: int = 0
    constraint_checks: int = 0

    def to_dict(self):
        return {
            "Solver": self.solver_name,
            "Solved": "Yes" if self.solved else "No",
            "Time (s)": f"{self.execution_time:.6f}",
            "Nodes": self.nodes_expanded,
            "Backtracks": self.backtracks,
            "Checks": self.constraint_checks,
        }


class MetricsCollector:

    def __init__(self):
        self.results = []
        self._timer_start = None

    def start_timer(self):
        self._timer_start = time.perf_counter()

    def stop_timer(self):
        if self._timer_start is None:
            return 0.0
        elapsed = time.perf_counter() - self._timer_start
        self._timer_start = None
        return elapsed

    def record(self, solver_name, solved, elapsed, solver_metrics):
        metrics = SolverMetrics(
            solver_name=solver_name,
            solved=solved,
            execution_time=elapsed,
            nodes_expanded=solver_metrics.get("nodes_expanded", 0),
            backtracks=solver_metrics.get("backtracks", 0),
            constraint_checks=solver_metrics.get("constraint_checks", 0),
        )
        self.results.append(metrics)
        return metrics

    def get_comparison_table(self):
        return [r.to_dict() for r in self.results]

    def get_fastest(self):
        solved = [r for r in self.results if r.solved]
        return min(solved, key=lambda r: r.execution_time) if solved else None


# TODO (Anjali):
# - Add bar chart visualization using matplotlib
# - Export results to CSV
# - Add statistical comparison across multiple runs
