from io import StringIO
from function_version import create_board


def test_create_board():
    board = create_board()
    assert len(board) == 8
    for row in board:
        assert len(row) == 8
        for cell in row:
            assert cell["c"] in range(8)
            assert cell["r"] in range(8)
            assert cell["state"] in [0, 1, 2, 3]
    assert board[3][3]["state"] == 1
    assert board[3][4]["state"] == 2
    assert board[4][3]["state"] == 2
    assert board[4][4]["state"] == 1
