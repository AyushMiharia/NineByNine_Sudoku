"""
Constraint Checking for Sudoku CSP
Author: Salwa
Status: COMPLETE

Row, column, and box uniqueness validation.
Used by all solvers for placement legality checks.
"""


def is_valid_placement(board, row, col, value):
    """Check if placing 'value' at (row, col) violates no constraints."""
    for c in range(board.SIZE):
        if c != col and board.get(row, c) == value:
            return False
    for r in range(board.SIZE):
        if r != row and board.get(r, col) == value:
            return False
    box_r = (row // board.BOX_SIZE) * board.BOX_SIZE
    box_c = (col // board.BOX_SIZE) * board.BOX_SIZE
    for r in range(box_r, box_r + board.BOX_SIZE):
        for c in range(box_c, box_c + board.BOX_SIZE):
            if (r, c) != (row, col) and board.get(r, c) == value:
                return False
    return True


def get_legal_values(board, row, col):
    """Return set of values that can be legally placed at (row, col)."""
    if not board.is_empty(row, col):
        return set()
    used = set()
    used.update(board.get_row(row))
    used.update(board.get_col(col))
    used.update(board.get_box(row, col))
    used.discard(board.EMPTY)
    return set(range(1, 10)) - used


def is_board_valid(board):
    """Check if the entire board state is consistent."""
    for r in range(board.SIZE):
        for c in range(board.SIZE):
            val = board.get(r, c)
            if val == board.EMPTY:
                continue
            board.clear(r, c)
            if not is_valid_placement(board, r, c, val):
                board.set(r, c, val)
                return False
            board.set(r, c, val)
    return True
