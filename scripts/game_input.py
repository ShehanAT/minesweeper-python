import sys, pygame
import game_draw

def on_quit(event, game):
    sys.exit()


def on_key_down(event, game):
    if event.key == pygame.K_ESCAPE:
        sys.exit()


def on_mouse_down(event, gameState, hexMSBoard, hexMSGame, surface):
    if event.button == 1 and gameState.is_valid_move():
        gameState.take_move(hexMSBoard, gameState, surface)
        gameState.show_tile_bottom(gameState, hexMSBoard)
        hexMSGame.play_move("click", gameState.nearest_tile_to_mouse.grid_position[0], gameState.nearest_tile_to_mouse.grid_position[1])
        game_draw.update_grid(gameState, hexMSGame, surface)
    return ["click_event", gameState.nearest_tile_to_mouse]


def on_mouse_up(event, game):
    return


def on_mouse_move(event, game):
    game.nearest_tile_to_mouse = game.nearest_hex_tile(event.pos)
    return


event_handlers = {
    pygame.QUIT: on_quit,
    pygame.KEYDOWN: on_key_down,
    pygame.MOUSEBUTTONDOWN: on_mouse_down,
    pygame.MOUSEBUTTONUP: on_mouse_up,
    pygame.MOUSEMOTION: on_mouse_move
}


def handle_events(events, game, hexMSBoard, hexMSGame, surface):
    for event in events:
        if not event.type in event_handlers:
            continue
        if event.type == pygame.MOUSEBUTTONDOWN:
            return event_handlers[event.type](event, game, hexMSBoard, hexMSGame, surface)
        else:                                                                                                                                                                                                                                                              
            event_handlers[event.type](event, game)
