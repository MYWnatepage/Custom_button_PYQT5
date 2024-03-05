# ---------------头文件---------------
import random
import sys
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QBrush, QColor, QPainterPath, QRadialGradient
from PyQt5.QtCore import Qt, QPoint
# ---------------绘制陨石---------------
class Meteorites():
    def __init__(self, x, y, radius, color1, color2, color3 ):
        # ---------------坐标---------------
        self.x = x
        self.y = y
        # ---------------半径---------------
        self.radius = radius
        # ---------------颜色---------------
        self.color1 = color1
        self.color2 = color2
        self.color3 = color3
        # ---------------Alpha值---------------
        #TODO:没用到
        self.A = 255
        # ---------------组成---------------
        #TODO:这里坐标不知道怎么设置，如果用太大倍率会导致其运动路径延长
        self.point = [
            {"x": 1.02 * self.x - 29, "y": 1.15 * self.y, "radius": 0.35 * self.radius},
            {"x": 0.96 * self.x + 19, "y": 0.53 * self.y, "radius": 0.26 * self.radius},
            {"x": 1.09 * self.x + 26, "y": 1.29 * self.y, "radius": 0.19 * self.radius},
        ]
    def draw_Meteorites(self, painter):
        for i, point in enumerate(self.point):
            radialGradient = QRadialGradient(point["x"], point["y"], point["radius"])
            radialGradient.setColorAt(0, self.color1)
            radialGradient.setColorAt(0.7, self.color2)
            radialGradient.setColorAt(1, self.color3)
            painter.setBrush(radialGradient)
            painter.drawEllipse(QPoint(point["x"], point["y"]), point["radius"], point["radius"])


