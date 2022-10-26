import random
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
            cell = {"r": r, "c": c, "state": 0, "reversible_cells": []}
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


# Game Manager
def create_game_manager():
    """Create a game manager object."""
    return {
        "turn": 1,
        "current_turn": LIGHT,
        "is_game_over": False,
        "is_passed": False,
        "is_passed_previous": False,
        "count_state": [0, 0, 0, 0],  # EMPTY, LIGHT, DARK, AVAILABLE
        "players": {
            1: {"name": "A", "is_random": True},
            2: {"name": "B", "is_random": True},
        }
    }


def refresh_board(board, gm):
    """Refresh board."""
    gm["count_state"] = [0, 0, 0, 0]
    gm["is_passed"] = True
    for r in range(8):
        for c in range(8):
            board[r][c]["reversible_cells"] = []
            if board[r][c]["state"] == AVAILABLE:
                board[r][c]["state"] = EMPTY
            if board[r][c]["state"] == EMPTY:
                board[r][c]["reversible_cells"] = get_reversible_cells(
                    board, board[r][c], gm["current_turn"])
            if len(board[r][c]["reversible_cells"]) > 0:
                board[r][c]["state"] = AVAILABLE
                gm["is_passed"] = False
            gm["count_state"][board[r][c]["state"]] += 1

# board = create_board()


# gm["current_turn"] = LIGHT
# refresh_board(board, gm)
# display_board(board)


def manual_selection():
    """Converts user input to integer indices."""
    selection = input("Select a cell (e.g r0 c4 => 04): ")
    if len(selection) != 2:
        raise Exception("The number of characters is limited to 2.")
    r = int(selection[0])
    c = int(selection[1])
    return r, c


def automatic_selection(board):
    """Selects a cell automatically."""
    while True:
        r = random.randint(0, 7)
        c = random.randint(0, 7)
        if board[r][c]["state"] == AVAILABLE:
            return r, c


def play_game():
    """"""
    ############################
    # 初期化
    gm["turn"] = 1
    # プレイヤー作成
    gm["players"][1]["is_random"] = True
    gm["players"][2]["is_random"] = True
    board = create_board()
    ############################

    # is_game_over = Falseなら続ける
    while not gm["is_game_over"]:
        ############################
        # ターンごとの初期化
        # is_passed を is_passed_previous へコピーし、初期化
        gm["is_passed_previous"] = gm["is_passed"]
        gm["is_passed"] = False
        # 現ターンの色 (LIGHT or DARK)
        if gm["turn"] % 2 == 0:
            # 偶数ターン
            gm["current_turn"] = DARK
        else:
            # 奇数ターン
            gm["current_turn"] = LIGHT
        ############################

        ############################
        # 表示
        # 現ターンの色のセルをリフレッシュ
        refresh_board(board, gm)

        print(
            f"""\
-----------------------------------
 {STATE_COLORS[gm["current_turn"]]}　TURN {gm["turn"]} [{STATE_COLORS[1]}　: {gm["count_state"][1]} {STATE_COLORS[2]}　: {gm["count_state"][2]}] 
-----------------------------------""")
        display_board(board)
        ############################

        ############################
        # 終了条件チェック
        # 置ける場所があるかどうか判定
        # 置ける場所がない場合、つまり is_passed = True の場合
        if gm["is_passed"]:

            if gm["count_state"][1] + gm["count_state"][2] >= 64:
                # diskの合計数が64になったら終了
                gm["is_game_over"] = True
                # print('\n The total of LIGHT and DARK cells is now 64.)
                print('\n 合計数が64になったので終了します。')
                break
            elif gm["is_passed_previous"]:
                # 1. 前回もスキップしていればゲーム終了（両者とも置けないので）
                gm["is_game_over"] = True
                # print('\n It is the second pass in a row, so it is terminated.')
                print('\n 2回連続でパスなので終了します。')
                break  # continueでもOK
            else:
                # 2. 前回は置けていたら、ターンをスキップして次のターンへ
                gm["is_passed"] = True
                # print('\n There is no place to put, so skip the turn.')
                print(
                    f'\n {STATE_COLORS[gm["current_turn"]]}　は置ける場所がないのでスキップします。')
                # ターンを進める
                gm["turn"] += 1
                continue
        ############################

        ############################
        # 置く場所を選択
        # 置ける場所がある場合
        # 現在のターンプレイヤーがランダムかどうか判定
        if gm["players"][gm["current_turn"]]["is_random"]:
            # ランダムならランダムで選択
            selected_r, selected_c = automatic_selection(board)
        else:
            # User
            while True:
                # ユーザー入力のセルを取得
                selected_r, selected_c = manual_selection()
                # ユーザー入力のセルが置けるかどうか判定
                if board[selected_r][selected_c]["state"] != AVAILABLE:
                    print("置けません。")
                    continue
                break
        ############################

        ############################
        # 反転する
        # 1. 選択セルを反転
        board[selected_r][selected_c]["state"] = gm["current_turn"]
        # 2. 選択セルの反転可能なセルを反転
        for cell in board[selected_r][selected_c]["reversible_cells"]:
            cell["state"] = gm["current_turn"]
        ############################

        # ターンを進める
        gm["turn"] += 1

    # print(f'\n ゲーム終了')

    if gm['count_state'][LIGHT] > gm['count_state'][DARK]:
        print(f'\n WINNER: {STATE_COLORS[1]}')
    elif gm['count_state'][LIGHT] < gm['count_state'][DARK]:
        print(f'\n WINNER: {STATE_COLORS[2]}')
    else:
        print(f'\n DRAW')
