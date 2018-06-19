from PyQt5.QtWidgets import QPushButton, QLabel
from PyQt5.QtGui import QFont


class HoverButton(QPushButton):

    def __init__(self, label, width, height):
        QPushButton.__init__(self)
        super().setFixedSize(width, height)
        self.label = QLabel(label)
        self.label.setFixedSize(width, height)
        self.label.setParent(self)
        font = QFont("Arial", 34)
        font.setBold(True)
        self.label.setFont(font)
        self.setMouseTracking(True)
        self.setStyleSheet('background: transparent; color: Tan')

    def enterEvent(self, event):
        self.label.setStyleSheet('color: cornSilk')

    def leaveEvent(self, event):
        self.label.setStyleSheet('color: Tan')


