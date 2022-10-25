from io import StringIO
from function_version import STATE_COLORS, EMPTY, LIGHT, DARK, create_board, display_board


def test_const():
    assert STATE_COLORS[EMPTY] == "🟩"
    assert STATE_COLORS[LIGHT] == "🟡"
    assert STATE_COLORS[DARK] == "🔵"
    assert STATE_COLORS[3] == "🟫"


def test_create_board():
    board = create_board()
    assert len(board) == 8
    for row in board:
        assert len(row) == 8
        for cell in row:
            assert cell["c"] in range(8)
            assert cell["r"] in range(8)
            assert cell["state"] in STATE_COLORS.keys()
    assert board[3][3]["state"] == LIGHT
    assert board[3][4]["state"] == DARK
    assert board[4][3]["state"] == DARK
    assert board[4][4]["state"] == LIGHT


def test_display_board(capfd):
    board = create_board()
    display_board(board)
    # verification of output content
    out, err = capfd.readouterr()
    # there is a green cell
    assert STATE_COLORS[EMPTY] in out
    # there is a yellow cell
    assert STATE_COLORS[LIGHT] in out
    # there is a blue cell
    assert STATE_COLORS[DARK] in out
