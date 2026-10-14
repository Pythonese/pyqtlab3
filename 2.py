import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("task2.ui", self)

        self.current_path = None
        self.dirty = False

        # подключаем действия меню
        self.actionNew.triggered.connect(self.new_file)
        self.actionOpen.triggered.connect(self.open_file)
        self.actionSave.triggered.connect(self.save_file)
        self.actionSaveAs.triggered.connect(self.save_file_as)

        # отслеживаем изменения текста
        self.textEdit.textChanged.connect(self._on_change)

    # ---------- служебные ----------
    def _on_change(self):
        if not self.dirty:
            self.dirty = True
            self._update_title()

    def _update_title(self):
        name = self.current_path if self.current_path else "Без имени"
        star = " *" if self.dirty else ""
        self.setWindowTitle(f"Редактор — {name}{star}")

    def _maybe_save(self) -> bool:
        """Спросить у пользователя, сохранять ли изменения.
        Возвращает False, если пользователь отменил действие."""
        if not self.dirty:
            return True
        res = QMessageBox.question(
            self, "Сохранение",
            "Документ был изменён. Сохранить изменения?",
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No |
            QMessageBox.StandardButton.Cancel
        )
        if res == QMessageBox.StandardButton.Yes:
            return self.save_file()
        if res == QMessageBox.StandardButton.Cancel:
            return False
        return True  # No — продолжать без сохранения

    # ---------- действия ----------
    def new_file(self):
        if not self._maybe_save():
            return
        self.textEdit.clear()
        self.current_path = None
        self.dirty = False
        self._update_title()

    def open_file(self):
        if not self._maybe_save():
            return
        path, _ = QFileDialog.getOpenFileName(
            self, "Открыть файл", "",
            "Текстовые файлы (*.txt);;Все файлы (*)"
        )
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
        except OSError as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось открыть файл:\n{e}")
            return

        # блокируем сигнал, чтобы открытие не помечало документ как изменённый
        self.textEdit.blockSignals(True)
        self.textEdit.setPlainText(text)
        self.textEdit.blockSignals(False)

        self.current_path = path
        self.dirty = False
        self._update_title()

    def save_file(self) -> bool:
        if self.current_path is None:
            return self.save_file_as()
        try:
            with open(self.current_path, "w", encoding="utf-8") as f:
                f.write(self.textEdit.toPlainText())
        except OSError as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить файл:\n{e}")
            return False
        self.dirty = False
        self._update_title()
        return True

    def save_file_as(self) -> bool:
        path, _ = QFileDialog.getSaveFileName(
            self, "Сохранить как", "",
            "Текстовые файлы (*.txt);;Все файлы (*)"
        )
        if not path:
            return False
        self.current_path = path
        return self.save_file()

    # ---------- закрытие окна ----------
    def closeEvent(self, event):
        if self._maybe_save():
            event.accept()
        else:
            event.ignore()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
