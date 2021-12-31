import pygame
import os 
from os.path import join 
# from hex_geometry import HexTileSprite, Block 
import hex_geometry
# from hex_geometry import HexTileSprite
PACKAGE_PATH = os.path.dirname(os.path.abspath(__file__))
PACKAGE_IMGS_PATH = os.path.join(PACKAGE_PATH, "imgs")
from constants import BOARD_WIDTH, BOARD_HEIGHT 
import game_draw 

try:
    from PyQt4 import QtGui, QtCore
    from PyQt4.QCore import QWidget, QLabel, QGridLayout, QHBoxLayout
    from PyQt4.QCore import QPushButton, QLCDNumber
except ImportError:
    from PyQt5 import QtGui, QtCore
    from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QHBoxLayout
    from PyQt5.QtWidgets import QPushButton, QLCDNumber

try:
    # Python 2
    xrange
except NameError:
    # Python 3, xrange is now named range
    xrange = range

NUMBER_PATHS = [join(PACKAGE_IMGS_PATH, "one.png"),
                join(PACKAGE_IMGS_PATH, "one.png"),
                join(PACKAGE_IMGS_PATH, "two.png"),
                join(PACKAGE_IMGS_PATH, "three.png"),
                join(PACKAGE_IMGS_PATH, "four.png"),
                join(PACKAGE_IMGS_PATH, "five.png"),
                join(PACKAGE_IMGS_PATH, "six.png"),
                join(PACKAGE_IMGS_PATH, "seven.png"),
                join(PACKAGE_IMGS_PATH, "eight.png")
                ]

FLAG_PATH = join(PACKAGE_IMGS_PATH, "flag.png")
QUESTION_PATH = join(PACKAGE_IMGS_PATH, "question.png")
BOOM_PATH = join(PACKAGE_IMGS_PATH, "boom.png")
EMPTY_PATH = join(PACKAGE_IMGS_PATH, "blue_circle.png")
NUMBER_PATHS = [join(PACKAGE_IMGS_PATH, "zero.png"),
                join(PACKAGE_IMGS_PATH, "one.png"),
                join(PACKAGE_IMGS_PATH, "two.png"),
                join(PACKAGE_IMGS_PATH, "three.png"),
                join(PACKAGE_IMGS_PATH, "four.png"),
                join(PACKAGE_IMGS_PATH, "five.png"),
                join(PACKAGE_IMGS_PATH, "six.png"),
                join(PACKAGE_IMGS_PATH, "seven.png"),
                join(PACKAGE_IMGS_PATH, "eight.png")]
WIN_PATH = join(PACKAGE_IMGS_PATH, "win.png")
LOSE_PATH = join(PACKAGE_IMGS_PATH, "lose.png")
CONTINUE_PATH = join(PACKAGE_IMGS_PATH, "continue.png")

# TILE_IMG_0 = pygame.image.load('c:\\Users\\sheha\\OneDrive\\Documents\\GitHub\\minesweeper-master\\scripts\\imgs\\zero.png').convert_alpha()

# TILE_IMG_2 = pygame.image.load('c:\\Users\\sheha\\OneDrive\\Documents\\GitHub\\minesweeper-master\\scripts\\imgs\\two.png').convert_alpha()
# TILE_IMG_3 = pygame.image.load('c:\\Users\\sheha\\OneDrive\\Documents\\GitHub\\minesweeper-master\\scripts\\imgs\\three.png').convert_alpha()
# TILE_IMG_4 = pygame.image.load('c:\\Users\\sheha\\OneDrive\\Documents\\GitHub\\minesweeper-master\\scripts\\imgs\\four.png').convert_alpha()
# TILE_IMG_5 = pygame.image.load('c:\\Users\\sheha\\OneDrive\\Documents\\GitHub\\minesweeper-master\\scripts\\imgs\\five.png').convert_alpha()
# TILE_IMG_6 = pygame.image.load('c:\\Users\\sheha\\OneDrive\\Documents\\GitHub\\minesweeper-master\\scripts\\imgs\\six.png').convert_alpha()
# TILE_IMG_7 = pygame.image.load('c:\\Users\\sheha\\OneDrive\\Documents\\GitHub\\minesweeper-master\\scripts\\imgs\\seven.png').convert_alpha()
# TILE_IMG_8 = pygame.image.load('c:\\Users\\sheha\\OneDrive\\Documents\\GitHub\\minesweeper-master\\scripts\\imgs\\eight.png').convert_alpha()

