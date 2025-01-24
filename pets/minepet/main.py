import os, shutil, time, PIL, sys

import importlib
import importlib.util

import patch
from player import JUMP_FALL_FRAMES, P_LEFT, PLAYER_SIZE, Player
from world import *

from blinka_displayio_pygamedisplay import PyGameDisplay
PyGameDisplay._initialize = patch.blinka_pygame_display_initalize_patched
PyGameDisplay._pygame_refresh = patch.blinka_pygame_display_pygamerefresh_patched
import displayio
displayio.Bitmap.__init__ = patch.bitmap_create_init_patched
displayio.TileGrid._fill_area = patch.tilegrid_fill_area_patched
displayio.Palette._get_alpha_palette = patch.palette_make_alpha_palette_patched
import pygame
import pygame.locals as pgl

import adafruit_display_text
import adafruit_display_text.label
import adafruit_display_text.text_box
import displayio._structs
try:
    import terminalio
except: pass

# # od_player_bmp = displayio.OnDiskBitmap("sprites/player.bmp")
# od_player_bmp = displayio.OnDiskBitmap("sprites/player_indexed.bmp")
# print(od_player_bmp._image)
# od_player_bmp_palette = od_player_bmp.pixel_shader
# # print(od_player_bmp_palette)
player_sprite_design = [
    "00000000 00011100 00000000",
    "02000000 021A3A10 00000000",
    "24200000 24203000 00000000",
    "02566600 02566600 00888800",
    "05676760 05676760 08898980",
    "56666666 56666666 88888888",
    "56667766 56667766 88889988",
    "05555550 05555550 08888880",
]
PSCALE = 2
# PLAYER_BMP = displayio.Bitmap(width=od_player_bmp.width*PSCALE, height=od_player_bmp.height*PSCALE, value_count=(2**32))
# for x in range(od_player_bmp.width):
#     for y in range(od_player_bmp.height):
#         color = od_player_bmp[x, y]
#         color = (color[0], color[1], color[2], color[3])
#         for dx in range(PSCALE):
#             for dy in range(PSCALE):
#                 PLAYER_BMP[x * PSCALE + dx, y * PSCALE + dy] = color
PLAYER_COLOR_COUNT = 11
PLAYER_BMP = displayio.Bitmap(width=PLAYER_SIZE * PSCALE * 3, height=PLAYER_SIZE * PSCALE, value_count=PLAYER_COLOR_COUNT)
for y, line in enumerate(player_sprite_design):
    x = 0
    for rx, char in enumerate(line):
        if char == " ": continue
        for dx in range(PSCALE):
            for dy in range(PSCALE):
                PLAYER_BMP[x * PSCALE + dx, y * PSCALE + dy] = int(char, 16)
        # print(int(char, 16), end="")
        x += 1
PLAYER_PRESET_COLORS = {
    1: 0xd77bba,
    2: 0xac3232,
    3: 0x222034,
    4: 0xd95763,
    8: 0x00FF00,
    9: 0xFF0000,
    10: 0xbd71a5,
}
PLAYER_COLORS_NO_RAINBOW = {
    5: 0x454580,
    6: 0x505094,
    7: 0x6e98e0,
}
PLAYER_RAINBOW_COLOR_OFFSETS = {
    5: -.05,
    6: .0,
    7: .5,
}
player_rainbow_mode = False


tpflash_shape = displayio.Shape(128, 128)
tpflash_shape_palette = displayio.Palette(1)
tpflash_shape_palette._colors[0]["transparent"] = True
# color is set before adding to game_box
TELEPORT_FLASH_TILE = displayio.TileGrid(tpflash_shape, pixel_shader=tpflash_shape_palette)
TELEPORT_FLASH_DURATION = 8


