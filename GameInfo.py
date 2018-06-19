from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt, pyqtSlot
from main.GameBoard import GameBoard
from PyQt5.QtGui import QFont
from main.HoverButton import HoverButton


class GameInfo(QWidget):

    def __init__(self):
        super().__init__()
        super().setFixedHeight(800)
        super().setFixedWidth(660)
        button = HoverButton('Play', 220, 100)
        font = QFont("Arial", 40)
        font.setBold(True)
        button.setFont(font)
        button.setStyleSheet('text-align: center; background: transparent; color: Tan')
        button.clicked.connect(self.start_game)

        turn = QLabel("")
        turn.setFixedSize(340, 100)
        font = QFont('Arial', 30)
        font.setBold(True)
        turn.setObjectName("turn")
        turn.setStyleSheet('background: transparent; color: Tan')
        turn.setFont(font)

        self.layout = QHBoxLayout(self)
        self.layout.setSpacing(65)
        self.layout.setContentsMargins(140, 0, 0, 40)  # left, top, right, bottom
        self.layout.addWidget(button, 0, Qt.AlignBottom)
        self.layout.addWidget(turn, 0, Qt.AlignBottom)

    @pyqtSlot()
    def start_game(self):
        button = self.sender()
        board = self.window().findChild(GameBoard, "gameBoard")
        board.game_enabled = True
        if button.label.text() == 'Play':
            board.enable_all_mini_boards()
            button.label.setText('Restart')
            font = QFont('Arial', 30)
            font.setBold(True)
            button.label.setFont(font)
            turn = self.findChild(QLabel, "turn")
            symbol = board.players[board.turn]
            turn.setText("Play %s!" % symbol)
        else:
            board.restart_game()






