import sys
import time
import random

CIRCUITPYTHON = False
try:
    import board
    import displayio
    CIRCUITPYTHON = True
except ImportError:
    from blinka_displayio_pygamedisplay import PyGameDisplay
    import pygame

if CIRCUITPYTHON:
    display = board.DISPLAY  
else:
    pygame.init()
    display = PyGameDisplay(width=128, height=128)  

def load_bitmap(filename):
    if CIRCUITPYTHON:
        return displayio.OnDiskBitmap(open(filename, "rb"))  
    else:
        return pygame.image.load(filename)  

background = load_bitmap("hp-background.png")
reaper_img = load_bitmap("reaper.png")
soul_img = load_bitmap("soul.png")
spirit_img = load_bitmap("spirit.png")
gravestone_img = load_bitmap("gravestone.png")

reaper_x, reaper_y = 64, 100  
jumping = False
jump_velocity = 0
score = 0

souls = [{"x": random.randint(10, 118), "y": 20} for _ in range(3)]
spirits = [{"x": random.randint(10, 118), "y": 40} for _ in range(2)]
gravestones = [{"x": random.randint(10, 118), "y": 110} for _ in range(2)]

running = True
while running:
    if not CIRCUITPYTHON:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    for soul in souls:
        soul["y"] += 1
        if soul["y"] > 128:
            soul["y"] = 0

    for soul in souls:
        if abs(reaper_x - soul["x"]) < 10 and abs(reaper_y - soul["y"]) < 10:
            score += 1
            soul["y"] = 0  

    if not CIRCUITPYTHON:
        display.surface.blit(background, (0, 0))
        display.surface.blit(reaper_img, (reaper_x, reaper_y))
        for soul in souls:
            display.surface.blit(soul_img, (soul["x"], soul["y"]))
        pygame.display.flip()  

    time.sleep(0.1)
