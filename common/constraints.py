def is_valid_placement(board, row, col, value):
    for c in range(9):
        if c != col and board.get(row, c) == value: return False
    for r in range(9):
        if r != row and board.get(r, col) == value: return False
    br, bc = (row//3)*3, (col//3)*3
    for r in range(br, br+3):
        for c in range(bc, bc+3):
            if (r, c) != (row, col) and board.get(r, c) == value: return False
    return True


def get_legal_values(board, row, col):
    if not board.is_empty(row, col): return set()
    used = set(board.get_row(row)) | set(board.get_col(col)) | set(board.get_box(row, col))
    used.discard(0)
    return set(range(1, 10)) - used


def is_board_valid(board):
    for r in range(9):
        for c in range(9):
            v = board.get(r, c)
            if v == 0: continue
            board.clear(r, c)
            ok = is_valid_placement(board, r, c, v)
            board.set(r, c, v)
            if not ok: return False
    return True
