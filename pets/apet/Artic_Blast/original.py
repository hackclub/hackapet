import pygame
import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
from adafruit_display_text import label

import random
import time 
import math
import os

immunity_active = False
immunity_start_time = 0
def restart_game():
    global game_over, game_started, immunity_active, immunity_start_time
    hide_game_over_screen()
    game_over = False
    game_started = True
    immunity_active = False
    immunity_start_time = 0
    seal_sprite.x = 64
    seal_sprite.y = 80

    for obj in oil + garbage + seaweed + fish:
        if obj in splash:
            splash.remove(obj)

    oil.clear()
    garbage.clear()
    fish.clear()
    seaweed.clear()
immunity_active = False
immunity_start_time = 0


IMMUNITY_DURATION = 2  #touch or eat them and grbge cant harm u
game_over_start_time = 0
MAX_OIL =1 #default invocation helps contgrol traffic  multiple will messup gameplay so dount touch 
MAX_GARBAGE= 2
MAX_FISH=1
MAX_SEAWEED=2




pygame.init()
display = PyGameDisplay(width=128, height=128)
splash = displayio.Group()
display.show(splash)

my_background = displayio.OnDiskBitmap("articbg.bmp")
bg_sprite = displayio.TileGrid(my_background, pixel_shader=my_background.pixel_shader)
splash.append(bg_sprite)


game_over_bitmap = displayio.OnDiskBitmap("gameover.bmp")
print("Game over bitmap dimensions:", game_over_bitmap.width, "x", game_over_bitmap.height)
game_over_bitmap = displayio.OnDiskBitmap("gameover.bmp")
total_width = game_over_bitmap.width
frame_width = total_width // 5
game_over_sprite = displayio.TileGrid(
    game_over_bitmap,
    pixel_shader=game_over_bitmap.pixel_shader,
    width=1,
    height=1,
    tile_width=128,#do not touch debugging will be hell 
    tile_height=102, 
    x=0, 
    y=13 
)

# Add black background
black_bg = displayio.Bitmap(128, 128, 1)
black_palette = displayio.Palette(1)
black_palette[0] = 0x000000  # Black color
black_bg_sprite = displayio.TileGrid(black_bg, pixel_shader=black_palette)

def show_game_over_screen():
    if black_bg_sprite not in splash:
        splash.append(black_bg_sprite)
    if game_over_sprite not in splash:
        splash.append(game_over_sprite)
    
def hide_game_over_screen():
    if game_over_sprite in splash:
        splash.remove(game_over_sprite)
    if black_bg_sprite in splash:
        splash.remove(black_bg_sprite)

# def restart_game():
#     global game_over, game_started, immunity_active, immunity_start_time #issues fixeed the imunity should vbe global so added that here
#     hide_game_over_screen()
#     game_over = False
#     game_started = True
#     immunity_active = False
#     immunity_start_time = 0
#     seal_sprite.x = 64
#     seal_sprite.y = 80

#     for obj in oil + garbage + seaweed + fish:
#         if obj in splash:
#             splash.remove(obj)
    
#     oil.clear()
#     garbage.clear()
#     fish.clear()
#     seaweed.clear()





my_background=displayio.OnDiskBitmap("articbg.bmp")
bg_sprite= displayio.TileGrid(my_background, pixel_shader=my_background.pixel_shader)
splash.append(bg_sprite)


seal_sheet=displayio.OnDiskBitmap("sealsheet.bmp")

#objects loading like above asprte sprites 
oil_bitmap=displayio.OnDiskBitmap("oil.bmp")
garbage_bitmap=displayio.OnDiskBitmap("garbage.bmp")
oil=[]
garbage=[]

fish_bitmap=displayio.OnDiskBitmap("fish.bmp")
seaweed_bitmap=displayio.OnDiskBitmap("seaweed.bmp")
fish=[]
seaweed=[]


#contriol seal movement to male objs fall
game_over= False
key_pressed = False
game_started = False

#can add mote but no plan for now lets finfish basic game first -added in form of garbade and fish weed
hazards=[]
food=[]


