import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
import pygame
import time
import random

pygame.init()

display = PyGameDisplay(width=128, height=128)
splash = displayio.Group()
display.show(splash)

lives = 3

beach_background = displayio.OnDiskBitmap("beach-background.bmp")

bg_sprite = displayio.TileGrid(
    beach_background,
    pixel_shader=beach_background.pixel_shader
)

splash.append(bg_sprite)

seagull_sheet = displayio.OnDiskBitmap("seagull-sheet.bmp")

tile_width = 32
tile_height = 32

seagull_sprite = displayio.TileGrid(
    seagull_sheet,
    pixel_shader = seagull_sheet.pixel_shader,
    width = 1,
    height = 1,
    tile_width = tile_width,
    tile_height = tile_height,
    default_tile = 0,
    x = (display.width // 2) - (tile_width // 2),
    y = display.height - tile_height - 10
)

splash.append(seagull_sprite)

fries_bitmap = displayio.OnDiskBitmap("fries-pixel.bmp")
fries = []

def spawn_fries():
    x_position = random.randint(0, display.width - fries_bitmap.width)
    fries_sprite = displayio.TileGrid(
        fries_bitmap,
        pixel_shader = fries_bitmap.pixel_shader,
        width = 1,
        height = 1,
        tile_width = fries_bitmap.width,
        tile_height = fries_bitmap.height,
        x = x_position,
        y = -32
    )
    fries.append(fries_sprite)
    splash.append(fries_sprite)

spawn_fries()

heart_bitmap = displayio.OnDiskBitmap("heart-pixel.bmp")
hearts = []
def update_hearts():
    for heart in hearts:
        splash.remove(heart)
    hearts.clear()
    x_position = 5
    for i in range(lives):
        heart_sprite = displayio.TileGrid(
            heart_bitmap,
            pixel_shader = heart_bitmap.pixel_shader,
            width = 1,
            height = 1,
            tile_width = heart_bitmap.width,
            tile_height = heart_bitmap.height,
            x = x_position,
            y = 10
        )
        x_position += 15
        hearts.append(heart_sprite)
        splash.append(heart_sprite)


def check_collision(sprite1, sprite2):
    return (
        sprite1.x < sprite2.x + 32 and
        sprite1.x > sprite2.x - 32 and
        sprite1.y < sprite2.y + 32 and
        sprite1.y > sprite2.y - 32
    )

death = displayio.OnDiskBitmap("restart.bmp")

def display_game_over():
    global death_hi
    death_hi = displayio.TileGrid(
        death,
        pixel_shader = seagull_sheet.pixel_shader,
        width = 1,
        height=1,
        tile_width = 64,
        tile_height = 32,
        default_tile = 0,
        x = (display.width - 64) // 2,  
        y = (display.height - 32) // 2  
    )

    splash.append(death_hi)
    for fry in fries:
        splash.remove(fry)
    fries.clear()

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
                for fry in fries:
                    splash.remove(fry)
                fries.clear()
                splash.remove(death_hi)
                lives = 3
                game_over = False

    keys = pygame.key.get_pressed()
    update_hearts()

    if game_over == False:
        if keys[pygame.K_LEFT]:
            seagull_sprite.x -= speed
        if keys[pygame.K_RIGHT]:
            seagull_sprite.x += speed
        if random.random() < 0.05:
            spawn_fries()

    for fry in fries:
        fry.y += 5
        if fry.y > display.height - 32:
            lives -= 1
            splash.remove(fry)
            fries.remove(fry)
            
            if lives == 0:
                game_over = True
                display_game_over()
        elif check_collision(seagull_sprite, fry):
            splash.remove(fry)
            fries.remove(fry)

    seagull_sprite[0] = frame
    frame = (frame + 1) % (seagull_sheet.width // tile_width)

    time.sleep(0.1)