# ---------------头文件---------------
import random
import sys
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QBrush, QColor, QPainterPath
from PyQt5.QtCore import Qt
# ---------------绘制阴影---------------
class Shadows():
    def __init__(self, x, y, radius, color1, color2, color3):
        # ---------------坐标---------------
        self.x = x
        self.y = y
        # ---------------半径---------------
        self.radius = radius
        # ---------------颜色---------------
        self.color1 = color1
        self.color2 = color2
        self.color3 = color3
        # ---------------组成---------------
        self.circle = [
            {"x": 1 * self.x, "y": self.y, "radius": 1.25 * self.radius, "color": self.color1},
            {"x": 1 * self.x, "y": self.y, "radius": 1.75 * self.radius, "color": self.color2},
            {"x": 1 * self.x, "y": self.y, "radius": 2.25 * self.radius, "color": self.color3},

        ]
    def draw_shadow(self, painter):
        for shadow in self.circle:
            path = QPainterPath()
            path.addEllipse(QtCore.QPointF(shadow["x"], shadow["y"]), shadow["radius"], shadow["radius"])
            brush = QBrush(QColor(shadow["color"]))
            painter.setBrush(brush)
            painter.setPen(Qt.NoPen)
            painter.drawPath(path)



