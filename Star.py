# ---------------头文件---------------
import random
import sys
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QBrush, QColor, QPainterPath
from PyQt5.QtCore import Qt
# ---------------绘制星星---------------
class Stars():
    def __init__(self, x, y, radius, color1,):
        # ---------------坐标---------------
        self.x = x
        self.y = y
        # ---------------半径---------------
        self.radius = radius
        # ---------------颜色---------------
        self.color1 = color1
        # ---------------组成---------------
        self.circle = [
            {"x": 1 * self.x, "y": self.y, "radius": 1.25 * self.radius, },
            {"x": 1 * self.x, "y": self.y, "radius": 1.75 * self.radius, },
            {"x": 1 * self.x, "y": self.y, "radius": 2.25 * self.radius, },
            {"x": 1 * self.x, "y": self.y, "radius": 2.25 * self.radius, },
            {"x": 1 * self.x, "y": self.y, "radius": 2.25 * self.radius, },
            {"x": 1 * self.x, "y": self.y, "radius": 2.25 * self.radius, },
            {"x": 1 * self.x, "y": self.y, "radius": 2.25 * self.radius, },
            {"x": 1 * self.x, "y": self.y, "radius": 2.25 * self.radius, },
        ]











    def draw_Stars(self, painter):
        for star in self.circle:
            path = QPainterPath()

            path.moveTo(rect.x(), rect.y() + halfside)  # 起点
            path.arcTo(rect.x() - halfside, rect.y() - halfside, side, side, -90, 90)
            path.arcTo(x + halfside, y - halfside, side, side, 180, 90)
            path.arcTo(x + halfside, y + halfside, side, side, 90, 90)
            path.arcTo(x - halfside, y + halfside, side, side, 0, 90)

            return path

        def paintEvent(self, event):
            painter = QPainter(self)
            rect = QRect(50, 50, 300, 300)
            path = self.create_star(rect)
            painter.drawPath(path)

            brush = QBrush(QColor(shadow["color"]))
            painter.setBrush(brush)
            painter.setPen(Qt.NoPen)

            painter.drawPath(path)


    def create_star(self, rect: QRect):
        side = min(rect.width(), rect.height())
        halfside = side / 2
        x = rect.x()
        y = rect.y()





