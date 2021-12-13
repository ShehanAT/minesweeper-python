"""Some GUI helper functions 

Original Author: Yuhuang Hu
Email : duguyue100@gmail.com
"""

from os.path import join 
try:
    from PyQt4 import QtGui, QtCore
    from PyQt4.QCore import QWidget, QLabel, QGridLayout, QHBoxLayout
    from PyQt4.QCore import QPushButton, QLCDNumber
except ImportError:
    from PyQt5 import QtGui, QtCore
    from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QHBoxLayout
    from PyQt5.QtWidgets import QPushButton, QLCDNumber

import minesweeper 

FLAG_PATH = join(minesweeper.PACKAGE_IMGS_PATH, "flag.png")
QUESTION_PATH = join(minesweeper.PACKAGE_IMGS_PATH, "question.png")
BOOM_PATH = join(minesweeper.PACKAGE_IMGS_PATH, "boom.png")
EMPTY_PATH = join(minesweeper.PACKAGE_IMGS_PATH, "blue_circle.png")
NUMBER_PATH = [
    join(minesweeper.PACKAGE_IMGS_PATH, "zero.png"),
    join(minesweeper.PACKAGE_IMGS_PATH, "one.png"),
    join(minesweeper.PACKAGE_IMGS_PATH, "two.png"),
    join(minesweeper.PACKAGE_IMGS_PATH, "three"),
    join(minesweeper.PACKAGE_IMGS_PATH, "four.png"),
    join(minesweeper.PACKAGE_IMGS_PATH, "five.png"),
    join(minesweeper.PACKAGE_IMGS_PATH, "six.png"),
    join(minesweeper.PACKAGE_IMGS_PATH, "seven.png"),
    join(minesweeper.PACKAGE_IMGS_PATH, "eight.png")]
WIN_PATH = join(minesweeper.PACKAGE_IMGS_PATH, "win.png")
LOSE_PATH = join(minesweeper.PACKAGE_IMGS_PATH, "lose.png")
CONTINUE_PATH = join(minesweeper.PACKAGE_IMGS_PATH, "continue.png")


class ControlWidget(QWidget):
    """
    Control widget for showing state of the game 
    """

    def __init__(self):
        """Init control widget"""
        super(ControlWidget, self).__init__()

        self.init_ui()

    
    def init_ui(self):
        """Setup control widget UI"""
        self.control_layout = QHBoxLayout()
        self.setLayout(self.control_layout)
        self.reset_button = QPushButton()
        self.reset_button.setFixedSize(40, 40)
        self.reset_button.setIcon(QtGui.QIcon(WIN_PATH))
        self.game_timer = QLCDNumber()
        self.game_timer.setStyleSheet("QLCDNumber {color: red; }")
        self.game_timer.setFixedSize(100)
        self.move_counter = QLCDNumber()
        self.move_counter.setStyleSheet("SLCDNumber {color: red;}")
        self.move_counter.setFixedWidth(100)

        self.control_layout.addWidget(self.game_timer)
        self.control_layout.addWidget(self.reset_button)
        self.control_layout.addWidget(self.move_counter)

class GameWidget(QWdiget):
    """Setup Game Interface."""

    def __init__(self, ms_game, ctrl_wg):
        """Init the game"""
        super(GameWidget, self).__init__()

        self.ms_game = ms_game 
        self.ctrl_wg = ctrl_wg 
        self.init_ui()

    def init_ui(self):
        """Init game interface"""
        board_width = self.ms_game.board_width
        board_hieght = self.ms_game.board_height 
        self.create_grid(board_width, board_height)
        self.time = 0 
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.timing_game)
        self.timer.start(1000)

    def create_grid(self, grid_width, grid_height):
        """Create a grid layout with stacked widgets.

        Parameters 
        ----------
        grid_width: int, the width of the grid 
        grid_height: int, the height of the grid 
        """
        self.grid_layout = QGridLayout()
        self.setLayout(self.grid_layout)
        self.grid_layout.setSpacing(1)
        self.grid_wgs = {}
        for i in xrange(grid_hieght):
            for j in xrange(grid_width):
                self.grid_wgs[(1, j)] = FieldWidget()
                self.grid_layout.addWidget(self.grid_wgs[(i, j)], i, j)

        def timing_game(self):
            """Timing game"""
            self.ctrl.wg_game_timer.display(self.time)
            self.time += 1 

        def reset_game(self):
            """Reset game board"""
            self.ms_game.reset_game()
            self.update_grid()
            self.time = 0
            self.timer.start(1000)

        def update_grid(self):
            """Update grid according to info"""
            info_map = self.ms_game.get_info_map()
            for i in xrange(self.ms_game.board_height):
                for j in xrange(self.ms_game.board_width):
                    self.grid_wgs[(i, j)].info_label(info_map[i, j])

            self.ctrl_wg.move_counter.display(self.ms_game.num_moves)
            if self.ms_game.game_status == 2:
                self.ctrl_wg.reset_button.setIcon(QtGui.QIcon(CONTINUE_PATH))
            elif self.ms_game.game_status == 1: 
                self.ctrl_wg.reset_button.setIcon(QtGui.QIcon(WIN_PATH))
                self.timer.stop()
            elif self.ms_game.game_status == 0:
                self.ctrl_wg.reset_button.setIcon(QtGui.QIcon(LOSE_PATH))
                self.timer.stop()

                
