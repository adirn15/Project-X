from main.GameBoard import GameBoard
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QHBoxLayout, QApplication
from main.GameInfo import GameInfo
import sys


class App(QDialog):
    def __init__(self):
        super().__init__()
        self.setObjectName("app")
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Super Tic Tac Toe')
        self.setFixedSize(1920, 970)
        self.move(-10, 0)
        window_layout = QHBoxLayout()
        game_info = GameInfo()
        self.setStyleSheet("background-image: url(resources/background.jpg)")
        window_layout.setSpacing(0)
        window_layout.addWidget(game_info)
        window_layout.addWidget(GameBoard(), 0, Qt.AlignCenter)
        window_layout.setContentsMargins(0, 90, 0, 0)  # left, top, right, bottom
        self.setLayout(window_layout)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec())
