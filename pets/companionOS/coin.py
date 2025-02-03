import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
import pygame
import time
import random
import os

script_dir = os.path.dirname(__file__)
coin_img_dir = os.path.join(script_dir, "coin")

# Display
pygame.init()
display = PyGameDisplay(width=128, height=128)
splash = displayio.Group()
display.show(splash)

# Initial Plain Screen
start_path = os.path.join(coin_img_dir, "coin.bmp")
start = displayio.OnDiskBitmap(start_path)
bg_sprite = displayio.TileGrid(
    start,
    pixel_shader=start.pixel_shader
)
splash.append(bg_sprite)

# Update Display
def update_coin_image(coin_side):
    coin_path = os.path.join(coin_img_dir, f"coin{coin_side}.bmp")
    new_coin = displayio.OnDiskBitmap(coin_path)
    splash.pop()  # Remove the old sprite
    new_sprite = displayio.TileGrid(new_coin, pixel_shader=new_coin.pixel_shader)
    splash.append(new_sprite)  # Add the new sprite

# Main loop
while True:
    time.sleep(0.1)
    display.refresh()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                # Flip the coin (assuming 1 = heads, 2 = tails)
                coin_side = random.randint(1, 2)
                update_coin_image(coin_side)
            elif event.key == pygame.K_DOWN:
                print("Down key pressed")
