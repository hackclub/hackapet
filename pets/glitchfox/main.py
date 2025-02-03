import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import label
import time
import pygame
import random

WIDTH = 128
HEIGHT = 128

display = PyGameDisplay(width=WIDTH, height=HEIGHT)
splash = displayio.Group()

# Main game background.
background = displayio.OnDiskBitmap("assets/background.bmp")
bg_tile = displayio.TileGrid(background, pixel_shader=displayio.ColorConverter())
splash.append(bg_tile)

# Fox sprite.
fox_sprites = displayio.OnDiskBitmap("assets/glitch_fox_idle.bmp")
frame_width = 64
frame_height = 64
total_frames = 32
fox = displayio.TileGrid(
    fox_sprites,
    pixel_shader=displayio.ColorConverter(),
    width=1, height=1,
    tile_width=frame_width,
    tile_height=frame_height,
    x=32,
    y=HEIGHT - frame_height,
)
splash.append(fox)

# Load font.
font = bitmap_font.load_font("assets/Dina_i400-8.bdf")

level_label = label.Label(font, text="Level: 1", color=0xFFFFFF, x=5, y=5)
splash.append(level_label)

bytes_label = label.Label(font, text="Bytes: 0/3", color=0xFFFFFF, x=5, y=20)
splash.append(bytes_label)

feedback_label = label.Label(font, text="", color=0xFFFF00, x=5, y=35)
splash.append(feedback_label)

health_label = label.Label(font, text="Health: 3", color=0xFFFFFF, x=5, y=50)
splash.append(health_label)

display.show(splash)

def reset_game():
    """Reset all game variables to their initial values."""
    global current_level, bytes_collected, bytes_required
    global byte_speed, fox_speed, byte_size, health
    global fox_x, byte_y, current_frame, feedback_timer

    current_level = 1
    bytes_collected = 0
    bytes_required = 3
    byte_speed = 1
    fox_speed = 8
    byte_size = 16
    fox_x = 32
    fox.x = fox_x
    byte_y = 0
    current_frame = 0
    feedback_timer = 0
    health = 3

def generate_byte():
    global byte_size
    byte = displayio.Bitmap(byte_size, byte_size, 2)
    byte_palette = displayio.Palette(2)
    byte_palette[0] = 0x000000
    byte_palette[1] = 0xFFFF00
    byte_item = displayio.TileGrid(
        byte,
        pixel_shader=byte_palette,
        x=random.randint(0, WIDTH - byte_size),
        y=0
    )
    for x in range(byte_size):
        for y in range(byte_size):
            byte[x, y] = 1
    return byte_item

