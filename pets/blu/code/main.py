import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
import pygame
import time
from adafruit_display_text import label
import random

pygame.init()

display = PyGameDisplay(width=128, height=128)
splash = displayio.Group()
display.show(splash)

ocean_background = displayio.OnDiskBitmap("resources/backbackground-Sheet.bmp")
ocean_background_width = ocean_background.width
ocean_background_height = ocean_background.height
num_frames = 6

bg_sprite = displayio.TileGrid(
    ocean_background, 
    pixel_shader=ocean_background.pixel_shader, 
    width=1, height=1, 
    x=0, y=0,
    tile_width=128,
    tile_height=128
)

splash.append(bg_sprite)

animated_bg = displayio.OnDiskBitmap("resources/frontbackground-Sheet.bmp")
animated_bg_width = animated_bg.width
animated_bg_height = animated_bg.height

animated_bg_sprite = displayio.TileGrid(
    animated_bg, 
    pixel_shader=animated_bg.pixel_shader, 
    width=1, height=1, 
    x=0, y=0,
    tile_width=128,
    tile_height=128
)

splash.append(animated_bg_sprite)

blahaj_sheet = displayio.OnDiskBitmap("resources/blahaj.bmp")
blahaj_chomp = displayio.OnDiskBitmap("resources/blahajchomp.bmp")

tile_width = 32
tile_height = 32

blahaj_sprite = displayio.TileGrid(
    blahaj_sheet,
    pixel_shader=blahaj_sheet.pixel_shader,
    width=1,
    height=1,
    tile_width=tile_width,
    tile_height=tile_height,
    default_tile=0,
    x=(display.width - tile_width) // 2,
    y=(display.height - tile_height) // 2
)

splash.append(blahaj_sprite)

fish_bitmap = displayio.OnDiskBitmap("resources/fish.bmp")
fish_list = []

def spawn_fish():
    side = random.choice(["left", "right"])
    if side == "left":
        x_position = -fish_bitmap.width
    else:
        x_position = display.width
    
    fish_sprite = displayio.TileGrid(
        fish_bitmap,
        pixel_shader=fish_bitmap.pixel_shader,
        width=1,
        height=1,
        tile_width=fish_bitmap.width,
        tile_height=fish_bitmap.height,
        x=x_position,
        y=random.randint(20, display.height - 20)
    )
    fish_list.append(fish_sprite)
    splash.append(fish_sprite)

def check_collision(sprite1, sprite2):
    return (
        sprite1.x < sprite2.x + 32 and
        sprite1.x + 32 > sprite2.x and
        sprite1.y < sprite2.y + 32 and
        sprite1.y + 32 > sprite2.y
    )

speed = 3
fish_speed = 2
running = True

bg_frame = 0
animated_bg_frame = 0

def chomp_animation():
    blahaj_sprite.bitmap = blahaj_chomp
    time.sleep(0.1)  
    blahaj_sprite.bitmap = blahaj_sheet 

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        blahaj_sprite.x -= speed
        blahaj_sprite.flip_x = False
    if keys[pygame.K_RIGHT]:
        blahaj_sprite.x += speed
        blahaj_sprite.flip_x = True

    if random.random() < 0.05:
        spawn_fish()

    for fish in fish_list[:]:
        if fish.x < blahaj_sprite.x:
            fish.x += fish_speed
        else:
            fish.x -= fish_speed
        
        if check_collision(blahaj_sprite, fish):
            splash.remove(fish)
            fish_list.remove(fish)
            chomp_animation() 
            
    bg_frame = (bg_frame + 1) % num_frames
    bg_sprite[0] = bg_frame

    animated_bg_frame = (animated_bg_frame + 1) % num_frames
    animated_bg_sprite[0] = animated_bg_frame

    time.sleep(0.1)

pygame.quit()
