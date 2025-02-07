"""
sarahs_space_game

Copyright © 2024 Sarah C <sarah@srh.dog>
This work is free. You can redistribute it and/or modify it under the
terms of the Do What The Fuck You Want To Public License, Version 2,
as published by Sam Hocevar. See the LICENSE.md file for more details.
"""

from math import cos, pi, sin, sqrt
from random import randint
from time import monotonic, sleep
import sys
from blinka_displayio_pygamedisplay import PyGameDisplay
import pygame
import displayio

IS_CIRCUITPYTHON = sys.implementation.name == "circuitpython"

if IS_CIRCUITPYTHON:
    def dummy(*_args, **_kwargs):
        pass
    
    debug = dummy
    warning = dummy
    error = dummy
else:
    import logging
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    
    debug = logger.debug
    warning = logger.warning
    error = logger.error

ACCELERATION_FACTOR = 1.2
ACCELERATION_CONSTANT = 400
ACCELERATION_CEILING = 5000
ROTATIONAL_VELOCITY_FACTOR = 2
VELOCITY_DECAY_FACTOR = -0.7
VELOCITY_DECAY_CONSTANT = 490
DISPLAY_SCALING_FACTOR = 3
WIDTH = 128

spaceship = displayio.OnDiskBitmap("spaceship.bmp")


class Palette:
    NOT_BLACK = 0x313950
    LESS_BLACK = 0x434B65
    EVEN_LESS_BLACK = 0x5B647E
    NOT_WHITE = 0xCBD8FF

# Setup and initialisation code
display = PyGameDisplay(
    width=WIDTH*DISPLAY_SCALING_FACTOR,
    height=WIDTH*DISPLAY_SCALING_FACTOR,
    hw_accel=False
)
splash = displayio.Group(scale=DISPLAY_SCALING_FACTOR)
display.show(splash)

dt = 0  # in ms

bitmap = displayio.Bitmap(WIDTH*2, WIDTH*2, 2)
for i in range((WIDTH*2)**2):
    bitmap[i // (WIDTH*2), i % (WIDTH*2)] = randint(0, 2)

# hundredths of a pixel per sec
velocity_x = 0
velocity_y = 0
orientation = 0
global_x = 0
global_y = 0

def create_bg():
    global global_x
    global global_y
    global velocity_x
    global velocity_y
    
    color_palette = displayio.Palette(3)
    color_palette[0] = Palette.NOT_BLACK
    color_palette[1] = Palette.LESS_BLACK
    color_palette[2] = Palette.EVEN_LESS_BLACK
    
    factor_x = 1 if velocity_x < 0 else -1
    factor_y = 1 if velocity_x < 0 else -1
    
    velocity_x += VELOCITY_DECAY_CONSTANT * dt * factor_x
    velocity_y += VELOCITY_DECAY_CONSTANT * dt * factor_y
    velocity_x *= 1 + VELOCITY_DECAY_FACTOR * dt
    velocity_y *= 1 + VELOCITY_DECAY_FACTOR * dt
    
    print(f"velocity {velocity_x} {velocity_y}")
    
    global_x += velocity_x * dt
    global_y += velocity_y * dt
    
    whole_x = global_x // 100
    whole_y = global_y // 100
    
    tile_width = WIDTH // 2
    
    viewport_x = int(whole_x % tile_width)
    viewport_y = int(whole_y % tile_width)
    
    tile_x = int((whole_x // tile_width) % 4)
    tile_y = int((whole_y // tile_width) % 4)
    
    sprite = displayio.TileGrid(
        bitmap,
        pixel_shader=color_palette,
        x=viewport_x - tile_width,
        y=viewport_y - tile_width,
        tile_width=tile_width,
        tile_height=tile_width,
        width=4,
        height=4
    )
    
    for x in range(4):
        for y in range(4):
            sprite[x, y] = (((y - tile_y) % 4) * 4) + ((x - tile_x) % 4)
    
    return sprite


def render(group: displayio.Group):
    group.append(create_bg())
    
    color_palette = displayio.Palette(2)
    color_palette.make_transparent(0)
    color_palette[1] = Palette.NOT_WHITE
    
    player = displayio.TileGrid(
        spaceship,
        x=(WIDTH//2)-16,
        y=(WIDTH//2)-16,
        tile_width=32,
        tile_height=32,
        width=17,
        height=1,
        default_tile=16,
        pixel_shader=color_palette
    )
    
    player[0] = int(orientation // (pi / 8))
    
    group.append(player)
    


last_it = monotonic()
last_dt_it = last_it
while True:
    # Time tracking nonsense
    cur_it = monotonic()
    rt = (cur_it - last_it) * 1000
    dt = (cur_it - last_dt_it)
    if rt > (1000/60):
        warning(f"took {rt:1f}ms - over target")
    else:
        debug(f"took {rt:1f}ms")
        
    last_dt_it = monotonic()
    
    wait_time = (1/60) - (cur_it - last_it)
    
    if wait_time > 0:
        debug(f"sleeping {wait_time*1000:1f}ms")
        sleep(wait_time)
    
    last_it = monotonic()
    
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT] and keys[pygame.K_RIGHT]:
        # And who said trigonometry wasn't useful!
        velocity = sqrt(velocity_x**2 + velocity_y**2)
        velocity_mult_coef = (velocity * (1 + (ACCELERATION_FACTOR * dt))) + ACCELERATION_CONSTANT * dt
        velocity_x += sin(orientation) * velocity_mult_coef
        velocity_y += cos(orientation) * velocity_mult_coef
        velocity_x = max(min(velocity_x, ACCELERATION_CEILING), -ACCELERATION_CEILING)
        velocity_y = max(min(velocity_y, ACCELERATION_CEILING), -ACCELERATION_CEILING)
        
    elif keys[pygame.K_LEFT]:
        orientation = (orientation + (ROTATIONAL_VELOCITY_FACTOR * dt)) % (pi * 2)
        
    elif keys[pygame.K_RIGHT]:
        orientation = (orientation - (ROTATIONAL_VELOCITY_FACTOR * dt)) % (pi * 2)
    
    group = displayio.Group(scale=DISPLAY_SCALING_FACTOR)
    render(group)
    display.show(group)
    
    if display.check_quit():
        break
