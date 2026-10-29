import sys
from pathlib import Path

from PyQt6 import uic
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QApplication, QMainWindow, QListWidgetItem


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        ui_file = Path(__file__).parent / "ui" / "main_window.ui"
        uic.loadUi(str(ui_file), self)

        # Для каждого упражнения храним название, категорию и оборудование.
        self.exercises = [
            ("Тяга верхнего блока", "Спина", "Тренажёр"),
            ("Тяга гантели в наклоне", "Спина", "Гантель"),
            ("Жим штанги лёжа", "Грудь", "Штанга"),
            ("Отжимания", "Грудь", "Собственный вес"),
            ("Приседания", "Ноги", "Собственный вес"),
            ("Жим ногами", "Ноги", "Тренажёр"),
        ]
        self.buttons = [
            self.backButton, self.chestButton, self.legsButton,
            self.rehabButton, self.stretchButton, self.beginnerButton,
        ]
        self.show_all = False

        self.searchEdit.textChanged.connect(self.filter_exercises)
        for button in self.buttons:
            button.clicked.connect(self.filter_exercises)
        self.allExercisesButton.clicked.connect(self.show_all_exercises)
        self.filter_exercises()

    def filter_exercises(self):
        query = self.searchEdit.text().strip().lower().replace("ё", "е")
        category = ""
        for button in self.buttons:
            if button.isChecked():
                category = button.text()

        # Оставляем упражнения, подходящие под категорию и поисковую строку.
        found = []
        for name, group, equipment in self.exercises:
            if category and group != category:
                continue
            text = f"{name} {group} {equipment}".lower().replace("ё", "е")
            if query in text:
                found.append((name, group, equipment))
        if not query and not category and not self.show_all:
            found = found[:2]

        self.exerciseList.clear()
        for name, group, equipment in found:
            item = QListWidgetItem(f"{name}\n{group} · {equipment}")
            item.setSizeHint(QSize(0, 102))
            self.exerciseList.addItem(item)
        self.resultCountLabel.setText(f"Найдено: {len(found)}")
        self.emptyStateLabel.setVisible(len(found) == 0)
        if query:
            self.sectionTitleLabel.setText("Результаты поиска")
            self.emptyStateLabel.setText("Ничего не найдено. Попробуй другое название.")
        elif category:
            self.sectionTitleLabel.setText(f"Упражнения: {category}")
            self.emptyStateLabel.setText("В этой категории пока нет упражнений.")
        elif self.show_all:
            self.sectionTitleLabel.setText("Все упражнения")
        else:
            self.sectionTitleLabel.setText("Популярные упражнения")

    def show_all_exercises(self):
        # Сбрасываем выбранную категорию и поисковую строку.
        self.show_all = True
        for button in self.buttons:
            button.setAutoExclusive(False)
            button.setChecked(False)
            button.setAutoExclusive(True)
        self.searchEdit.clear()
        self.filter_exercises()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
