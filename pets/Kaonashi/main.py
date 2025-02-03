import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
import pygame
import time
import random
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font
from datetime import datetime

pygame.init()

# Initialize display
display = PyGameDisplay(width=128, height=128)
splash = displayio.Group()
display.show(splash)

# Load assets
forest_background = displayio.OnDiskBitmap("bg.png")
bg_sprite = displayio.TileGrid(forest_background, pixel_shader=forest_background.pixel_shader)
splash.append(bg_sprite)

sheet = displayio.OnDiskBitmap("kaonashi.png")
sheet_flipped = displayio.OnDiskBitmap("kaonashiflipped.png")

tile_width = 10
tile_height = 20

sprite = displayio.TileGrid(
    sheet,
    pixel_shader=sheet.pixel_shader,
    width=1,
    height=1,
    tile_width=tile_width,
    tile_height=tile_height,
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
        sprite1.x + sprite1.tile_width > sprite2.x and
        sprite1.y < sprite2.y + sprite2.tile_height and
        sprite1.y + sprite2.tile_height > sprite2.y
    )

def reset_game():
    global blocks, health, move_counter, rest_counter
    for block in blocks:
        splash.remove(block)
    blocks.clear()
    sprite.x = (display.width - tile_width) // 2
    sprite.y = display.height - tile_height - 10
    health = 3
    move_counter = 0
    rest_counter = 0
    update_health_bar()

def display_time():
    # Display the current time, date, and day
    current_time = datetime.now().strftime("%I:%M:%S %p")
    current_date = datetime.now().strftime("%Y-%m-%d")
    current_day = datetime.now().strftime("%A")
    time_text = f"{current_time}\n{current_date}\n{current_day}"
    time_label = label.Label(font, text=time_text, color=color)
    time_label.x = (display.width - time_label.bounding_box[2]) // 2
    time_label.y = (display.height - time_label.bounding_box[3]) // 2
    return time_label

def update_health_bar():
    global health_bar
    if health_bar in splash:
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
            x=display.width - (i + 1) * 32 - 5,
            y=5
        )
        health_bar.append(health_icon)
    splash.append(health_bar)

def show_restart_message():
    restart_image = displayio.OnDiskBitmap("restart.png")
    restart_sprite = displayio.TileGrid(
        restart_image,
        pixel_shader=restart_image.pixel_shader,
        width=1,
        height=1,
        tile_width=restart_image.width,
        tile_height=restart_image.height,
        x=(display.width - restart_image.width) // 2,
        y=(display.height - restart_image.height) // 2
    )
    splash.append(restart_sprite)
    display.refresh()
    time.sleep(2)
    splash.remove(restart_sprite)

font = bitmap_font.load_font("Arial-12.bdf")
color = 0x000000

starting_image = displayio.OnDiskBitmap("starting.png")
starting_sprite = displayio.TileGrid(
    starting_image,
    pixel_shader=starting_image.pixel_shader,
    width=1,
    height=1,
    tile_width=starting_image.width,
    tile_height=starting_image.height,
    x=(display.width - starting_image.width) // 2,
    y=(display.height - starting_image.height) // 2
)
splash.append(starting_sprite)
display.refresh()
time.sleep(2)
splash.remove(starting_sprite)

health = 3
move_counter = 0
rest_counter = 0
health_bar = displayio.Group()
update_health_bar()

frame = 0
speed = 3
show_time = False
bg_night_loaded = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_t:
            show_time = not show_time
            if show_time:
                for block in blocks:
                    splash.remove(block)
                blocks.clear()
                if health_bar in splash:
                    splash.remove(health_bar)
                time_label = display_time()
                splash.append(time_label)
            else:
                if time_label in splash:
                    splash.remove(time_label)
                update_health_bar()

    if show_time:
        time.sleep(1)
        continue

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

    if sprite.x < -tile_width:
        sprite.x = display.width
    elif sprite.x > display.width:
        sprite.x = -tile_width

    if moved:
        move_counter += 1
        rest_counter = 0
    else:
        rest_counter += 1

    if move_counter >= 50:
        health -= 1
        move_counter = 0
        if health <= 0:
            show_restart_message()
            reset_game()
        else:
            update_health_bar()

    if rest_counter >= 100 and health < 3:
        health += 1
        rest_counter = 0
        update_health_bar()

    if random.random() < 0.05:
        spawn_block()

    for block in blocks[:]:
        block.y += 5
        if block.y > display.height:
            splash.remove(block)
            blocks.remove(block)
        elif check_collision(sprite, block):
            show_restart_message()
            reset_game()

    sprite[0] = frame
    frame = (frame + 1) % (sheet.width // tile_width)

    current_hour = datetime.now().hour
    if 18 <= current_hour or current_hour < 6:
        if not bg_night_loaded:
            splash.remove(bg_sprite)
            night_background = displayio.OnDiskBitmap("nightbg.png")
            bg_sprite = displayio.TileGrid(night_background, pixel_shader=night_background.pixel_shader)
            splash.insert(0, bg_sprite)
            bg_night_loaded = True
    else:
        if bg_night_loaded:
            splash.remove(bg_sprite)
            bg_sprite = displayio.TileGrid(forest_background, pixel_shader=forest_background.pixel_shader)
            splash.insert(0, bg_sprite)
            bg_night_loaded = False

    time.sleep(0.1)
