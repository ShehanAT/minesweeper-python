from __future__ import print_function
import numpy as np 
from collections import deque

from msboard import MSBoard 

try:
    # Python 2
    xrange
except NameError:
    # Python 3, xrange is now named range
    xrange = range
    

class HexMSBoard(object):
    """"Define a Mine Sweeper Game Board."""
    
    
    def __init__(self, board_width, board_height, num_mines):
        """The init function of Mine Sweeper Game.

        Parameters
        ----------
        board_width : int
            the width of the board (> 0)
        board_height : int
            the height of the board (> 0)
        num_mines : int
            the number of mines, cannot be larger than
            (board_width x board_height)
        """
        if (board_width <= 0):
            raise ValueError("the board width cannot be non-positive!")
        else:
            self.board_width = board_width

        if (board_height <= 0):
            raise ValueError("the board height cannot be non-positive!")
        else:
            self.board_height = board_height

        if (num_mines >= (board_width*board_height)):
            raise ValueError("The number of mines cannot be larger than "
                             "number of grids!")
        else:
            self.num_mines = num_mines

        self.move_types = ["click", "flag", "unflag", "question"]

        self.init_board()
        self.init_new_game()

    def init_board(self):
        """Init a valid board by given settings.

        Parameters
        ----------
        mine_map : numpy.ndarray
            the map that defines the mine
            0 is empty, 1 is mine
        info_map : numpy.ndarray
            the map that is presented to the player
            0-8 is number of mines in surrounding.
            9 is flagged field.
            10 is questioned field.
            11 is undiscovered field.
            12 is a mine field.
        """
        self.mine_map = np.zeros((self.board_height, self.board_width),
                                 dtype=np.uint8)
        idx_list = np.random.permutation(self.board_width*self.board_height)
        # idx_list = np.random.permutation(12)
        idx_list = idx_list[:self.num_mines]

        for idx in idx_list:
            idx_x = int(idx % self.board_width)
            idx_y = int(idx / self.board_width)

            self.mine_map[idx_y, idx_x] = 1

        self.info_map = np.ones((self.board_height, self.board_width),
                                dtype=np.uint8)*11

    def click_field(self, move_x, move_y):
        """Click one grid by given position."""
        field_status = self.info_map[move_y, move_x]

        # can only click blank region
        if field_status == 11:
            if self.mine_map[move_y, move_x] == 1:
                self.info_map[move_y, move_x] = 12
            else:
                # discover the region.
                self.discover_region(move_x, move_y)

    def discover_region(self, move_x, move_y):
        """Discover region from given location."""
        field_list = deque([(move_y, move_x)])

        while len(field_list) != 0:
            field = field_list.popleft()

            (tl_idx, br_idx, region_sum) = self.get_region(field[1], field[0])
            if region_sum == 0:
                self.info_map[field[0], field[1]] = region_sum
                # get surrounding to queue
                region_mat = self.info_map[tl_idx[0]:br_idx[0]+1,
                                           tl_idx[1]:br_idx[1]+1]
                x_list, y_list = np.nonzero(region_mat == 11)

                for x_idx, y_idx in zip(x_list, y_list):
                    field_temp = (x_idx+max(field[0]-1, 0),
                                  y_idx+max(field[1]-1, 0))
                    if field_temp not in field_list:
                        field_list.append(field_temp)
            elif region_sum > 0:
                self.info_map[field[0], field[1]] = region_sum

    def get_region(self, move_x, move_y):
        """Get region around a location."""
        top_left = (max(move_y-1, 0), max(move_x-1, 0))
        bottom_right = (min(move_y+1, self.board_height-1),
                        min(move_x+1, self.board_width-1))
        region_sum = self.mine_map[top_left[0]:bottom_right[0]+1,
                                   top_left[1]:bottom_right[1]+1].sum()

        return top_left, bottom_right, region_sum
    
    def get_info_map(self):
        return self.info_map

    def flag_field(self, move_x, move_y):
        """Flag a grid by given position."""
        field_status = self.info_map[move_y, move_x]

        # a questioned or undiscovered field
        if field_status != 9 and (field_status == 10 or field_status == 11):
            self.info_map[move_y, move_x] = 9

    def unflag_field(self, move_x, move_y):
        """Unflag or unquestion a grid by given position."""
        field_status = self.info_map[move_y, move_x]

        if field_status == 9 or field_status == 10:
            self.info_map[move_y, move_x] = 11

    def question_field(self, move_x, move_y):
        """Question a grid by given position."""
        field_status = self.info_map[move_y, move_x]

        # a questioned or undiscovered field
        if field_status != 10 and (field_status == 9 or field_status == 11):
            self.info_map[move_y, move_x] = 10

    def check_board(self):
        """Check the board status and give feedback."""
        num_mines = np.sum(self.info_map == 12)
        num_undiscovered = np.sum(self.info_map == 11)
        num_questioned = np.sum(self.info_map == 10)

        if num_mines > 0:
            return 0
        elif np.array_equal(self.info_map == 9, self.mine_map):
            return 1
        elif num_undiscovered > 0 or num_questioned > 0:
            return 2

    def print_board(self):
        """Print board in structural way."""
        print(self.board_msg())

    def board_msg(self):
        """Structure a board as in print_board."""
        board_str = "s\t\t"
        for i in xrange(self.board_width):
            board_str += str(i)+"\t"
        board_str = board_str.expandtabs(4)+"\n\n"

        for i in xrange(self.board_height):
            temp_line = str(i)+"\t\t"
            for j in xrange(self.board_width):
                if self.info_map[i, j] == 9:
                    temp_line += "@\t"
                elif self.info_map[i, j] == 10:
                    temp_line += "?\t"
                elif self.info_map[i, j] == 11:
                    temp_line += "*\t"
                elif self.info_map[i, j] == 12:
                    temp_line += "!\t"
                else:
                    temp_line += str(self.info_map[i, j])+"\t"
            board_str += temp_line.expandtabs(4)+"\n"

        return board_str
    
    def update_board(self, gameState):
        
        for i in gameState.hex_tiles():
            x = i.coord_position[0]
            y = i.coord_position[1]
            i.minesweeper_number = self.info_map[x][y]
      
    def create_board(self, board_width, board_height, num_mines):
        """Create a board by given parameters.

        Parameters
        ----------
        board_width : int
            the width of the board (> 0)
        board_height : int
            the height of the board (> 0)
        num_mines : int
            the number of mines, cannot be larger than
            (board_width x board_height)

        Returns
        -------
        board : MSBoard
        """
        return MSBoard(board_width, board_height, num_mines)

    def check_move(self, move_type, move_x, move_y):
        """Check if a move is valid.

        If the move is not valid, then shut the game.
        If the move is valid, then setup a dictionary for the game,
        and update move counter.

        TODO: maybe instead of shut the game, can end the game or turn it into
        a valid move?

        Parameters
        ----------
        move_type : string
            one of four move types:
            "click", "flag", "unflag", "question"
        move_x : int
            X position of the move
        move_y : int
            Y position of the move
        """
        if move_type not in self.move_types:
            raise ValueError("This is not a valid move!")
        if move_x < 0 or move_x >= self.board_width:
            raise ValueError("This is not a valid X position of the move!")
        if move_y < 0 or move_y >= self.board_height:
            raise ValueError("This is not a valid Y position of the move!")

        move_des = {}
        move_des["move_type"] = move_type
        move_des["move_x"] = move_x
        move_des["move_y"] = move_y
        self.num_moves += 1

        return move_des
    
    def init_new_game(self):
        """Init a new game.

        Parameters
        ----------
        board : MSBoard
            define a new board.
        game_status : int
            define the game status:
            0: lose, 1: win, 2: playing
        moves : int
            how many moves carried out.
        """
        self.board = self.create_board(self.board_width, self.board_height,
                                       self.num_mines)
        self.game_status = 2
        self.num_moves = 0
        self.move_history = []

    def play_move(self, move_type, move_x, move_y):
        """Update board by a given move.

        Parameters
        ----------
        move_type : string
            one of four move types:
            "click", "flag", "unflag", "question"
        move_x : int
            X position of the move
        move_y : int
            Y position of the move
        """
        game_over = False 
        # record the move
        if self.game_status == 2:
            self.move_history.append(self.check_move(move_type, move_x,
                                                     move_y))
        else:
            self.end_game()
            game_over = True 

        # play the move, update the board
        if move_type == "click":
            self.board.click_field(move_x, move_y)
        elif move_type == "flag":
            self.board.flag_field(move_x, move_y)
        elif move_type == "unflag":
            self.board.unflag_field(move_x, move_y)
        elif move_type == "question":
            self.board.question_field(move_x, move_y)

        # check the status, see if end the game
        if self.board.check_board() == 0:
            self.game_status = 0  # game loses
            # self.print_board()
            self.end_game()
            return game_over 
        elif self.board.check_board() == 1:
            self.game_status = 1  # game wins
            # self.print_board()
            self.end_game()
        elif self.board.check_board() == 2:
            self.game_status = 2  # game continues
            # self.print_board()

    def print_board(self):
        """Print board."""
        self.board.print_board()

    def get_board(self):
        """Get board message."""
        return self.board.board_msg()

    def get_info_map(self):
        """Get info map."""
        return self.board.info_map

    def get_mine_map(self):
        """Get mine map."""
        return self.board.mine_map

    def end_game(self):
        """Settle the end game.

        TODO: some more expections..
        """
        if self.game_status == 0:
            print("[MESSAGE] YOU LOSE!")
        elif self.game_status == 1:
            print("[MESSAGE] YOU WIN!")

    def parse_move(self, move_msg):
        """Parse a move from a string.

        Parameters
        ----------
        move_msg : string
            a valid message should be in:
            "[move type]: [X], [Y]"

        Returns
        -------
        """
        # TODO: some condition check
        type_idx = move_msg.index(":")
        move_type = move_msg[:type_idx]
        pos_idx = move_msg.index(",")
        move_x = int(move_msg[type_idx+1:pos_idx])
        move_y = int(move_msg[pos_idx+1:])

        return move_type, move_x, move_y

    def play_move_msg(self, move_msg):
        """Another play move function for move message.

        Parameters
        ----------
        move_msg : string
            a valid message should be in:
            "[move type]: [X], [Y]"
        """
        move_type, move_x, move_y = self.parse_move(move_msg)
        self.play_move(move_type, move_x, move_y)

      