# NineByNine AI

### A Multi-Strategy Sudoku CSP Solver

> CS 5100 — Foundations of Artificial Intelligence · Northeastern University

---

## What Is This?

NineByNine AI models Sudoku as a **Constraint Satisfaction Problem** and solves it using multiple AI strategies — from brute-force backtracking to intelligent heuristic-driven search. The goal is to compare how different CSP techniques perform and demonstrate the power of smart variable/value selection.

---

## Team

| Member | Role |
|--------|------|
| **Salwa** | Board representation, constraint checking, puzzle generation, Plain Backtracking solver, MRV solver |
| **Anjali** | Domain tracking, Forward Checking solver, metrics collection system |
| **Ayush** | Min-Conflicts local search solver, strategy runner, integration |

---

## Algorithms

**Plain Backtracking** — The baseline. Fills cells left-to-right, top-to-bottom, tries values 1–9, and backtracks on constraint violations. Simple but explores many unnecessary branches.

**Backtracking + MRV** — Smarter cell selection. Always picks the most constrained cell (fewest legal values remaining). Dramatically reduces the search space compared to plain backtracking.

**MRV + Forward Checking** — Adds constraint propagation. After each assignment, prunes that value from all neighboring cells' domains. If any domain becomes empty, backtracks immediately without wasting time.

**Min-Conflicts (Local Search)** — A completely different paradigm. Fills the board randomly and iteratively repairs conflicts by swapping values within 3×3 boxes. No search tree — purely iterative repair. *(Early stage)*

---

## How to Run

No external dependencies — pure Python 3.

```bash
python demo.py
```

This runs the available solvers on built-in easy and hard sample puzzles and prints a comparison of their performance.

---

## Project Structure

```
├── common/                  # Shared foundation
│   ├── board.py             # SudokuBoard — grid, clone, neighbors
│   ├── constraints.py       # Validation and legal value computation
│   └── generator.py         # Puzzle generation (4 difficulty levels)
│
├── salwa/                   # Salwa's work
│   ├── backtracking.py      # Plain Backtracking solver
│   └── mrv_solver.py        # Backtracking + MRV solver
│
├── anjali/                  # Anjali's work
│   ├── domains.py           # Domain tracker for forward checking
│   ├── forward_checking.py  # MRV + Forward Checking solver
│   └── metrics.py           # Performance metrics collector
│
├── ayush/                   # Ayush's work
│   ├── min_conflicts.py     # Min-Conflicts local search solver
│   └── runner.py            # Strategy runner orchestration
│
├── demo.py                  # Run and compare solvers
└── README.md
```

---

## Current Status

- **Board, Constraints, Generator** — Complete. Supports 9×9 grids, four difficulty levels (Easy/Medium/Hard/Expert), neighbor lookups, and board cloning for solver isolation.
- **Plain Backtracking** — Complete. Serves as the performance baseline.
- **Backtracking + MRV** — Core MRV selection working. Degree heuristic tiebreaker and LCV ordering planned.
- **MRV + Forward Checking** — Functional with domain pruning. AC-3 arc consistency planned.
- **Metrics Collection** — Basic timing and metric recording. Chart visualization planned.
- **Min-Conflicts** — Early-stage box-swap approach. Not yet integrated into the runner.

---

## Next Steps

- Optimize Min-Conflicts with sideways moves and stale detection (Ayush)
- Add degree heuristic tiebreaker and LCV value ordering to MRV (Salwa)
- Implement AC-3 arc consistency propagation (Anjali)
- Build metrics chart visualization (Anjali)
- Develop interactive web frontend with hints and AI solve modes (Ayush)
- Full benchmark suite across all difficulty levels (All)
