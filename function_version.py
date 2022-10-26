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


# current turn == yellow
current_turn = LIGHT

# board
board = create_board()
board[3][3]["state"] = EMPTY
board[3][4]["state"] = EMPTY
board[4][3]["state"] = EMPTY
board[4][4]["state"] = EMPTY

board[0][0]["state"] = current_turn
board[0][7]["state"] = LIGHT

board[0][1]["state"] = DARK
board[0][2]["state"] = DARK
board[0][3]["state"] = DARK
board[0][4]["state"] = DARK
board[0][5]["state"] = DARK
board[0][6]["state"] = DARK
display_board(board)

# base_cell
base_cell = board[0][0]

# target_cell
target_cell = board[0][1]

# dirs
dirs = get_directions(base_cell, target_cell)
dirs

# １つの向きに進んで反転可能なセルを取得

# 反転可能なリスト


# ループ条件
# ボード外なら終了
# カラーが Green or Brown なら終了
# 同じ色ならリストに加えて（後で挟めるか判定するため）終了
# 相手色ならリストに追加


# ループ後のリストをチェック
