import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
import pygame
import time
import random

pygame.init()

display = PyGameDisplay(width=128, height=128)
splash = displayio.Group()
display.show(splash)

forest_background = displayio.OnDiskBitmap("bg.png")
bg_sprite = displayio.TileGrid(forest_background, pixel_shader=forest_background.pixel_shader)
splash.append(bg_sprite)

sheet = displayio.OnDiskBitmap("kaonashi32.png")
sheet_flipped = displayio.OnDiskBitmap("kaonashiflipped.png")

tile_width = 32
tile_height = 32

sprite = displayio.TileGrid(
    sheet,
    pixel_shader=sheet.pixel_shader,
    width=1,
    height=1,
    tile_width=tile_width,
    tile_height=tile_height,
    default_tile=0,
    x=(display.width - tile_width) // 2,  
    y=display.height - tile_height - 10     
)

splash.append(sprite)

block_bitmap = displayio.OnDiskBitmap("kunai.png")

blocks = []

def spawn_block():
    x_position = random.randint(0, display.width - block_bitmap.width)
    block = displayio.TileGrid(
        block_bitmap,
        pixel_shader=block_bitmap.pixel_shader,
        width=1,
        height=1,
        tile_width=block_bitmap.width,
        tile_height=block_bitmap.height,
        x=x_position,
        y=-32
    )
    blocks.append(block)
    splash.append(block)

def check_collision(sprite1, sprite2):
    return (
        sprite1.x < sprite2.x + sprite2.tile_width and
        sprite1.x + sprite2.tile_width > sprite2.x and
        sprite1.y < sprite2.y + sprite2.tile_height and
        sprite1.y + sprite2.tile_height > sprite2.y
    )

def reset_game():
    global blocks, health, move_counter, rest_counter
    for block in blocks:
        splash.remove(block)
    blocks.clear()
    splash.remove(sprite)  # Remove the sprite
    sprite.x = (display.width - tile_width) // 2
    sprite.y = display.height - tile_height - 10
    splash.append(sprite)  # Re-add the sprite
    health = 3  # Reset health
    move_counter = 0
    rest_counter = 0

health = 3  # Initial health
move_counter = 0
rest_counter = 0
health_bar = displayio.Group()
for i in range(health):
    health_icon = displayio.TileGrid(
        displayio.OnDiskBitmap("riceball.png"),
        pixel_shader=displayio.OnDiskBitmap("riceball.png").pixel_shader,
        width=1,
        height=1,
        tile_width=32,
        tile_height=32,
        x=display.width - (i + 1) * 32 - 5,  # Adjust x position to be at the top right
        y=5  # Adjust y position to be at the top right
    )
    health_bar.append(health_icon)
splash.append(health_bar)

frame = 0
speed = 3
play_time = 0  # Timer to track play time
bg_night_loaded = False  # Flag to check if night background is loaded

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    keys = pygame.key.get_pressed()

    moved = False
    if keys[pygame.K_LEFT]:
        sprite.x -= speed
        sprite.bitmap = sheet_flipped
        moved = True
    if keys[pygame.K_RIGHT]:
        sprite.x += speed
        sprite.bitmap = sheet
        moved = True

    # Wrap around logic
    if sprite.x < -tile_width:
        sprite.x = display.width
    elif sprite.x > display.width:
        sprite.x = -tile_width

    if moved:
        move_counter += 1
        rest_counter = 0
    else:
        rest_counter += 1

    if move_counter >= 50:  # Decrease health after moving 50 times
        health -= 1
        move_counter = 0
        if health <= 0:
            reset_game()
        else:
            splash.remove(health_bar)
            health_bar = displayio.Group()
            for i in range(health):
                health_icon = displayio.TileGrid(
                    displayio.OnDiskBitmap("riceball.png"),
                    pixel_shader=displayio.OnDiskBitmap("riceball.png").pixel_shader,
                    width=1,
                    height=1,
                    tile_width=32,
                    tile_height=32,
                    x=display.width - (i + 1) * 32 - 5,  # Adjust x position to be at the top right
                    y=5  # Adjust y position to be at the top right
                )
                health_bar.append(health_icon)
            splash.append(health_bar)

    if rest_counter >= 100 and health < 3:  # Increase health after resting for 100 cycles
        health += 1
        rest_counter = 0
        splash.remove(health_bar)
        health_bar = displayio.Group()
        for i in range(health):
            health_icon = displayio.TileGrid(
                displayio.OnDiskBitmap("riceball.png"),
                pixel_shader=displayio.OnDiskBitmap("riceball.png").pixel_shader,
                width=1,
                height=1,
                tile_width=32,
                tile_height=32,
                x=display.width - (i + 1) * 32 - 5,  # Adjust x position to be at the top right
                y=5  # Adjust y position to be at the top right
            )
            health_bar.append(health_icon)
        splash.append(health_bar)

    if random.random() < 0.05:  # spawn rate
        spawn_block()

    for block in blocks:
        block.y += 5 
        if block.y > display.height:
            splash.remove(block)
            blocks.remove(block)
        elif check_collision(sprite, block):  # Check for collision with kunai
            reset_game()

    sprite[0] = frame
    frame = (frame + 1) % (sheet.width // tile_width)

    play_time += 0.05  # Increment play time
    if play_time >= 30 and not bg_night_loaded:  # Change background after few seconds
        splash.remove(bg_sprite)
        night_background = displayio.OnDiskBitmap("nightbg.png")
        bg_sprite = displayio.TileGrid(night_background, pixel_shader=night_background.pixel_shader)
        splash.insert(0, bg_sprite)  # Insert new background at the bottom of the group
        bg_night_loaded = True

    time.sleep(0.1)
