import unittest
from XOGameModel import XOGameModel

class test_XOGameModel(unittest.TestCase):
    def setUp(self):
        self.model = XOGameModel(size=5)

    def test_play_move(self):
        """Проверка выполнения хода"""
        self.model.play_move(0, 0)
        self.assertEqual(self.model.board[0][0], 'X')

    def test_check_win_horizontal(self):
        """Проверка победы по горизонтали"""
        self.model.board = [['X', 'X', 'X', 'X', 'X']] + [[''] * 5 for _ in range(4)]
        self.assertTrue(self.model.check_win(0, 4))

    def test_check_win_vertical(self):
        """Проверка победы по вертикали"""
        self.model.board = [['X', '', '', '', '']] + [['X', '', '', '', '']] + [['X', '', '', '', '']] + [['X', '', '', '', '']] + [['X', '', '', '', '']]
        self.assertTrue(self.model.check_win(4, 0))

    def test_check_win_diagonal(self):
        """Проверка победы по диагонали"""
        self.model.board = [['X', '', '', '', '']] + [['', 'X', '', '', '']] + [['', '', 'X', '', '']] + [['', '', '', 'X', '']] + [['', '', '', '', 'X']]
        self.assertTrue(self.model.check_win(4, 4))

if __name__ == "__main__":
    unittest.main()
