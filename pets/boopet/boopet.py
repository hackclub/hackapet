import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font
import pygame
import time
import random

pygame.init()

# Initialize the display
display = PyGameDisplay(width=128, height=128)
splash = displayio.Group()
display.show(splash)

# Load the night background
night_background = displayio.OnDiskBitmap("night.bmp")
bg_sprite = displayio.TileGrid(night_background, pixel_shader=night_background.pixel_shader)
splash.append(bg_sprite)

# Load the ghost sprite sheet
ghost_sheet = displayio.OnDiskBitmap("ghost-sheet.bmp")

tile_width = 32
tile_height = 32

# Add the ghost sprite
ghost_sprite = displayio.TileGrid(
    ghost_sheet,
    pixel_shader=ghost_sheet.pixel_shader,
    width=1,
    height=1,
    tile_width=tile_width,
    tile_height=tile_height,
    default_tile=0,
    x=(display.width - tile_width) // 2,  
    y=display.height - tile_height       
)
splash.append(ghost_sprite)

# Load a bitmap font
font = bitmap_font.load_font("Arial-16.bdf")  # Replace with your font file
text_color = 0xFFFFFF  # White text

# Create a label for the score
score = 0
score_label = label.Label(
    font,
    text=f"Score: {score}",
    color=text_color,
    x=5,  # Top-left corner
    y=10
)
splash.append(score_label)

# Load the star sprite sheet
star_sheet = displayio.OnDiskBitmap("star.bmp")
star_size = 5  # Size of the star in pixels

# Create a list of stars
stars = []
num_stars = 5

for _ in range(num_stars):
    star = displayio.TileGrid(
        star_sheet,
        pixel_shader=star_sheet.pixel_shader,
        width=1,
        height=1,
        tile_width=star_size,
        tile_height=star_size,
        default_tile=0,
        x=random.randint(0, display.width - star_size),
        y=random.randint(0, display.height - star_size)
    )
    stars.append(star)
    splash.append(star)

frame = 0
speed = 2
ghostvity = 1  # Gravity for ghost

# Function to respawn a star
def respawn_star(star):
    star.x = random.randint(0, display.width - star_size)
    star.y = random.randint(0, display.height - star_size)

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                ghost_sprite.x -= speed
            elif event.key == pygame.K_RIGHT:
                ghost_sprite.x += speed
            elif event.key == pygame.K_UP:
                ghost_sprite.y -= speed

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        ghost_sprite.x -= speed

    if keys[pygame.K_RIGHT]:
        ghost_sprite.x += speed

    if keys[pygame.K_UP]:
        ghost_sprite.y -= speed

    if ghost_sprite.y < display.height - tile_height:
        ghost_sprite.y += ghostvity

    if ghost_sprite.y < 0 or ghost_sprite.y > display.height - tile_height:
        ghost_sprite.y += 1

    # Check for collisions with stars
    for star in stars:
        if (
            abs(ghost_sprite.x - star.x) < tile_width - 5
            and abs(ghost_sprite.y - star.y) < tile_height - 5
        ):
            score += 1
            score_label.text = f"Score: {score}"  # Update score display
            respawn_star(star)  # Respawn the collected star

    # Animate the ghost sprite
    ghost_sprite[0] = frame
    frame = (frame + 1) % (ghost_sheet.width // tile_width)

    time.sleep(0.1)
