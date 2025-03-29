import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
import pygame
import time
import random

# Initialize Pygame
pygame.init()

# Setup display
display = PyGameDisplay(width=128, height=128)
splash = displayio.Group()
display.show(splash)

# Load background bitmap
sweet_background = displayio.OnDiskBitmap("sweetbackground.bmp")
bg_sprite = displayio.TileGrid(
    sweet_background,
    pixel_shader=sweet_background.pixel_shader,
    width=1,
    height=1,
    tile_width=sweet_background.width // 11,
    tile_height=sweet_background.height,
    default_tile=0
)
splash.append(bg_sprite)

# Load bonnie sprite sheet
bonnie_sheet = displayio.OnDiskBitmap("Bonnie.bmp")
bonnie_sprite = displayio.TileGrid(
    bonnie_sheet,
    pixel_shader=bonnie_sheet.pixel_shader,
    width=1,
    height=1,
    tile_width=bonnie_sheet.width // 6,
    tile_height=bonnie_sheet.height,
    default_tile=0,
    x=(display.width - 16) // 2,
    y=display.height - 24 - 23
)
splash.append(bonnie_sprite)

# Load counter sprite sheet
counter_sheet = displayio.OnDiskBitmap("Counter.bmp")
counter_sprite = displayio.TileGrid(
    counter_sheet,
    pixel_shader=counter_sheet.pixel_shader,
    width=1,
    height=1,
    tile_width=counter_sheet.width // 101,
    tile_height=counter_sheet.height,
    default_tile=0,
    x=3,
    y=3
)
splash.append(counter_sprite)

# Define items and their spawn functions
strawberry_bitmap = displayio.OnDiskBitmap("Strawberry!.bmp")
goldberry_bitmap = displayio.OnDiskBitmap("Goldberry!.bmp")
bomb_bitmap = displayio.OnDiskBitmap("CocoaBomb!.bmp")
strawberries = []
goldberries = []
bombs = []

def spawn_strawberry():
    x_position = random.randint(0, display.width - strawberry_bitmap.width)
    strawberry = displayio.TileGrid(
        strawberry_bitmap,
        pixel_shader=strawberry_bitmap.pixel_shader,
        width=1,
        height=1,
        tile_width=strawberry_bitmap.width,
        tile_height=strawberry_bitmap.height,
        x=x_position,
        y=-32
    )
    strawberries.append(strawberry)
    splash.append(strawberry)

def spawn_goldberry():
    x_position = random.randint(0, display.width - goldberry_bitmap.width)
    goldberry = displayio.TileGrid(
        goldberry_bitmap,
        pixel_shader=goldberry_bitmap.pixel_shader,
        width=1,
        height=1,
        tile_width=goldberry_bitmap.width,
        tile_height=goldberry_bitmap.height,
        x=x_position,
        y=-32
    )
    goldberries.append(goldberry)
    splash.append(goldberry)

def spawn_bomb():
    x_position = random.randint(0, display.width - bomb_bitmap.width)
    bomb = displayio.TileGrid(
        bomb_bitmap,
        pixel_shader=bomb_bitmap.pixel_shader,
        width=1,
        height=1,
        tile_width=bomb_bitmap.width,
        tile_height=bomb_bitmap.height,
        x=x_position,
        y=-32
    )
    bombs.append(bomb)
    splash.append(bomb)

def spawn_item():
    spawn_chance = random.random()
    if spawn_chance < 0.03:
        spawn_bomb()
    elif spawn_chance < 0.04:
        spawn_goldberry()
    elif spawn_chance < 0.06:
        spawn_strawberry()

# Function to check for collisions
def check_collision(sprite1, sprite2):
    return (
        sprite1.x < sprite2.x + sprite2.tile_width and
        sprite1.x + sprite1.tile_width > sprite2.x and
        sprite1.y < sprite2.y + sprite2.tile_height and
        sprite1.y + sprite1.tile_height > sprite2.y
    )

# Display the "Game Over" screen
lose = displayio.OnDiskBitmap("RestartDead.bmp")
def display_dead():
    global dead
    dead = displayio.TileGrid(
        lose,
        pixel_shader=bonnie_sheet.pixel_shader,
        width=1,
        height=1,
        tile_width=64,
        tile_height=32,
        default_tile=0,
        x=(display.width - 64) // 2,
        y=(display.height - 32) // 2
    )
    splash.append(dead)
    for bomb in bombs:
        splash.remove(bomb)
    for strawberry in strawberries:
        splash.remove(strawberry)
    for goldberry in goldberries:
        splash.remove(goldberry)
    bombs.clear()
    strawberries.clear()
    goldberries.clear()
    timeout_duration = 999999
    state = 4

