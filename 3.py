import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("task3.ui", self)
        self.original = None
        self.channel = "all"
        self.rotation = 0

        self.btnRed.clicked.connect(lambda: self.set_channel("r"))
        self.btnGreen.clicked.connect(lambda: self.set_channel("g"))
        self.btnBlue.clicked.connect(lambda: self.set_channel("b"))
        self.btnAll.clicked.connect(lambda: self.set_channel("all"))
        self.btnLeft.clicked.connect(lambda: self.rotate(-90))
        self.btnRight.clicked.connect(lambda: self.rotate(90))

        # диалог выбора изображения при старте
        path, _ = QFileDialog.getOpenFileName(
            self, "Открыть изображение", "",
            "Изображения (*.png *.jpg *.jpeg *.bmp)"
        )
        if path:
            self.load_image(path)

    def load_image(self, path):
        img = QImage(path)
        if img.isNull():
            QMessageBox.critical(self, "Ошибка", "Не удалось открыть изображение")
            return
        self.original = img
        self.rotation = 0
        self.channel = "all"
        self.update_view()

    def set_channel(self, ch):
        self.channel = ch
        self.update_view()

    def rotate(self, angle):
        self.rotation = (self.rotation + angle) % 360
        self.update_view()

    def update_view(self):
        if self.original is None:
            return
        img = self.original.convertToFormat(QImage.Format.Format_ARGB32)

        if self.channel != "all":
            for y in range(img.height()):
                for x in range(img.width()):
                    c = img.pixelColor(x, y)
                    r, g, b = c.red(), c.green(), c.blue()
                    if self.channel == "r":
                        img.setPixelColor(x, y, c.fromRgb(r, 0, 0))
                    elif self.channel == "g":
                        img.setPixelColor(x, y, c.fromRgb(0, g, 0))
                    elif self.channel == "b":
                        img.setPixelColor(x, y, c.fromRgb(0, 0, b))

        if self.rotation == 90:
            img = img.transformed(
                __import__("PyQt6.QtGui", fromlist=["QTransform"]).QTransform().rotate(90)
            )
        elif self.rotation == 180:
            from PyQt6.QtGui import QTransform
            img = img.transformed(QTransform().rotate(180))
        elif self.rotation == 270:
            from PyQt6.QtGui import QTransform
            img = img.transformed(QTransform().rotate(270))

        pix = QPixmap.fromImage(img)
        self.imageLabel.setPixmap(
            pix.scaled(self.imageLabel.size(),
                       Qt.AspectRatioMode.KeepAspectRatio,
                       Qt.TransformationMode.SmoothTransformation)
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