class FieldWidget(QLabel):
    """A customized Field Widget."""

    def __init__(self, field_width=25, field_height=25):
        """Init the field."""
        super(FieldWidget, self).__init__()

        self.field_width = field_width
        self.field_height = field_height

        self.init_ui()

    def init_ui(self):
        """Init the ui."""
        self.id = 11
        self.setFixedSize(self.field_width, self.field_height)
        self.setPixmap(QtGui.QPixmap(EMPTY_PATH).scaled(
                self.field_width*3, self.field_height*3))
        self.setStyleSheet("QLabel {background-color: blue;}")

    def mousePressEvent(self, event):
        """Define mouse press event."""
        if event.button() == QtCore.Qt.LeftButton:
            # get label position
            p_wg = self.parent()
            p_layout = p_wg.layout()
            idx = p_layout.indexOf(self)
            loc = p_layout.getItemPosition(idx)[:2]
            if p_wg.ms_game.game_status == 2:
                p_wg.ms_game.play_move("click", loc[1], loc[0])
                p_wg.update_grid()
        elif event.button() == QtCore.Qt.RightButton:
            p_wg = self.parent()
            p_layout = p_wg.layout()
            idx = p_layout.indexOf(self)
            loc = p_layout.getItemPosition(idx)[:2]
            if p_wg.ms_game.game_status == 2:
                if self.id == 9:
                    self.info_label(10)
                    p_wg.ms_game.play_move("question", loc[1], loc[0])
                    p_wg.update_grid()
                elif self.id == 11:
                    self.info_label(9)
                    p_wg.ms_game.play_move("flag", loc[1], loc[0])
                    p_wg.update_grid()
                elif self.id == 10:
                    self.info_label(11)
                    p_wg.ms_game.play_move("unflag", loc[1], loc[0])
                    p_wg.update_grid()

    def info_label(self, indicator):
        """Set info label by given settings.

        Parameters
        ----------
        indicator : int
            A number where
            0-8 is number of mines in srrounding.
            12 is a mine field.
        """
        if indicator in xrange(1, 9):
            self.id = indicator
            self.setPixmap(QtGui.QPixmap(NUMBER_PATHS[indicator]).scaled(
                    self.field_width, self.field_height))
        elif indicator == 0:
            self.id == 0
            self.setPixmap(QtGui.QPixmap(NUMBER_PATHS[0]).scaled(
                    self.field_width, self.field_height))
        elif indicator == 12:
            self.id = 12
            self.setPixmap(QtGui.QPixmap(BOOM_PATH).scaled(self.field_width,
                                                           self.field_height))
            self.setStyleSheet("QLabel {background-color: black;}")
        elif indicator == 9:
            self.id = 9
            self.setPixmap(QtGui.QPixmap(FLAG_PATH).scaled(self.field_width,
                                                           self.field_height))
            self.setStyleSheet("QLabel {background-color: #A3C1DA;}")
        elif indicator == 10:
            self.id = 10
            self.setPixmap(QtGui.QPixmap(QUESTION_PATH).scaled(
                    self.field_width, self.field_height))
            self.setStyleSheet("QLabel {background-color: yellow;}")
        elif indicator == 11:
            self.id = 11
            self.setPixmap(QtGui.QPixmap(EMPTY_PATH).scaled(
                    self.field_width*3, self.field_height*3))
            self.setStyleSheet('QLabel {background-color: blue;}')

def create_grid():
       for i in xrange(grid_height):
            for j in xrange(grid_width):
                self.grid_wgs[(i, j)] = FieldWidget()
                self.grid_layout.addWidget(self.grid_wgs[(i, j)], i, j)

def draw_hex_polygon(surface, game, tile):
    """Used to draw hex polygon shapes on game board

    Args:
        surface ([type]): pygame window() instance
        game ([type]): GameState() instance
        tile ([type]): HexTile() instance 
    """
    center_point = tile.center_point(game.board_position)
    corner_points = tile.corner_points(game.board_position)
    pygame.draw.polygon(surface, tile.colour, corner_points)
    pygame.draw.polygon(surface, (255, 255, 255), corner_points, 2) # border  

    return center_point

def draw_hex_tile(surface, game, tile):
    center_point = draw_hex_polygon(surface, game, tile)
      
    if tile == game.nearest_tile_to_mouse:
        if not game.is_game_over():
            pygame.draw.circle(surface, game.cursor_colour, center_point, 12)

