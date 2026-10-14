import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QColorDialog
from PyQt6.QtGui import QPixmap, QPainter, QColor, QPen, QBrush
from PyQt6.QtCore import Qt, QRect


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("task6.ui", self)
        self.color = QColor(255, 220, 0)
        self.btnColor.clicked.connect(self.choose_color)
        self.sliderScale.valueChanged.connect(self.draw_smile)
        self.draw_smile()

    def choose_color(self):
        c = QColorDialog.getColor(self.color, self, "Выбор цвета")
        if c.isValid():
            self.color = c
            self.draw_smile()

    def draw_smile(self):
        scale = self.sliderScale.value() / 200.0
        size = int(300 * scale)
        size = max(50, min(size, 500))
        pix = QPixmap(size, size)
        pix.fill(Qt.GlobalColor.transparent)
        p = QPainter(pix)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        margin = int(size * 0.05)
        rect = QRect(margin, margin, size - 2 * margin, size - 2 * margin)

        # лицо
        p.setBrush(QBrush(self.color))
        p.setPen(QPen(Qt.GlobalColor.black, max(1, size // 100)))
        p.drawEllipse(rect)

        # глаза
        eye_r = size * 0.06
        eye_y = rect.top() + rect.height() * 0.35
        p.setBrush(QBrush(Qt.GlobalColor.black))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawEllipse(int(rect.left() + rect.width() * 0.32 - eye_r),
                      int(eye_y - eye_r), int(eye_r * 2), int(eye_r * 2))
        p.drawEllipse(int(rect.left() + rect.width() * 0.68 - eye_r),
                      int(eye_y - eye_r), int(eye_r * 2), int(eye_r * 2))

        # улыбка
        pen = QPen(Qt.GlobalColor.black, max(1, size // 60))
        p.setPen(pen)
        p.setBrush(Qt.BrushStyle.NoBrush)
        smile_rect = QRect(
            int(rect.left() + rect.width() * 0.22),
            int(rect.top() + rect.height() * 0.42),
            int(rect.width() * 0.56),
            int(rect.height() * 0.42),
        )
        p.drawArc(smile_rect, 180 * 16, 180 * 16)

        p.end()
        self.smileLabel.setPixmap(pix)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
