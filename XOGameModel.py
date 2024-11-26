class XOGameModel:
    def __init__(self, size=5):
        self.size = size
        self.board = [['' for _ in range(size)] for _ in range(size)]
        self.current_player = 'X'
        self.game_over = False
        self.timer_x = 60
        self.timer_o = 60
        self.winner = None

    def play_move(self, row, col):
        if self.game_over:
            return None

        if self.board[row][col] == '':
            self.board[row][col] = self.current_player
            if self.check_win(row, col):
                self.game_over = True
                self.winner = self.current_player
                return f"Player {self.current_player} wins!"
            elif self.is_draw():
                self.game_over = True
                self.winner = "Draw"
                return "It's a draw!"
            else:
                self.switch_player()
        return None

    def check_win(self, row, col):
        return (self.check_line(row, col, 0, 1) or  # Horizontal
                self.check_line(row, col, 1, 0) or  # Vertical
                self.check_line(row, col, 1, 1) or  # Diagonal \
                self.check_line(row, col, 1, -1))   # Diagonal /

    def check_line(self, row, col, d_row, d_col):
        count = 0
        win_length = 5 if self.size >= 5 else self.size

        for i in range(-win_length + 1, win_length):
            r, c = row + i * d_row, col + i * d_col
            if 0 <= r < self.size and 0 <= c < self.size and self.board[r][c] == self.current_player:
                count += 1
                if count == win_length:
                    return True
            else:
                count = 0
        return False

    def is_draw(self):
        all_filled = all(cell != '' for row in self.board for cell in row)
        return all_filled and not any(
            self.check_win(row, col)
            for row in range(self.size)
            for col in range(self.size)
        )

    def switch_player(self):
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def update_timer(self):
        if self.current_player == 'X':
            self.timer_x -= 1
            if self.timer_x <= 0:
                self.game_over = True
                self.winner = 'O'
                return "O win"
        elif self.current_player == 'O':
            self.timer_o -= 1
            if self.timer_o <= 0:
                self.game_over = True
                self.winner = 'X'
                return "X win"
        return None

    def reset(self):
        self.__init__(self.size)
