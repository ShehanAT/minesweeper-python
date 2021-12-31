from msboard import MSBoard

# class HexMSGame(object):
    
    # def __init__(self, board_width, board_height, num_mines,
    #     port=5678, ip_add="127.0.0.1"):
        
    #     if (board_width <= 0):
    #             raise ValueError("the board width cannot be non-positive!")
    #     else:
    #         self.board_width = board_width

    #     if (board_height <= 0):
    #         raise ValueError("the board height cannot be non-positive!")
    #     else:
    #         self.board_height = board_height

    #     if (num_mines >= (board_width*board_height)):
    #         raise ValueError("The number of mines cannot be larger than "
    #                          "number of grids!")
    #     else:
    #         self.num_mines = num_mines

    #     self.TCP_PORT = port
    #     self.TCP_IP = ip_add
    #     self.BUFFER_SIZE = 1024

    #     self.move_types = ["click", "flag", "unflag", "question"]
        
    #     self.board = self.create_board(self.board_width, self.board_height,
    #         self.num_mines)
    #     self.init_new_game()
        
    # def create_board(self, board_width, board_height, num_mines):
    #     """Create a board by given parameters.

    #     Parameters
    #     ----------
    #     board_width : int
    #         the width of the board (> 0)
    #     board_height : int
    #         the height of the board (> 0)
    #     num_mines : int
    #         the number of mines, cannot be larger than
    #         (board_width x board_height)

    #     Returns
    #     -------
    #     board : MSBoard
    #     """
    #     return MSBoard(board_width, board_height, num_mines)
    
    # def check_move(self, move_type, move_x, move_y):
    #     """Check if a move is valid.

    #     If the move is not valid, then shut the game.
    #     If the move is valid, then setup a dictionary for the game,
    #     and update move counter.

    #     TODO: maybe instead of shut the game, can end the game or turn it into
    #     a valid move?

    #     Parameters
    #     ----------
    #     move_type : string
    #         one of four move types:
    #         "click", "flag", "unflag", "question"
    #     move_x : int
    #         X position of the move
    #     move_y : int
    #         Y position of the move
    #     """
    #     if move_type not in self.move_types:
    #         raise ValueError("This is not a valid move!")
    #     if move_x < 0 or move_x >= self.board_width:
    #         raise ValueError("This is not a valid X position of the move!")
    #     if move_y < 0 or move_y >= self.board_height:
    #         raise ValueError("This is not a valid Y position of the move!")

    #     move_des = {}
    #     move_des["move_type"] = move_type
    #     move_des["move_x"] = move_x
    #     move_des["move_y"] = move_y
    #     self.num_moves += 1

    #     return move_des
    
    # def init_new_game(self):
    #     """Init a new game.

    #     Parameters
    #     ----------
    #     board : MSBoard
    #         define a new board.
    #     game_status : int
    #         define the game status:
    #         0: lose, 1: win, 2: playing
    #     moves : int
    #         how many moves carried out.
    #     """
    #     self.board = self.create_board(self.board_width, self.board_height,
    #                                    self.num_mines)
    #     self.game_status = 2
    #     self.num_moves = 0
    #     self.move_history = []

    # def play_move(self, move_type, move_x, move_y):
    #     """Update board by a given move.

    #     Parameters
    #     ----------
    #     move_type : string
    #         one of four move types:
    #         "click", "flag", "unflag", "question"
    #     move_x : int
    #         X position of the move
    #     move_y : int
    #         Y position of the move
    #     """
    #     # record the move
    #     if self.game_status == 2:
    #         self.move_history.append(self.check_move(move_type, move_x,
    #                                                  move_y))
    #     else:
    #         self.end_game()

    #     # play the move, update the board
    #     if move_type == "click":
    #         self.board.click_field(move_x, move_y)
    #     elif move_type == "flag":
    #         self.board.flag_field(move_x, move_y)
    #     elif move_type == "unflag":
    #         self.board.unflag_field(move_x, move_y)
    #     elif move_type == "question":
    #         self.board.question_field(move_x, move_y)

    #     # check the status, see if end the game
    #     if self.board.check_board() == 0:
    #         self.game_status = 0  # game loses
    #         # self.print_board()
    #         self.end_game()
    #     elif self.board.check_board() == 1:
    #         self.game_status = 1  # game wins
    #         # self.print_board()
    #         self.end_game()
    #     elif self.board.check_board() == 2:
    #         self.game_status = 2  # game continues
    #         # self.print_board()

    # def print_board(self):
    #     """Print board."""
    #     self.board.print_board()

    # def get_board(self):
    #     """Get board message."""
    #     return self.board.board_msg()

    # def get_info_map(self):
    #     """Get info map."""
    #     return self.board.info_map

    # def get_mine_map(self):
    #     """Get mine map."""
    #     return self.board.mine_map

    # def end_game(self):
    #     """Settle the end game.

    #     TODO: some more expections..
    #     """
    #     if self.game_status == 0:
    #         print("[MESSAGE] YOU LOSE!")
    #     elif self.game_status == 1:
    #         print("[MESSAGE] YOU WIN!")

    # def parse_move(self, move_msg):
    #     """Parse a move from a string.

    #     Parameters
    #     ----------
    #     move_msg : string
    #         a valid message should be in:
    #         "[move type]: [X], [Y]"

    #     Returns
    #     -------
    #     """
    #     # TODO: some condition check
    #     type_idx = move_msg.index(":")
    #     move_type = move_msg[:type_idx]
    #     pos_idx = move_msg.index(",")
    #     move_x = int(move_msg[type_idx+1:pos_idx])
    #     move_y = int(move_msg[pos_idx+1:])

    #     return move_type, move_x, move_y

    # def play_move_msg(self, move_msg):
    #     """Another play move function for move message.

    #     Parameters
    #     ----------
    #     move_msg : string
    #         a valid message should be in:
    #         "[move type]: [X], [Y]"
    #     """
    #     move_type, move_x, move_y = self.parse_move(move_msg)
    #     self.play_move(move_type, move_x, move_y)
