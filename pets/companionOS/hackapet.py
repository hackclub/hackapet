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
start = displayio.OnDiskBitmap(r"C:\Users\Briyan\Documents\hackapet\splash1.bmp")
bg_sprite = displayio.TileGrid(
    start,
    pixel_shader=start.pixel_shader
)
splash.append(bg_sprite)

while True:
    time.sleep(0.1)
    display.refresh()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()