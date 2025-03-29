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

# Variables
frame = 0
speed = 7
game_over = False

# Background sprite
bg_sheet = displayio.OnDiskBitmap("sprites/home.bmp")
bg_sprite = displayio.TileGrid(
    bg_sheet,
    pixel_shader=bg_sheet.pixel_shader,
    width=1,
    height=1,
    tile_width=128,
    tile_height=128,
    default_tile=0,
    x=(display.width - 128) // 2,
    y=display.height - 128 - 0
    )
splash.append(bg_sprite)

# Eevee sprite
eevee_sheet = displayio.OnDiskBitmap("sprites/EeveeIdle.bmp")
eevee_sprite = displayio.TileGrid(
    eevee_sheet,
    pixel_shader=eevee_sheet.pixel_shader,
    width=1,
    height=1,
    tile_width=32,
    tile_height=32,
    default_tile=0,
    x=(display.width - 32) // 2,  
    y=display.height - 32 - 10     
)
splash.append(eevee_sprite)

# Dropping objects
electric_bitmap = displayio.OnDiskBitmap("sprites/biscuits/electric.bmp")
fire_bitmap = displayio.OnDiskBitmap("sprites/biscuits/fire.bmp")
water_bitmap = displayio.OnDiskBitmap("sprites/biscuits/water.bmp")
fireball_bitmap = displayio.OnDiskBitmap("sprites/chocolate.bmp")

# Start screen
start_sheet = displayio.OnDiskBitmap("sprites/start.bmp")
start_sprite = displayio.TileGrid(
    start_sheet,
    pixel_shader=bg_sheet.pixel_shader,
    width=1,
    height=1,
    tile_width=128,
    tile_height=128,
    default_tile=0,
    x=(display.width - 128) // 2,
    y=display.height - 128 - 0
)

screen = 1 # 1: Start screen, 2: Main game

# Function to display the start screen
def display_start_screen():
    splash.append(start_sprite)

# Restart sprite
restart = displayio.OnDiskBitmap("sprites/restart.bmp")

fireballs = []
biscuits = []

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

def spawn_electric():
    x_position = random.randint(0, display.width - electric_bitmap.width)
    electric = displayio.TileGrid(
        electric_bitmap,
        pixel_shader=electric_bitmap.pixel_shader,
        width=1,
        height=1,
        tile_width=electric_bitmap.width,
        tile_height=electric_bitmap.height,
        x=x_position,
        y=-32
    )
    biscuits.append(electric)
    splash.append(electric)

def spawn_water():
    x_position = random.randint(0, display.width - water_bitmap.width)
    water = displayio.TileGrid(
        water_bitmap,
        pixel_shader=water_bitmap.pixel_shader,
        width=1,
        height=1,
        tile_width=water_bitmap.width,
        tile_height=water_bitmap.height,
        x=x_position,
        y=-32
    )
    biscuits.append(water)
    splash.append(water)

def spawn_fire():
    x_position = random.randint(0, display.width - fire_bitmap.width)
    fire = displayio.TileGrid(
        fire_bitmap,
        pixel_shader=fire_bitmap.pixel_shader,
        width=1,
        height=1,
        tile_width=fire_bitmap.width,
        tile_height=fire_bitmap.height,
        x=x_position,
        y=-32
    )
    biscuits.append(fire)
    splash.append(fire)

# Function to check for collisions
def check_collision(sprite1, sprite2):
    return (
        sprite1.x < sprite2.x + 32 and
        sprite1.x + 32 > sprite2.x and
        sprite1.y < sprite2.y + 32 and
        sprite1.y + 32 > sprite2.y
    )

restart = displayio.OnDiskBitmap("sprites/restart.bmp")

def display_death():
    global death
    death = displayio.TileGrid(
        restart,
        pixel_shader=eevee_sheet.pixel_shader,
        width=1,
        height=1,
        tile_width=64,
        tile_height=32,
        default_tile=0,
        x=(display.width - 64) // 2,  
        y=(display.height - 32) // 2  
    )
    splash.append(death)
    for i in fireballs:
        splash.remove(i)
    fireballs.clear()
    for i in biscuits:
        splash.remove(i)
    biscuits.clear()

display_start_screen()

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
                splash.remove(death)
                game_over = False
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP and screen == 1:
                splash.remove(start_sprite)
                splash.append(bg_sprite)
                splash.append(eevee_sprite)
                screen = 2

    keys = pygame.key.get_pressed()

    if screen == 2 and game_over == False:
        if keys[pygame.K_LEFT] and eevee_sprite.x > 0:
            eevee_sprite.x -= speed
        if keys[pygame.K_RIGHT] and eevee_sprite.x < 98:
            eevee_sprite.x += speed
        if random.random() < 0.026:  # spawn rate
            spawn_fireball()
        if random.random() < 0.025:
            spawn_electric()
        if random.random() < 0.025:
            spawn_water()
        if random.random() < 0.025:
            spawn_fire()

    for fireball in fireballs:
        fireball.y += 5 
        if fireball.y > display.height:
            splash.remove(fireball)
            fireballs.remove(fireball)
        elif check_collision(eevee_sprite, fireball):
            game_over = True
            display_death()

    for electric in biscuits:
        electric.y += 3 
        if electric.y > display.height:
            splash.remove(electric)
            biscuits.remove(electric)
        elif check_collision(eevee_sprite, electric):
            splash.remove(electric)
            biscuits.remove(electric)

    for water in biscuits:
        water.y += 3 
        if water.y > display.height:
            splash.remove(water)
            biscuits.remove(water)
        elif check_collision(eevee_sprite, water):
            splash.remove(water)
            biscuits.remove(water)


    for fire in biscuits:
        fire.y += 3 
        if fire.y > display.height:
            splash.remove(fire)
            biscuits.remove(fire)
        elif check_collision(eevee_sprite, fire):
            splash.remove(fire)
            biscuits.remove(fire)

    eevee_sprite[0] = frame
    frame = (frame + 1) % 4

    bg_sprite[0] = frame
    frames = (frame + 1) % 4

    time.sleep(0.12)