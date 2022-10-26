from io import StringIO
from function_version import *


def test_const():
    assert STATE_COLORS[EMPTY] == "🟩"
    assert STATE_COLORS[LIGHT] == "🟡"
    assert STATE_COLORS[DARK] == "🔵"
    assert STATE_COLORS[AVAILABLE] == "🟫"


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


def test_get_surrounding_cells():
    board = create_board()
    # verify surrounding cells
    r0c0_srrounging_cells = get_surrounding_cells(board, board[0][0])
    r0c1_srrounging_cells = get_surrounding_cells(board, board[0][1])
    r7c7_srrounging_cells = get_surrounding_cells(board, board[7][7])
    r3c3_srrounging_cells = get_surrounding_cells(board, board[3][3])
    # number of cells around the top-left-most cell
    assert len(r0c0_srrounging_cells) == 3
    # number of cells around the cell one right from the top left
    assert len(r0c1_srrounging_cells) == 5
    # number of cells around the bottom right-most cell
    assert len(r7c7_srrounging_cells) == 3
    # number of cells around the cell per center
    assert len(r3c3_srrounging_cells) == 8


def test_get_directions():
    board = create_board()
    # Check the cell in the right direction
    assert get_directions(board[0][0], board[0][1]) == (0, 1)
    # Check the cell in the bottom right direction
    assert get_directions(board[0][0], board[1][1]) == (1, 1)
    # Check the cell in the bottom direction
    assert get_directions(board[0][0], board[1][0]) == (1, 0)


def test_get_reversiable_cells_in_one_dir():
    # Check the cell in the right direction
    # Row 1: [1,2,2,2,2,1,0,0]
    # Current turn color: 1
    # base_cell: Top left cell
    # dirs: Right direction
    current_turn = LIGHT
    next_turn = DARK
    board = create_board()
    # Make the first line as configured.
    for i, cell in enumerate(board[0]):
        if i == 0 or i == 5:
            cell["state"] = 1
        elif i < 5:
            cell["state"] = 2
        else:
            cell["state"] = 0
    base_cell = board[0][0]
    dirs = get_directions(base_cell, board[0][1])
    reversiable_cells_in_one_dir = get_reversible_cells_in_one_dir(
        board, current_turn, base_cell, dirs)
    # Number of reversible cells
    assert len(reversiable_cells_in_one_dir) == 4
    # All colors are opposite to the current color
    for reversiable_cell in reversiable_cells_in_one_dir:
        assert reversiable_cell["state"] == next_turn
