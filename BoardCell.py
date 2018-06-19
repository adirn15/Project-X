from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QPushButton, QLabel
from PyQt5.QtGui import QFont
from PyQt5.Qt import Qt


class BoardCell(QPushButton):

    def __init__(self, label):
        QPushButton.__init__(self)
        self.label = QLabel(label)
        self.label.setParent(self)
        self.label.move(self.x()+10, self.y())
        self.setFixedSize(70, 70)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.hide()
        self.played = False
        self.setMouseTracking(True)
        self.label.setFont(QFont('SansSerif', 22))
        self.setStyleSheet('background: transparent; color: black')
        self.clicked.connect(self.cell_chosen)

    def enterEvent(self, event):
        big_board = self.parent().parent()
        if not big_board.game_enabled:
            return
        i = int(self.objectName()[4])
        j = int(self.objectName()[5])
        mini_board = self.parent().mini_grid_layout.itemAtPosition(i, j)
        if mini_board is not None \
                and self.parent().mini_game_winner is None \
                and mini_board.widget().label.text() == ' ':
            self.label.setText(big_board.players[big_board.turn])
            if self.played or not self.parent().isEnabled():
                self.label.setStyleSheet('color: silver')
            else:
                self.label.setStyleSheet('color: black')
            self.label.show()

    def leaveEvent(self, event):
        if not self.played:
            self.label.setText(' ')
            self.label.hide()

    @pyqtSlot()
    def cell_chosen(self):
        self.played = True