def draw_tile(surface, game, tile_indicator, x_index, y_index):
    # Main task: use sprites instead of polygons to represent the minesweeper tiles and the 
    # numbered tiles. Try using pygame.draw.sprite.LayeredDirty.draw() to replace pygame.draw.polygon()
    game_tile = game.hex_grid.tiles[(x_index, y_index)]

    center_point = draw_hex_polygon(surface, game, game_tile)
    
    if game_tile == game.nearest_tile_to_mouse:
        if not game.is_game_over():
            pygame.draw.circle(surface, game.cursor_colour, center_point, 12)
    
    TILE_IMG_1 = pygame.image.load('c:\\Users\\sheha\\OneDrive\\Documents\\GitHub\\minesweeper-master\\scripts\\imgs\\three.png').convert_alpha()
    
    if tile_indicator in xrange(1, 9):
        # self.id = tile_indicator
        game_tile.image = pygame.image.load(game_draw.NUMBER_PATHS[tile_indicator]).convert_alpha()
        new_image = pygame.image.load(game_draw.NUMBER_PATHS[tile_indicator]).convert_alpha()

    elif tile_indicator == 0:
        # self.id == 0
        game_tile.image = pygame.image.load(game_draw.NUMBER_PATHS[0]).convert_alpha()
        new_image = pygame.image.load(game_draw.NUMBER_PATHS[0]).convert_alpha()
    elif tile_indicator == 12:
        # self.id = 12
        game_tile.image = pygame.image.load(game_draw.BOOM_PATH).convert_alpha()
        new_image = pygame.image.load(game_draw.BOOM_PATH).convert_alpha()
    elif tile_indicator == 9:
        # self.id = 9
        game_tile.image = pygame.image.load(game_draw.FLAG_PATH).convert_alpha()
        new_image = pygame.image.load(game_draw.FLAG_PATH).convert_alpha()
    elif tile_indicator == 10:
        # self.id = 10
        game_tile.image = pygame.image.load(game_draw.QUESTION_PATH).convert_alpha()
        new_image = pygame.image.load(game_draw.QUESTION_PATH).convert_alpha()
    elif tile_indicator == 11:
        # self.id = 11
        game_tile.image = pygame.image.load(game_draw.EMPTY_PATH).convert_alpha()
        new_image = pygame.image.load(game_draw.EMPTY_PATH).convert_alpha()
    game_tile.image = pygame.transform.scale(game_tile.image, (30, 30))
    # game_tile.draw(surface)
    # game_tile.rect = game_tile.image.get_rect()
    game_tile.rect.x = game_tile.grid_position[0]
    game_tile.rect.y = game_tile.grid_position[1]
    # game_tile.rect.w = 30 
    # game_tile.rect.h = 30 
    # pygame.display.update()
    surface.blit(game_tile.image, game_tile.rect)  
  
def draw_hex_neighbours(surface, game, tile, colour):  
    width = 4
    from_point = tile.center_point(game.board_position)
    for neighbour in tile.neighbours:
        to_point = neighbour.center_point(game.board_position)
        pygame.draw.line(surface, colour, from_point, to_point, width)


def draw_hex_path(surface, game, path, colour):
    width = 4
    for i in range(len(path)-1):
        from_point = path[i].center_point(game.board_position)
        to_point = path[i+1].center_point(game.board_position)
        pygame.draw.line(surface, colour, from_point, to_point, width)


def draw_hex_top_border(surface, game, tile, colour):
    width = 4
    corner_points = tile.corner_points(game.board_position)
    pygame.draw.lines(surface, colour, False, corner_points[3:6], width)


def draw_hex_bottom_border(surface, game, tile, colour):
    width = 4
    corner_points = tile.corner_points(game.board_position)
    pygame.draw.lines(surface, colour, False, corner_points[0:3], width)


def draw_hex_left_border(surface, game, tile, colour):
    width = 4
    corner_points = tile.corner_points(game.board_position)
    pygame.draw.lines(surface, colour, False, corner_points[1:4], width)


def draw_hex_right_border(surface, game, tile, colour):
    width = 4
    corner_points = tile.corner_points(game.board_position)
    points = (corner_points[4], corner_points[5], corner_points[0])
    pygame.draw.lines(surface, colour, False, points, width)


def draw_board(surface, game, hex_ms_board):
    if hex_ms_board != None:
        for x_index, tile_row in enumerate(hex_ms_board.get_info_map()):
            for y_index, tile in enumerate(tile_row):
                draw_tile(surface, game, tile, x_index, y_index)
                # pass 
    # for tile in game.hex_tiles():
    #     x_pos = tile.coord_position[0]
    #     y_pos = tile.coord_position[1]
    #     if game.info_map[(x_pos, y_pos)] == 0:
    #         draw_hex_tile(surface, game, tile)
  
    # if game.solution != None:
    #     draw_hex_path(surface, game, game.solution, (255, 255, 255))

def draw_end_zones(surface, game):
    player_one_colour = game.player_colour[0]
    player_two_colour = game.player_colour[1]

    for tile in game.hex_grid.top_row():
        draw_hex_top_border(surface, game, tile, player_one_colour)

    for tile in game.hex_grid.bottom_row():
        draw_hex_bottom_border(surface, game, tile, player_one_colour)

    for tile in game.hex_grid.left_column():
        draw_hex_left_border(surface, game, tile, player_two_colour)

    for tile in game.hex_grid.right_column():
        draw_hex_right_border(surface, game, tile, player_two_colour)


def draw_frame(surface, game, hex_ms_game, number_tile=None):
    surface.fill(game.background_colour)
    draw_board(surface, game, hex_ms_game)
    draw_end_zones(surface, game)
    pygame.display.flip()
    
def update_grid(gameState, hexMSGame, surface):
    info_map = hexMSGame.get_info_map()
    for i in xrange(BOARD_WIDTH):
        for j in xrange(BOARD_HEIGHT):
            tile = gameState.hex_grid.tiles.get((i, j))
            tile.info_label(info_map[i, j], surface, gameState)
