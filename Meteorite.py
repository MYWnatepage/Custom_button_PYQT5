# 头文件-----------------------------------------------------------------------------------------------------------------
from PyQt5.QtGui import QColor, QRadialGradient
from PyQt5.QtCore import QPoint
# 陨石类-----------------------------------------------------------------------------------------------------------------
class Meteorites():
    def __init__(self, x, y, radius, A):
        # ---------------颜色---------------
        self.Meteorites_color1 = QColor(150, 160, 180, A)
        self.Meteorites_color2 = QColor(150, 160, 180, A)
        self.Meteorites_color3 = QColor(108, 115, 130, A)
        # ---------------组成---------------
        self.point =    [
            {"x": 1.02 * x - 29, "y": 1.15 * y, "radius": 0.35 * radius},
            {"x": 0.96 * x + 19, "y": 0.53 * y, "radius": 0.26 * radius},
            {"x": 1.09 * x + 26, "y": 1.29 * y, "radius": 0.19 * radius},
                        ]
# 绘制陨石---------------------------------------------------------------------------------------------------------------
    def draw_Meteorites(self, painter):
        for i, point in enumerate(self.point):
            radialGradient = QRadialGradient(point["x"], point["y"], point["radius"])
            radialGradient.setColorAt(0, self.Meteorites_color1)
            radialGradient.setColorAt(0.7, self.Meteorites_color2)
            radialGradient.setColorAt(1, self.Meteorites_color3)
            painter.setBrush(radialGradient)
            painter.drawEllipse(QPoint(point["x"], point["y"]), point["radius"], point["radius"])


