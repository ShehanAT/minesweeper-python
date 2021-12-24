import pygame
import os 
from os.path import join 
# import minesweeper
# from . import PACKAGE_IMGS_PATH
from hex_geometry import HexTileSprite, Block 
PACKAGE_PATH = os.path.dirname(os.path.abspath(__file__))
PACKAGE_IMGS_PATH = os.path.join(PACKAGE_PATH, "imgs")
from constants import BOARD_WIDTH, BOARD_HEIGHT 

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

# pygame.init()
# screen = pygame.display.set_mode((800, 600))

# TILE_IMG_0 = pygame.image.load('c:\\Users\\sheha\\OneDrive\\Documents\\GitHub\\minesweeper-master\\scripts\\imgs\\zero.png').convert_alpha()
# TILE_IMG_1 = pygame.image.load('imgs/one.png').convert_alpha()
# TILE_IMG_2 = pygame.image.load('c:\\Users\\sheha\\OneDrive\\Documents\\GitHub\\minesweeper-master\\scripts\\imgs\\two.png').convert_alpha()
# TILE_IMG_3 = pygame.image.load('c:\\Users\\sheha\\OneDrive\\Documents\\GitHub\\minesweeper-master\\scripts\\imgs\\three.png').convert_alpha()
# TILE_IMG_4 = pygame.image.load('c:\\Users\\sheha\\OneDrive\\Documents\\GitHub\\minesweeper-master\\scripts\\imgs\\four.png').convert_alpha()
# TILE_IMG_5 = pygame.image.load('c:\\Users\\sheha\\OneDrive\\Documents\\GitHub\\minesweeper-master\\scripts\\imgs\\five.png').convert_alpha()
# TILE_IMG_6 = pygame.image.load('c:\\Users\\sheha\\OneDrive\\Documents\\GitHub\\minesweeper-master\\scripts\\imgs\\six.png').convert_alpha()
# TILE_IMG_7 = pygame.image.load('c:\\Users\\sheha\\OneDrive\\Documents\\GitHub\\minesweeper-master\\scripts\\imgs\\seven.png').convert_alpha()
# TILE_IMG_8 = pygame.image.load('c:\\Users\\sheha\\OneDrive\\Documents\\GitHub\\minesweeper-master\\scripts\\imgs\\eight.png').convert_alpha()

TILE_DRAW_COORDS = {
    (0, 0): [100, 100],
    (0, 1): [100, 200],
    (0, 2): [100, 300],
    (0, 3): [100, 400],
    (0, 4): [100, 500],
}

def draw_hex_tile(surface, game, tile):
    center_point = tile.center_point(game.board_position)
    corner_points = tile.corner_points(game.board_position)
    pygame.draw.polygon(surface, tile.colour, corner_points)
    pygame.draw.polygon(surface, (255, 255, 255), corner_points, 2) # border  
    
    TILE_IMG_1 = pygame.image.load('c:\\Users\\sheha\\OneDrive\\Documents\\GitHub\\minesweeper-master\\scripts\\imgs\\one.png').convert_alpha()
    x_coord = 100
    y_coord = 100
    hex_tile_1 = HexTileSprite(TILE_IMG_1, x_coord, y_coord)
    all_hex_tiles = pygame.sprite.Group()
    all_hex_tiles.add(hex_tile_1)
    all_hex_tiles.draw(surface)

    if tile == game.nearest_tile_to_mouse:
        if not game.is_game_over():
            pygame.draw.circle(surface, game.cursor_colour, center_point, 12)
            #draw_hex_neighbours(surface, game, tile, (255, 255, 255))

def draw_numbered_tile(surface, game, tile):
    # Main task: use sprites instead of polygons to represent the minesweeper tiles and the 
    # numbered tiles. Try using pygame.draw.sprite.LayeredDirty.draw() to replace pygame.draw.polygon()

    x_pos = tile.grid_position[0]
    y_pos = tile.grid_position[1]
    window_coords = (x_pos, y_pos)
    print(window_coords)
    for k, v in TILE_DRAW_COORDS.items():
        if(k == window_coords):
            x_coord = v[0]
            y_coord = v[1]
            
    

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


def draw_board(surface, game):
    for tile in game.hex_tiles():
        draw_hex_tile(surface, game, tile)
    if game.solution != None:
        draw_hex_path(surface, game, game.solution, (255, 255, 255))


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


def draw_frame(surface, game):
    surface.fill(game.background_colour)

    draw_board(surface, game)
    draw_end_zones(surface, game)

    pygame.display.flip()
