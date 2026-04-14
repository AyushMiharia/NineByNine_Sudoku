"""9x9 Sudoku grid wrapper."""

import random


class SudokuBoard:
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
        b = SudokuBoard(self.grid)
        if self.original:
            b.original = [row[:] for row in self.original]
        return b

    def get(self, r, c): return self.grid[r][c]
    def set(self, r, c, v): self.grid[r][c] = v
    def clear(self, r, c): self.grid[r][c] = self.EMPTY
    def is_empty(self, r, c): return self.grid[r][c] == self.EMPTY

    def get_empty_cells(self):
        return [(r, c) for r in range(self.SIZE) for c in range(self.SIZE) if self.is_empty(r, c)]

    def get_row(self, r): return self.grid[r][:]
    def get_col(self, c): return [self.grid[r][c] for r in range(self.SIZE)]

    def get_box(self, r, c):
        br, bc = (r // 3) * 3, (c // 3) * 3
        return [self.grid[rr][cc] for rr in range(br, br+3) for cc in range(bc, bc+3)]

    def get_neighbors(self, r, c):
        n = set()
        for i in range(9):
            if i != c: n.add((r, i))
            if i != r: n.add((i, c))
        br, bc = (r//3)*3, (c//3)*3
        for rr in range(br, br+3):
            for cc in range(bc, bc+3):
                if (rr, cc) != (r, c): n.add((rr, cc))
        return n

    def is_complete(self):
        return all(self.grid[r][c] != 0 for r in range(9) for c in range(9))

    def save_original(self):
        self.original = [row[:] for row in self.grid]

    def to_json(self):
        return self.grid

    def __str__(self):
        lines = ["+-------+-------+-------+"]
        for r in range(9):
            if r > 0 and r % 3 == 0:
                lines.append("+-------+-------+-------+")
            s = "|"
            for c in range(9):
                if c > 0 and c % 3 == 0: s += "|"
                v = self.grid[r][c]
                s += f" {v if v else '.'} "
            lines.append(s + "|")
        lines.append("+-------+-------+-------+")
        return "\n".join(lines)
