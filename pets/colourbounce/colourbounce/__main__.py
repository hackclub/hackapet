import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
import pygame
import time
import logging
import pathlib
import random

logging.basicConfig(level=logging.INFO)
SCALE = 4


def rotate_columns(data):
    data = data.copy()
    cols = data["grid"]
    col = cols.pop()
    cols.insert(0, col)
    data["grid"] = cols
    data["player_pos"] = (data["player_pos"][0] + 1 if data["player_pos"][0] < 7 else 0, data["player_pos"][1])
    data["move"] += 1
    return data


def rotate_rows(data):
    data = data.copy()
    cols = data["grid"]
    for col in cols:
        col.insert(0, col.pop())

    data["player_pos"] = (data["player_pos"][0], data["player_pos"][1] + 1 if data["player_pos"][1] < 7 else 0)
    data["move"] += 1
    return data


def rerender(display, splash, data):
    layers = splash._layers 
    for i, layer in enumerate(layers):
        splash.pop(i)
    for x, col in enumerate(data["grid"]):
        for y, colour in enumerate(col):
            sprite = displayio.OnDiskBitmap(str(colour.absolute()))
            sprite = displayio.TileGrid(
                sprite,
                pixel_shader=sprite.pixel_shader,
                width=1,
                height=1,
                tile_width=16,
                tile_height=16,
                x=x*16,
                y=y*16
            )
            splash.append(sprite)
    player_sprite = displayio.OnDiskBitmap("assets/player.bmp")
    player_sprite = displayio.TileGrid(
        player_sprite, 
        pixel_shader=player_sprite.pixel_shader,
        width=1,
        height=1,
        tile_width=14,
        tile_height=14,
        x=convert_grid_pos_to_pixel_pos(data["player_pos"])[0],
        y=convert_grid_pos_to_pixel_pos(data["player_pos"])[1]
    )
    
    button_sprite = displayio.OnDiskBitmap("assets/button.bmp")
    button_sprite = displayio.TileGrid(
        button_sprite, 
        pixel_shader=button_sprite.pixel_shader,
        width=1,
        height=1,
        tile_width=14,
        tile_height=14,
        x=convert_grid_pos_to_pixel_pos(data["btn_pos"])[0],
        y=convert_grid_pos_to_pixel_pos(data["btn_pos"])[1]
    )
    splash.append(button_sprite)
    splash.append(player_sprite)

    display.show(splash)


def convert_grid_pos_to_pixel_pos(grid_pos):
    return (grid_pos[0] * 16, grid_pos[1] * 16)


def handle_movement(data):
    cols = data["grid"]
    pos = data["player_pos"]
    current_pos = cols[pos[0]][pos[1]]
    up_pos = (pos[0], pos[1] - 1) if pos[1] > 0 else None
    down_pos = (pos[0], pos[1] + 1) if pos[1] < 7 else None
    left_pos = (pos[0] - 1, pos[1]) if pos[0] > 0 else None
    right_pos = (pos[0] + 1, pos[1]) if pos[0] < 7 else None

    tile_up = cols[pos[0]][pos[1] - 1] if pos[1] > 0 else None
    tile_down = cols[pos[0]][pos[1] + 1] if pos[1] < 7 else None
    tile_left = cols[pos[0] - 1][pos[1]] if pos[0] > 0 else None
    tile_right = cols[pos[0] + 1][pos[1]] if pos[0] < 7 else None

    allowed = []
    prev_pos = data["prev_pos"]
    btn_pos = data["btn_pos"]
    if (tile_up == current_pos or up_pos == btn_pos) and not up_pos == prev_pos:
        allowed.append(up_pos)
    elif (tile_down == current_pos or down_pos == btn_pos) and not down_pos == prev_pos:
        allowed.append(down_pos)
    elif (tile_left == current_pos or left_pos == btn_pos) and not left_pos == prev_pos:
        allowed.append(left_pos)
    elif (tile_right == current_pos or right_pos == btn_pos) and not right_pos == prev_pos:
        allowed.append(right_pos)
    
    try:
        data["player_pos"] = random.choice(allowed)
        data["prev_pos"] = prev_pos
    except IndexError:
        return data
    
    data["move"] += 1
    return data


def randomise_player(banned_pos):
    new_pos = (random.randint(0, 7), random.randint(0, 7))
    while new_pos in banned_pos:
        new_pos = (random.randint(0, 7), random.randint(0, 7))
    return new_pos


def menu(display, splash, win=False):
    if win:
        win_sprite = displayio.OnDiskBitmap("assets/win.bmp")
        win_sprite = displayio.TileGrid(
            win_sprite,
            pixel_shader=win_sprite.pixel_shader,
            width=1,
            height=1,
            tile_width=128,
            tile_height=128,
            x=0,
            y=0
        )
        splash.append(win_sprite)
    else:
        title = displayio.OnDiskBitmap("assets/title.bmp")
        title = displayio.TileGrid(
            title,
            pixel_shader=title.pixel_shader,
            width=1,
            height=1,
            tile_width=128,
            tile_height=128,
            x=0,
            y=0
        )
        splash.append(title)
    display.show(splash)
    undecided = True
    while undecided:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                logging.info("Exiting Colour Bounce")
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    undecided = False
                    start_game(display, splash)


def start_game(display, splash):
    logging.info("Starting Colour Bounce")
    
    colours = [colour for colour in pathlib.Path("assets/colours").iterdir() if colour.is_file() and colour.suffix == ".bmp"]

    data = {
        "grid": [],
        "player_pos": (0, 0),
        "prev_pos": (0, 0),
        "btn_pos": (random.randint(0, 7), random.randint(0, 7)),
        "move": 0
    }

    while data["btn_pos"] == data["player_pos"]:
        data["btn_pos"] = (random.randint(0, 7), random.randint(0, 7))

    last_colour = None
    for x in range(8):
        col = []
        for y in range(8):
            weighted_colours = colours.copy()
            if last_colour:
                weighted_colours += [last_colour] * 2
            colour = random.choice(weighted_colours)
            last_colour = colour
            col.append(colour)
        data["grid"].append(col)

    rerender(display, splash, data)
    playing = True
    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                logging.info("Exiting Colour Bounce")
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    data = rotate_rows(data)
                    rerender(display, splash, data)
                if event.key == pygame.K_x:
                    handle_movement(data)
                    rerender(display, splash, data)
                if event.key == pygame.K_c:
                    data = rotate_columns(data)
                    rerender(display, splash, data)
            
            if data["move"] == 7:
                data["player_pos"] = randomise_player([data["btn_pos"], data["player_pos"]])
                data["move"] = 0
                rerender(display, splash, data)
            if data["player_pos"] == data["btn_pos"]:
                logging.info("You win!")
                playing = False
                menu(display, splash, win=True)
        time.sleep(0.01)


def start():
    display = PyGameDisplay(width=128*SCALE, height=128*SCALE)
    splash = displayio.Group(scale=SCALE)
    menu(display, splash)

if __name__ == "__main__":
    start()
