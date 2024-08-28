# ---------------头文件---------------
import random
import sys
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QBrush, QColor, QPainterPath
from PyQt5.QtCore import Qt
# ---------------绘制云朵---------------
class Clouds():
    def __init__(self, x, y, radius, color, shift, random):
        # ---------------坐标---------------
        self.x = x
        self.y = y
        # ---------------随机数---------------
        #TODO:云层飘动的效果可以有但是我不会做 该参数没用到
        self.random = random
        # ---------------半径---------------
        self.radius = radius
        # ---------------颜色---------------
        self.color = color
        # ---------------云层距离---------------
        self.shift = shift
        # ---------------组成圆形---------------
        self.clouds = [
            {"x": 1.30 * x, "y": (2.53 * y + self.shift), "radius": 0.92 * radius},
            {"x": 1.90 * x, "y": (2.40 * y + self.shift), "radius": 1.05 * radius},
            {"x": 2.79 * x, "y": (2.13 * y + self.shift), "radius": 1.03 * radius},
            {"x": 3.64 * x, "y": (2.19 * y + self.shift), "radius": 0.95 * radius},
            {"x": 4.33 * x, "y": (1.72 * y + self.shift), "radius": 0.75 * radius},
            {"x": 4.97 * x, "y": (1.37 * y + self.shift), "radius": 0.97 * radius}
        ]
    # TODO: 这里会吃掉大量的性能，可以优化
    def build_path(self):
        path = QPainterPath()
        first = True
        for cloud in self.clouds:
            circle_path = QPainterPath()
            circle_path.addEllipse(QtCore.QPointF(cloud["x"], cloud["y"]), cloud["radius"], cloud["radius"])
            if first:
                path = circle_path  # 设置第一个圆的路径
                first = False
            else:
                path = path.united(circle_path)  # 合并下一个圆的路径
        return path
    def draw_clouds(self, painter):
        path = self.build_path()  # 创建云朵的路径
        painter.setBrush(QBrush(self.color))
        painter.setPen(QtCore.Qt.NoPen)  # No border
        painter.setRenderHint(QPainter.Antialiasing)
        painter.drawPath(path)  # 绘制路径



