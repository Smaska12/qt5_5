from PyQt5.QtWidgets import QMainWindow, QMessageBox, QPushButton, QLabel
from PyQt5.QtCore import QTimer, Qt
from pl import Ui_MainWindow
from PyQt5.QtCore import pyqtSlot
from XOGameModel import XOGameModel
import csv, os
from datetime import datetime

class XOGameWidget(QMainWindow):
    def __init__(self, model, settings):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.model = model
        self.settings = settings
        self.buttons = []

        self.timer_x = 60
        self.timer_o = 60
        self.timer_running = False
        self.current_timer = None
        self.game_active = False

        self.initUI()

    def initUI(self):
        size = self.settings.get("size", 5)

        for row in self.buttons:
            for button in row:
                button.deleteLater()

        self.buttons = []
        for i in range(size):
            row_buttons = []
            for j in range(size):
                button_index = i * size + j + 1
                button_name = f"pushButton_{button_index}"
                button = QPushButton(self)
                button.setFixedSize(50, 50)
                button.setText("")
                button.clicked.connect(self.onGameButtonClicked)
                row_buttons.append(button)
                self.ui.gridLayout.addWidget(button, i, j)
            self.buttons.append(row_buttons)

        self.model = XOGameModel(size=size)

        self.start_button = QPushButton("Старт", self)
        self.start_button.setFixedSize(100, 40)
        self.start_button.clicked.connect(self.start_game)
        self.ui.gridLayout.addWidget(self.start_button, size, 0, 1, size, alignment=Qt.AlignHCenter)

        self.timer_label = QLabel(f"X: {self.timer_x}s/60s | O: {self.timer_o}s/60s", self)
        self.timer_label.setStyleSheet("padding: 5px; font-size: 14px; text-align: center;")
        self.ui.gridLayout.addWidget(self.timer_label, size + 1, 0, 1, size, alignment=Qt.AlignHCenter)

        self.update_ui()

        self.ui.gridLayout.addWidget(self.ui.lineEdit, size + 2, 0, 1, size, alignment=Qt.AlignHCenter)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)

    def start_game(self):
        self.model.reset()
        self.game_active = True
        self.start_button.setEnabled(False)
        self.timer.start(1000)  # Запуск таймера
        self.timer_label.setText(f"X: {self.model.timer_x}s/60s | O: {self.model.timer_o}s/60s")
        self.ui.lineEdit.setText("")
        self.update_ui()

    def update_time(self):
        result = self.model.update_timer()
        if result:
            self.show_winner(result)
            return

        self.timer_label.setText(f"X: {self.model.timer_x}s/60s | O: {self.model.timer_o}s/60s")

    def onGameButtonClicked(self):
        if not self.game_active:
            return

        if self.model.game_over:
            return

        button = self.sender()
        row, col = self.get_button_position(button)
        result = self.model.play_move(row, col)

        self.update_ui()

        if result:
            self.show_winner(result)


    def get_button_position(self, button):
        for i in range(self.model.size):
            for j in range(self.model.size):
                if self.buttons[i][j] == button:
                    return i, j
        return -1, -1

    def update_ui(self):
        for i in range(self.model.size):
            for j in range(self.model.size):
                button = self.buttons[i][j]
                button.setText(self.model.board[i][j])
                button.setEnabled(self.model.board[i][j] == '' and not self.model.game_over)


    def show_winner(self, result):
        self.ui.lineEdit.setText(result)

        for i in range(self.model.size):
            for j in range(self.model.size):
                self.buttons[i][j].setEnabled(False)

        self.timer.stop()
        self.game_active = False


        winner = "Draw" if "draw" in result.lower() else result.split()[1]
        self.save_game_result(winner, "Win" if winner != "Draw" else "Draw")

    def save_game_result(self, player, result):
        if not os.path.exists(self.settings["path"]):
            with open(self.settings["path"], "w") as f:
                f.write("Date,Player,Result\n")

        with open(self.settings["path"], "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), player, result])
