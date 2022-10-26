import pandas as pd

# for .py file
display = print

EMPTY = 0
LIGHT = 1
DARK = 2
AVAILABLE = 3
STATE_COLORS = {
    EMPTY: "🟩",
    LIGHT: "🟡",
    DARK: "🔵",
    AVAILABLE: "🟫",
}


def create_board():
    """Create initial board."""
    board = []
    for r in range(8):
        board.append([])
        for c in range(8):
            cell = {"r": r, "c": c, "state": 0}
            if r == 3 and c == 3:
                cell["state"] = 1
            elif r == 3 and c == 4:
                cell["state"] = 2
            elif r == 4 and c == 3:
                cell["state"] = 2
            elif r == 4 and c == 4:
                cell["state"] = 1
            board[r].append(cell)
    return board


def display_board(board):
    """Display boards using Pandas."""
    df = pd.DataFrame(board)
    df = df.applymap(lambda v: v["state"])
    df = df.replace(EMPTY, STATE_COLORS[EMPTY])
    df = df.replace(LIGHT, STATE_COLORS[LIGHT])
    df = df.replace(DARK, STATE_COLORS[DARK])
    df = df.replace(AVAILABLE, STATE_COLORS[AVAILABLE])
    display(df)


def get_surrounding_cells(board, base_cell):
    """Get the surrounding cells from the base cell."""
    start_r = base_cell["r"] - 1
    start_c = base_cell["c"] - 1
    end_r = base_cell["r"] + 1
    end_c = base_cell["c"] + 1
    surrounding_cells = []
    for r in range(start_r, end_r+1):
        for c in range(start_c, end_c+1):
            if not (-1 < r < 8) or not (-1 < c < 8):
                continue
            if r == base_cell["r"] and c == base_cell["c"]:
                continue
            surrounding_cells.append(board[r][c])
    return surrounding_cells


def get_directions(base_cell, target_cell):
    """Get directions from target and base cells."""
    r_dir = target_cell["r"] - base_cell["r"]
    c_dir = target_cell["c"] - base_cell["c"]
    return r_dir, c_dir


def get_reversible_cells_in_one_dir(board, current_turn, base_cell, dirs):
    """Get all reversible cells in one direction."""
    reversible_cells_in_one_dir = []
    next_r = base_cell["r"]
    next_c = base_cell["c"]
    while True:
        next_r += dirs[0]
        next_c += dirs[1]
        if not (-1 < next_r < 8) or not (-1 < next_c < 8):
            break
        if board[next_r][next_c]["state"] == EMPTY or board[next_r][next_c]["state"] == AVAILABLE:
            break
        if board[next_r][next_c]["state"] == current_turn:
            reversible_cells_in_one_dir.append(board[next_r][next_c])
            break
        if board[next_r][next_c]["state"] != current_turn:
            reversible_cells_in_one_dir.append(board[next_r][next_c])

    if len(reversible_cells_in_one_dir) > 0:
        if reversible_cells_in_one_dir[-1]["state"] == current_turn:
            reversible_cells_in_one_dir.pop()
        else:
            reversible_cells_in_one_dir.clear()
    return reversible_cells_in_one_dir


def get_reversible_cells(board, base_cell, current_turn):
    """Get all reversible cells in all directions."""
    reversible_cells = []
    surrounding_cells = get_surrounding_cells(board, base_cell)
    for cell in surrounding_cells:
        dirs = get_directions(base_cell, cell)
        reversible_cells_in_one_dir = get_reversible_cells_in_one_dir(
            board, current_turn, base_cell, dirs)
        reversible_cells.extend(reversible_cells_in_one_dir)
    return reversible_cells