def spawn_oil():
    Frame_width=32 # a multiple of full width needs to be adjusted to a no that can divided no of framws
    x_position=random.randint(0, display.width -Frame_width)
    oil_sprite = displayio.TileGrid(
        oil_bitmap,
        pixel_shader=oil_bitmap.pixel_shader,
        width=1,
        height=1,
        tile_width=Frame_width,
        tile_height=32,
        x=x_position,
        y=-32

        )
    oil.append(oil_sprite)
    splash.append(oil_sprite)

def spawn_garbage():
    Frame_width=32
    x_position=random.randint(0,display.width - Frame_width)
    garbage_sprite = displayio.TileGrid(
        garbage_bitmap,
        pixel_shader=garbage_bitmap.pixel_shader,
        width=1,
        height=1,           
        tile_width=Frame_width,
        tile_height=32,
        x=x_position,
        y=-32
    )
    garbage.append(garbage_sprite)
    splash.append(garbage_sprite)
#are just copies of what was used in the example code -reffered code given in hackpet

#change of code made - there was problem of the objects garbage and oil just appearing some distance above 
#and not touching and gave over occured so adjustment creted so it needs to be at least 3 px on seal
def check_collisoon(sprite1,sprite2):

    overlap_x=min(
        abs((sprite1.x + 32) - sprite2.x),
        abs((sprite2.x + 32) - sprite1.x)
    )

    overlap_y=min(
        abs((sprite1.y +32 ) - sprite2.y),
        abs((sprite2.y +32) - sprite1.y)
    )

    MIN_OVERLAP=3


    return(sprite1.x < sprite2.x +32 and
           sprite1.x +32 > sprite2.x and
           sprite1.y < sprite2.y +32 and
           sprite1.y + 32 > sprite2.y and
           overlap_x>= MIN_OVERLAP and
           overlap_y>= MIN_OVERLAP

    )
# death = displayio.OnDiskBitmap("restart.bmp")
# not yet implemented trying cause its too difficult

#food 
def spawn_fish():


    Frame_width=32
    x_position = random.randint(0,display.width - Frame_width)
    fish_sprite = displayio.TileGrid(
        fish_bitmap,
        pixel_shader=fish_bitmap.pixel_shader,
        width=1,
        height=1,
        tile_width=Frame_width,
        tile_height=32,
        x=x_position,
        y=-32
    )
    fish.append(fish_sprite)
    splash.append(fish_sprite)


def spawn_seaweed():
    Frame_width =16
    x_position =random.randint(0, display.width - Frame_width)
    seaweed_sprite = displayio.TileGrid(
        seaweed_bitmap,
        pixel_shader=seaweed_bitmap.pixel_shader,
        width=1,
        height=1,
        tile_width=Frame_width,
        tile_height=16,
        x=x_position,
        y=-32
    )
    seaweed.append(seaweed_sprite)
    splash.append(seaweed_sprite)






#adjusting tilegrid function as the sizes are different for the bmp files 
def create_tile_grid(sheet, tile_width, tile_height, x=0, y=0):
    if sheet == game_over_bitmap:
        tile_width = 128  
    
    return displayio.TileGrid(
        sheet,
        pixel_shader=sheet.pixel_shader,
        width=1,
        height=1,
        tile_height=tile_height,
        tile_width=tile_width,
        x=x,
        y=y
    )


    

#direct including caused problems so needed a list of all sprite problems 
sprites_info = [
    {"file": "sealsheet.bmp", "tile_width": 432, "tile_height": 48},  # Correct size
    {"file": "fish.bmp", "tile_width": 256, "tile_height": 32},  # Correct size
    {"file": "fish2.bmp", "tile_width": 224, "tile_height": 32},  # Correct size
    {"file": "garbage.bmp", "tile_width": 256, "tile_height": 32},  # Correct size
    {"file": "oil.bmp", "tile_width": 224, "tile_height": 32},  # Correct size
    {"file":"gameover.bmp","tile_width":128,"tile_height":102},#man debugged this for 4 hrs 
    {"file": "seaweed.bmp", "tile_width": 112, "tile_height": 16}  
]

# fish_bitmap = bitmaps.get("fish.bmp")

bitmaps ={}
for sprite_info in sprites_info:
    try:
        
        bitmaps[sprite_info["file"]]= displayio.OnDiskBitmap(sprite_info["file"])
    except ValueError as e:
        print(f"error loding {sprite_info['file']}:{e}")

