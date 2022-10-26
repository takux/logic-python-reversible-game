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


class Player():
    def __init__(self, name, is_random=True):
        self.name = name
        self.is_random = is_random


class Cell():
    def __init__(self, r, c, state=EMPTY):
        self.r = r
        self.c = c
        self.state = state
        self.reversible_cells = []


class Direction():
    def __init__(self, base_cell, target_cell):
        self.r_dir = target_cell.r - base_cell.r
        self.c_dir = target_cell.c - base_cell.c


class Board():
    def __init__(self):
        self.board = self.create_board()

    def create_board(self):
        """Create initial board."""
        board = []
        for r in range(8):
            board.append([])
            for c in range(8):
                cell = Cell(r, c)
                if r == 3 and c == 3:
                    cell.state = LIGHT
                elif r == 3 and c == 4:
                    cell.state = DARK
                elif r == 4 and c == 3:
                    cell.state = DARK
                elif r == 4 and c == 4:
                    cell.state = LIGHT
                board[r].append(cell)
        return board

    def display_board(self):
        """Display boards using Pandas."""
        df = pd.DataFrame(self.board)
        df = df.applymap(lambda v: v.state)
        df = df.replace(EMPTY, STATE_COLORS[EMPTY])
        df = df.replace(LIGHT, STATE_COLORS[LIGHT])
        df = df.replace(DARK, STATE_COLORS[DARK])
        df = df.replace(AVAILABLE, STATE_COLORS[AVAILABLE])
        display(df)


class GameManager(Board):
    def __init__(self):
        super().__init__()
        self.turn = 1
        self.current_turn = LIGHT
        self.is_game_over = False
        self.is_passed = False
        self.is_passed_previous = False
        self.count_state = [0, 0, 0, 0]  # EMPTY, LIGHT, DARK, AVAILABLE
        self.players = {
            LIGHT: Player("A"),
            DARK: Player("B"),
        }

    def get_surrounding_cells(self, base_cell):
        """Get the surrounding cells from the base cell."""
        start_r = base_cell.r - 1
        start_c = base_cell.c - 1
        end_r = base_cell.r + 1
        end_c = base_cell.c + 1
        surrounding_cells = []
        for r in range(start_r, end_r+1):
            for c in range(start_c, end_c+1):
                if not (-1 < r < 8) or not (-1 < c < 8):
                    continue
                if r == base_cell.r and c == base_cell.c:
                    continue
                surrounding_cells.append(self.board[r][c])
        return surrounding_cells

    def get_reversible_cells_in_one_dir(self, base_cell, dirs):
        """Get all reversible cells in one direction."""
        reversible_cells_in_one_dir = []
        next_r = base_cell.r
        next_c = base_cell.c
        while True:
            next_r += dirs.r_dir
            next_c += dirs.c_dir
            if not (-1 < next_r < 8) or not (-1 < next_c < 8):
                break
            if self.board[next_r][next_c].state == EMPTY or self.board[next_r][next_c].state == AVAILABLE:
                break
            if self.board[next_r][next_c].state == self.current_turn:
                reversible_cells_in_one_dir.append(self.board[next_r][next_c])
                break
            if self.board[next_r][next_c].state != self.current_turn:
                reversible_cells_in_one_dir.append(self.board[next_r][next_c])

        if len(reversible_cells_in_one_dir) > 0:
            if reversible_cells_in_one_dir[-1].state == self.current_turn:
                reversible_cells_in_one_dir.pop()
            else:
                reversible_cells_in_one_dir.clear()
        return reversible_cells_in_one_dir

    def get_reversible_cells(self, base_cell):
        """Get all reversible cells in all directions."""
        reversible_cells = []
        surrounding_cells = self.get_surrounding_cells(base_cell)
        for cell in surrounding_cells:
            dirs = Direction(base_cell, cell)
            reversible_cells_in_one_dir = self.get_reversible_cells_in_one_dir(
                base_cell, dirs)
            reversible_cells.extend(reversible_cells_in_one_dir)
        return reversible_cells

    def refresh_board(self):
        """Refresh board."""
        self.count_state = [0, 0, 0, 0]
        self.is_passed = True
        for r in range(8):
            for c in range(8):
                self.board[r][c].reversible_cells = []
                if self.board[r][c].state == AVAILABLE:
                    self.board[r][c].state = EMPTY
                if self.board[r][c].state == EMPTY:
                    self.board[r][c].reversible_cells = self.get_reversible_cells(
                        self.board[r][c])
                if len(self.board[r][c].reversible_cells) > 0:
                    self.board[r][c].state = AVAILABLE
                    self.is_passed = False
                self.count_state[self.board[r][c].state] += 1

    def manual_selection(self):
        """Converts user input to integer indices."""
        while True:
            selection = input("Select a cell (e.g r0 c4 => 04): ")
            if len(selection) != 2:
                raise Exception("The number of characters is limited to 2.")
            r = int(selection[0])
            c = int(selection[1])
            if self.board[r][c].state == AVAILABLE:
                return r, c

    def automatic_selection(self):
        """Selects a cell automatically."""
        while True:
            r = random.randint(0, 7)
            c = random.randint(0, 7)
            if self.board[r][c].state == AVAILABLE:
                return r, c

    def play_game(self):
        """Run the game with all codes."""
        self.players[LIGHT].is_random = True
        self.players[DARK].is_random = True

        while True:
            self.is_passed_previous = self.is_passed
            self.is_passed = False
            if self.turn % 2 == 0:
                self.current_turn = DARK
            else:
                self.current_turn = LIGHT

            self.refresh_board()

            print("""\
        -----------------------------------
        {} TURN {} [{}　: {} {}　: {}] 
        -----------------------------------""".format(
                STATE_COLORS[self.current_turn],
                self.turn,
                STATE_COLORS[LIGHT],
                self.count_state[LIGHT],
                STATE_COLORS[DARK],
                self.count_state[DARK],
            ))

            self.display_board()

            if self.is_passed:
                if self.count_state[LIGHT] + self.count_state[DARK] >= 64:
                    self.is_game_over = True
                    print('\n 合計数が64になったので終了します。')
                    break
                elif self.is_passed_previous:
                    self.is_game_over = True
                    print('\n 2回連続でパスなので終了します。')
                    break
                else:
                    print('\n 置ける場所がないのでパスします。')
                    self.turn += 1
                    continue

            if self.players[self.current_turn].is_random:
                selected_r, selected_c = self.automatic_selection()
            else:
                selected_r, selected_c = self.manual_selection()

            self.board[selected_r][selected_c].state = self.current_turn
            for cell in self.board[selected_r][selected_c].reversible_cells:
                cell.state = self.current_turn

            self.turn += 1

        if self.count_state[LIGHT] > self.count_state[DARK]:
            print(f'\n WINNER: {STATE_COLORS[LIGHT]}')
        elif self.count_state[LIGHT] < self.count_state[DARK]:
            print(f'\n WINNER: {STATE_COLORS[DARK]}')
        else:
            print('\n DRAW')
