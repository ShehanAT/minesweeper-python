#!/usr/bin/env python
"""GUI for Mine Sweeper.

Author: Yuhuang Hu
Email : duguyue100@gmail.com
"""

from __future__ import print_function
import argparse
import sys, time, pygame
# from scripts.constants import BOARD_WIDTH, BOARD_HEIGHT, NUM_MINES, PORT, IP_ADD
# sys.path.insert(0, '../hex-py')
import game_state, game_draw, game_input, game_board
import constants
from constants import BOARD_HEIGHT, NUM_MINES, BOARD_WIDTH
from hex_geometry import Block, HexTileSprite



try:
    from PyQt4 import QtGui, QtCore
    from PyQt4.QCore import QWidget, QApplication, QGridLayout
except ImportError:
    from PyQt5 import QtCore
    from PyQt5.QtWidgets import QWidget, QApplication, QGridLayout

from minesweeper import MSGame, gui

def game_loop(game):
    pygame.init()
    screen = pygame.display.set_mode(game.screen_size)
    
    ms_game = MSGame(constants.BOARD_WIDTH, constants.BOARD_HEIGHT, constants.NUM_MINES, constants.PORT, constants.IP_ADD)
    
    hex_ms_board = game_board.HexMSBoard(BOARD_WIDTH, BOARD_HEIGHT, NUM_MINES)
    # hex_game= hex_ms_game.HexMSGame(BOARD_WIDTH, BOARD_HEIGHT, NUM_MINES)
    
    pygame.display.flip()
    
    while True:
        event_handler_result = game_input.handle_events(pygame.event.get(), game, hex_ms_board, screen)
        try:
            if event_handler_result[0] == "click_event":
                game_draw.draw_frame(screen, game, hex_ms_board, event_handler_result[1])
                raise ValueError
        except ValueError:
            game_draw.draw_frame(screen, game, hex_ms_board)
        except TypeError:
            game_draw.draw_frame(screen, game, hex_ms_board)
            
        sys.stdout.flush()
        time.sleep(0.05) # cap at 20 fps

def ms_hex_game_main():
    game = game_state.GameState()
    game_loop(game)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Mine Sweeper Minesweeper \
                                                  with interfaces for \
                                                  Reinforcement Learning \
                                                  by Yuhuang Hu")
    parser.add_argument("--board-width", type=int,
                        default=20,
                        help="width of the board.")
    parser.add_argument("--board-height", type=int,
                        default=20,
                        help="height of the board.")
    parser.add_argument("--num-mines", type=int,
                        default=40,
                        help="number of mines.")
    parser.add_argument("--port", type=int,
                        default=5678,
                        help="The port for TCP connection.")
    parser.add_argument("--ip-add", type=str,
                        default="127.0.0.1",
                        help="The IP address for TCP connection.")
    args = parser.parse_args()
    # ms_game_main(**vars(args))
    ms_hex_game_main()
