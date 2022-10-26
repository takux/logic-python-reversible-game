from io import StringIO
from class_version import *


class TestBoard():

    def test_create_board(self):
        gm = GameManager()
        assert len(gm.board) == 8
        for row in gm.board:
            assert len(row) == 8
            for cell in row:
                assert cell.c in range(8)
                assert cell.r in range(8)
                assert cell.state in STATE_COLORS.keys()

    def test_display_board(self, capfd):
        gm = GameManager()
        gm.display_board()
        # 出力内容の検証
        out, err = capfd.readouterr()
        # 緑セルがあるかどうか
        assert STATE_COLORS[EMPTY] in out
        # 黄色セルがあるかどうか
        assert STATE_COLORS[LIGHT] in out
        # 青セルがあるかどうか
        assert STATE_COLORS[DARK] in out

    def test_surrounding_cells(self):
        gm = GameManager()
        # 周囲のセルを検証
        r0c0_cells = gm.get_surrounding_cells(gm.board[0][0])
        r0c1_cells = gm.get_surrounding_cells(gm.board[0][1])
        r7c7_cells = gm.get_surrounding_cells(gm.board[7][7])
        r3c3_cells = gm.get_surrounding_cells(gm.board[3][3])
        # 一番左上のセルの周囲のセル数
        assert len(r0c0_cells) == 3
        # 左上から１つ右のセルの周囲のセル数
        assert len(r0c1_cells) == 5
        # 一番右下のセルの周囲のセル数
        assert len(r7c7_cells) == 3
        # 中央あたり[3][3]のセルの周囲のセル数
        assert len(r3c3_cells) == 8

    def test_dirs(self):
        gm = GameManager()
        # 右方向のセルを検証
        dirs = Direction(gm.board[0][0], gm.board[0][1])
        assert dirs.r_dir == 0 and dirs.c_dir == 1
        # 右下方向のセルを検証
        dirs = Direction(gm.board[0][0], gm.board[1][1])
        assert dirs.r_dir == 1 and dirs.c_dir == 1
        # 下方向のセルを検証
        dirs = Direction(gm.board[0][0], gm.board[1][0])
        assert dirs.r_dir == 1 and dirs.c_dir == 0

    def test_get_reversible_cells_in_one_dir(self):
        # 右方向のセルを検証
        # １行目: [1,2,2,2,2,1,0,0]
        # 現在ターンカラー: 1
        # base_cell: 一番左上のセル
        # directions: 右方向
        next_turn = DARK
        gm = GameManager()
        # １行目を設定通りにする
        for i, cell in enumerate(gm.board[0]):
            if i == 0 or i == 5:
                cell.state = LIGHT
            elif i < 5:
                cell.state = DARK
            else:
                cell.state = EMPTY
        base_cell = gm.board[0][0]
        dirs = Direction(base_cell, gm.board[0][1])
        gm.current_turn = LIGHT
        reversible_cells_in_one_dir = gm.get_reversible_cells_in_one_dir(
            base_cell, dirs)
        # 反転可能なセルの数
        assert len(reversible_cells_in_one_dir) == 4
        # 全て現カラーと反対の色
        for reversible_cell in reversible_cells_in_one_dir:
            assert reversible_cell.state == next_turn

    def test_reversible_cells(self):
        """
        🟡  🟡  🟡  🟡  🟡  🟡  🟡  🟡
        🟡  🔵  🔵  🔵  🟡  🟡  🟡  🟡
        🟡  🔵  🟩  🔵  🔵  🟡  🟡  🟡
        🟡  🔵  🟡  🔵  🟡  🟡  🟡  🟡
        🟡  🟡  🟡  🟡  🔵  🟡  🟡  🟡
        🟡  🟡  🟡  🟡  🟡  🟡  🟡  🟡
        🟡  🟡  🟡  🟡  🟡  🟡  🟡  🟡
        🟡  🟡  🟡  🟡  🟡  🟡  🟡  🔵
        この状態で [2][2] の緑セルへ黄色を置いた場合の
        reversible_cells を正しく取得できているか検証
        """
        gm = GameManager()
        # board = gm.board
        # まず全て黄色にする
        for row in gm.board:
            for cell in row:
                cell.state = LIGHT
        gm.board[1][1].state = DARK
        gm.board[1][2].state = DARK
        gm.board[1][3].state = DARK

        gm.board[2][1].state = DARK
        gm.board[2][2].state = EMPTY
        gm.board[2][3].state = DARK
        gm.board[2][4].state = DARK

        gm.board[3][1].state = DARK
        gm.board[3][3].state = DARK

        gm.board[4][4].state = DARK

        gm.board[7][7].state = DARK

        gm.current_turn = LIGHT
        reversible_cells = gm.get_reversible_cells(gm.board[2][2])
        # 反転可能なセルの数
        assert len(reversible_cells) == 9


def test_refresh_board(capfd):
    gm = GameManager()
    gm.current_turn = LIGHT
    gm.refresh_board()
    gm.display_board()
    """
    # この状態を検証
    🟩  🟩  🟩  🟩  🟩  🟩  🟩  🟩
    🟩  🟩  🟩  🟩  🟩  🟩  🟩  🟩
    🟩  🟩  🟩  🟩  🟫  🟩  🟩  🟩
    🟩  🟩  🟩  🟡  🔵  🟫  🟩  🟩
    🟩  🟩  🟫  🔵  🟡  🟩  🟩  🟩
    🟩  🟩  🟩  🟫  🟩  🟩  🟩  🟩
    🟩  🟩  🟩  🟩  🟩  🟩  🟩  🟩
    🟩  🟩  🟩  🟩  🟩  🟩  🟩  🟩
    """
    # 茶色セルがあるかどうか
    out, err = capfd.readouterr()
    assert STATE_COLORS[AVAILABLE] in out
    assert gm.board[2][4].state == AVAILABLE
    assert len(gm.board[2][4].reversible_cells) > 0
    assert gm.board[2][4].reversible_cells[0].r == 3
    assert gm.board[2][4].reversible_cells[0].c == 4


class TestGameManager():

    def test_game_maneger(self):
        gm = GameManager()
        assert gm.turn == 1
        assert gm.current_turn == LIGHT
        assert gm.is_game_over == False
        assert gm.is_passed == False
        assert gm.is_passed_previous == False
        assert gm.count_state == [0, 0, 0, 0]
        assert gm.players[1].name == "A"
        assert gm.players[2].name == "B"

    def test_play_game(self):
        gm = GameManager()
        gm.play_game()
