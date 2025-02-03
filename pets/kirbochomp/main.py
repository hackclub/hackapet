import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
import pygame
import time
import random
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font

pygame.init()

display = PyGameDisplay(width=128, height=128)
splash = displayio.Group()
display.show(splash)

# load backgrounds
title_bg = displayio.OnDiskBitmap("assets/main_bg.bmp")
game_bg = displayio.OnDiskBitmap("assets/game_bg.bmp")

title_sprite = displayio.TileGrid(
    title_bg, 
    pixel_shader=title_bg.pixel_shader
)

bg_sprite = displayio.TileGrid(
    game_bg,
    pixel_shader=game_bg.pixel_shader
)

splash.append(title_sprite)

# load font
font = bitmap_font.load_font("assets/courB08.bdf")
reg_font = bitmap_font.load_font("assets/courB12.bdf")
text_color = 0xFFE0EE

# setup title text
title_text = label.Label(font, text="KIRBOCHOMP", color=text_color, x=(display.width//2)-len("KIRBOCHOMP")-48, y=display.height//2-36, scale=2)
left_arrow_text = label.Label(reg_font, text="LEFT - UP", color=text_color, x=(display.width//2)-50, y=(display.height//2)-8)
right_arrow_text = label.Label(reg_font, text="RIGHT - DOWN", color=text_color, x=(display.width//2)-60, y=(display.height//2)+10)
start_text_1 = label.Label(reg_font, text="press to", color=text_color, x=(display.width//2)-40, y=(display.height//2)+24)
start_text_2 = label.Label(reg_font, text="start!", color=text_color, x=(display.width//2)-28, y=(display.height//2)+38)

splash.append(title_text)
splash.append(left_arrow_text)
splash.append(right_arrow_text)
splash.append(start_text_1)
splash.append(start_text_2)

# setup score
score = 0

# load kirbo sprites
kirbo_sheet = displayio.OnDiskBitmap("assets/kirbo_idle.bmp")
kirbo_float_absorb = displayio.OnDiskBitmap("assets/kirbo_absorb_up.bmp")
kirbo_absorb_sheet = displayio.OnDiskBitmap("assets/kirbo_absorb_down.bmp")

tile_width = 48
tile_height = 48
ground_height = display.height - tile_height - 24
x_coord = (display.width - tile_width) // 6

kirbo_sprite = displayio.TileGrid(
    kirbo_sheet,
    pixel_shader=kirbo_sheet.pixel_shader,
    width=1,
    height=1,
    tile_width=tile_width,
    tile_height=tile_height,
    default_tile=0,
    x=x_coord,
    y=ground_height
)

kirbo_float = displayio.TileGrid(
    kirbo_float_absorb,
    pixel_shader=kirbo_float_absorb.pixel_shader,
    width=1,
    height=1,
    tile_width=tile_width,
    tile_height=tile_height,
    default_tile=0,
    x=x_coord,
    y=ground_height
)

kirbo_absorb = displayio.TileGrid(
    kirbo_absorb_sheet,
    pixel_shader=kirbo_absorb_sheet.pixel_shader,
    width=1,
    height=1,
    tile_width=tile_width,
    tile_height=tile_height,
    default_tile=0,
    x=x_coord,
    y=ground_height
)

# add/subtract from sprite's y position
def jump(kirbo_sprite, speed, dir):
    if dir:
        kirbo_sprite.y -= speed
    else:
        kirbo_sprite.y += speed

# load food sprites
cake_bitmap = displayio.OnDiskBitmap("assets/cake.bmp")
candy_bitmap = displayio.OnDiskBitmap("assets/candy.bmp")
star_bitmap = displayio.OnDiskBitmap("assets/star.bmp")
tomato_bitmap = displayio.OnDiskBitmap("assets/tomato.bmp")
foods = []

# spawn random food in top or bottom half of screen
def spawn_food():
    y_pos = random.choice([26, 58])
    cur_food = random.choice([cake_bitmap, candy_bitmap, star_bitmap, tomato_bitmap])
    food = displayio.TileGrid(
        cur_food,
        pixel_shader=cur_food.pixel_shader,
        width=1,
        height=1,
        tile_width=tile_width,
        tile_height=tile_height,
        default_tile=0,
        x=display.width + 48,
        y=y_pos
    )
    foods.append(food)
    splash.append(food)

# check if two sprites collide
def check_collision(sprite1, sprite2):
    if sprite1.x > sprite2.x - 16 and sprite1.x < sprite2.x + 16 and sprite1.y > sprite2.y - 16 and sprite1.y < sprite2.y + 16:
        return True
    return False

# clear screen and display game end bg
def display_game_over(splash, title_sprite, foods):
    for layer in splash:
        splash.remove(layer)
    foods.clear()

    # setup game over text + score
    game_over_text = label.Label(font, text="GAME OVER!", color=text_color, x=(display.width//2)-58, y=(display.height//2)-28, scale=2)
    score_text = label.Label(reg_font, text=f"score: {score}", color=text_color, x=(display.width//2)-40-len(str(score)), y=(display.height//2)-12)
    restart_text_1 = label.Label(reg_font, text="press to", color=text_color, x=(display.width//2)-44, y=(display.height//2)+12)
    restart_text_2 = label.Label(reg_font, text="play again!", color=text_color, x=(display.width//2)-54, y=(display.height//2)+30)

    splash.append(title_sprite)
    splash.append(game_over_text)
    splash.append(score_text)
    splash.append(restart_text_1)
    splash.append(restart_text_2)

# keep track of frame, speed, current kirbo sprite
frame = 0
speed = 16
cur_kirbo = kirbo_sprite

game_start = False
game_over = False

# keep track of kirbo movement
jump_up = False
fall_down = False
to_float = False
to_absorb = False
absorb_time = 0

# keep track of food spawning
food_time = 0
food_speed_up = 0
spawn_food_time = 20

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    keys = pygame.key.get_pressed()

    # display title screen on start, begin game by pressing a key
    if not game_start:
        if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_SPACE]:
            game_start = True
            for layer in splash:
                splash.remove(layer)

            splash.append(bg_sprite)
            splash.append(kirbo_sprite)

    # start game again after game over and a key is pressed
    elif game_over:
        if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_SPACE]:
            game_over = False
            for layer in splash:
                splash.remove(layer)

            splash.append(bg_sprite)
            splash.append(kirbo_sprite)

            jump_up = False
            fall_down = False
            to_float = False
            to_absorb = False
            absorb_time = 0

            food_time = 0
            food_speed_up = 0
            spawn_food_time = 20

            cur_kirbo = kirbo_sprite
            score = 0
    
    # game stuff
    else:
        food_time += 1

        # setup float sprite and jump if left key is pressed
        if keys[pygame.K_LEFT]:
            jump_up = True
            kirbo_float.y = ground_height
            absorb_time = 0
            to_absorb = False

            if kirbo_absorb in splash:
                splash.remove(kirbo_absorb)
            if kirbo_sprite in splash:
                splash.remove(kirbo_sprite)
            if kirbo_float in splash:
                splash.remove(kirbo_float)
            splash.append(kirbo_float)

            frame = 0
            cur_kirbo = kirbo_float
        
        # set up absorb sprite if right key is pressed
        if keys[pygame.K_RIGHT]:
            to_absorb = True
            absorb_time = 0
            jump_up = False
            to_float = False
            fall_down = False

            if kirbo_float in splash:
                splash.remove(kirbo_float)
            if kirbo_sprite in splash:
                splash.remove(kirbo_sprite)
            if kirbo_absorb in splash:
                splash.remove(kirbo_absorb)
            splash.append(kirbo_absorb)

            frame = 0
            cur_kirbo = kirbo_absorb
        
        # move up until sprite is above y = 24
        if jump_up:
            jump(kirbo_float, speed, True)

            frame = (frame + 1) % (kirbo_float_absorb.width // kirbo_float.tile_width)
            kirbo_float[0] = frame

            if kirbo_float.y <= 24:
                jump_up = False
                to_float = True
        
        # sprite stays in air for a bit
        elif to_float:
            absorb_time += 1
            kirbo_float[0] = 2

            if absorb_time == 3:
                to_float = False
                absorb_time = 0
                fall_down = True
        
        # sprite falls back to the ground
        elif fall_down:
            jump(kirbo_float, speed, False)

            frame = (frame + 1) % (kirbo_float_absorb.width // kirbo_float.tile_width)
            kirbo_float[0] = frame

            if kirbo_float.y >= ground_height:
                kirbo_float.y = ground_height
                fall_down = False
                splash.append(kirbo_sprite)
                splash.remove(kirbo_float)
                cur_kirbo = kirbo_sprite
        
        # sprote absorb animation on ground level
        elif to_absorb:
            absorb_time += 1
            
            if 4 >= absorb_time >= 2:
                frame = 2
            else:
                frame = (frame + 1) % (kirbo_float_absorb.width // kirbo_float.tile_width)
            kirbo_absorb[0] = frame

            if absorb_time == 6:
                to_absorb = False
                absorb_time = 0
                splash.append(kirbo_sprite)
                splash.remove(kirbo_absorb)
                cur_kirbo = kirbo_sprite
        
        # otherwise, animate idle kirbo
        else:
            kirbo_sprite[0] = frame
            frame = (frame + 1) % (kirbo_sheet.width // kirbo_sprite.tile_width)
        
        # spawn new food
        if food_time == spawn_food_time:
            spawn_food()
            food_time = 0
            food_speed_up += 1
            # increase frequency of food spawn after every 5 spawned foods
            if food_speed_up == 5:
                food_speed_up = 0
                spawn_food_time = round(spawn_food_time*0.9)
        
        # move foods across screen
        for item in foods:
            item.x -= 8
            if cur_kirbo != kirbo_sprite and check_collision(cur_kirbo, item):
                splash.remove(item)
                foods.remove(item)
                score += 1
            # end game if kirbo misses a food
            if item.x < -32:
                game_over = True
                for layer in splash:
                    splash.remove(layer)
                display_game_over(splash, title_sprite, foods)
                break

    time.sleep(0.08)