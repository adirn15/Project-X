from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QMessageBox, QGraphicsView, QGraphicsScene, QGraphicsTextItem
from main.BoardUtils import BoardUtils
from main.BoardCell import BoardCell
from PyQt5.QtGui import QFont, QPen, QColor
from PyQt5.QtCore import pyqtSlot, Qt, QRectF, QTimer


class MiniBoard(QWidget):

    def __init__(self):
        super().__init__()
        self.mini_game_winner = None
        self.fonts = {u"\u274C": 80, u"\u2B55": 75}
        self.mini_grid_layout = QGridLayout(self)
        self.mini_grid_layout.setSpacing(5)
        self.mini_grid_layout.setContentsMargins(0, 0, 0, 0)
        self.view = QGraphicsView(self)
        self.view.setFixedSize(220, 220)
        self.view.setStyleSheet('''background: transparent; 
                              border-style: double; border-width: 6px; 
                              border-color: blue''')
        self.view.hide()
        for i in range(0, 3):
            for j in range(0, 3):
                button = BoardCell(' ')
                button.setObjectName("cell%d%d" % (i, j))
                button.clicked.connect(self.play_turn)
                self.mini_grid_layout.addWidget(button, i, j)

    def enable_free_cells(self):
        self.setEnabled(True)

    def is_mini_game_over(self, symbol):
        board = BoardUtils.grid_to_2d_array(self.mini_grid_layout)
        p1 = self.parent().players[0]
        p2 = self.parent().players[1]
        win_move = BoardUtils.winner_move(board, symbol)
        if win_move is not None:
            return win_move
        return BoardUtils.is_tie(board, p1, p2)

    @pyqtSlot()
    def play_turn(self):
        button = self.sender()
        game_board = self.parent()
        next_turn_i = int(button.objectName()[4])
        next_turn_j = int(button.objectName()[5])
        cur_symbol = game_board.players[game_board.turn]
        button.label.setText(cur_symbol)
        button.label.setStyleSheet('color: royalBlue')
        cur_turn_result = self.is_mini_game_over(cur_symbol)
        if cur_turn_result is not None:
            if cur_turn_result[0] == -1:
                self.mini_game_winner = 'Tie'
                self.view.hide()
            else:
                self.mini_game_winner = cur_symbol
            cur_i = int(self.objectName()[4])
            cur_j = int(self.objectName()[5])
            if self.mini_game_winner != 'Tie':
                self.draw_line(cur_turn_result)
            game_board.final_scores[cur_i][cur_j] = self.mini_game_winner
            # check if full game is over
            final_game_result = game_board.is_game_over(cur_symbol)
            if final_game_result is not None:
                self.window().findChild(QLabel, "turn").setText("Nice!")
                if final_game_result[0] != -1:
                    game_board.draw_line(final_game_result)
                game_board.disable_all_mini_boards()
                game_board.game_enabled = False
                if final_game_result[0] == -1:
                    self.alert("it's a tie, wanna try again?")
                else:
                    self.alert("the %s's win!" % cur_symbol)
                return
        button.setEnabled(False)
        game_board.disable_all_mini_boards()
        if self.mini_game_winner is None:
            self.view.hide()
        next_turn_board = game_board.findChild(MiniBoard, "mini%d%d" % (next_turn_i, next_turn_j))
        if next_turn_board.mini_game_winner is None:
            next_turn_board.view.show()
        game_board.turn = (game_board.turn+1) % 2
        if (next_turn_board is not None) and next_turn_board.mini_game_winner is None:
            next_turn_board.enable_free_cells()
        else:
            game_board.enable_all_mini_boards()
        self.window().findChild(QLabel, "turn").setText("Play %s!" % game_board.players[game_board.turn])

    @staticmethod
    def alert(message):
        w = QMessageBox()
        w.setMinimumHeight(200)
        w.setText(message)
        w.setFont(QFont('Arial', 20))
        w.setWindowTitle('Game Over')
        w.setIcon(QMessageBox.Information)
        w.setStandardButtons(QMessageBox.Ok)
        w.exec()

    def draw_line(self, line_tuple):
        self.view.setStyleSheet('background: transparent; border-style: none')
        del self.view
        self.view = QGraphicsView(self)
        x = self.x()
        y = self.y()
        width = self.width()
        height = self.height()
        scene = QGraphicsScene(QRectF(x, y, width, height))
        self.view.setStyleSheet('background: transparent; border-style: none')
        self.view.setFixedSize(width, height)
        self.view.setScene(scene)
        pen = QPen()
        pen.setColor(QColor(65, 105, 225))
        pen.setWidth(10)
        line_coordinates = self.get_line_coordinates(line_tuple)
        scene.addLine(line_coordinates[0], line_coordinates[1], line_coordinates[2], line_coordinates[3], pen)
        winner_label = self.create_winner_label()
        scene.addItem(winner_label)
        self.view.show()
        timer = QTimer(self.view)
        timer.timeout.connect(winner_label.show)
        timer.start(1000)

    def create_winner_label(self):
        w = QGraphicsTextItem()
        w.setPlainText("%s" % self.mini_game_winner)
        game_board = self.parent()
        print(game_board)
        w.setFont(QFont('SansSerif', self.fonts[self.mini_game_winner]))
        w.setDefaultTextColor(Qt.black)
        w.setPos(self.x(), self.y())
        w.setVisible(False)
        return w

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
            new_x1 = x + (width/3) * cell1_x - 80
            new_y1 = y + (height/3) * cell1_y - 40
            new_x2 = x + (width/3) * cell2_x
            new_y2 = y + (height/3) * cell2_y - 40
        elif line_points[4] == 'col':
            new_x1 = x + (width/3) * cell1_x - 30
            new_y1 = y + (height/3) * cell1_y - 60
            new_x2 = x + (width/3) * cell2_x - 30
            new_y2 = y + (height/3) * cell2_y - 20
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


















