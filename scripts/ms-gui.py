#!/usr/bin/env python
"""GUI for Mine Sweeper.

Author: Yuhuang Hu
Email : duguyue100@gmail.com
"""

from __future__ import print_function
import argparse
import sys, time, pygame
import game_state, game_draw, game_input, game_board
from hex_geometry import GameLabel
import constants
from constants import BOARD_HEIGHT, NUM_MINES, BOARD_WIDTH
from minesweeper import MSGame, gui
from hex_geometry import HexTileSprite, points_up_tile_corner_points

def game_loop(game):
    pygame.init()
    screen = pygame.display.set_mode(game.screen_size)
    game_over = False 
    # ms_game = MSGame(constants.BOARD_WIDTH, constants.BOARD_HEIGHT, constants.NUM_MINES, constants.PORT, constants.IP_ADD)
    
    hex_ms_board = game_board.HexMSBoard(BOARD_WIDTH, BOARD_HEIGHT, NUM_MINES)
    
    pygame.display.flip()
    
    while True:
        game_tile = HexTileSprite(pygame.image.load(game_draw.GAME_OVER_IMG_PATH).convert_alpha(), 20, 20, 32, True, 20, 20)
        game_tile.image = pygame.transform.scale(game_tile.image, (30, 30))
        game_tile.rect.x = 0
        game_tile.rect.y = 0
        pygame.draw.polygon(screen, pygame.Color(50, 50, 50), points_up_tile_corner_points(
                # self.grid_position,
                (0, 0),
                100,
                100,
                (20, 20)
            ))
        screen.blit(game_tile.image, game_tile.rect)  
        show_game_over_prompt(screen)
        event_handler_result = game_input.handle_events(pygame.event.get(), game, hex_ms_board, screen)
        try:
            if event_handler_result[0] == "click_event":
                game_over = game_draw.draw_frame(screen, game, hex_ms_board, event_handler_result[1])
                raise ValueError
            print(game_over)
        except ValueError:
            game_over = game_draw.draw_frame(screen, game, hex_ms_board, None)
        except TypeError:
            game_over = game_draw.draw_frame(screen, game, hex_ms_board, None)
        if game_over == True:
            show_game_over_prompt(screen)
        sys.stdout.flush()
        time.sleep(0.05) # cap at 20 fps

def show_game_over_prompt(screen):
    # game_tile.image = pygame.image.load(game_draw.EMPTY_PATH).convert_alpha()


    
    game_over_img = pygame.image.load(game_draw.GAME_OVER_IMG_PATH).convert_alpha()
    game_over_sprite = GameLabel(game_over_img, 20, 20, 50)
    game_over_sprite.rect.x = 20
    game_over_sprite.rect.y = 20
    
    screen.blit(game_over_sprite.image, game_over_sprite.rect)
    

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
    ms_hex_game_main()
