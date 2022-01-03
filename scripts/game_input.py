import sys, pygame
import game_draw

game_over_event = pygame.USEREVENT + 1

def on_quit(event, game):
    sys.exit()


def on_key_down(event, game):
    if event.key == pygame.K_ESCAPE:
        sys.exit()


def on_mouse_down(event, gameState, hexMSBoard, surface):
    if event.button == 1 and gameState.is_valid_move():
        game_over = hexMSBoard.play_move("click", gameState.nearest_tile_to_mouse.coord_position[0], gameState.nearest_tile_to_mouse.coord_position[1])
        game_draw.update_grid(gameState, hexMSBoard, surface)
        game_draw.draw_board(surface, gameState, hexMSBoard)
        if game_over:
            return ["game_over", True]
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


def handle_events(events, game_state, hexMSBoard, surface):
    for event in events:
        if not event.type in event_handlers:
            continue
        if event.type == pygame.MOUSEBUTTONDOWN:
            game_event = on_mouse_down(event, game_state, hexMSBoard, surface)
            if game_event[0] == "game_over":
                game_state.game_over = True 
                return ["game_over", True]
            return event_handlers[event.type](event, game_state, hexMSBoard, surface)
        else:                                                                                                                                                                                                                                                              
            event_handlers[event.type](event, game_state)
