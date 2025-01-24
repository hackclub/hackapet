from blinka_displayio_pygamedisplay import PyGameDisplay
import displayio
import asyncio
import pygame
import random
import time

pygame.init()

display = PyGameDisplay(width=128, height=128)
splash = displayio.Group()

display.show(splash)

background = displayio.OnDiskBitmap("background.bmp")
bg_sprite = displayio.TileGrid(background, pixel_shader=background.pixel_shader)
splash.append(bg_sprite)

cpu_sheet = displayio.OnDiskBitmap("tools-sheet.bmp")
cpu_sprite = displayio.TileGrid(
    cpu_sheet,
    pixel_shader=cpu_sheet.pixel_shader,
    tile_width=64,
    tile_height=64,
    default_tile=3,
    x=32,  
    y=10
)

rock_img = displayio.OnDiskBitmap("rock_2x.bmp")
paper_img = displayio.OnDiskBitmap("paper_2x.bmp")
scissors_img = displayio.OnDiskBitmap("scissors_2x.bmp")
texts_img = displayio.OnDiskBitmap("texts.bmp")

rock = displayio.TileGrid(
    rock_img,
    pixel_shader=rock_img.pixel_shader,
    x=0,
    y=128-32
)

text_sprite = displayio.TileGrid(
    texts_img,
    pixel_shader=texts_img.pixel_shader,
    tile_width=128,
    tile_height=128,
    default_tile=3,
)

paper = displayio.TileGrid(
    paper_img,
    pixel_shader=paper_img.pixel_shader,
    x=48,
    y=128-32
)

scissors = displayio.TileGrid(
    scissors_img,
    pixel_shader=scissors_img.pixel_shader,
    x=48*2,
    y=128-32
)

splash.append(cpu_sprite)
splash.append(rock)
splash.append(paper)
splash.append(scissors)
splash.append(text_sprite)

def lose():
    text_sprite[0] = 0

def draw():
    text_sprite[0] = 1
    
def win():
    text_sprite[0] = 2

try:
    from server import *
    async def start_server():
        print("Starting server...")
        try:
            server.start(str(wifi.radio.ipv4_address))
            while True:
                server.poll()
        except Exception as e:
            print(f"Server error: {e}")

    asyncio.run(start_server())
except:
    print("Unable to start webserver :'(")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            cpu_choose = random.randint(0,2)
            if event.key == pygame.K_LEFT:
                if cpu_choose == 0:
                    draw()
                elif cpu_choose == 1:
                    lose()
                else:
                    win()
            elif event.key == pygame.K_DOWN:
                if cpu_choose == 0:
                    win()
                elif cpu_choose == 1:
                    draw()
                else:
                    lose()
            elif event.key == pygame.K_RIGHT:
                if cpu_choose == 0:
                    lose()
                elif cpu_choose == 1:
                    win()
                else:
                    draw()

            cpu_sprite[0] = cpu_choose
            time.sleep(1)
            text_sprite[0] = 3
            cpu_sprite[0] = 3

    time.sleep(0.25)