# 头文件-----------------------------------------------------------------------------------------------------------------
import random
import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QPropertyAnimation, QParallelAnimationGroup, pyqtProperty, QPoint, QSequentialAnimationGroup
from PyQt5.QtGui import QPainter, QColor
from Cloud import Clouds
from Shadow import Shadows
from Meteorite import Meteorites
from Star import Stars
# 自定义按钮类------------------------------------------------------------------------------------------------------------
#TODO:
# 问题1：拉伸问题 如果尺寸不固定 星星，陨石坑，云层位置都会出现问题
# 问题2：光晕/阴影问题暂无解决思路
class CustomButton(QtWidgets.QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        # ---------------初始大小---------------
        self.resize(525, 210)
        # ---------------状态---------------
        self.state = True
        # ---------------无边框---------------
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint, True)
        # ---------------颜色---------------
        self.sun_color = QtGui.QColor(255, 195, 35)                                                         # 太阳颜色
        self.daytime_bg_color = QtGui.QColor(70, 133, 192)                                                  # 日间背景颜色
        self.moon_color = QtGui.QColor(195, 200, 210)                                                       # 月亮颜色
        self.night_bg_color = QtGui.QColor(25, 30, 50)                                                      # 夜间背景颜色

        self.color_Point =  self.sun_color                                                                  # 当前圆圈颜色
        self.color_Background = self.daytime_bg_color                                                       # 当前背景颜色

        self.color_white = QtGui.QColor(255, 255, 255, 255)                                                 # 云朵颜色
        self.color_grey = QtGui.QColor(164, 195, 227, 100)                                                  # 云朵阴影颜色
        # ---------------透明度-适用于陨石坑---------------
        self.Meteorite_alpha = 0
        # ---------------透明度-适用于星星---------------
        self.Star_alpha = 255
        # ---------------光晕脉动动画---------------
        self.shadow_scale = 1.0
        # ---------------云层偏移量---------------
        self.cloud_shift = 0
        # ---------------星星数量---------------
        self.star_count = 0
        # ---------------星星位置参数---------------
        self.random_star_params = []
        # ---------------随机比例系数---------------
        self.random_Cloud = [random.uniform(0, 1) for _ in range(6)]
        # ---------------边缘差值---------------
        self.edge = 10                                                                                      # 槽和圆圈之间的距离
        # ---------------槽与信号连接---------------
        self.clicked.connect(self.on_clicked)                                                               # 转换信号绑定
        # ---------------半径---------------
        self.radius = self.height() // 2 - self.edge                                                        # 圆圈半径大小
        # ---------------位置---------------
        self.center_point_on = QtCore.QPoint(self.radius + self.edge, self.height() // 2)                   # 初始位置
        self.center_point_off = QtCore.QPoint(self.width() - self.radius - self.edge, self.height() // 2)   # 结束位置
        self.center_point = self.center_point_on                                                            # 当前位置
        # ---------------Point移动动画---------------
        self.pos_animation = QPropertyAnimation(self, b'point_pos')
        self.pos_animation.setDuration(250)
        # ---------------Point颜色动画---------------
        self.color_point_animation = QPropertyAnimation(self, b'point_color')
        self.color_point_animation.setDuration(250)
        # ---------------Background颜色动画---------------
        self.color_Background_animation = QPropertyAnimation(self, b'Background_color')
        self.color_Background_animation.setDuration(250)
        # ---------------陨石坑透明度动画---------------
        self.alpha_animation = QPropertyAnimation(self, b'alpha_value')
        self.alpha_animation.setDuration(250)
        # ---------------云朵飘动动画---------------
        self.cloud_anim_forward = QPropertyAnimation(self, b"cloud_shift")
        self.cloud_anim_forward.setDuration(2500)
        self.cloud_anim_forward.setStartValue(-5)
        self.cloud_anim_forward.setEndValue(5)
        self.cloud_anim_forward.setEasingCurve(QtCore.QEasingCurve.InOutSine)
        self.cloud_anim_backward = QPropertyAnimation(self, b"cloud_shift")
        self.cloud_anim_backward.setDuration(2500)
        self.cloud_anim_backward.setStartValue(5)
        self.cloud_anim_backward.setEndValue(-5)
        self.cloud_anim_backward.setEasingCurve(QtCore.QEasingCurve.InOutSine)
        self.cloud_group = QSequentialAnimationGroup()
        self.cloud_group.addAnimation(self.cloud_anim_forward)
        self.cloud_group.addAnimation(self.cloud_anim_backward)
        self.cloud_group.setLoopCount(-1)
        self.cloud_group.start()
        # ---------------星星呼吸动画---------------
        self.star_anim_forward = QPropertyAnimation(self, b"Star_alpha")
        self.star_anim_forward.setDuration(1500)
        self.star_anim_forward.setStartValue(0)
        self.star_anim_forward.setEndValue(255)
        self.star_anim_backward = QPropertyAnimation(self, b"Star_alpha")
        self.star_anim_backward.setDuration(1500)
        self.star_anim_backward.setStartValue(255)
        self.star_anim_backward.setEndValue(0)
        self.star_group = QSequentialAnimationGroup()
        self.star_group.addAnimation(self.star_anim_forward)
        self.star_group.addAnimation(self.star_anim_backward)
        self.star_group.setLoopCount(-1)
        self.star_group.start()
        # ---------------光晕脉动动画---------------
        self.shadow_anim_forward = QPropertyAnimation(self, b"shadow_scale")
        self.shadow_anim_forward.setDuration(1500)
        self.shadow_anim_forward.setStartValue(0.95)
        self.shadow_anim_forward.setEndValue(1.05)
        self.shadow_anim_forward.setEasingCurve(QtCore.QEasingCurve.InOutSine)
        self.shadow_anim_backward = QPropertyAnimation(self, b"shadow_scale")
        self.shadow_anim_backward.setDuration(1500)
        self.shadow_anim_backward.setStartValue(1.05)
        self.shadow_anim_backward.setEndValue(0.95)
        self.shadow_anim_backward.setEasingCurve(QtCore.QEasingCurve.InOutSine)
        self.shadow_group = QSequentialAnimationGroup()
        self.shadow_group.addAnimation(self.shadow_anim_forward)
        self.shadow_group.addAnimation(self.shadow_anim_backward)
        self.shadow_group.setLoopCount(-1)
        self.shadow_group.start()
        # ---------------并行动画组---------------
        self.animation_group = QParallelAnimationGroup()
        self.animation_group.addAnimation(self.pos_animation)
        self.animation_group.addAnimation(self.color_point_animation)
        self.animation_group.addAnimation(self.color_Background_animation)
        self.animation_group.addAnimation(self.alpha_animation)
        # ---------------显示画面---------------
        self.show()
    def resizeEvent(self, event):                                                                          #--------------------------
        # 递归保护检查
        if hasattr(self, '_resizing') and self._resizing:
            return
        self._resizing = True

        # 获取有效尺寸变化
        old_size = event.oldSize()
        new_size = event.size()

        # 判断是否需要处理（首次显示或真实变化）
        if not old_size.isValid() or new_size.isEmpty():
            return super().resizeEvent(event)

        # 计算目标尺寸
        target_width = new_size.width()
        target_height = int(target_width / 2.5)

        # 当用户垂直拖动时自动修正
        if abs(new_size.height() - old_size.height()) > abs(new_size.width() - old_size.width()):
            target_height = new_size.height()
            target_width = int(target_height * 2.5)

        # 应用尺寸修正
        if (self.width(), self.height()) != (target_width, target_height):
            # 使用阻塞式调整避免闪烁
            self.blockSignals(True)  # 临时阻止信号
            self.resize(target_width, target_height)
            self.blockSignals(False)

            # 异步更新布局参数
            QtCore.QTimer.singleShot(0, self.updateLayoutParams)

        super().resizeEvent(event)
        self._resizing = False
# 更新星星---------------------------------------------------------------------------------------------------------------
    def generate_new_stars_params(self):
        """生成新的星星位置和数量参数"""
        self.safe_area = QtCore.QRect(0, 0, self.width() - (self.radius * 2 + self.edge), self.height())        # 安全区域
        self.star_count = random.randint(4, 7)                                                                  # 生成随机星星数量
        self.random_star_params = []
        max_attempts = 100                                                                                      # 防止无限循环的最大尝试次数
        for _ in range(self.star_count):
            attempts = 0
            while attempts < max_attempts:
                # 生成候选坐标和大小
                x = random.uniform(45, self.safe_area.width()-45)
                y = random.uniform(45, self.safe_area.height()-45)
                size = random.randint(15, 45)                                                                   # 星星尺寸
                collision = False
                for (ex_x, ex_y, ex_size) in self.random_star_params:                                           # 检查与现有星星的碰撞（使用平方比较优化性能）
                    dx = x - ex_x
                    dy = y - ex_y
                    min_distance = size + ex_size
                    if dx * dx + dy * dy < min_distance * min_distance:
                        collision = True
                        break
                if not collision:
                    self.random_star_params.append((x, y, size))
                    break
                attempts += 1
            else:
                self.star_count = len(self.random_star_params)
                break
# 更新尺寸---------------------------------------------------------------------------------------------------------------
    def updateLayoutParams(self):
        """单独更新布局参数的方法"""
        self.radius = self.height() // 2 - self.edge                                                            # 半径大小
        self.center_point_on = QtCore.QPoint(self.radius + self.edge, self.height() // 2)                       # 起始位置
        self.center_point_off = QtCore.QPoint(self.width() - self.radius - self.edge, self.height() // 2)       # 结束位置
        self.center_point = self.center_point_on if self.state else self.center_point_off                       # 当前位置
        self.update()                                                                                           # 更新
# 动画组件---------------------------------------------------------------------------------------------------------------
    @pyqtProperty(QPoint)
    def point_pos(self):
        return self.center_point
    @point_pos.setter
    def point_pos(self, pos):
        self.center_point = pos
        self.update()
    @pyqtProperty(QColor)
    def point_color(self):
        return  self.color_Point
    @point_color.setter
    def point_color(self, color):
        self.color_Point = color
        self.update()
    @pyqtProperty(QColor)
    def Background_color(self):
        return self.color_Background
    @Background_color.setter
    def Background_color(self, color):
        self.color_Background = color
        self.update()
    @pyqtProperty(int)
    def alpha_value(self):
        return self.Meteorite_alpha
    @alpha_value.setter
    def alpha_value(self, value):
        self.Meteorite_alpha = value
        self.update()
    @pyqtProperty(float)
    def cloud_shift(self):
        return self._cloud_shift
    @cloud_shift.setter
    def cloud_shift(self, value):
        self._cloud_shift = value
        self.update()
    @pyqtProperty(int)
    def Star_alpha(self):
        return self._star_alpha
    @Star_alpha.setter
    def Star_alpha(self, value):
        self._star_alpha = value
        self.update()
    @pyqtProperty(float)
    def shadow_scale(self):
        return self._shadow_scale
    @shadow_scale.setter
    def shadow_scale(self, value):
        self._shadow_scale = value
        self.update()
# 点击事件---------------------------------------------------------------------------------------------------------------
    def on_clicked(self):
        self.animation_group.stop()
        if self.state:
            self.pos_animation.setStartValue(self.center_point_on)
            self.pos_animation.setEndValue(self.center_point_off)
            self.color_point_animation.setStartValue(self.sun_color)
            self.color_point_animation.setEndValue(self.moon_color)
            self.color_Background_animation.setStartValue(self.daytime_bg_color)
            self.color_Background_animation.setEndValue(self.night_bg_color)
            self.alpha_animation.setStartValue(0)
            self.alpha_animation.setEndValue(255)
            self.generate_new_stars_params()
        else:
            self.pos_animation.setStartValue(self.center_point_off)
            self.pos_animation.setEndValue(self.center_point_on)
            self.color_point_animation.setStartValue(self.moon_color)
            self.color_point_animation.setEndValue(self.sun_color)
            self.color_Background_animation.setStartValue(self.night_bg_color)
            self.color_Background_animation.setEndValue(self.daytime_bg_color)
            self.alpha_animation.setStartValue(255)
            self.alpha_animation.setEndValue(0)
            self.random_Cloud = [random.uniform(0, 1) for _ in range(6)]
            self.Star_alpha = 0
        self.state = not self.state
        self.animation_group.start()
# 绘制事件---------------------------------------------------------------------------------------------------------------
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        # 抗锯齿---------------------------------------------------------------------------------------------------------
        painter.setRenderHint(QPainter.Antialiasing)
        # 公共剪切路径----------------------------------------------------------------------------------------------------
        rectPath = QtGui.QPainterPath()
        rectPath.addRoundedRect(0, 0, self.width(), self.height(), self.height() // 2, self.height() // 2)
        painter.setClipPath(rectPath)
        painter.setBrush(self.color_Background)
        painter.drawPath(rectPath)
        # 阴影-----------------------------------------------------------------------------------------------------------
        Shadow = Shadows(self.center_point.x(), self.center_point.y(), self.radius * self.shadow_scale)
        Shadow.draw_shadow(painter)
        # 星星-----------------------------------------------------------------------------------------------------------
        if not self.state:
            if self.Star_alpha == 0 :
                self.generate_new_stars_params()
            Star = Stars(self.random_star_params, self.Star_alpha)
            Star.draw_Stars(painter)
        # ---------------绘制太阳/月亮---------------
        painter.setBrush(self.color_Point)
        painter.drawEllipse(self.center_point, self.radius, self.radius)
        # ---------------绘制陨石坑---------------
        Meteorite = Meteorites(self.center_point.x(), self.center_point.y(), self.radius, self.Meteorite_alpha)
        Meteorite.draw_Meteorites(painter)
        # ---------------云朵---------------
        clouds_grey = Clouds(self.center_point.x(), self.center_point.y(), self.radius, self.color_grey, self.cloud_shift-15, self.random_Cloud)
        clouds_grey.draw_clouds(painter)
        clouds_white = Clouds(self.center_point.x(), self.center_point.y(), self.radius, self.color_white, self.cloud_shift+15, self.random_Cloud)
        clouds_white.draw_clouds(painter)
        # ---------------关闭剪切---------------
        painter.setClipping(False)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = CustomButton()
    sys.exit(app.exec_())