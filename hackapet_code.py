import os
import time
import pygame
from blinka_displayio_pygamedisplay import PyGameDisplay
import displayio
import random
#thanks to my akiva for helping me set this up, i love you sm
# Initialize Pygame
pygame.init()

# Set up the display
display = PyGameDisplay(width=128, height=128)
splash = displayio.Group()
display.show(splash)

forest_background = displayio.OnDiskBitmap("C:/Users/Nili/Downloads/forest_background.bmp")

bg_sprite = displayio.TileGrid(
    forest_background, 
    pixel_shader=forest_background.pixel_shader
)

splash.append(bg_sprite)

teddy_sheet = displayio.OnDiskBitmap("C:/Users/Nili/Downloads/teddywalking!.bmp")

# Correctly declare tile_width and tile_height as integers
tile_width = 32
tile_height = 32

teddy_sprite = displayio.TileGrid(
    teddy_sheet,
    pixel_shader=teddy_sheet.pixel_shader,
    width=1,
    height=1,
    tile_width=tile_width,
    tile_height=tile_height,
    default_tile=0,
    x=int((display.width - tile_width) // 2),
    y=int(display.height - tile_height - 10),
)

splash.append(teddy_sprite)
frame = 0
speed = 4 
full = 0
game_over = False
keys = pygame.key.get_pressed()
# ADDING THE ICONS THINGIES
food = []
shoes = []
pill_bitmap = displayio.OnDiskBitmap("C:/Users/Nili/Downloads/pill.bmp")
def spawn_pill():
    x_position = random.randint(0, 128)
    y_position = 128
    pill_sprite = displayio.TileGrid(
     pill_bitmap,
     pixel_shader=pill_bitmap.pixel_shader,
     width=1,
     height=1,
     tile_width=16,
     tile_height=16,
     default_tile=0,
     x=random.randint(0, display.width - 16),
     y=random.randint(0, display.height - 16),
    )
    splash.append(pill_sprite)
    food.append(pill_sprite)
shoe_bitmap = displayio.OnDiskBitmap("C:/Users/Nili/Downloads/shoe.bmp")
def spawn_shoe():
    x_position = random.randint(0,128)
    y_position = 0
    shoe_sprite = displayio.TileGrid(
     shoe_bitmap,
     pixel_shader=shoe_bitmap.pixel_shader,
     width=1,
     height=1,
     tile_width=16,
     tile_height=16,
     default_tile=0,
     x=random.randint(0, display.width - 16),
     y=random.randint(0, display.height - 16),
    )
    splash.append(shoe_sprite)
    shoes.append(shoe_sprite)
win_screen = displayio.TileGrid(
    displayio.OnDiskBitmap("C:/Users/Nili/Downloads/youwin.bmp"),
    pixel_shader=displayio.OnDiskBitmap("C:/Users/Nili/Downloads/youwin.bmp").pixel_shader,
    width=1,
    height=1,
    tile_width=128,
    tile_height=128,
    x=0,
    y=0
)
challah_bitmap = displayio.OnDiskBitmap("C:/Users/Nili/Downloads/challah.bmp")
challah_sprite = displayio.TileGrid(
    challah_bitmap,
    pixel_shader=challah_bitmap.pixel_shader,
    width=1,
    height=1,
    tile_width=32,
    tile_height=32,
    x=0,
    y=0
)
def spawn_challah():
    x_position = random.randint(0, 128)
    y_position = 128
    challah_sprite = displayio.TileGrid(
     challah_bitmap,
     pixel_shader=challah_bitmap.pixel_shader,
     width=1,
     height=1,
     tile_width=16,
     tile_height=16,
     default_tile=0,
     x=random.randint(0, display.width - 16),
     y=random.randint(0, display.height - 16),
    )
    splash.append(challah_sprite)
    food.append(challah_sprite)
meter_empty = displayio.OnDiskBitmap("C:/Users/Nili/Downloads/meter empty.bmp")
meter_full = displayio.OnDiskBitmap("C:/Users/Nili/Downloads/meter full.bmp")
meter_quarter = displayio.OnDiskBitmap("C:/Users/Nili/Downloads/meter quarter.bmp")
meter_three_quarters = displayio.OnDiskBitmap("C:/Users/Nili/Downloads/meter three quarters.bmp")
meter_half = displayio.OnDiskBitmap("C:/Users/Nili/Downloads/meter half.bmp")
meter_sprite = displayio.TileGrid(
    meter_empty,
    pixel_shader=meter_empty.pixel_shader,
    width=1,
    height=1,
    tile_width=32,
    tile_height=32,
    x=0,
    y=0
)
splash.append(meter_sprite)
def check_collision(sprite1, sprite2):
    return (
        sprite1.x < sprite2.x + 32 and
        sprite1.x + 32 > sprite2.x and
        sprite1.y < sprite2.y + 32 and
        sprite1.y + 32 > sprite2.y
    )
last_spawn_time = time.time()
spawn_pill()
spawn_shoe()
spawn_challah()
# i THINK my game is gonna be like collecting pills to get points and avoiding things that take points down
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    keys = pygame.key.get_pressed()
    if game_over == False:
        if keys[pygame.K_LEFT]:
            teddy_sprite.x -= speed
        if keys[pygame.K_RIGHT]:
            teddy_sprite.x += speed
        if keys[pygame.K_UP]:
            teddy_sprite.y -=  speed
            time.sleep(0.05)
            teddy_sprite.y += speed
        for pill in food:
            pill.y += 1
            if pill.y > display.height:
                splash.remove(pill)
                food.remove(pill)
            if check_collision(teddy_sprite, pill):
                splash.remove(pill)
                food.remove(pill)
                full += 2
        for shoe in shoes:
            shoe.y += 1
            if shoe.y > display.height:
                splash.remove(shoe)
                shoes.remove(shoe)
            if check_collision(teddy_sprite, shoe):
                splash.remove(shoe)
                shoes.remove(shoe)
                full -= 1
        for challah in food:
            challah.y += 1
            if challah.y > display.height:
                splash.remove(challah)
                food.remove(challah)
            if check_collision(teddy_sprite, challah):
                splash.remove(challah)
                food.remove(challah)
                full += 1
        if full == 8:
            splash.remove(meter_sprite)
            meter_sprite = displayio.TileGrid(
                meter_full,
                pixel_shader=meter_full.pixel_shader,
                width=1,
                height=1,
                tile_width=32,
                tile_height=32,
                x=0,
                y=0
            )
            display.show(win_screen)
            time.sleep(3)
            full = 0
            game_over = True
        elif full == 2:
            splash.remove(meter_sprite)
            meter_sprite = displayio.TileGrid(
                meter_quarter,
                pixel_shader=meter_quarter.pixel_shader,
                width=1,
                height=1,
                tile_width=32,
                tile_height=32,
                x=0,
                y=0
            )
            splash.append(meter_sprite)
        elif full == 4:
            splash.remove(meter_sprite)
            meter_sprite = displayio.TileGrid(
                meter_half,
                pixel_shader=meter_half.pixel_shader,
                width=1,
                height=1,
                tile_width=32,
                tile_height=32,
                x=0,
                y=0
            )
            splash.append(meter_sprite)
        elif full == 6:
            splash.remove(meter_sprite)
            meter_sprite = displayio.TileGrid(
                meter_three_quarters,
                pixel_shader=meter_three_quarters.pixel_shader,
                width=1,
                height=1,
                tile_width=32,
                tile_height=32,
                x=0,
                y=0
            )
        elif full == 0:
            splash.remove(meter_sprite)
            meter_sprite = displayio.TileGrid(
                meter_empty,
                pixel_shader=meter_empty.pixel_shader,
                width=1,
                height=1,
                tile_width=32,
                tile_height=32,
                x=0,
                y=0
            )
            splash.append(meter_sprite)
    current_time = time.time()
    if current_time - last_spawn_time >= 5:
        spawn_pill()
        spawn_shoe()
        spawn_shoe()
        spawn_challah()
        spawn_challah()
        last_spawn_time = current_time
    display.refresh()
    time.sleep(0.01)