def show_title_screen():
    """Display a title screen with a 'Press any key to start' prompt."""
    title_splash = displayio.Group()
    # Animated title background: a 4-frame (2x2) BMP spritesheet.
    title_bg = displayio.OnDiskBitmap("assets/title_background.bmp")
    title_tile = displayio.TileGrid(
        title_bg,
        pixel_shader=displayio.ColorConverter(),
        width=1, height=1,
        tile_width=WIDTH, tile_height=HEIGHT
    )
    title_splash.append(title_tile)
    
    # Center the title text near the top.
    title_label = label.Label(font, text="GLITCH FOX", color=0xFF00FF)
    title_label.anchor_point = (0.5, 0)
    title_label.anchored_position = (WIDTH // 2, 10)
    title_splash.append(title_label)
    
    prompt_label = label.Label(font, text="Press any key", color=0xFFFFFF)
    prompt_label.anchor_point = (0.5, 0)
    prompt_label.anchored_position = (WIDTH // 2, 30)
    title_splash.append(prompt_label)
    
    display.show(title_splash)
    waiting = True
    frame_delay = 0.1  # seconds per frame for title animation
    last_update = time.monotonic()
    frame_index = 0
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit()
            elif event.type == pygame.KEYDOWN:
                waiting = False
        current_time = time.monotonic()
        if current_time - last_update > frame_delay:
            frame_index = (frame_index + 1) % 4  # Cycle through 4 frames
            title_tile[0] = frame_index
            last_update = current_time
        time.sleep(0.01)
    display.show(splash)

def show_death_screen():
    """Display a 'Game Over' screen until any key is pressed.
       Assumes the death background BMP is a horizontal strip of three 128x128 frames."""
    death_splash = displayio.Group()
    death_bg = displayio.OnDiskBitmap("assets/death_background.bmp")
    death_tile = displayio.TileGrid(
        death_bg,
        pixel_shader=displayio.ColorConverter(),
        width=1, height=1,
        tile_width=WIDTH, tile_height=HEIGHT
    )
    death_splash.append(death_tile)
    
    # Center the death text near the top.
    game_over_label = label.Label(font, text="GAME OVER", color=0xFF0000)
    game_over_label.anchor_point = (0.5, 0)
    game_over_label.anchored_position = (WIDTH // 2, 10)
    death_splash.append(game_over_label)
    
    prompt_label = label.Label(font, text="Press any key.", color=0xFFFFFF)
    prompt_label.anchor_point = (0.5, 0)
    prompt_label.anchored_position = (WIDTH // 2, 30)
    death_splash.append(prompt_label)
    
    display.show(death_splash)
    waiting = True
    frame_delay = 0.3  # seconds per frame for death animation
    last_update = time.monotonic()
    frame_index = 0
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit()
            elif event.type == pygame.KEYDOWN:
                waiting = False
        current_time = time.monotonic()
        if current_time - last_update > frame_delay:
            frame_index = (frame_index + 1) % 3  # Cycle through 3 frames
            death_tile[0] = frame_index
            last_update = current_time
        time.sleep(0.01)
    display.show(splash)

animation_speed = 0.05
running = True
show_title_screen()
reset_game()
byte_item = generate_byte()
splash.append(byte_item)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                fox_x = max(0, fox_x - fox_speed)
                fox.flip_x = False
            elif event.key == pygame.K_RIGHT:
                fox_x = min(WIDTH - frame_width, fox_x + fox_speed)
                fox.flip_x = True
    fox.x = fox_x
    byte_y += byte_speed
    byte_item.y = int(byte_y)
    if (byte_y >= HEIGHT - frame_height) and (fox_x <= byte_item.x <= fox_x + frame_width):
        bytes_collected += 1
        feedback_label.text = "You caught a byte!"
        feedback_timer = 20
        splash.remove(byte_item)
        byte_y = 0
        byte_item = generate_byte()
        splash.append(byte_item)
        if bytes_collected >= bytes_required:
            current_level += 1
            bytes_collected = 0
            bytes_required += 2
            byte_speed += 1
            fox_speed = min(16, fox_speed + 2)
            byte_size = max(4, byte_size - 2)
            health = min(3, health + 1)
            splash.remove(byte_item)
            byte_item = generate_byte()
            splash.append(byte_item)
            feedback_label.text = f"Level {current_level}!"
    elif byte_y > HEIGHT:
        health -= 1
        feedback_label.text = "You missed a byte."
        feedback_timer = 20
        splash.remove(byte_item)
        byte_y = 0
        byte_item = generate_byte()
        splash.append(byte_item)
    if health <= 0:
        show_death_screen()
        reset_game()
        splash.remove(byte_item)
        byte_item = generate_byte()
        splash.append(byte_item)
        feedback_label.text = ""
        continue
    level_label.text = f"Level: {current_level}"
    bytes_label.text = f"Bytes: {bytes_collected}/{bytes_required}"
    health_label.text = f"Health: {health}"
    if 'feedback_timer' in globals() and feedback_timer > 0:
        feedback_timer -= 1
    else:
        feedback_label.text = ""
    current_frame = (current_frame + 1) % total_frames
    fox[0] = current_frame
    time.sleep(animation_speed)

pygame.quit()
