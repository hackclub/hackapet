import os
import time
import random
import pygame
from blinka_displayio_pygamedisplay import PyGameDisplay
import displayio

# Initialize Pygame
pygame.init()

# Set up the display
display = PyGameDisplay(width=128, height=128)
splash = displayio.Group()
display.show(splash)

forest_background = displayio.OnDiskBitmap("C:/Users/Nili/Pictures/forestbackground.bmp")

bg_sprite = displayio.TileGrid(
    forest_background, 
    pixel_shader=forest_background.pixel_shader
)

splash.append(bg_sprite)

teddy_idle = displayio.OnDiskBitmap("C:/Users/Nili/OneDrive/silly_dog/teddy_idle.bmp")
teddy_right = displayio.OnDiskBitmap("C:/Users/Nili/OneDrive/silly_dog/teddy_walking.bmp")
teddy_left = displayio.OnDiskBitmap("C:/Users/Nili/OneDrive/silly_dog/teddywalking! left.bmp")

# Correctly declare tile_width and tile_height as integers
tile_width = 32
tile_height = 32

teddy_sprite = displayio.TileGrid(
    teddy_idle,
    pixel_shader=teddy_idle.pixel_shader,
    width=1,
    height=1,
    tile_width=tile_width,
    tile_height=tile_height,
    default_tile=0,
    x=int((display.width - tile_width) // 2),
    y=int(display.height - tile_height - 10)
)

splash.append(teddy_sprite)

frame = 0
speed = 4 
game_over = False

food = []
shoes = []
pill_bitmap = displayio.OnDiskBitmap("C:/Users/Nili/OneDrive/silly_dog/pill.bmp")
shoe_bitmap = displayio.OnDiskBitmap("C:/Users/Nili/OneDrive/silly_dog/shoe.bmp")

def spawn_pill():
    x_position = random.randint(0, display.width - pill_bitmap.width)
    y_position = random.randint(0, 50)
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

def spawn_shoe():
    x_position = random.randint(0, display.width - shoe_bitmap.width)
    y_position = random.randint(0, 50)
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

# Call spawn_pill and spawn_shoe to spawn them initially
spawn_pill()
spawn_shoe()
full = 0
meter_empty = displayio.OnDiskBitmap("C:/Users/Nili/OneDrive/silly_dog/meter empty.bmp")
meter_full = displayio.OnDiskBitmap("C:/Users/Nili/OneDrive/silly_dog/meter full.bmp")
meter_quarter = displayio.OnDiskBitmap("C:/Users/Nili/OneDrive/silly_dog/meter quarter.bmp")
meter_half = displayio.OnDiskBitmap("C:/Users/Nili/OneDrive/silly_dog/meter half.bmp")
meter_three_quarters = displayio.OnDiskBitmap("C:/Users/Nili/OneDrive/silly_dog/meter three quarters.bmp")
win_screen = displayio.OnDiskBitmap("C:/Users/Nili/OneDrive/silly_dog/youwin.bmp")

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

while True:
    try:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        
        keys = pygame.key.get_pressed()
        if not game_over:
             if keys[pygame.K_RIGHT]:
                teddy_sprite.x += speed
                splash.remove(teddy_sprite)
                teddy_sprite = displayio.TileGrid(
                teddy_right,
                pixel_shader=teddy_right.pixel_shader,
                width=1,
                height=1,
                tile_width=32,
                tile_height=32,
                x=teddy_sprite.x,
                y=teddy_sprite.y
            )
                splash.append(teddy_sprite)
             elif keys[pygame.K_LEFT]:
                teddy_sprite.x -= speed
                splash.remove(teddy_sprite)
                teddy_sprite = displayio.TileGrid(
                teddy_left,
                pixel_shader=teddy_left.pixel_shader,
                width=1,
                height=1,
                tile_width=32,
                tile_height=32,
                x=teddy_sprite.x,
                y=teddy_sprite.y
            )
                splash.append(teddy_sprite)
             elif keys[pygame.K_UP]:
                if keys[pygame.K_UP]:
                    teddy_sprite.y -= speed
                    teddy_sprite.y -= speed
                    time.sleep(0.1)
                    teddy_sprite.y += speed
                    teddy_sprite.y += speed
                    splash.remove(teddy_sprite)
                    teddy_sprite = displayio.TileGrid(
                        teddy_idle,
                        pixel_shader=teddy_idle.pixel_shader,
                        width=1,
                        height=1,
                        tile_width=32,
                        tile_height=32,
                        x=teddy_sprite.x,
                        y=teddy_sprite.y
                        )
                    splash.append(teddy_sprite)
            # Check for collisions with food
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
                splash.append(meter_sprite)
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
                splash.append(meter_sprite)

        # Check if 5 seconds have passed to spawn a new pill and shoe
        current_time = time.time()
        if current_time - last_spawn_time >= 5:
            spawn_pill()
            spawn_shoe()
            last_spawn_time = current_time
        
        display.refresh()
        time.sleep(0.01)
    except Exception as e:
        print(f"An error occurred: {e}")
        pygame.quit()
        exit()