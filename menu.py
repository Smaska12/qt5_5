from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout
from xogamewidget import XOGameWidget
from XOGameModel import XOGameModel
from SettingsWidget import SettingsWidget
from StatsWidget import StatsWidget
import json

class Menu(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Меню")
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        play_button = QPushButton("Играть")
        play_button.clicked.connect(self.openGame)
        layout.addWidget(play_button)

        settings_button = QPushButton("Настройки")
        settings_button.clicked.connect(self.openSettings)
        layout.addWidget(settings_button)

        stats_button = QPushButton("Статистика")
        stats_button.clicked.connect(self.openStats)
        layout.addWidget(stats_button)

        self.setLayout(layout)

    def openGame(self):
        settings = self.load_settings()
        model = XOGameModel(size=settings["size"])
        self.game = XOGameWidget(model, settings)
        self.game.show()

    def load_settings(self):
        try:
            with open("settings.json", "r") as f:
                settings = json.load(f)
        except FileNotFoundError:
            settings = {"path": "default_results.csv", "size": 5}
        return settings


    def openSettings(self):
        self.settings = SettingsWidget()
        self.settings.show()

    def openStats(self):
        settings = {"path": "default_results.csv"}
        self.stats = StatsWidget(settings)

        results = self.stats.load_game_results()

        self.stats.update_stats(results)

        self.stats.show()


