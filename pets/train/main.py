import random

import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
import pygame
from adafruit_display_text import label
import time
from adafruit_bitmap_font import bitmap_font

pygame.init()

display = PyGameDisplay(width=128, height=128)
splash = displayio.Group()
display.show(splash)

background_files = ["plains.bmp", "plainstodesert.bmp", "desert.bmp", "deserttomountains.bmp", "mountains.bmp",
                    "mountainstoplains.bmp"]
backgrounds = [displayio.OnDiskBitmap(file) for file in background_files]

bg_sprite_1 = displayio.TileGrid(
    backgrounds[0], pixel_shader=backgrounds[0].pixel_shader,
    width=1, height=1, tile_width=256, tile_height=128
)
bg_sprite_2 = displayio.TileGrid(
    backgrounds[1], pixel_shader=backgrounds[1].pixel_shader,
    width=1, height=1, tile_width=256, tile_height=128
)
platform_bitmap = displayio.OnDiskBitmap("platform.bmp")
platform_sprite = displayio.TileGrid(
    platform_bitmap, pixel_shader=platform_bitmap.pixel_shader,
    width=1, height=1, tile_width=92, tile_height=61
)
platform_sprite.x = 128
platform_sprite.y = 20
train_bitmap = displayio.OnDiskBitmap("train.bmp")
train_sprite = displayio.TileGrid(
    train_bitmap, pixel_shader=train_bitmap.pixel_shader,
    width=1, height=1, tile_width=128, tile_height=128
)
splash.append(bg_sprite_1)
splash.append(bg_sprite_2)
splash.append(platform_sprite)
splash.append(train_sprite)

progress_bar_width = 128
progress_bar_height = 8
progress_color = 0x00FF00
border_padding = 4
border_color = 0xFFFFFF

border_bitmap = displayio.Bitmap(progress_bar_width,
                                 progress_bar_height + 2 * border_padding, 1)
border_palette = displayio.Palette(1)
border_palette[0] = border_color
progress_border = displayio.TileGrid(border_bitmap, pixel_shader=border_palette)
progress_border.y = 8 - border_padding
splash.append(progress_border)

progress_bar_bitmap = displayio.Bitmap(progress_bar_width, progress_bar_height, 1)
progress_bar_palette = displayio.Palette(1)
progress_bar_palette[0] = progress_color
progress_bar = displayio.TileGrid(progress_bar_bitmap, pixel_shader=progress_bar_palette)
progress_bar.y = 8
splash.append(progress_bar)

FONT = bitmap_font.load_font("TenStamps-16.bdf")

bar_label = label.Label(FONT, text="HP", color=0xFFFFFF, x=1, y=11)
splash.append(bar_label)

x_offset = 0
current_bg = 0
next_bg = 1
bg_width = 256
screen_width = 128
train_speed = 1

bg_sprite_2.x = screen_width

progress_decrement = 1
progress_bar_current_width = progress_bar_width
platform_x = screen_width
platform_on_screen = False

game_over = False
score = 0
score_label = None
restart_label = None


title_label1 = label.Label(FONT, text="Train", color=0xFFFFFF, x=28, y=30)
title_label2 = label.Label(FONT, text="Game", color=0xFFFFFF, x=36, y=46)
start_label = label.Label(FONT, text="¸Start", color=0xFFFFFF, x=21, y=80)
splash.append(start_label)
splash.append(title_label1)
splash.append(title_label2)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_DOWN]:
        splash.remove(start_label)
        splash.remove(title_label1)
        splash.remove(title_label2)
        break
    time.sleep(0.1)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    if progress_bar_current_width >= 256:
        game_over = True
        if score_label is None or restart_label is None:
            score_label = label.Label(FONT, text=f"Score: \n{score}", color=0xFFFFFF, x=20, y=30)
            restart_label = label.Label(FONT, text="¸Restart", color=0xFFFFFF, x=6, y=80)
            splash.append(score_label)
            splash.append(restart_label)
        train_speed = 0

    x_offset -= train_speed
    bg_sprite_1.x = x_offset
    bg_sprite_2.x = x_offset + bg_width
    if platform_on_screen:
        platform_x -= train_speed
    platform_sprite.x = platform_x

    if x_offset <= -bg_width:
        x_offset = 0

        if random.randint(0, 2) == 0 and current_bg % 2 == 0:
            next_bg = current_bg
            bg_sprite_1.bitmap = backgrounds[current_bg]
            bg_sprite_2.bitmap = backgrounds[next_bg]
            bg_sprite_2.x = bg_width
        else:
            current_bg = (current_bg + 1) % len(backgrounds)
            next_bg = (current_bg + 1) % len(backgrounds)
            bg_sprite_1.bitmap = backgrounds[current_bg]
            bg_sprite_2.bitmap = backgrounds[next_bg]
            bg_sprite_2.x = bg_width

        if random.randint(0, 4) == 0:
            platform_sprite.x = screen_width
            platform_x = screen_width
            platform_on_screen = True
        else:
            platform_on_screen = False

        progress_bar_current_width += progress_decrement * train_speed
        score += 1
    progress_bar.x = 128 - progress_bar_current_width
    progress_bar_bitmap = displayio.Bitmap(progress_bar_current_width, progress_bar_height, 1)

    if not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if train_speed > 0:
                train_speed -= 1
        elif keys[pygame.K_RIGHT]:
            if train_speed < 10:
                train_speed += 1
        elif keys[pygame.K_DOWN]:
            if 100 > platform_x > -50 and train_speed == 0:
                progress_bar_current_width = max(128, progress_bar_current_width - 10)
        elif keys[pygame.K_UP]: # DEBUG ONLY - remove in final version
            progress_bar_current_width = 255
    else:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            score = 0
            progress_bar_current_width = 128
            train_speed = 1
            game_over = False
            score_label.hidden = True
            restart_label.hidden = True
            splash.remove(score_label)
            splash.remove(restart_label)
            score_label = None
            restart_label = None

    time.sleep(0.1)
