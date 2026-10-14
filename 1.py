import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("task1.ui", self)
        self.stats = None
        self.btnLoad.clicked.connect(self.load_file)
        self.btnSave.clicked.connect(self.save_file)

    def load_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Открыть файл", "", "Текстовые файлы (*.txt)"
        )
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            tokens = content.split()
            if not tokens:
                raise ValueError("Файл пуст")
            numbers = [int(t) for t in tokens]
        except (ValueError, OSError) as e:
            QMessageBox.critical(
                self, "Ошибка",
                f"Неверный формат данных:\n{e}"
            )
            return

        mx, mn = max(numbers), min(numbers)
        avg = sum(numbers) / len(numbers)
        self.stats = (mx, mn, avg)
        self.lblMax.setText(f"Максимум: {mx}")
        self.lblMin.setText(f"Минимум: {mn}")
        self.lblAvg.setText(f"Среднее: {avg:.4f}")

    def save_file(self):
        if self.stats is None:
            QMessageBox.warning(self, "Внимание", "Сначала загрузите файл")
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Сохранить файл", "", "Текстовые файлы (*.txt)"
        )
        if not path:
            return
        mx, mn, avg = self.stats
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(f"Максимум: {mx}\n")
                f.write(f"Минимум: {mn}\n")
                f.write(f"Среднее: {avg:.4f}\n")
        except OSError as e:
            QMessageBox.critical(self, "Ошибка", str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
