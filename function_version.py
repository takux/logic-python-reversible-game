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


initial_board = create_board()
