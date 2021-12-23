import hex_geometry
import sys, time, pygame 
sys.path.insert(0, '../scripts')
import constants 
import numpy as np 

class GameState:

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

        self.generate_maps()   
        self.generate_board()

    # def generate_board(self):
    #     points_up = True

    #     self.hex_grid = hex_geometry.HexGrid(
    #         self.board_width_tiles,
    #         self.board_height_tiles,
    #         self.hex_tile_size,
    #         points_up)

    #     for tile in self.hex_tiles():
    #         tile.colour = self.empty_hex_colour

    def generate_board(self):
        points_up = True

        self.hex_grid = hex_geometry.HexGrid(
            self.board_width_tiles,
            self.board_height_tiles,
            self.hex_tile_size,
            points_up)
              
        for tile in self.hex_tiles():
            print(str(tile.grid_position[0])+ " - " + str(tile.grid_position[1]))
            x = tile.grid_position[0]
            y = tile.grid_position[1]
            if self.mine_map[x][y] == 1:
                tile.tile_status = 1
            tile.colour = self.empty_hex_colour 
            #     tile.colour = self.empty_hex_colour
            # elif self.mine_map[x][y] == 0:
            #     tile.colour = self.mine_hex_colour
                
      
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
      

    def hex_tiles(self):
        return self.hex_grid.tiles.values()


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


    def take_move(self, tile=None):
        if tile == None:
            tile = self.nearest_tile_to_mouse
        tile.colour = self.player_colour[self.current_player]
        self.moves.append(tile)
        self.toggle_player_turn()
        self.solution = self.find_solution()


    def toggle_player_turn(self):
        if self.current_player == 0:
            self.current_player = 1
        else:
            self.current_player = 0
            
    def show_tile_bottom(self, state, hexMSBoard):
        print(state.nearest_tile_to_mouse)
        x = state.nearest_tile_to_mouse.grid_position[0]
        y = state.nearest_tile_to_mouse.grid_position[1]
        print(x)
        print(y)
        print(self.mine_map[x][y])
        print(self.info_map[x][y])
        hexMSBoard.discover_region(x, y)
        print(hexMSBoard.info_map)
                                     
