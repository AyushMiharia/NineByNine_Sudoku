"""
Sudoku Puzzle Generator
Author: Salwa
Status: COMPLETE

Generates valid Sudoku puzzles with configurable difficulty.
Uses backtracking to create a full solution, then removes cells.
"""

import random
from common.board import SudokuBoard
from common.constraints import is_valid_placement


DIFFICULTY_CLUES = {
    "easy": 45,
    "medium": 35,
    "hard": 28,
    "expert": 22,
}


def generate_puzzle(difficulty="medium"):
    """Generate a puzzle board and its solution."""
    board = SudokuBoard()
    _fill_board(board)

    solution = [row[:] for row in board.grid]
    clues = DIFFICULTY_CLUES.get(difficulty, 35)
    cells = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(cells)

    remove_count = 81 - clues
    for r, c in cells:
        if remove_count <= 0:
            break
        board.clear(r, c)
        remove_count -= 1

    board.save_original()
    return board, solution


def _fill_board(board):
    """Fill a blank board with a valid complete Sudoku."""
    empty = board.get_empty_cells()
    if not empty:
        return True
    row, col = empty[0]
    nums = list(range(1, 10))
    random.shuffle(nums)
    for num in nums:
        if is_valid_placement(board, row, col, num):
            board.set(row, col, num)
            if _fill_board(board):
                return True
            board.clear(row, col)
    return False


# Predefined puzzles for consistent testing
SAMPLE_PUZZLES = {
    "easy": [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ],
    "hard": [
        [0, 0, 0, 6, 0, 0, 4, 0, 0],
        [7, 0, 0, 0, 0, 3, 6, 0, 0],
        [0, 0, 0, 0, 9, 1, 0, 8, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 5, 0, 1, 8, 0, 0, 0, 3],
        [0, 0, 0, 3, 0, 6, 0, 4, 5],
        [0, 4, 0, 2, 0, 0, 0, 6, 0],
        [9, 0, 3, 0, 0, 0, 0, 0, 0],
        [0, 2, 0, 0, 0, 0, 1, 0, 0],
    ],
}
