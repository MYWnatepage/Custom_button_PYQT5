# 头文件-----------------------------------------------------------------------------------------------------------------
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QBrush, QColor, QPainterPath
from PyQt5.QtCore import Qt
# 阴影类-----------------------------------------------------------------------------------------------------------------
class Shadows():
    def __init__(self, x, y, radius):
        # ---------------颜色---------------
        self.color_circle1 = QtGui.QColor(255, 255, 255, 52)  # 内圈光晕颜色
        self.color_circle2 = QtGui.QColor(255, 255, 255, 26)  # 中圈光晕颜色
        self.color_circle3 = QtGui.QColor(255, 255, 255, 13)  # 外圈光晕颜色
        # ---------------组成---------------
        self.circle =   [
            {"x": 1 * x, "y": y, "radius": 1.35 * radius, "color": self.color_circle1},
            {"x": 1 * x, "y": y, "radius": 1.75 * radius, "color": self.color_circle2},
            {"x": 1 * x, "y": y, "radius": 2.25 * radius, "color": self.color_circle3},
                        ]
# 绘制阴影---------------------------------------------------------------------------------------------------------------
    def draw_shadow(self, painter):
        for shadow in self.circle:
            path = QPainterPath()
            path.addEllipse(QtCore.QPointF(shadow["x"], shadow["y"]), shadow["radius"], shadow["radius"])
            brush = QBrush(QColor(shadow["color"]))
            painter.setBrush(brush)
            painter.setPen(Qt.NoPen)
            painter.drawPath(path)