BLOCKS = {
    B_GRASS: (0, 0),
    B_DIRT: (1, 0),
    B_LOG: (2, 0),
    B_LEAVES: (3, 0),
    B_STONE: (0, 1),
    B_PLANKS: (1, 1),
    B_SAND: (2, 1),
    B_BRICKS: (3, 1),
    B_GLASS: (0, 2),
    B_STAIRSL: (1, 2),
    B_STAIRSR: (2, 2),
    B_FLOWER: (3, 2),
}
BLOCK_IDS = tuple(BLOCKS.keys())
BLOCK_SIZE = 16

od_block_atlas = displayio.OnDiskBitmap("sprites/block_atlas.bmp")
BASCALE = 2

BLOCK_ATLAS = displayio.Bitmap(width=od_block_atlas.width * BASCALE, height=od_block_atlas.height * BASCALE, value_count=(2**32))

for x in range(od_block_atlas.width):
    for y in range(od_block_atlas.height):
        color = od_block_atlas[x, y]
        # color = (color[0], color[1], color[2])
        for dx in range(BASCALE):
            for dy in range(BASCALE):
                BLOCK_ATLAS[x * BASCALE + dx, y * BASCALE + dy] = color

BLOCK_COUNT = (BLOCK_ATLAS.width // BLOCK_SIZE) * (BLOCK_ATLAS.height // BLOCK_SIZE)
def block_coords(i: int):
    w = BLOCK_ATLAS.width // BLOCK_SIZE
    return (i % w, i // w)

def gc(c: int):
    """convert block coord to grid coord"""
    return c * BLOCK_SIZE

def block_tile(id: int, x: int = 0, y: int = 0):
    bx, by = BLOCKS[id]
    w = BLOCK_ATLAS.width // BLOCK_SIZE
    b = displayio.TileGrid(
        BLOCK_ATLAS,
        pixel_shader=None,
        tile_height=BLOCK_SIZE, tile_width=BLOCK_SIZE,
        default_tile=(by * w + bx),
        x=gc(x), y=gc(y),
        # width=2, height=2
    )
    b._current_area = displayio._structs.RectangleStruct(0, 0, 2, 2)
    b._absolute_transform = displayio._structs.TransformStruct(0, 0, 2, 2, 2, False, False, False)
    b._pixel_height = 16
    b._pixel_width = 16
    b._update_transform(displayio._structs.TransformStruct(0, 0, 1, 1, 2))
    return b

break_dialog_bmp = displayio.OnDiskBitmap("sprites/break_dialog.bmp")
BREAK_DIALOG = displayio.TileGrid(
    break_dialog_bmp,
    pixel_shader=break_dialog_bmp.pixel_shader,
    x=64 - break_dialog_bmp.width // 2,
    y=64 - break_dialog_bmp.height // 2 - 40,
)

BUILD_DIALOG = displayio.Group()
buildd_bgo = displayio.Shape(128, 64)
buildd_bgo_palette = displayio.Palette(1)
buildd_bgo_palette[0] = 0x000000
buildd_bg = displayio.Shape(124, 60)
buildd_bg_palette = displayio.Palette(1)
buildd_bg_palette[0] = 0xFFFFFF
BUILD_DIALOG.append(displayio.TileGrid(buildd_bgo, pixel_shader=buildd_bgo_palette))
BUILD_DIALOG.append(displayio.TileGrid(buildd_bg, pixel_shader=buildd_bg_palette, x=2, y=2))
buildd_info_bmp = displayio.OnDiskBitmap("sprites/build_dialog_info.bmp")
buildd_info = displayio.TileGrid(buildd_info_bmp, pixel_shader=buildd_info_bmp.pixel_shader, x=76, y=4)
BUILD_DIALOG.append(buildd_info)
buildd_selout = displayio.Shape(20, 20)
buildd_selout_palette = displayio.Palette(1)
buildd_selout_palette[0] = 0xFF0000
BUILD_DIALOG_SELECTION_OUTLINE = displayio.TileGrid(
    buildd_selout,
    pixel_shader=buildd_selout_palette,
    x=4,
    y=4
)
build_dialog_block_tiles = []
build_dialog_selection_id = 0
def update_build_dialog_selection_display():
    global build_dialog_selection_id

    try: BUILD_DIALOG.remove(BUILD_DIALOG_SELECTION_OUTLINE)
    except: pass
    for tile in build_dialog_block_tiles: BUILD_DIALOG.remove(tile)
    build_dialog_block_tiles.clear()

    bsx, bsy = block_coords(build_dialog_selection_id)
    BUILD_DIALOG_SELECTION_OUTLINE.x = 4 + (bsx * (BLOCK_SIZE + 2))
    BUILD_DIALOG_SELECTION_OUTLINE.y = 4 + (bsy * (BLOCK_SIZE + 2))
    BUILD_DIALOG.append(BUILD_DIALOG_SELECTION_OUTLINE)

    for i, bid in enumerate(BLOCK_IDS):
        bx, by = block_coords(i)
        tile = block_tile(bid, 0, 0)
        tile.x = bx * (BLOCK_SIZE + 2) + 6
        tile.y = by * (BLOCK_SIZE + 2) + 6
        BUILD_DIALOG.append(tile)
        build_dialog_block_tiles.append(tile)
update_build_dialog_selection_display()


def interpolate_colors(color1, color2, num_colors):
    r1, g1, b1 = (color1 >> 16) & 0xFF, (color1 >> 8) & 0xFF, color1 & 0xFF
    r2, g2, b2 = (color2 >> 16) & 0xFF, (color2 >> 8) & 0xFF, color2 & 0xFF

    colors = []
    for i in range(num_colors):
        ratio = i / (num_colors - 1)
        r = int(r1 + (r2 - r1) * ratio)
        g = int(g1 + (g2 - g1) * ratio)
        b = int(b1 + (b2 - b1) * ratio)
        interpolated_color = (r << 16) | (g << 8) | b
        colors.append(interpolated_color)

    return colors

def rainbow_color(percentage):
    percentage = percentage % 1.0

    if percentage < 1/6:
        # Red to Yellow
        r = 255
        g = int(255 * (percentage * 6))
        b = 0
    elif percentage < 2/6:
        r = int(255 * (1 - (percentage - 1/6) * 6))
        g = 255
        b = 0
    elif percentage < 3/6:
        r = 0
        g = 255
        b = int(255 * ((percentage - 2/6) * 6))
    elif percentage < 4/6:
        r = 0
        g = int(255 * (1 - (percentage - 3/6) * 6))
        b = 255
    elif percentage < 5/6:
        r = int(255 * ((percentage - 4/6) * 6))
        g = 0
        b = 255
    else:
        r = 255
        g = 0
        b = int(255 * (1 - (percentage - 5/6) * 6))

    return (r, g, b)

def main():
    global build_dialog_selection_id, player_rainbow_mode

    display_scale = 4
    display = PyGameDisplay(128*display_scale, 128*display_scale, caption="MinePet")
    game_box = displayio.Group(scale=display_scale)
    display.show(game_box)

    # background = displayio.OnDiskBitmap("sprites/background.bmp")
    bg_value_count = 32
    bg_bitmap = displayio.Bitmap(128, 128, value_count=bg_value_count)
    for x in range(128):
        for y in range(128):
            bg_bitmap[x, y] = int((y / 128.0) * bg_value_count)
    bg_px_shader = displayio.Palette(bg_value_count)
    for i, col in enumerate(interpolate_colors(0x2980B9, 0x6DD5Fa, bg_value_count)):
        bg_px_shader[i] = col
    background_tile = displayio.TileGrid(
        bitmap=bg_bitmap,
        pixel_shader=bg_px_shader,
    )

    world = World()
    cam = [0, 0]
    blocks = []
    player = Player(world.random.height_at(0) + 1, world)
    player_tile = [None, 0, None] # [player tilegrid, rainbow counter, player coord text]

    def render_world():
        for b in blocks:
            game_box.remove(b)
        blocks.clear()

        dx, dy = 0, 0
        for x in range(cam[0] - (128 // BLOCK_SIZE), cam[0]):
            dy = 0
            for y in range(cam[1], cam[1] - (128 // BLOCK_SIZE), -1):
                bid = world.block_at(x, y, ignore_collision=True)
                if bid is not None:
                    b = block_tile(bid, dx, dy)
                    blocks.append(b)
                    game_box.append(b)
                dy += 1
            dx += 1
    
    def update_player():
        """Contains call to `render_world()` for camera update!"""

        # print(cam, player.x, player.y)
        # r = False
        # if player.x >= cam[0]:
        #     cam[0] += 8
        #     r = True
        # elif player.x < cam[0] - 8:
        #     cam[0] -= 8
        #     r = True
        # if player.y > cam[1]:
        #     cam[1] += 8
        #     r = True
        # elif player.y <= cam[1] - 8:
        #     cam[1] -= 8
        #     r = True
        # if r: render_world()
        cam[0] = player.x + 4
        cam[1] = player.y + 4
        # print(cam, player.x, player.y)
        render_world()
        
        player.should_update = False

        dx, dy = 0, 0
        for x in range(cam[0] - (128 // BLOCK_SIZE), cam[0]):
            dy = 0
            for y in range(cam[1], cam[1] - (128 // BLOCK_SIZE), -1):
                # print(x, y, player.x, player.y)
                if x == player.x and y == player.y:
                    player_tile[0].x = gc(dx)
                    player_tile[0].y = gc(dy)
                dy += 1
            dx += 1
        
        player.should_render = True

    def render_player():
        if player_tile[0] is not None:
            game_box.remove(player_tile[0])

        player_palette = displayio.Palette(PLAYER_COLOR_COUNT)
        player_palette._colors[0] = player_palette._make_color(0x0, transparent=True)
        player_palette._update_rgba(0)
        player_tile[1] += .01
        if player_tile[1] > 1: player_tile[1] -= 1
        for i in range(1, PLAYER_COLOR_COUNT):
            if i in PLAYER_PRESET_COLORS or not player_rainbow_mode:
                player_palette[i] = PLAYER_PRESET_COLORS[i] if i in PLAYER_PRESET_COLORS else PLAYER_COLORS_NO_RAINBOW[i] if i in PLAYER_COLORS_NO_RAINBOW else 0x0
            else:
                player_palette[i] = rainbow_color(player_tile[1] + (PLAYER_RAINBOW_COLOR_OFFSETS[i] if i in PLAYER_RAINBOW_COLOR_OFFSETS else .0))
        player_tile[0] = displayio.TileGrid(
            PLAYER_BMP,
            pixel_shader=player_palette,
            tile_height=PLAYER_SIZE*PSCALE, tile_width=PLAYER_SIZE*PSCALE,
            default_tile=player.texture_tile,
            x=player_tile[0].x if player_tile[0] is not None else 0,
            y=player_tile[0].y if player_tile[0] is not None else 0,
        )
        
        if player.looking == P_LEFT: player_tile[0].flip_x = True
        
        if player_tile[2] is not None:
            game_box.remove(player_tile[2])
            player_tile[2] = None
        if player.noclip:
            try:
                player_tile[2] = adafruit_display_text.label.Label(terminalio.FONT, text=f"x: {player.x}, y: {player.y}")
                game_box.append(player_tile[2])
            except:
                if player.should_render: print("Player coordinates: x:", player.x, "- y:", player.y)
        
        game_box.append(player_tile[0])

        player.should_render = False


    def move_camera(cam: list[int, int], dx: int = 0, dy: int = 0):
        cam[0] += dx
        cam[1] += dy
        render_world()

    # for x in range(8):
    #     b = block_tile(B_GRASS)
    #     b.y = 5 * BLOCK_SIZE
    #     b.x = x * BLOCK_SIZE
    #     game_box.append(b)
    #     for y in range(6, 8):
    #         b = block_tile(B_DIRT)
    #         b.y = y * BLOCK_SIZE
    #         b.x = x * BLOCK_SIZE
    #         game_box.append(b)

    # for bid in BLOCKS:
    #     bx, by = BLOCKS[bid]
    #     block = block_tile(bid)

    #     block.x = bx * (BLOCK_SIZE + 4)
    #     block.y = by * (BLOCK_SIZE + 4)
        
    #     game_box.append(block)
    
    # for block in gen_tree(4, 4): game_box.append(block)
    
    # game_box[1].y = 20

    # render_world()

    splash_bmp = displayio.OnDiskBitmap("sprites/splash.bmp")
    splash = displayio.TileGrid(splash_bmp, pixel_shader=splash_bmp.pixel_shader)

    c = 0
    left_down = False
    right_down = False
    middle_down = False
    move_cooldown = 0
    ticking = True
    showing_splash = True
    dialog_open = None
    input_cooldown = 0
    jump_countdown = 0
    tpflash_remove_in = -1
    forcefall_countdown = 0
    prevent_toggling_rainbow_mode = False

    if showing_splash:
        game_box.append(splash)
    else:
        game_box.append(background_tile)
        render_player()
        update_player()

    while True:
        time.sleep(1/60)
        for event in pygame.event.get():
            if event.type == pgl.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN and input_cooldown == 0:
                if showing_splash:
                    showing_splash = False
                    game_box.pop()
                    game_box.append(background_tile)
                    world.random.seed = 100 if event.key == pygame.K_a else 201 if event.key == pygame.K_d else 300
                    render_player()
                    update_player()
                    continue
                # if event.key in [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s]:
                #     move_camera(cam, *{ pygame.K_a: (-1, 0), pygame.K_d: (1, 0), pygame.K_s: (0, -1), pygame.K_w: (0, 1) }[event.key])
                if event.key == pygame.K_a:
                    left_down = True
                if event.key == pygame.K_d:
                    right_down = True
                if event.key == pygame.K_SPACE:
                    middle_down = True
                prevent_toggling_rainbow_mode = False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    left_down = False
                if event.key == pygame.K_d:
                    right_down = False
                if event.key == pygame.K_SPACE:
                    middle_down = False
        
        close_dialog = False
        if dialog_open == "break" and input_cooldown == 0:
            if left_down and not right_down:
                if middle_down:
                    world.break_block(player.x, player.y - 1)
                else:
                    world.break_block(player.x - 1, player.y)
                close_dialog = True
                game_box.remove(BREAK_DIALOG)
            elif right_down and not left_down:
                if middle_down:
                    world.break_block(player.x, player.y + 1)
                else:
                    world.break_block(player.x + 1, player.y)
                close_dialog = True
                game_box.remove(BREAK_DIALOG)
        elif dialog_open == "build" and input_cooldown == 0:
            if left_down and not right_down:
                build_dialog_selection_id = (build_dialog_selection_id - 1) if build_dialog_selection_id > 0 else len(BLOCKS) - 1
                update_build_dialog_selection_display()
                input_cooldown = 5
            elif right_down and not left_down:
                build_dialog_selection_id = (build_dialog_selection_id + 1) if build_dialog_selection_id < len(BLOCKS) - 1 else 0
                update_build_dialog_selection_display()
                input_cooldown = 5
            elif middle_down and not left_down and not right_down:
                world.place_block(player.x, player.y, BLOCK_IDS[build_dialog_selection_id])
                close_dialog = True
                game_box.remove(BUILD_DIALOG)
                BUILD_DIALOG._update_transform(None)
                if not player.noclip and not BLOCK_IDS[build_dialog_selection_id] in NO_COLLISION_BLOCKS:
                    up = 1
                    while world.block_at(player.x, player.y + up) is not None and up < 30:
                        up += 1
                    player.move(0, up)
        if close_dialog:
            dialog_open = None
            ticking = True
            input_cooldown = 10
            middle_down = False
            left_down = False
            right_down = False
            player.move(0, 0)
            update_player()

        if not showing_splash and ticking and not close_dialog:
            if move_cooldown > 0: move_cooldown -= 1

            if left_down:
                if not middle_down and not right_down and move_cooldown == 0:
                    ledgeup = not player.noclip and (world.block_at(player.x - 1, player.y) is not None and world.block_at(player.x - 1, player.y + 1) is None)
                    if player.move(-1, 1 if ledgeup else 0):
                        move_cooldown = 8 if not player.noclip else 3
                        if ledgeup and world.block_at(player.x + 1, player.y) is not None:
                            tpflash_remove_in = TELEPORT_FLASH_DURATION
                elif middle_down and not right_down and dialog_open is None:
                    game_box.append(BUILD_DIALOG)
                    ticking = False
                    dialog_open = "build"
                    input_cooldown = 10
                    middle_down = False
                    left_down = False
                    right_down = False
            elif right_down:
                if not middle_down and not left_down and move_cooldown == 0:
                    ledgeup = not player.noclip and (world.block_at(player.x + 1, player.y) is not None and world.block_at(player.x + 1, player.y + 1) is None)
                    if player.move(1, 1 if ledgeup else 0):
                        move_cooldown = 8 if not player.noclip else 3
                        if ledgeup and world.block_at(player.x - 1, player.y) is not None:
                            tpflash_remove_in = TELEPORT_FLASH_DURATION
                elif middle_down and not left_down and dialog_open is None:
                    game_box.append(BREAK_DIALOG)
                    ticking = False
                    dialog_open = "break"
                    input_cooldown = 10
                    middle_down = False
                    left_down = False
                    right_down = False
            elif middle_down:
                if not left_down and not right_down:
                    if player.falling_frame > 0 or (player.jump_frame > 0 and player.jump_frame < JUMP_FALL_FRAMES * .75):
                        if forcefall_countdown == 0: forcefall_countdown = 20
                        elif forcefall_countdown == 1:
                            down = 0
                            while world.block_at(player.x, player.y - down - 1) is None:
                                down += 1
                            player.move(0, -down)
                        
                        if forcefall_countdown > 0: forcefall_countdown -= 1
                        jump_countdown = 0
                    else:
                        if jump_countdown == 0: jump_countdown = 10
                        elif jump_countdown > 1: jump_countdown -= 1
                        elif jump_countdown == 1:
                            if player.noclip: player.move(0, 1)
                            else: player.jump()
                            jump_countdown = 0
                        forcefall_countdown = 0
            
            # print(left_down, middle_down, right_down)
            if left_down and right_down and not middle_down and not prevent_toggling_rainbow_mode:
                player_rainbow_mode = not player_rainbow_mode
                # left_down = False
                # right_down = False
                input_cooldown = 2
                prevent_toggling_rainbow_mode = True
                if not player_rainbow_mode: player.should_render = True
            elif left_down and right_down and middle_down:
                player_rainbow_mode = False
                prevent_toggling_rainbow_mode = True
                middle_down = False
                player.toggle_noclip()

            if not middle_down:
                jump_countdown = 0
                forcefall_countdown = 0

            if ticking: player.tick()
            
            if player.should_update: update_player()

        if input_cooldown > 0:
            input_cooldown -= 1
        
        if not showing_splash and (player_rainbow_mode or player.should_render): render_player()

        if tpflash_remove_in >= 0:
            tpflash_remove_in -= 1
            try: game_box.remove(TELEPORT_FLASH_TILE)
            except: pass
            if tpflash_remove_in > 0:
                TELEPORT_FLASH_TILE.pixel_shader._colors[0]["rgba"] = (255, 255, 255, int(255 * tpflash_remove_in / TELEPORT_FLASH_DURATION))
                game_box.append(TELEPORT_FLASH_TILE)
                # print("FLASH!")

        display._pygame_refresh()

if __name__ == "__main__":
    # try:
    #     main()
    # except Exception as e:
    #     import traceback
    #     traceback.print_exception(e)
    try:
        main()
    except pygame.error as e:
        if not str(e).endswith("quit"): raise e

