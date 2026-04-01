"""
Metrics Collection and Comparison
Author: Anjali
Status: Complete (upgraded in PR2)
  - PR1: Basic collection and JSON export
  - PR2: Added formatted comparison table, speedup analysis, summary stats
"""

import time


class SolverMetrics:
    def __init__(self, name, solved, time_s, nodes, backtracks, checks, extra=None):
        self.name = name
        self.solved = solved
        self.time = time_s
        self.nodes = nodes
        self.backtracks = backtracks
        self.checks = checks
        self.extra = extra or {}

    # PR1-compatible aliases
    @property
    def solver_name(self): return self.name
    @property
    def execution_time(self): return self.time

    def to_dict(self):
        d = {
            "solver": self.name, "solved": self.solved,
            "time": round(self.time, 6), "nodes": self.nodes,
            "backtracks": self.backtracks, "checks": self.checks,
        }
        d.update(self.extra)
        return d


class MetricsCollector:
    def __init__(self):
        self.results = []
        self._t0 = None

    def start(self):
        self._t0 = time.perf_counter()

    def stop(self):
        t = time.perf_counter() - self._t0 if self._t0 else 0
        self._t0 = None
        return t

    def record(self, name, solved, elapsed, metrics, extra=None):
        m = SolverMetrics(name, solved, elapsed,
            metrics.get("nodes_expanded", 0),
            metrics.get("backtracks", 0),
            metrics.get("constraint_checks", 0),
            extra)
        self.results.append(m)
        return m

    def to_json(self):
        return [r.to_dict() for r in self.results]

    # PR1-compatible alias
    def get_comparison_table(self):
        """Return list of dicts with PR1-compatible keys."""
        out = []
        for r in self.results:
            out.append({
                "Solver": r.name, "Solved": "Yes" if r.solved else "No",
                "Time (s)": f"{r.time:.6f}", "Nodes": r.nodes,
                "Backtracks": r.backtracks, "Checks": r.checks,
            })
        return out

    def get_fastest(self):
        ok = [r for r in self.results if r.solved]
        return min(ok, key=lambda r: r.time) if ok else None

    def get_most_efficient(self):
        ok = [r for r in self.results if r.solved]
        return min(ok, key=lambda r: r.nodes) if ok else None

    def print_comparison(self):
        """Print a formatted comparison table to the terminal."""
        if not self.results:
            print("No results recorded.")
            return

        cols = ["Solver", "Solved", "Time (s)", "Nodes", "Backtracks", "Checks"]
        widths = [30, 8, 12, 12, 12, 14]

        # Header
        header = " | ".join(f"{c:<{w}}" for c, w in zip(cols, widths))
        sep = "-+-".join("-" * w for w in widths)
        print(sep)
        print(header)
        print(sep)

        # Rows
        for r in self.results:
            vals = [
                r.name,
                "Yes" if r.solved else "No",
                f"{r.time:.6f}",
                f"{r.nodes:,}",
                f"{r.backtracks:,}",
                f"{r.checks:,}",
            ]
            print(" | ".join(f"{v:<{w}}" for v, w in zip(vals, widths)))

        print(sep)

        # Summary
        fastest = self.get_fastest()
        efficient = self.get_most_efficient()
        if fastest:
            print(f"\n  Fastest:        {fastest.name} ({fastest.time:.6f}s)")
        if efficient:
            print(f"  Most Efficient: {efficient.name} ({efficient.nodes:,} nodes)")

        # Speedup vs baseline
        solved = [r for r in self.results if r.solved]
        if len(solved) >= 2:
            base = solved[0]
            if base.time > 0:
                print(f"\n  Speedup vs {base.name}:")
                for r in solved[1:]:
                    if r.time > 0:
                        sp = base.time / r.time
                        print(f"    {r.name:<30} {sp:.1f}x")

# TODO: Export to CSV
# TODO: Bar chart visualization with matplotlib (PR3)
