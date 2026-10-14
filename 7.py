import sys
import os
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt6.QtCore import QUrl
from PyQt6.QtMultimedia import QSoundEffect


class MainWindow(QMainWindow):
    NOTE_FILES = {
        "C": "sounds/C.wav",
        "D": "sounds/D.wav",
        "E": "sounds/E.wav",
        "F": "sounds/F.wav",
        "G": "sounds/G.wav",
        "A": "sounds/A.wav",
        "B": "sounds/B.wav",
    }

    def __init__(self):
        super().__init__()
        uic.loadUi("task7.ui", self)
        self.effects = {}
        self._load_sounds()

        self.btnC.clicked.connect(lambda: self.play("C"))
        self.btnD.clicked.connect(lambda: self.play("D"))
        self.btnE.clicked.connect(lambda: self.play("E"))
        self.btnF.clicked.connect(lambda: self.play("F"))
        self.btnG.clicked.connect(lambda: self.play("G"))
        self.btnA.clicked.connect(lambda: self.play("A"))
        self.btnB.clicked.connect(lambda: self.play("B"))

    def _load_sounds(self):
        for note, path in self.NOTE_FILES.items():
            if not os.path.exists(path):
                continue
            eff = QSoundEffect()
            eff.setSource(QUrl.fromLocalFile(os.path.abspath(path)))
            eff.setVolume(0.9)
            self.effects[note] = eff

    def play(self, note):
        eff = self.effects.get(note)
        if eff is None:
            QMessageBox.warning(
                self, "Нет звука",
                f"Файл для ноты «{note}» не найден.\n"
                f"Поместите WAV-файлы в папку sounds/."
            )
            return
        eff.play()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
