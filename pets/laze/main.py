import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
import pygame
import time

pygame.init()
display = PyGameDisplay(width=128, height=128)
splash = displayio.Group()
display.show(splash)

bg = displayio.OnDiskBitmap("bg.bmp")

bg_sprite = displayio.TileGrid(
	bg, 
	pixel_shader=bg.pixel_shader
)

splash.append(bg_sprite)

