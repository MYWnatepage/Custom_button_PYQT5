# ---------------头文件---------------
import random
import sys
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QBrush, QColor, QPainterPath
from PyQt5.QtCore import Qt
# ---------------绘制星星---------------
class Stars():
    def __init__(self, x, y, color1, width, height, randoms):
        # ---------------坐标---------------
        self.x = x
        self.y = y
        # ---------------随机数---------------
        self.random = randoms
        # ---------------形状---------------
        self.width = width
        self.height = height
        # ---------------颜色---------------
        self.color = color1
        #TODO:每次调用到PaintEvent时随机参数self.Rect_Size都会发生改变（会闪烁）
        # ---------------正方形尺寸---------------
        # self.Rect_Size = [random.randint(int(0.12 * min(self.width, self.height)), int(0.36 * min(self.width, self.height))) for _ in range(5)]
        self.Rect_Size =[49, 65, 36, 31, 63]
        # ---------------组成---------------
        self.Rects = [
            {"x": 45, "y": (self.x - self.width/1.5) * 0.578, "size":self.Rect_Size[0]},
            {"x": 200, "y": (self.x - self.width/1.5) * 1.388, "size":self.Rect_Size[1]},
            {"x": 112, "y": (self.x - self.width/1.5) * 0.812, "size":self.Rect_Size[2]},
            {"x": 262, "y": (self.x - self.width/1.5) * 0.689, "size":self.Rect_Size[3]},
            {"x": 70, "y": (self.x - self.width/1.5) * 1.679, "size":self.Rect_Size[4]},
            {"x": 173, "y": (self.x - self.width / 1.5) * 0.286, "size": self.Rect_Size[4]}
        ]
    def draw_Stars(self, painter):
        for Rect in self.Rects:
            path = QPainterPath()
            side = Rect["size"]
            halfside = Rect["size"]/2
            path.moveTo(Rect["x"], Rect["y"] + halfside)  # 起点
            path.arcTo(Rect["x"] - halfside, Rect["y"] - halfside, side, side, -90, 90)
            path.arcTo(Rect["x"] + halfside, Rect["y"] - halfside, side, side, 180, 90)
            path.arcTo(Rect["x"] + halfside, Rect["y"] + halfside, side, side, 90, 90)
            path.arcTo(Rect["x"] - halfside, Rect["y"] + halfside, side, side, 0, 90)
            painter.setBrush(QBrush(self.color))
            painter.setPen(QtCore.Qt.NoPen)  # No border
            painter.setRenderHint(QPainter.Antialiasing)
            painter.drawPath(path)  # 绘制路径









