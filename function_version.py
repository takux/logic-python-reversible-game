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


board = create_board()
display_board(board)

board = create_board()

r = 1
c = 1
print(board[r][c])

start_r = r - 1
start_c = c - 1
print(board[start_r][start_c])

end_r = r + 1
end_c = c + 1
print(board[end_r][end_c])
