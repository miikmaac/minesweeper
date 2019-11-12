import random


class Minesweeper:

    _BOMB = -1
    _PLAYER_LOSES = -1
    _PLAYER_WINS = 1
    _NO_WINNER_YET = 0
    _NEIGHBORS = [[-1, -1], [-1, 0], [-1, 1], [0, 1], [1, 1], [1, 0], [1, -1], [0, -1]]

    def __init__(self, num_rows=10, num_cols=12, num_bombs=6):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.num_bombs = num_bombs
        self.board = [[0 for _ in range(self.num_cols)] for _ in range(self.num_rows)]
        self.facade = [['X' for _ in range(self.num_cols)] for _ in range(self.num_rows)]
        self.num_covered = self.num_rows * self.num_cols
        self.bombs = set()
        self.board_state = self._NO_WINNER_YET
        self.reset_board()

    def _valid_square(self, r, c):
        return 0 <= r < self.num_rows and 0 <= c < self.num_cols

    def _init_bomb(self, bomb_r, bomb_c):
        self.board[bomb_r][bomb_c] = self._BOMB

        for r, c in self._NEIGHBORS:
            neighbor_r = bomb_r + r
            neighbor_c = bomb_c + c
            if self._valid_square(neighbor_r, neighbor_c) and self.board[neighbor_r][neighbor_c] != self._BOMB:
                self.board[neighbor_r][neighbor_c] += 1

    def reset_board(self):
        # get random bomb positions and place them in the board
        # save the set of bomb positions for 0(1) checking if the user has lost the game at each play
        for i in range(self.num_bombs):
            r = random.randint(0, self.num_rows - 1) # adjusting for 0 based indexing, the stop value is inclusive
            c = random.randint(0, self.num_cols - 1) # adjusting for 0 based indexing, the stop value is inclusive
            if (r, c) in self.bombs:
                i -= 1
            else:
                self.bombs.add((r, c))

        for (bomb_r, bomb_c) in self.bombs:
            self._init_bomb(bomb_r, bomb_c)

    def print_board(self):
        for row in range(self.num_rows):
            col_rep = ' '.join(self.facade[row])
            print(col_rep)

    def _update_board(self, r, c, visited):
        if (r, c) in visited:
            return

        visited.add((r, c))
        self.facade[r][c] = str(self.board[r][c])

        if (r, c) in self.bombs:
            self.board_state = self._PLAYER_LOSES
            return

        self.num_covered -= 1

        if self.num_covered == self.num_bombs:
            self.board_state = self._PLAYER_WINS
            return

        if self.board[r][c] == 0:
            for next_r, next_c in self._NEIGHBORS:
                neighbor_r = r + next_r
                neighbor_c = c + next_c
                if self._valid_square(neighbor_r, neighbor_c):
                    self._update_board(neighbor_r, neighbor_c, visited)

    def update_board(self, r, c):
        self._update_board(r, c, set())

    def get_board_state(self):
        return self.board_state


if __name__ == '__main__':
    start_game = True
    while start_game:
        print('Starting MINESWEEPER')
        ms = Minesweeper()
        ms.print_board()
        while ms.get_board_state() == 0:
            print('Please enter a move: (r, c) ')
            [r, c] = input().split(',')
            ms.update_board(int(r), int(c))
            print('Thanks for playing! Heres the updated board: ')
            ms.print_board()

        if ms.get_board_state() == -1:
            print('Sorry, you lost! Try again? (\'y\'/\'n\') ')

        else:
            print('Congratulations! Play again? (\'y\'/\'n\') ')

        start_game = True if str(input()) == 'y' else False
