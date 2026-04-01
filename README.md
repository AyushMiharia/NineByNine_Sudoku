# NineByNine AI

### A Multi-Strategy Sudoku CSP Solver

> CS 5100 — Foundations of Artificial Intelligence · Northeastern University

---

## What Is This?

NineByNine AI models Sudoku as a **Constraint Satisfaction Problem** and solves it using four AI strategies — from brute-force backtracking to intelligent heuristic-driven search to local search. The project compares how these techniques perform and includes an interactive web frontend.

---

## Team

| Member | Role |
|--------|------|
| **Salwa** | Board, constraints, generator, Backtracking, MRV + Degree + LCV |
| **Anjali** | Domain tracking, Forward Checking + AC-3, metrics system |
| **Ayush** | Min-Conflicts solver, strategy runner, HTML/CSS/JS frontend |

---

## Algorithms

**Plain Backtracking** — Baseline DFS. Fills cells in row-major order, tries 1–9, backtracks on violation.

**Backtracking + MRV + Degree + LCV** — Always picks the most constrained cell. Degree heuristic breaks ties. Least Constraining Value ordering tries values that leave the most options for neighbors.

**MRV + Forward Checking + AC-3** — After each assignment, prunes that value from neighbors' domains. AC-3 arc consistency cascades further reductions. Domain wipeout triggers immediate backtracking.

**Min-Conflicts (Local Search)** — No search tree. Fills each box with a valid permutation, then swaps cells to reduce row/column conflicts. Sideways moves escape plateaus. Stale detection triggers early restarts.

---

## How to Run

**Backend demo** (no dependencies):
```bash
python demo.py
```

**Frontend** (no server needed):
```
Open frontend/index.html in any browser
```

---

## Project Structure

```
├── common/                  # Shared foundation
│   ├── board.py             # SudokuBoard class
│   ├── constraints.py       # Validation and legal values
│   └── generator.py         # Puzzle generation (4 levels)
│
├── salwa/                   # Salwa's work
│   ├── backtracking.py      # Plain Backtracking
│   └── mrv_solver.py        # MRV + Degree + LCV
│
├── anjali/                  # Anjali's work
│   ├── domains.py           # Domain tracker
│   ├── forward_checking.py  # Forward Checking + AC-3
│   └── metrics.py           # Collection + comparison table
│
├── ayush/                   # Ayush's work
│   ├── min_conflicts.py     # Min-Conflicts (box swaps)
│   └── runner.py            # Strategy runner (all 4 solvers)
│
├── frontend/                # Web UI
│   ├── index.html           # Home, play, result screens
│   ├── style.css            # Styling
│   └── app.js               # Game logic + all 4 JS solvers
│
├── demo.py                  # Run and compare all solvers
└── README.md
```

---

## What Changed Since PR1

- **MRV solver** now includes degree heuristic tiebreaker and LCV value ordering (Salwa)
- **Forward Checking** now includes AC-3 arc consistency propagation (Anjali)
- **Min-Conflicts** fully optimized with sideways moves, stale detection, and integrated into runner (Ayush)
- **Metrics** upgraded with formatted comparison table and speedup analysis (Anjali)
- **Frontend** built — interactive board, difficulty selection, hints, AI solve with all 4 algorithms, result page with metrics (Ayush)
- **Runner** now orchestrates all 4 solvers (Ayush)

---

## Next Steps

- Step-by-step solve animation in frontend
- Full benchmark suite across all difficulty levels with statistical averaging
- Metrics chart visualization with matplotlib
- Enhanced algorithm explanation pages with step-by-step walkthrough
- Final UI polish and comprehensive comparison report