fish_bitmap = bitmaps.get("fish.bmp")
if fish_bitmap is None:
    print("eror fish.bmp not loaded")


for sprite_info in sprites_info:
    sprite_sheet=displayio.OnDiskBitmap(sprite_info["file"])
    sprite = create_tile_grid(
        sprite_sheet,
        sprite_info["tile_width"],
        sprite_info["tile_height"],
        x=64,
        y=64
    )

Frame_width=48
seal_sprite=displayio.TileGrid(
    seal_sheet,
    pixel_shader=seal_sheet.pixel_shader,
    width=1,
    height=1,
    tile_height=48,
    tile_width=Frame_width,
    x=64,
    y=80
)
splash.append(seal_sprite)

#var fir game
frame =0
speed=4
game_over=False
animation_timer =0
is_moving= False

num_frames = seal_sheet.width // seal_sprite.tile_width 



while True:
    current_time = time.time()

    if game_over:
        time_since_game_over = current_time - game_over_start_time
        if time_since_game_over <= 1.0:
            frame_number = min(4, int(time_since_game_over * 5))
            game_over_sprite[0] = frame_number

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if game_over:
                if current_time - game_over_start_time >= 2:
                    restart_game()
            elif not game_started:
                game_started = True

    if game_started and not game_over: 
        if immunity_active and (current_time - immunity_start_time >= IMMUNITY_DURATION):
            immunity_active = False

        if len(oil) < MAX_OIL and random.random() < 0.08:
            spawn_oil()
        if len(garbage) < MAX_GARBAGE and random.random() < 0.07:
            spawn_garbage()
        if len(fish) < MAX_FISH and random.random() < 0.1:
            spawn_fish()
        if len(seaweed) < MAX_SEAWEED and random.random() < 0.1:
            spawn_seaweed()

        for oil_sprite in oil[:]:
            oil_sprite.y += 3
            if oil_sprite.y > display.height:
                if oil_sprite in splash:
                    splash.remove(oil_sprite)
                oil.remove(oil_sprite)
            elif not immunity_active and check_collisoon(seal_sprite, oil_sprite):
                game_over = True
                game_over_start_time = current_time
                show_game_over_screen()

        for garbage_sprite in garbage[:]:
            garbage_sprite.y += 3
            if garbage_sprite.y > display.height:
                if garbage_sprite in splash:
                    splash.remove(garbage_sprite)
                garbage.remove(garbage_sprite)
            elif not immunity_active and check_collisoon(seal_sprite, garbage_sprite):
                game_over = True
                game_over_start_time = current_time
                show_game_over_screen()

        for fish_sprite in fish[:]:
            fish_sprite.y += 2
            if fish_sprite.y > display.height:
                if fish_sprite in splash:
                    splash.remove(fish_sprite)
                fish.remove(fish_sprite)
            elif check_collisoon(seal_sprite, fish_sprite):
                if not immunity_active:
                    immunity_active = True
                    immunity_start_time = current_time
                    if fish_sprite in splash:
                        splash.remove(fish_sprite)
                    fish.remove(fish_sprite)

        for seaweed_sprite in seaweed[:]:
            seaweed_sprite.y += 2
            if seaweed_sprite.y > display.height:
                if seaweed_sprite in splash:
                    splash.remove(seaweed_sprite)
                seaweed.remove(seaweed_sprite)
            elif check_collisoon(seal_sprite, seaweed_sprite):
                if not immunity_active:
                    immunity_active = True
                    immunity_start_time = current_time
                    if seaweed_sprite in splash:
                        splash.remove(seaweed_sprite)
                    seaweed.remove(seaweed_sprite)

        keys = pygame.key.get_pressed()
        is_moving = False

        if keys[pygame.K_LEFT]:
            seal_sprite.x = max(0, seal_sprite.x - speed)
            is_moving = True

        if keys[pygame.K_RIGHT]:
            seal_sprite.x = min(display.width - Frame_width, seal_sprite.x + speed)
            is_moving = True

        if current_time - animation_timer >= 0.1:
            if is_moving:
                frame = (frame + 1) % num_frames
                seal_sprite[0] = frame
            else:
                seal_sprite[0] = 0
            animation_timer = current_time

    display.refresh()
    time.sleep(0.05)