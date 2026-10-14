import sys
import math
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt6.QtGui import QPixmap, QPainter, QPen, QColor
from PyQt6.QtCore import Qt


class LSystem:
    def __init__(self, name, sides, axiom, rules):
        self.name = name
        self.sides = sides          # на сколько частей делится плоскость
        self.axiom = axiom
        self.rules = rules          # dict: символ -> строка
        self.angle = 360.0 / sides  # угол поворота

    def expand(self, steps):
        s = self.axiom
        for _ in range(steps):
            s = "".join(self.rules.get(ch, ch) for ch in s)
        return s


def parse_lsystem(path):
    with open(path, "r", encoding="utf-8") as f:
        lines = [ln.rstrip("\n") for ln in f.readlines() if ln.strip() != ""]
    if len(lines) < 4:
        raise ValueError("Недостаточно строк в файле")
    name = lines[0].strip()
    sides = int(lines[1].strip())
    if sides < 2:
        raise ValueError("Число сторон должно быть ≥ 2")
    axiom = lines[2].strip()
    rules = {}
    for line in lines[3:]:
        parts = line.split()
        if len(parts) < 2:
            continue
        rules[parts[0]] = "".join(parts[1:])
    return LSystem(name, sides, axiom, rules)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("task8.ui", self)
        self.lsys = None
        self.sliderStep.valueChanged.connect(self.render)

        path, _ = QFileDialog.getOpenFileName(
            self, "Открыть определение L-системы", "",
            "Текстовые файлы (*.txt)"
        )
        if not path:
            QMessageBox.information(self, "Отмена", "Файл не выбран, выход")
            sys.exit(0)
        try:
            self.lsys = parse_lsystem(path)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Неверный файл: {e}")
            sys.exit(1)

        self.lblName.setText(f"Название: {self.lsys.name}")
        self.sliderStep.setMaximum(7)
        self.sliderStep.setValue(1)
        self.render()

    def render(self):
        if self.lsys is None:
            return
        step = self.sliderStep.value()
        self.lblStep.setText(f"Шаг: {step}")
        s = self.lsys.expand(step)

        size = 700
        pix = QPixmap(size, size)
        pix.fill(Qt.GlobalColor.white)
        p = QPainter(pix)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setPen(QPen(QColor(0, 0, 0), 1))

        # стартовое положение — снизу по центру
        x, y = size / 2, size - 50
        angle = -90.0  # вверх
        length = 6.0 / (1 + 0.15 * step)  # уменьшаем длину при росте шага
        stack = []

        for ch in s:
            if ch == "F" or ch == "G":
                nx = x + length * math.cos(math.radians(angle))
                ny = y + length * math.sin(math.radians(angle))
                p.drawLine(int(x), int(y), int(nx), int(ny))
                x, y = nx, ny
            elif ch == "+":
                angle += self.lsys.angle
            elif ch == "-":
                angle -= self.lsys.angle
            elif ch == "[":
                stack.append((x, y, angle))
            elif ch == "]":
                if stack:
                    x, y, angle = stack.pop()
        p.end()
        self.canvasLabel.setPixmap(pix)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
