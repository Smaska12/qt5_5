from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem
from statistics import Ui_MainWindow
import csv
import sys


class StatsWidget(QMainWindow, Ui_MainWindow):
    def __init__(self, settings):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Статистика")
        self.settings = settings

    def load_game_results(self):
        results = []
        path = self.settings.get("path", "default_results.csv")

        try:
            with open(path, "r") as f:
                reader = csv.reader(f)
                next(reader)
                for row in reader:
                    results.append(row)
        except FileNotFoundError:
            print(f"Файл {path} не найден.")
        except Exception as e:
            print(f"Ошибка при чтении файла: {e}")

        return results



    def update_stats(self, results):
        games = len(results)
        x_wins = sum(1 for result in results if result[1] == 'X' and result[2] == 'Win')
        o_wins = sum(1 for result in results if result[1] == 'O' and result[2] == 'Win')
        draws = sum(1 for result in results if result[2] == 'Draw')

        self.ui.label.setText(f"Всего игр: {games}")
        self.ui.label_2.setText(f"Победы X: {x_wins}")
        self.ui.label_3.setText(f"Победы O: {o_wins}")

        self.ui.tableWidget.setRowCount(0)

        for row_index, row_data in enumerate(results):
            self.ui.tableWidget.insertRow(row_index)
            for col_index, data in enumerate(row_data):
                item = QTableWidgetItem(data)
                self.ui.tableWidget.setItem(row_index, col_index, item)


