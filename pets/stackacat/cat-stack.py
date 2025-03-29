import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
import pygame
import time
from adafruit_display_text import label
import adafruit_imageload
from adafruit_bitmap_font import bitmap_font
import random

display = PyGameDisplay(width=128, height=128)
splash = displayio.Group()
display.show(splash)

pygame.init()

background = displayio.OnDiskBitmap("sky.bmp")
bg_sprite = displayio.TileGrid(
    background,
    pixel_shader=background.pixel_shader,
    width=4,
    height=1,
    tile_width=128,
    tile_height=512,
    x=0,
    y=-324
)
splash.append(bg_sprite)

sprite, palette = adafruit_imageload.load("cat-60.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette)
cat_first_sprite = displayio.TileGrid(
    sprite, 
    pixel_shader=palette, 
    width=1, 
    height=1, 
    tile_width=60, 
    tile_height=16, 
    x=34, 
    y=112
)
palette.make_transparent(0)
splash.append(cat_first_sprite)

sprite, palette = adafruit_imageload.load("cat-fall.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette)
fall = displayio.TileGrid(
        sprite, 
        pixel_shader=palette, 
        width=1, 
        height=1, 
        tile_width=40, 
        tile_height=16,
        x=0,
        y=96
)
palette.make_transparent(0)

sprite, palette = adafruit_imageload.load("cat-win.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette)
win = displayio.TileGrid(
        sprite, 
        pixel_shader=palette, 
        width=1, 
        height=1, 
        tile_width=40, 
        tile_height=40,
        x=0,
        y=56
)
palette.make_transparent(0)

def spawn_cat(width):
    # even cat
    if width % 2 != 0:
        width -= 1
    
    sprite, palette = adafruit_imageload.load(f"cat-{width}.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette)
    cat_sprite = displayio.TileGrid(
        sprite, 
        pixel_shader=palette, 
        width=1, 
        height=1, 
        tile_width=width, 
        tile_height=16,
        x=random.randint(0, 128 - width),
        y=96
    )
    palette.make_transparent(0)
    splash.append(cat_sprite)
    return cat_sprite

# fake camera move down
def next_cat():
    if not isWin:
        for i in range(16):
            for sprite in splash:
                if isinstance(sprite, displayio.TileGrid):
                    sprite.y += 1
            time.sleep(0.01)

# width for next cat
def check_stack(cat1, cat2):
    cat1_x = cat1.x
    cat1_y = cat1.y
    cat1_width = cat1.tile_width

    cat2_x = cat2.x
    cat2_y = cat2.y
    cat2_width = cat2.tile_width

    if cat1_y + 16 == cat2_y:
        if (cat1_x < cat2_x + cat2_width and 
            cat1_x + cat1_width > cat2_x):
            overlap = min(cat1_x + cat1_width, cat2_x + cat2_width) - max(cat1_x, cat2_x)
            if overlap <= 3:
                return 4
            return overlap
    return 0

# cat go left and right
def move_cat(cat, speed):
    if cat.x >= 128 - cat.tile_width:
        speed = -abs(speed)
    elif cat.x <= 0:
        speed = abs(speed)
    cat.x += speed
    return speed

def move_text(text):
    if text.y <= 56:
        direction = 1
    else:
        direction = -1
    text.y += direction

# sad
def cat_fall(cat):
    cat.y += 1

font = bitmap_font.load_font("ib8x16u.bdf")
text = "Press down key \nto start"
text_area = label.Label(font, text=text, color=0x000000, x=12, y=56)
splash.append(text_area)

start = False
isLoopOne = True
moving_cat = spawn_cat(60)
moving_cat.y = 96
last_stacked_cat = cat_first_sprite
last_text = time.monotonic()
fall_mode = False
isWin = False
cat_v = 2

while True:
    if display.check_quit():
        pygame.quit()
        exit()

    now = time.monotonic()

    # animate text
    if now - last_text > 0.5:
        move_text(text_area)
        last_text = now

    # cat fall
    if fall_mode:
        cat_fall(fall)
        if fall.y > 128:
            text_area.x = 28
            text_area.color = 0x0074D9
            text_area.text = "Game Over\n-> Restart"
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT]:
                # restart
                if fall in splash:
                    splash.remove(fall)
                
                # remove all cats (sowy cant figure out)
                for sprite in splash[:]:
                    if isinstance(sprite, displayio.TileGrid) and sprite != bg_sprite and sprite != text_area:
                        splash.remove(sprite)

                fall.y = 96
                moving_cat = spawn_cat(60)
                moving_cat.y = 96
                last_stacked_cat = cat_first_sprite
                fall_mode = False

                splash.append(cat_first_sprite)

                text_area.x = 12
                text_area.y = 56
                text_area.color = 0x000000
                text_area.text = "Press down key \nto start"

                start = False
                isLoopOne = True
                bg_sprite.y = -324
                cat_first_sprite.y = 112
                moving_cat.y = 96
                continue
                
        time.sleep(0.05)
        continue

    # check for win
    if bg_sprite.y >= 50:
        win.x = last_stacked_cat.x
        if moving_cat in splash:
            splash.remove(moving_cat)
        splash.append(win)
        isWin = True

    if isWin:
        next_cat()
        time.sleep(1)
        text_area.x = 32
        text_area.y = 30
        text_area.color = 0x0074D9
        text_area.text = "You Win!"
        continue

    keys = pygame.key.get_pressed()     

    if keys[pygame.K_DOWN]:
        if not start:
            start = True
            text_area.text = ""
        else:
            overlap = check_stack(moving_cat, last_stacked_cat)

            if overlap == 0:
                # fall like a cartoon cat
                time.sleep(0.5)
                fall.x = moving_cat.x
                splash.append(fall)
                splash.remove(moving_cat)
                fall_mode = True
            else:
                last_stacked_cat = moving_cat

                if isLoopOne:
                    moving_cat.y = 96
                    isLoopOne = False
                else:
                    next_cat()
            
                moving_cat = spawn_cat(overlap)
                moving_cat.y = 80
                time.sleep(0.2)
    
    cat_v = move_cat(moving_cat, cat_v)
    time.sleep(0.05)