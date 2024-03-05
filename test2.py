#---------------头文件---------------
import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QPropertyAnimation, QParallelAnimationGroup, pyqtProperty, QPoint
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QGraphicsDropShadowEffect

from Cloud import Clouds
from Shadow import Shadows
from Meteorite import Meteorites
#---------------自定义按钮类---------------
#TODO: 目前，星星 光晕阴影,陨石坑透明度没做
class CustomButton(QtWidgets.QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        # ---------------初始大小---------------
        self.resize(525, 210)
        # ---------------状态---------------
        self.state = True
        # ---------------颜色---------------
        self.sun_color = QtGui.QColor(255, 195, 35)
        self.daytime_bg_color = QtGui.QColor(70, 133, 192)
        self.moon_color = QtGui.QColor(195, 200, 210)
        self.night_bg_color = QtGui.QColor(25, 30, 50)
        self.color_Point =  QtGui.QColor(255, 195, 35)
        self.color_Background = QtGui.QColor(70, 133, 192)
        self.color_white = QtGui.QColor(255, 255, 255,255)
        self.color_grey = QtGui.QColor(164, 195, 227,100)
        self.color_circle1 = QtGui.QColor(255, 255, 255, 52)
        self.color_circle2 = QtGui.QColor(255, 255, 255, 26)
        self.color_circle3 = QtGui.QColor(255, 255, 255, 13)
        self.Meteorites_color1 = QColor(150, 160, 180, 255)
        self.Meteorites_color2 = QColor(150, 160, 180, 255)
        self.Meteorites_color3 = QColor(108, 115, 130, 255)
        # ---------------边缘差值---------------
        self.edge = 10
        # ---------------槽与信号连接---------------
        self.clicked.connect(self.on_clicked)
        # ---------------半径---------------
        self.radius = self.height() // 2 - self.edge
        # ---------------位置---------------
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
        # 创建并行动画组，用于同时执行位置动画和颜色动画
        self.animation_group = QParallelAnimationGroup()
        self.animation_group.addAnimation(self.pos_animation)
        self.animation_group.addAnimation(self.color_point_animation)
        self.animation_group.addAnimation(self.color_Background_animation)
        self.show()

    def effect_shadow_style(widget):
        effect_shadow = QGraphicsDropShadowEffect()
        effect_shadow.setOffset(0, 8)  # 设置阴影的偏移
        effect_shadow.setBlurRadius(48)  # 设置阴影的半径
        effect_shadow.setColor(QColor(162, 129, 247))  # 设置阴影的颜色
        widget.setGraphicsEffect(effect_shadow)
    def resizeEvent(self, event):
        new_width = event.size().width()
        new_height = event.size().height()
        # 保持 2:1 的长宽比
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
            self.color_point_animation.setStartValue(self.sun_color)
            self.color_point_animation.setEndValue(self.moon_color)
            self.color_Background_animation.setStartValue(self.daytime_bg_color)
            self.color_Background_animation.setEndValue(self.night_bg_color)
        else:
            self.pos_animation.setStartValue(self.center_point_off)
            self.pos_animation.setEndValue(self.center_point_on)
            self.color_point_animation.setStartValue(self.moon_color)
            self.color_point_animation.setEndValue(self.sun_color)
            self.color_Background_animation.setStartValue(self.night_bg_color)
            self.color_Background_animation.setEndValue(self.daytime_bg_color)
        self.state = not self.state
        # 开始并行动画组
        self.animation_group.start()

    def paintEvent(self, event):
        print(f"长{self.width()}")
        print(f"宽{self.height()}")
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        # ---------------绘制圆角矩形---------------
        painter.setBrush(self.color_Background)
        painter.setPen(QtCore.Qt.NoPen)  # No border
        rectPath = QtGui.QPainterPath()
        rectPath.addRoundedRect(0, 0, self.width(), self.height(), self.height() // 2, self.height() // 2)
        painter.drawPath(rectPath)
        # ---------------阴影---------------
        Shadow = Shadows(self.center_point.x(), self.center_point.y(), self.radius, self.color_circle1,
                         self.color_circle2, self.color_circle3)
        Shadow.draw_shadow(painter)
        # ---------------绘制太阳/月亮---------------
        painter.setBrush(self.color_Point)
        painter.setPen(QtCore.Qt.NoPen)  # No border
        painter.drawEllipse(self.center_point, self.radius, self.radius)
        # ---------------绘制陨石坑---------------
        Meteorite = Meteorites(self.center_point.x(), self.center_point.y(), self.radius, self.Meteorites_color1, self.Meteorites_color2, self.Meteorites_color3)
        Meteorite.draw_Meteorites(painter)
        # ---------------设置剪切区域以仅在圆角矩形内绘制云朵---------------
        painter.setClipPath(rectPath)
        # ---------------云朵---------------
        clouds_grey = Clouds(self.center_point.x(), self.center_point.y(), self.radius, self.color_grey, -15, 1)
        clouds_grey.draw_clouds(painter)
        clouds_white = Clouds(self.center_point.x(), self.center_point.y(), self.radius, self.color_white, 15, 1)
        clouds_white.draw_clouds(painter)
        # ---------------关闭剪切---------------
        painter.setClipping(False)




if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = CustomButton()
    sys.exit(app.exec_())