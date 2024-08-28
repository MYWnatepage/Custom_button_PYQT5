import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QPropertyAnimation, QParallelAnimationGroup, pyqtProperty, QPoint
from PyQt5.QtGui import QPainter, QColor, QPen


class CustomButton(QtWidgets.QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.state = True

        self.on_color = QtGui.QColor(255, 133, 0)
        self.off_color = QtGui.QColor(55, 55, 67)
        self.on_bg_color = QtGui.QColor(55, 55, 67)
        self.off_bg_color = QtGui.QColor("white")
        self.color_Point =  QtGui.QColor(255, 133, 0)
        self.color_Background = QtGui.QColor(55, 55, 67)
        self.edge = 8
        self.clicked.connect(self.on_clicked)
        self.radius = self.height() // 2 - self.edge
        self.center_point_on = QtCore.QPoint(self.radius + self.edge, self.height() // 2)
        self.center_point_off = QtCore.QPoint(self.width() - self.radius - self.edge, self.height() // 2)
        self.center_point = self.center_point_on
        # ---------------Point移动动画---------------
        self.pos_animation = QPropertyAnimation(self, b'point_pos')
        self.pos_animation.setDuration(250)
        # ---------------Point颜色动画---------------
        self.color_point_animation = QPropertyAnimation(self, b'point_color')
        self.color_point_animation.setDuration(250)
        # ---------------Background颜色动画---------------
        self.color_Background_animation = QPropertyAnimation(self, b'Background_color')
        self.color_Background_animation.setDuration(250)
        self.animation_group = QParallelAnimationGroup()
        self.animation_group.addAnimation(self.pos_animation)
        self.animation_group.addAnimation(self.color_point_animation)
        self.animation_group.addAnimation(self.color_Background_animation)
        self.show()
    def resizeEvent(self, event):
        new_width = event.size().width()
        new_height = event.size().height()
        # 保持 2.5:1 的长宽比
        expected_height = new_width / 2.5
        if new_height != expected_height:
            self.resize(new_width, int(expected_height))
        # 更新半径和中心点位置
        self.radius = self.height() // 2 - self.edge
        self.center_point_on = QtCore.QPoint(self.radius + self.edge, self.height() // 2)
        self.center_point_off = QtCore.QPoint(self.width() - self.radius - self.edge, self.height() // 2)
        self.center_point = self.center_point_on
    @pyqtProperty(QPoint)
    def point_pos(self):
        return self.center_point
    @point_pos.setter
    def point_pos(self, pos):
        self.center_point = pos
        self.update()  # 更新绘图区域
    @pyqtProperty(QColor)
    def point_color(self):
        return  self.color_Point
    @point_color.setter
    def point_color(self, color):
        self.color_Point = color
        self.update()  # 更新绘图区域
    @pyqtProperty(QColor)
    def Background_color(self):
        return self.color_Background
    @Background_color.setter
    def Background_color(self, color):
        self.color_Background = color
        self.update()  # 更新绘图区域
    def on_clicked(self):
        if self.state:
            self.pos_animation.setStartValue(self.center_point_on)
            self.pos_animation.setEndValue(self.center_point_off)
            self.color_point_animation.setStartValue(self.on_color)
            self.color_point_animation.setEndValue(self.off_color)
            self.color_Background_animation.setStartValue(self.on_bg_color)
            self.color_Background_animation.setEndValue(self.off_bg_color)
        else:
            self.pos_animation.setStartValue(self.center_point_off)
            self.pos_animation.setEndValue(self.center_point_on)
            self.color_point_animation.setStartValue(self.off_color)
            self.color_point_animation.setEndValue(self.on_color)
            self.color_Background_animation.setStartValue(self.off_bg_color)
            self.color_Background_animation.setEndValue(self.on_bg_color)
        self.state = not self.state
        # 开始并行动画组
        self.animation_group.start()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(self.color_Background)
        painter.setPen(QtCore.Qt.NoPen)
        rectPath = QtGui.QPainterPath()
        rectPath.addRoundedRect(0, 0, self.width(), self.height(), self.height() // 2, self.height() // 2)
        painter.drawPath(rectPath)
        background_rect = QtCore.QRectF(0, 0, self.width(), self.height())
        # 绘制描边
        painter.setBrush(QtCore.Qt.NoBrush)
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(QColor("white"), 4)
        painter.setPen(pen)
        # 缩小矩形用于描边，以保证描边不会被裁剪
        stroke_rect = background_rect.adjusted(2, 2, -2, -2)
        strokePath = QtGui.QPainterPath()
        strokePath.addRoundedRect(stroke_rect, (stroke_rect.height() / 2) - 2, (stroke_rect.height() / 2) - 2)
        painter.drawPath(strokePath)
        painter.setBrush(self.color_Point)
        painter.setPen(QtCore.Qt.NoPen)  # No border
        painter.drawEllipse(self.center_point, self.radius, self.radius)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = CustomButton()
    sys.exit(app.exec_())