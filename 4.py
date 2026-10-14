import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("task4.ui", self)
        self.img = None
        self.btnOpen.clicked.connect(self.open_image)
        self.sliderAlpha.valueChanged.connect(self.update_alpha)

    def open_image(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Открыть", "",
            "Изображения (*.png *.jpg *.jpeg *.bmp)"
        )
        if not path:
            return
        img = QImage(path)
        if img.isNull():
            QMessageBox.critical(self, "Ошибка", "Не удалось открыть изображение")
            return
        self.img = img.convertToFormat(QImage.Format.Format_ARGB32)
        self.update_alpha()

    def update_alpha(self):
        if self.img is None:
            return
        a = self.sliderAlpha.value()
        self.lblValue.setText(str(a))
        img = self.img.copy()
        for y in range(img.height()):
            for x in range(img.width()):
                c = img.pixelColor(x, y)
                c.setAlpha(a)
                img.setPixelColor(x, y, c)
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
