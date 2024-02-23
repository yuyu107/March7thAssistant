# coding:utf-8
from PyQt5.QtCore import Qt, QPropertyAnimation
from PyQt5.QtWidgets import QWidget, QFrame, QLabel, QVBoxLayout, QHBoxLayout, QGraphicsOpacityEffect, QAction

from qfluentwidgets import RoundMenu, Action, IconWidget, TextWrap, FlowLayout, CardWidget, Flyout, InfoBarIcon, TeachingTip, TeachingTipTailPosition
from qfluentwidgets import FluentIcon as FIF
from ..common.signal_bus import signalBus
from ..common.style_sheet import StyleSheet
from managers.config_manager import config

from tasks.base.command import start_task
from ..tools.disclaimer import disclaimer

import base64


class SampleCard(CardWidget):
    """ Sample card """

    def __init__(self, icon, title, action, parent=None):
        super().__init__(parent=parent)

        self.action = action

        self.iconWidget = IconWidget(icon, self)
        self.iconOpacityEffect = QGraphicsOpacityEffect(self)
        self.iconOpacityEffect.setOpacity(1)  # 设置初始半透明度
        self.iconWidget.setGraphicsEffect(self.iconOpacityEffect)

        self.titleLabel = QLabel(title, self)
        self.titleLabel.setStyleSheet("font-size: 16px; font-weight: 500;")
        self.titleOpacityEffect = QGraphicsOpacityEffect(self)
        self.titleOpacityEffect.setOpacity(1)  # 设置初始半透明度
        self.titleLabel.setGraphicsEffect(self.titleOpacityEffect)
        # self.contentLabel = QLabel(TextWrap.wrap(content, 45, False)[0], self)

        self.hBoxLayout = QVBoxLayout(self)
        self.vBoxLayout = QVBoxLayout()

        self.setFixedSize(130, 160)
        self.iconWidget.setFixedSize(110, 110)

        # self.hBoxLayout.setSpacing(28)
        # self.hBoxLayout.setContentsMargins(20, 0, 0, 0)
        self.vBoxLayout.setSpacing(2)
        # self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setAlignment(Qt.AlignVCenter)

        self.hBoxLayout.setAlignment(Qt.AlignVCenter)
        self.hBoxLayout.addWidget(self.iconWidget, alignment=Qt.AlignCenter)
        self.hBoxLayout.addLayout(self.vBoxLayout)
        self.vBoxLayout.addStretch(1)
        self.vBoxLayout.addWidget(self.titleLabel, alignment=Qt.AlignCenter)
        # self.vBoxLayout.addWidget(self.contentLabel)
        self.vBoxLayout.addStretch(1)

        self.titleLabel.setObjectName('titleLabel')
        # self.contentLabel.setObjectName('contentLabel')

    def showBottomTeachingTip(self):
        if not config.get_value(base64.b64decode("YXV0b191cGRhdGU=").decode("utf-8")):
            disclaimer(self)
        TeachingTip.create(
            target=self.iconWidget,
            icon=InfoBarIcon.SUCCESS,
            title='启动成功(＾∀＾●)',
            content="",
            isClosable=False,
            tailPosition=TeachingTipTailPosition.BOTTOM,
            duration=2000,
            parent=self
        )

    def createMenu(self, pos):
        menu = RoundMenu(parent=self)

        def create_triggered_function(task):
            def triggered_function():
                self.showBottomTeachingTip()
                start_task(task)
            return triggered_function

        for index, (key, value) in enumerate(self.action.items()):
            menu.addAction(QAction(key, triggered=create_triggered_function(value)))
            if index != len(self.action) - 1:  # 检查是否是最后一个键值对
                menu.addSeparator()

        menu.exec(pos, ani=True)

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)
        if isinstance(self.action, str):
            self.showBottomTeachingTip()
            start_task(self.action)
        elif isinstance(self.action, dict):
            self.createMenu(e.globalPos())

    def enterEvent(self, event):
        super().enterEvent(event)
        self.iconOpacityEffect.setOpacity(0.75)
        self.titleOpacityEffect.setOpacity(0.75)
        self.setCursor(Qt.PointingHandCursor)  # 设置鼠标指针为手形

    def leaveEvent(self, event):
        super().leaveEvent(event)
        self.iconOpacityEffect.setOpacity(1)
        self.titleOpacityEffect.setOpacity(1)
        self.setCursor(Qt.ArrowCursor)  # 恢复鼠标指针的默认形状


class SampleCardView1(QWidget):
    """ Sample card view """

    def __init__(self, title: str, parent=None):
        super().__init__(parent=parent)
        self.titleLabel = QLabel(title, self)
        self.vBoxLayout = QVBoxLayout(self)
        self.flowLayout = FlowLayout()

        self.vBoxLayout.setContentsMargins(20, 0, 20, 0)
        self.vBoxLayout.setSpacing(10)
        self.flowLayout.setContentsMargins(0, 0, 0, 0)
        self.flowLayout.setHorizontalSpacing(12)
        self.flowLayout.setVerticalSpacing(12)

        self.vBoxLayout.addWidget(self.titleLabel)
        self.vBoxLayout.addLayout(self.flowLayout, 1)

        self.titleLabel.setObjectName('viewTitleLabel')
        StyleSheet.SAMPLE_CARD.apply(self)

    def addSampleCard(self, icon, title, action):
        """ add sample card """
        card = SampleCard(icon, title, action, self)
        self.flowLayout.addWidget(card)
