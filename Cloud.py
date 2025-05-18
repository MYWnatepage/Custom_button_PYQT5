# 头文件-----------------------------------------------------------------------------------------------------------------
from PyQt5 import QtCore
from PyQt5.QtGui import QPainter, QBrush, QPainterPath
# 云朵类-----------------------------------------------------------------------------------------------------------------
class Clouds():
    def __init__(self, x, y, radius, color, shift, random_factors):
        # ---------------颜色---------------
        self.color = color
        # ---------------组成圆形---------------
        base_params  =  [
            {"x_coeff": 1.40, "y_coeff": 2.53, "radius_coeff": 0.92},
            {"x_coeff": 1.90, "y_coeff": 2.40, "radius_coeff": 1.05},
            {"x_coeff": 2.79, "y_coeff": 2.13, "radius_coeff": 1.03},
            {"x_coeff": 3.64, "y_coeff": 2.19, "radius_coeff": 0.95},
            {"x_coeff": 4.33, "y_coeff": 1.72, "radius_coeff": 0.75},
            {"x_coeff": 4.97, "y_coeff": 1.37, "radius_coeff": 0.97},
                        ]
        self.clouds = []
        for i in range(6):
            params = base_params[i]                                             # 圆形参数
            rf = random_factors[i]                                              # 随机因子
            x_offset = (rf - 0.5) * 20                                          # 计算随机偏移
            y_offset = (rf - 0.5) * 20                                          # 计算随机偏移
            self.clouds.append({"x": params["x_coeff"] * x + x_offset + shift, "y": params["y_coeff"] * y + shift + y_offset, "radius": params["radius_coeff"] * radius})
# 绘制云朵---------------------------------------------------------------------------------------------------------------
    def build_path(self):
        path = QPainterPath()
        first = True
        for cloud in self.clouds:
            circle_path = QPainterPath()
            circle_path.addEllipse(QtCore.QPointF(cloud["x"], cloud["y"]), cloud["radius"], cloud["radius"])
            path = path.united(circle_path) if not first else circle_path
            first = False
        return path
    def draw_clouds(self, painter):
        path = self.build_path()  # 创建云朵的路径
        painter.setBrush(QBrush(self.color))
        painter.setRenderHint(QPainter.Antialiasing)
        painter.drawPath(path)  # 绘制路径






