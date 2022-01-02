import hex_geometry
import sys, time, pygame

from constants import WINDOW_HEIGHT, WINDOW_WIDTH
from constants import BOARD_HEIGHT, BOARD_WIDTH

# from minesweeper import PACKAGE_IMGS_PATH 
sys.path.insert(0, '../scripts')
import constants 
import numpy as np 
import game_draw 


try:
    # Python 2
    xrange
except NameError:
    # Python 3, xrange is now named range
    xrange = range


class GameState:

    # Used to hold tile draw coordinate data
    TILE_DRAW_COORDS = {}  
    # Used to hold tile status in order to track current game status 
    TILE_STATUS_COORDS = {}

    def __init__(self):
        self.background_colour = 0, 0, 0 # rgb 256
        self.screen_size = 1024, 768 # pixels
        self.board_position = 100, 100 # pixels

        self.hex_tile_size = 32
        self.board_width_tiles = 11
        self.board_height_tiles = 11

        self.mine_hex_colour = (23, 45, 12)
        self.empty_hex_colour = (32, 32, 32)
        self.cursor_colour = (32, 128, 32)
        self.player_colour = [(255, 0, 0), (0, 0, 255)]

        self.nearest_tile_to_mouse = None
        self.current_player = 0
        self.moves = []
        self.solution = None

        self.mine_map = np.zeros((BOARD_HEIGHT, BOARD_WIDTH),
                                dtype=np.uint8)

        self.generate_draw_board()
        TILE_DRAW_COORDS = self.get_draw_tile_map()

        self.generate_board(TILE_DRAW_COORDS)
        
        self.create_tile_status_map()
        self.create_tile_draw_map()
        
        self.generate_maps()   
        
      
    def generate_draw_board(self):
        points_up = True 
        pygame.init()
        screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        HEX_TILE_IMG = pygame.image.load(constants.PACKAGE_IMGS_PATH + "hex_tile.png").convert_alpha()
        
        self.draw_hex_grid = hex_geometry.DrawHexGrid(
            HEX_TILE_IMG,
            self.board_width_tiles,
            self.board_height_tiles,
            self.hex_tile_size,
            points_up
        )
        

    def generate_board(self, TILE_DRAW_COORDS):
        points_up = True
        pygame.init()
                
        HEX_TILE_IMG = pygame.image.load(constants.PACKAGE_IMGS_PATH + "hex_tile.png").convert_alpha()
     
        self.hex_grid = hex_geometry.HexGrid(
            HEX_TILE_IMG,
            self.board_width_tiles,
            self.board_height_tiles,
            self.hex_tile_size,
            points_up,
            TILE_DRAW_COORDS)
              
        for tile in self.hex_tiles():
            x = tile.coord_position[0]
            y = tile.coord_position[1]
            if self.mine_map[x][y] == 1:
                tile.tile_status = 1
            tile.colour = self.empty_hex_colour 
                
    def generate_maps(self):
        """
        TODO: Creates mine_map and idx_list map variables in GameState object
        """
        self.mine_map = np.zeros((constants.BOARD_HEIGHT, constants.BOARD_WIDTH), dtype=np.uint8)
        
        self.idx_list = np.random.permutation(constants.BOARD_WIDTH * constants.BOARD_HEIGHT)
        self.idx_list = self.idx_list[:constants.NUM_MINES]
        
        
        for idx in self.idx_list:
            idx_x = int(idx % constants.BOARD_WIDTH)
            idx_y = int(idx / constants.BOARD_WIDTH)
            
            self.mine_map[idx_y, idx_x] = 1 
            
        self.info_map = np.ones((constants.BOARD_HEIGHT, constants.BOARD_WIDTH),
                                dtype=np.uint8)*11 
      
    def create_tile_status_map(self):
        """
        Used to create 2d array that will hold current tile status for all tiles in the game board 
        """
        x_coord = 0
        y_coord = 0 
        for i in xrange(constants.BOARD_WIDTH):
            x_coord += 100
            for j in xrange(constants.BOARD_HEIGHT):
                y_coord += 100
                self.TILE_STATUS_COORDS[(i, j)] = 0  
            y_coord = 0   
                      
        
    def create_draw_tile_map(self):
        x_coord = 0
        y_coord = 0 
        for tile in self.draw_hex_tiles():
            tile_coords = tile.center_point(self.board_position)
            x_coord = tile_coords[0]
            y_coord = tile_coords[1]
            
            tile_grid_pos = tile.grid_position
            tile_grid_pos_x = tile_grid_pos[0]
            tile_grid_pos_y = tile_grid_pos[1]
            self.TILE_DRAW_COORDS[(tile_grid_pos_x, tile_grid_pos_y)] = [x_coord, y_coord]

        print(tile.center_point(self.board_position))
        
    def get_draw_tile_map(self):
        if self.TILE_DRAW_COORDS != {}:
            return self.TILE_DRAW_COORDS 
        else:
            self.create_draw_tile_map()
            return self.TILE_DRAW_COORDS
    
    def create_tile_draw_map(self):
        """
        Used to create 2d array that will hold current tile coordinate information, used to draw numbered tiles on
        to the game board 
        """
        x_coord = 0
        y_coord = 0 
        for tile in self.hex_tiles():
            tile_coords = tile.center_point(self.board_position)
            x_coord = tile_coords[0]
            y_coord = tile_coords[1]
            
            tile_grid_pos = tile.grid_position
            tile_grid_pos_x = tile_grid_pos[0]
            tile_grid_pos_y = tile_grid_pos[1]
            self.TILE_DRAW_COORDS[(tile_grid_pos_x, tile_grid_pos_y)] = [x_coord, y_coord]

        print(tile.center_point(self.board_position))
    
    def get_tile_draw_map(self):
        if self.TILE_DRAW_COORDS != {}:
            return self.TILE_DRAW_COORDS
        else:
            self.create_tile_draw_map()
            return self.TILE_DRAW_COORDS
            
    def hex_tiles(self):
        return self.hex_grid.tiles.values()
    
    def draw_hex_tiles(self):
        return self.draw_hex_grid.tiles.values()


    def nearest_hex_tile(self, pos):
        result = None
        min_distance = None

        for tile in self.hex_tiles():
            tile_distance = tile.distance_squared(pos, self.board_position)
            if result == None:
                min_distance = tile_distance
                result = tile
            elif tile_distance < min_distance:
                min_distance = tile_distance
                result = tile

        return result


    def find_solution(self):
        for tile in self.hex_grid.top_row():
            path = self.hex_grid.find_path(
                tile,
                self.hex_grid.bottom_row(),
                lambda x: x.colour == self.player_colour[0])
            if path != None:
                return path

        for tile in self.hex_grid.left_column():
            path = self.hex_grid.find_path(
                tile,
                self.hex_grid.right_column(),
                lambda x: x.colour == self.player_colour[1])
            if path != None:
                return path

        return None


    def is_game_over(self):
        return self.solution != None


    def is_valid_move(self, tile=None):
        if self.is_game_over():
            return False
        if tile == None:
            tile = self.nearest_tile_to_mouse
        return not tile in self.moves


    def take_move(self, hexMSBoard, gameState, surface):
        if gameState.nearest_tile_to_mouse != False:
            tile = gameState.nearest_tile_to_mouse 
            x = tile.coord_position[0]
            y = tile.coord_position[1]

            hexMSBoard.discover_region(x, y)
            self.TILE_STATUS_COORDS[(x, y)] = 1
            game_draw.draw_tile(surface, gameState, tile)
        
        self.moves.append(tile)
        self.toggle_player_turn()
        self.solution = self.find_solution()
        hexMSBoard.update_board(gameState)
        
    def toggle_player_turn(self):
        if self.current_player == 0:
            self.current_player = 1
        else:
            self.current_player = 0
            
    def show_tile_bottom(self, state, hexMSBoard):
        x = state.nearest_tile_to_mouse.grid_position[0]
        y = state.nearest_tile_to_mouse.grid_position[1]                                     
