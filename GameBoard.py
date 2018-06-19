from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QGraphicsView, QGraphicsScene, QGraphicsLineItem
from main.MinBoard import MiniBoard
from PyQt5.QtGui import QPen
from main.BoardUtils import *
from PyQt5.QtCore import Qt, QRectF, QLineF
import random


class GameBoard(QWidget):
    game_enabled = False
    final_scores = np.ndarray(shape=(3, 3), dtype=object)

    def __init__(self):
        super().__init__()
        self.final_scores.fill(' ')
        self.setObjectName("gameBoard")
        self.view = None
        self.win_line = None
        self.players = {0: u"\u274C", 1: u"\u2B55"}
        self.turn = random.randint(0, 1)
        self.grid_layout = QGridLayout(self)
        self.grid_layout.setSpacing(0)
        self.grid_layout.setHorizontalSpacing(10)
        self.grid_layout.setVerticalSpacing(10)
        self.setContentsMargins(0, 0, 0, 0)
        for i in range(0, 3):
            for j in range(0, 3):
                cur_board = MiniBoard()
                cur_board.setEnabled(False)
                cur_board.setObjectName('mini%d%d' % (i, j))
                self.grid_layout.addWidget(cur_board, i, j)

    def disable_all_mini_boards(self):
        for i in range(0, 3):
            for j in range(0, 3):
                cell = self.grid_layout.itemAtPosition(i, j)
                if cell is not None:
                    self.grid_layout.itemAtPosition(i, j).widget().setEnabled(False)

    def enable_all_mini_boards(self):
        for i in range(0, 3):
            for j in range(0, 3):
                cell = self.grid_layout.itemAtPosition(i, j)
                if cell is not None and cell.widget().mini_game_winner is None:
                    cell.widget().setEnabled(True)

    def is_game_over(self, symbol):
        p1 = self.players[0]
        p2 = self.players[1]
        win_res = BoardUtils.winner_move(self.final_scores, symbol)
        if win_res is not None:
            return win_res
        tie_res = BoardUtils.is_tie(self.final_scores, p1, p2)
        return tie_res

    def restart_game(self):
        self.final_scores.fill(' ')
        if self.win_line is not None:
            scene = self.view.scene()
            scene.removeItem(self.win_line)

        for i in reversed(range(self.grid_layout.count())):
            item = self.grid_layout.itemAt(i)
            if item is not None:
                item.widget().setParent(None)
        for i in range(0, 3):
            for j in range(0, 3):
                cur_board = MiniBoard()
                cur_board.setEnabled(True)
                cur_board.setObjectName('mini%d%d' % (i, j))
                self.grid_layout.addWidget(cur_board, i, j)
        self.turn = random.randint(0, 1)
        self.window().findChild(QLabel, "turn").setText("Play %s!" % self.players[self.turn])

    def draw_line(self, line_tuple):
        x = self.x()
        y = self.y()
        width = self.width()
        height = self.height()
        scene = QGraphicsScene(QRectF(x, y, width, height))
        self.view = QGraphicsView(self)
        self.view.setStyleSheet('QGraphicsView{background: transparent; border: none}')
        self.view.setFixedSize(width, height)
        self.view.setScene(scene)
        pen = QPen()
        pen.setColor(Qt.black)
        pen.setWidth(26)
        line_coordinates = self.get_line_coordinates(line_tuple)
        line = QLineF(line_coordinates[0], line_coordinates[1], line_coordinates[2], line_coordinates[3])
        self.win_line = QGraphicsLineItem(line)
        scene.addItem(self.win_line)
        self.win_line.setPen(pen)
        self.view.show()

    def get_line_coordinates(self, line_points):
        x = self.x()
        y = self.y()
        height = self.height()
        width = self.width()
        cell1_y = line_points[0] + 1
        cell1_x = line_points[1] + 1
        cell2_y = line_points[2] + 1
        cell2_x = line_points[3] + 1
        if line_points[4] == 'row':
            new_x1 = x + (width/3) * cell1_x - 200
            new_y1 = y + (height/3) * cell1_y - 120
            new_x2 = x + (width/3) * cell2_x
            new_y2 = y + (height/3) * cell2_y - 120
        elif line_points[4] == 'col':
            new_x1 = x + (width/3) * cell1_x - 110
            new_y1 = y + (height/3) * cell1_y - 200
            new_x2 = x + (width/3) * cell2_x - 110
            new_y2 = y + (height/3) * cell2_y
        elif line_points[4] == 'diagonal left':
            new_x1 = x + 30
            new_y1 = y + 30
            new_x2 = x + width - 25
            new_y2 = y + height - 25
        else:
            new_x1 = x + 30
            new_y1 = y + height - 30
            new_x2 = x + width - 20
            new_y2 = y + 10
        return new_x1, new_y1, new_x2, new_y2
