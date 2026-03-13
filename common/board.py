"""
Board Representation for Sudoku CSP Solver
Author: Salwa
Status: COMPLETE

Core data structure shared by all solvers.
Handles 9x9 grid storage, cloning, neighbor lookup, and display.
"""

import random


class SudokuBoard:
    """Represents a 9x9 Sudoku board."""

    EMPTY = 0
    SIZE = 9
    BOX_SIZE = 3

    def __init__(self, grid=None):
        if grid is not None:
            self.grid = [row[:] for row in grid]
        else:
            self.grid = [[self.EMPTY] * self.SIZE for _ in range(self.SIZE)]
        self.original = None

    def clone(self):
        """Return a deep copy of this board."""
        new_board = SudokuBoard(self.grid)
        if self.original:
            new_board.original = [row[:] for row in self.original]
        return new_board

    def get(self, row, col):
        return self.grid[row][col]

    def set(self, row, col, value):
        self.grid[row][col] = value

    def clear(self, row, col):
        self.grid[row][col] = self.EMPTY

    def is_empty(self, row, col):
        return self.grid[row][col] == self.EMPTY

    def get_empty_cells(self):
        """Return list of (row, col) for all empty cells."""
        return [
            (r, c)
            for r in range(self.SIZE)
            for c in range(self.SIZE)
            if self.is_empty(r, c)
        ]

    def get_row(self, row):
        return self.grid[row][:]

    def get_col(self, col):
        return [self.grid[r][col] for r in range(self.SIZE)]

    def get_box(self, row, col):
        """Return all values in the 3x3 box containing (row, col)."""
        box_r = (row // self.BOX_SIZE) * self.BOX_SIZE
        box_c = (col // self.BOX_SIZE) * self.BOX_SIZE
        values = []
        for r in range(box_r, box_r + self.BOX_SIZE):
            for c in range(box_c, box_c + self.BOX_SIZE):
                values.append(self.grid[r][c])
        return values

    def get_neighbors(self, row, col):
        """Return set of (r, c) sharing row, col, or box with (row, col)."""
        neighbors = set()
        for c in range(self.SIZE):
            if c != col:
                neighbors.add((row, c))
        for r in range(self.SIZE):
            if r != row:
                neighbors.add((r, col))
        box_r = (row // self.BOX_SIZE) * self.BOX_SIZE
        box_c = (col // self.BOX_SIZE) * self.BOX_SIZE
        for r in range(box_r, box_r + self.BOX_SIZE):
            for c in range(box_c, box_c + self.BOX_SIZE):
                if (r, c) != (row, col):
                    neighbors.add((r, c))
        return neighbors

    def is_complete(self):
        return all(
            self.grid[r][c] != self.EMPTY
            for r in range(self.SIZE)
            for c in range(self.SIZE)
        )

    def save_original(self):
        """Snapshot current state as the original puzzle."""
        self.original = [row[:] for row in self.grid]

    def __str__(self):
        lines = ["+-------+-------+-------+"]
        for r in range(self.SIZE):
            if r > 0 and r % self.BOX_SIZE == 0:
                lines.append("+-------+-------+-------+")
            row_str = "|"
            for c in range(self.SIZE):
                if c > 0 and c % self.BOX_SIZE == 0:
                    row_str += "|"
                val = self.grid[r][c]
                row_str += f" {val if val != 0 else '.'} "
            row_str += "|"
            lines.append(row_str)
        lines.append("+-------+-------+-------+")
        return "\n".join(lines)
