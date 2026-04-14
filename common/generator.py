import random
from common.board import SudokuBoard
from common.constraints import is_valid_placement

DIFFICULTY_CLUES = {"easy": 45, "medium": 35, "hard": 28, "expert": 22}

def generate_puzzle(difficulty="medium"):
    board = SudokuBoard()
    _fill(board)
    solution = [row[:] for row in board.grid]
    clues = DIFFICULTY_CLUES.get(difficulty, 35)
    cells = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(cells)
    remove = 81 - clues
    for r, c in cells:
        if remove <= 0: break
        board.clear(r, c)
        remove -= 1
    board.save_original()
    return board, solution

def _fill(board):
    empty = board.get_empty_cells()
    if not empty: return True
    r, c = empty[0]
    nums = list(range(1, 10))
    random.shuffle(nums)
    for n in nums:
        if is_valid_placement(board, r, c, n):
            board.set(r, c, n)
            if _fill(board): return True
            board.clear(r, c)
    return False

SAMPLE_PUZZLES = {
    "easy": [
        [5,3,0,0,7,0,0,0,0],[6,0,0,1,9,5,0,0,0],[0,9,8,0,0,0,0,6,0],
        [8,0,0,0,6,0,0,0,3],[4,0,0,8,0,3,0,0,1],[7,0,0,0,2,0,0,0,6],
        [0,6,0,0,0,0,2,8,0],[0,0,0,4,1,9,0,0,5],[0,0,0,0,8,0,0,7,9],
    ],
    "hard": [
        [0,0,0,6,0,0,4,0,0],[7,0,0,0,0,3,6,0,0],[0,0,0,0,9,1,0,8,0],
        [0,0,0,0,0,0,0,0,0],[0,5,0,1,8,0,0,0,3],[0,0,0,3,0,6,0,4,5],
        [0,4,0,2,0,0,0,6,0],[9,0,3,0,0,0,0,0,0],[0,2,0,0,0,0,1,0,0],
    ],
}
