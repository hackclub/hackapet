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

# Defining bitmap graphics
walls_bitmap = displayio.OnDiskBitmap("assets/walls.bmp")
walls = displayio.TileGrid(walls_bitmap, pixel_shader=walls_bitmap.pixel_shader)
paddle_bitmap = displayio.OnDiskBitmap("assets/paddle.bmp")
paddle = displayio.TileGrid(
        paddle_bitmap,
        pixel_shader=paddle_bitmap.pixel_shader,
        width=1,
        height=1,
        tile_width=paddle_bitmap.width,
        tile_height=paddle_bitmap.height,
        x=48,
        y=112
    )
ball_bitmap = displayio.OnDiskBitmap("assets/ball.bmp")
ball = displayio.TileGrid(
    ball_bitmap,
    pixel_shader=ball_bitmap.pixel_shader,
    width=1,
    height=1,
    tile_width=11,
    tile_height=11,
    x=paddle.x+10,
    y=98
)
prompt_bitmap = displayio.OnDiskBitmap("assets/prompt.bmp")
prompt = displayio.TileGrid(prompt_bitmap, pixel_shader=prompt_bitmap.pixel_shader)
menu_bitmap = displayio.OnDiskBitmap("assets/settings.bmp")
menu = displayio.TileGrid(menu_bitmap, pixel_shader=menu_bitmap.pixel_shader)
menucursor_bitmap = displayio.OnDiskBitmap("assets/selector.bmp")
menucursor = displayio.TileGrid(
    menucursor_bitmap,
    pixel_shader=menucursor_bitmap.pixel_shader,
    width=1,
    height=1,
    tile_width=menucursor_bitmap.width,
    tile_height=menucursor_bitmap.height,
    x=0,
    y=0
)
bar_bitmap = displayio.OnDiskBitmap("assets/bar.bmp")
bar = displayio.TileGrid(
    bar_bitmap,
    pixel_shader=bar_bitmap.pixel_shader,
    width=1,
    height=1,
    tile_width=bar_bitmap.width,
    tile_height=bar_bitmap.height,
    x=0,
    y=0
)
barfiller_bitmap = displayio.OnDiskBitmap("assets/barfiller.bmp")
barfiller = displayio.TileGrid(
    barfiller_bitmap,
    pixel_shader=barfiller_bitmap.pixel_shader,
    width=1,
    height=1,
    tile_width=barfiller_bitmap.width,
    tile_height=barfiller_bitmap.height,
    x=-29,
    y=0
)
adjust_bitmap = displayio.OnDiskBitmap("assets/adjust.bmp")
adjust = displayio.TileGrid(
    adjust_bitmap,
    pixel_shader=adjust_bitmap.pixel_shader,
    width=1,
    height=1,
    tile_width=adjust_bitmap.width,
    tile_height=adjust_bitmap.height,
    x=0,
    y=0
)
credits_bitmap = displayio.OnDiskBitmap("assets/credits.bmp")
credits = displayio.TileGrid(credits_bitmap, pixel_shader=credits_bitmap.pixel_shader)

# 0 = game screen, 1 = settings screen, 2 = credits
screen = 0

# Screen definitions
def draw_elements():
    # Removes all existing elements from splash
    for i in range(len(splash)-1, -1, -1):
        del splash[i]
    if screen == 0:
        splash.append(walls)
        splash.append(paddle)
        splash.append(ball)
        splash.append(prompt)
    if screen == 1:
        splash.append(menu)
        splash.append(menucursor)
        splash.append(barfiller)
        splash.append(bar)
    if screen == 2:
        splash.append(credits)
draw_elements()

# Game vars
ball_x_speed = 0
ball_y_speed = 0
ball_x_dir = 1
ball_y_dir = 1
move_speed = 7
frame = 0
frame_offset = 2
game_over = True

# Settings vars
button_positions = [0,16,48]
cursor_pos = 0
adjusting = False
speed_seting = 4

while True:
    if display.check_quit():
        break
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            exit()

    keys = pygame.key.get_pressed()
    if screen == 0: # Game screen
        if keys[pygame.K_LEFT] and paddle.x > 16:
            paddle.x -= move_speed
        if keys[pygame.K_RIGHT] and paddle.x < 80:
            paddle.x += move_speed
        if keys[pygame.K_UP] and game_over == True:
            ball_x_speed = speed_seting
            ball_y_speed = speed_seting
            game_over = False
            splash.remove(prompt)
        if keys[pygame.K_LEFT] and keys[pygame.K_RIGHT] and game_over == True:
            screen = 1
            draw_elements()
        
        if game_over == True:
            ball.x = paddle.x + 10
            ball.y = 98
            ball_x_speed = 0
            ball_y_speed = 0
        
        ball.x += (ball_x_speed * ball_x_dir)
        ball.y -= (ball_y_speed * ball_y_dir)
        if ball.x >= 100:
            ball.x = 100
            ball_x_dir *= -1
            ball_x_speed = speed_seting + round(random.random()*3)
            frame_offset = (frame_offset + 1) % 3
        if ball.x <= 16:
            ball.x = 16
            ball_x_dir *= -1
            ball_x_speed = speed_seting + round(random.random()*3)
            frame_offset = (frame_offset + 1) % 3
        if ball.y <= 17:
            ball.y = 17
            ball_y_dir *= -1
            ball_y_speed = speed_seting + round(random.random()*3)
            frame_offset = (frame_offset + 1) % 3

        if ball.y >= 100:
            if ball.x >= paddle.x - 10 and ball.x <= paddle.x + 30:
                ball.y = 99
                ball_y_dir = 1
                ball_y_speed = speed_seting + round(random.random()*3)
                frame_offset = (frame_offset + 1) % 3
            else:
                splash.append(prompt)
                game_over = True
    elif screen == 1: # Settings screen
        if not adjusting:
            if keys[pygame.K_RIGHT] and cursor_pos < len(button_positions) - 1:
                cursor_pos += 1
            if keys[pygame.K_LEFT] and cursor_pos > 0:
                cursor_pos -= 1
            if keys[pygame.K_UP]:
                if cursor_pos == 0:
                    screen = 0
                    draw_elements()
                if cursor_pos == 1:
                    adjusting = True
                    splash.append(adjust)
                    adjust.y = menucursor.y
                if cursor_pos == 2:
                    screen = 2
                    draw_elements()
        else:
            if keys[pygame.K_RIGHT] and speed_seting < 6:
                speed_seting += 1
            elif keys[pygame.K_LEFT] and speed_seting > 1:
                speed_seting -= 1
            elif keys[pygame.K_UP]:
                adjusting = False
                splash.remove(adjust)

            barfiller.x = -89 + (speed_seting * 15)

        menucursor.y = button_positions[cursor_pos]
    elif screen == 2: # Credits screen
        if keys[pygame.K_RIGHT] or keys[pygame.K_LEFT]:
            screen = 1
            draw_elements()

    ball[0] = frame + frame_offset*4
    if game_over == False:
        frame = (frame + 1) % 4

    time.sleep(0.07)