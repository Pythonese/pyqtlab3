import sys
import random
from PyQt6 import uic
from PyQt6.QtWidgets import (QApplication, QMainWindow, QInputDialog)
from PyQt6.QtGui import QPixmap, QPainter, QColor
from PyQt6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("task5.ui", self)
        self.btnGenerate.clicked.connect(self.generate_flag)

    def generate_flag(self):
        n, ok = QInputDialog.getInt(
            self, "Количество цветов",
            "Введите число полос (2–10):", 5, 2, 10
        )
        if not ok:
            return

        w, h = 400, 300
        pix = QPixmap(w, h)
        pix.fill(Qt.GlobalColor.white)
        painter = QPainter(pix)
        stripe_h = h / n
        for i in range(n):
            color = QColor(
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255)
            )
            painter.fillRect(
                0, int(i * stripe_h), w, int(stripe_h) + 1, color
            )
        painter.end()
        self.flagLabel.setPixmap(pix)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
