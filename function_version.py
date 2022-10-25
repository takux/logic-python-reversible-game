# [[0, 0, 0, 0, 0, 0, 0, 0],
#  [0, 0, 0, 0, 0, 0, 0, 0],
#  [0, 0, 0, 0, 0, 0, 0, 0],
#  [0, 0, 0, 1, 2, 0, 0, 0],
#  [0, 0, 0, 2, 1, 0, 0, 0],
#  [0, 0, 0, 0, 0, 0, 0, 0],
#  [0, 0, 0, 0, 0, 0, 0, 0],
#  [0, 0, 0, 0, 0, 0, 0, 0]]


# board (8x8)
board = []

# 8 rows
for r in range(8):
    # print(r)
    board.append([])

    # 8 columns
    for c in range(8):

        # cell
        if r == 3 and c == 3:
            board[r].append(1)
        elif r == 3 and c == 4:
            board[r].append(2)
        elif r == 4 and c == 3:
            board[r].append(2)
        elif r == 4 and c == 4:
            board[r].append(1)
        else:
            board[r].append(0)


board