# Display the "Game Win" screen
win = displayio.OnDiskBitmap("RestartWin.bmp")
def display_end():
    global end
    end = displayio.TileGrid(
        win,
        pixel_shader=bonnie_sheet.pixel_shader,
        width=1,
        height=1,
        tile_width=64,
        tile_height=32,
        default_tile=0,
        x=(display.width - 64) // 2,
        y=(display.height - 32) // 2
    )
    splash.append(end)
    for bomb in bombs:
        splash.remove(bomb)
    for strawberry in strawberries:
        splash.remove(strawberry)
    for goldberry in goldberries:
        splash.remove(goldberry)
    bombs.clear()
    strawberries.clear()
    goldberries.clear()
    timeout_duration = 999999
    state = 2

# Game state and controls
count = 0
progress = 0
speed = 10
direction = 0
state = 0
last_collection_time = pygame.time.get_ticks()
timeout_duration = 2000
game_over = False
yay = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_over == True:
                for i in bombs:
                    splash.remove(i)
                for i in strawberries:
                    splash.remove(i)
                for i in goldberries:
                    splash.remove(i)
                bombs.clear()
                strawberries.clear()
                goldberries.clear()
                splash.remove(dead)
                splash.remove(end)
                game_over = False
                state = 0
                count = 0
                yay = 0

    keys = pygame.key.get_pressed()

    if not game_over:
        if keys[pygame.K_LEFT]:
            bonnie_sprite.x -= speed
            direction = 1
        if keys[pygame.K_RIGHT]:
            bonnie_sprite.x += speed
            direction = 0 
        
        spawn_item()

    current_time = pygame.time.get_ticks()
    
    if current_time - last_collection_time > timeout_duration:
        state = 0

    # Move bombs and check for collisions
    for bomb in bombs:
        bomb.y += 5
        if bomb.y > display.height:
            splash.remove(bomb)
            bombs.remove(bomb)
        elif check_collision(bonnie_sprite, bomb):
            timeout_duration = 999999
            last_collection_time = pygame.time.get_ticks()
            state = 4
            game_over = True
            display_end()
            display_dead()

    # Move strawberries and check for collisions
    for strawberry in strawberries:
        strawberry.y += 5
        if strawberry.y > display.height:
            splash.remove(strawberry)
            strawberries.remove(strawberry)
        elif check_collision(bonnie_sprite, strawberry):
            timeout_duration = 2000
            last_collection_time = pygame.time.get_ticks()
            state = 2
            count += 1
            splash.remove(strawberry)  # Remove strawberry after collection
            strawberries.remove(strawberry)

    # Move goldberries and check for collisions
    for goldberry in goldberries:
        goldberry.y += 5
        if goldberry.y > display.height:
            splash.remove(goldberry)
            goldberries.remove(goldberry)
        elif check_collision(bonnie_sprite, goldberry):
            timeout_duration = 2000
            last_collection_time = pygame.time.get_ticks()
            state = 2
            count += 3
            splash.remove(goldberry)  # Remove goldberry after collection
            goldberries.remove(goldberry)

    # Cap the score at 100
    if count >= 100:
        count = 100
        progress = 10
        timeout_duration = 999999
        last_collection_time = pygame.time.get_ticks()
        state = 2
        game_over = True
        display_dead()
        display_end()
        count = 0
        yay = 1
    elif count >= 90:
        progress = 9
    elif count >= 80:
        progress = 8
    elif count >= 70:
        progress = 7
    elif count >= 60:
        progress = 6
    elif count >= 50:
        progress = 5
    elif count >= 40:
        progress = 4
    elif count >= 30:
        progress = 3
    elif count >= 20:
        progress = 2
    elif count >= 10:
        progress = 1
    elif count >= 0 and game_over == False:
        progress = 0
    
    # Update the score counter and sprite frames
    bonnie_sprite[0] = direction + state
    if game_over == False:
        counter_sprite[0] = count
    elif yay == 1:
        counter_sprite[0] = 100
    bg_sprite[0] = progress
    time.sleep(0.1)