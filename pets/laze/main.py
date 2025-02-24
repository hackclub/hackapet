import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
import pygame
import time
from adafruit_display_text import label
import random

pygame.init()

display = PyGameDisplay(width=128, height=128)
splash = displayio.Group()
display.show(splash)

bg = displayio.OnDiskBitmap("bg.bmp")
bg_sprite = displayio.TileGrid(bg, pixel_shader=bg.pixel_shader)
splash.append(bg_sprite)

player0 = displayio.OnDiskBitmap("player0.bmp")

tile_width = 32
tile_height = 32

player0 = displayio.TileGrid(
    player0,
    pixel_shader=player0.pixel_shader,
    width=1,
    height=1,
    tile_width=tile_width,
    tile_height=tile_height,
    default_tile=0,
    x=(display.width - tile_width) // 2,  
    y=display.height - tile_height - 10     
)

splash.append(player0)

fireball_bitmap = displayio.OnDiskBitmap("fireball.bmp")
lava_bitmap = displayio.OnDiskBitmap("lava.bmp")

fireballs = []
lavas = []

def spawn_fireball():
    x_position = random.randint(0, display.width - fireball_bitmap.width)
    fireball = displayio.TileGrid(
        fireball_bitmap,
        pixel_shader=fireball_bitmap.pixel_shader,
        width=1,
        height=1,
        tile_width=fireball_bitmap.width,
        tile_height=fireball_bitmap.height,
        x=x_position,
        y=-32
    )
    fireballs.append(fireball)
    splash.append(fireball)

def spawn_lava():
    x_position = random.randint(0, display.width - lava_bitmap.width)
    lava = displayio.TileGrid(
        lava_bitmap,
        pixel_shader=lava_bitmap.pixel_shader,
        width=1,
        height=1,
        tile_width=lava_bitmap.width,
        tile_height=lava_bitmap.height,
        x=x_position,
        y=-32
    )
    lavas.append(lava)
    splash.append(lava)

# Function to check for collisions
def check_collision(sprite1, sprite2):
    return (
        sprite1.x < sprite2.x + 32 and
        sprite1.x + 32 > sprite2.x and
        sprite1.y < sprite2.y + 32 and
        sprite1.y + 32 > sprite2.y
    )

death = displayio.OnDiskBitmap("restart.bmp")

def display_game_over():
    global death_hi
    death_hi = displayio.TileGrid(
        death,
        pixel_shader=player0.pixel_shader,
        width=1,
        height=1,
        tile_width=64,
        tile_height=32,
        default_tile=0,
        x=(display.width - 64) // 2,  
        y=(display.height - 32) // 2  
    )
    splash.append(death_hi)
    for i in fireballs:
        splash.remove(i)
    fireballs.clear()
    for i in lavas:
        splash.remove(i)
    lavas.clear()

frame = 0
speed = 4 
game_over = False

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_over == True:
                for i in fireballs:
                    splash.remove(i)
                fireballs.clear()
                splash.remove(death_hi)
                game_over = False
                for i in lavas:
                    splash.remove(i)
                lavas.clear()
                splash.remove(death_hi)
                game_over = False


    keys = pygame.key.get_pressed()

    if game_over == False:
        if keys[pygame.K_LEFT]:
            player0.x -= speed
        if keys[pygame.K_RIGHT]:
            player0.x += speed
        if random.random() < 0.05:  # spawn rate
            spawn_fireball()
        if random.random() < 0.50:  # spawn rate
            spawn_lava()

    for fireball in fireballs:
        fireball.y += 5 
        if fireball.y > display.height:
            splash.remove(fireball)
            fireballs.remove(fireball)
        elif check_collision(player0, fireball):
            game_over = True
            display_game_over()
    for lava in lavas:
        lava.y += 5 
        if lava.y > display.height:
            splash.remove(lava)
            lavas.remove(lava)
        elif check_collision(player0, lava):
            game_over = True
            display_game_over()

    player0[0] = frame
    frame = (frame + 1) % (player0.width // tile_width)

    time.sleep(0.1)