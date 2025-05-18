# 头文件-----------------------------------------------------------------------------------------------------------------
from PyQt5.QtGui import QPainterPath, QBrush, QColor
# 星星类-----------------------------------------------------------------------------------------------------------------
class Stars:
    def __init__(self, star_params, alpha):
        # ---------------颜色---------------
        self.color = QColor(255, 255, 255, alpha)
        # ---------------转换参数格式为字典列表---------------
        self.Rects = [{"x": x, "y": y, "size": size} for x, y, size in star_params]
# 绘制星星---------------------------------------------------------------------------------------------------------------
    def draw_Stars(self, painter):
        for Rect in self.Rects:
            path = QPainterPath()
            side = Rect["size"]
            halfside = side / 2
            path.moveTo(Rect["x"], Rect["y"] + halfside)
            path.arcTo(Rect["x"] - halfside, Rect["y"] - halfside, side, side, -90, 90)
            path.arcTo(Rect["x"] + halfside, Rect["y"] - halfside, side, side, 180, 90)
            path.arcTo(Rect["x"] + halfside, Rect["y"] + halfside, side, side, 90, 90)
            path.arcTo(Rect["x"] - halfside, Rect["y"] + halfside, side, side, 0, 90)
            painter.setBrush(QBrush(self.color))
            painter.drawPath(path)