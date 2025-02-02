import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
import pygame
import time
import random

# Display
pygame.init()
display = PyGameDisplay(width=128, height=128)
splash = displayio.Group()
display.show(splash)

# Initial Plain Screen
start = displayio.OnDiskBitmap(r"\coin\coin.bmp")
bg_sprite = displayio.TileGrid(
    start,
    pixel_shader=start.pixel_shader
)
splash.append(bg_sprite)

# Update Display
def update_dice_image(diceno):
    dice_path = fr"\coin\coin{diceno}.bmp"
    new_dice = displayio.OnDiskBitmap(dice_path)
    splash.pop()  # Remove the old sprite
    new_sprite = displayio.TileGrid(new_dice, pixel_shader=new_dice.pixel_shader)
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
                # Roll the dice
                diceno = random.randint(1, 4)
                update_dice_image(diceno)
            elif event.key == pygame.K_DOWN:
                print("Down key pressed")
