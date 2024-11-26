from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLineEdit, QMainWindow, QMessageBox
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
from settings import Ui_MainWindow
import json
import os

class SettingsWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.save_settings)

    def save_settings(self):
        path = self.ui.lineEdit_2.text().strip()
        fields_count = self.ui.lineEdit.text().strip()

        if not path and not fields_count:
            QMessageBox.warning(self, "Ошибка", "Оба поля не могут быть пустыми. Заполните хотя бы одно из них.")
            return

        if not path:
            path = "default_results.csv"

        if not os.path.exists(path):
            if path == "default_results.csv":
                with open(path, "w") as f:
                    f.write("Date,Player,Result\n")
            else:
                QMessageBox.warning(self, "Ошибка", f"Указанный путь '{path}' не существует!")
                return

        if not fields_count:
            size = 5
        elif fields_count.isdigit() and 10 <= int(fields_count) <= 20 or int(fields_count) == 5:
            size = int(fields_count)
        else:
            QMessageBox.warning(self, "Ошибка", "Поле \"Количество полей\" должно быть пустым или числом в диапазоне от 10 до 20!")
            return

        settings = {
            "path": path,
            "size": size
        }

        with open("settings.json", "w") as f:
            json.dump(settings, f)

        QMessageBox.information(self, "Успешно", "Настройки сохранены!")
        self.close()
