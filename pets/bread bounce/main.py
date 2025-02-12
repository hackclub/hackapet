import displayio
from adafruit_bitmap_font import bitmap_font
from blinka_displayio_pygamedisplay import PyGameDisplay
import pygame
import time
import random
from adafruit_display_text import label


pygame.init()

display = PyGameDisplay(width=128, height=128)
splash = displayio.Group()
display.show(splash)


bg = displayio.OnDiskBitmap("bg.bmp")
bg_sprite = displayio.TileGrid(
    bg,
    pixel_shader=bg.pixel_shader,
    width=1,
    height=1,
    tile_width=128,
    tile_height=128,
    default_tile=0
    )

splash.append(bg_sprite)



bread_sheet = displayio.OnDiskBitmap("bread_spritesheet.bmp")

bread_sprite = displayio.TileGrid(
    bread_sheet,
    pixel_shader=bread_sheet.pixel_shader,
    width=1,
    height=1,
    tile_width=21,
    tile_height=22,
    default_tile=0,
    x=display.width // 2,
    y=2
)

splash.append(bread_sprite)

bread_sprite.speed_x = random.randint(-2, 2)
bread_sprite.speed_y = random.randint(-2, 2)



duck_sheet = displayio.OnDiskBitmap("duck_eye_open_spritesheet.bmp")

tile_width = 26
tile_height = 24

duck_sprite = displayio.TileGrid(
    duck_sheet,
    pixel_shader=duck_sheet.pixel_shader,
    width=1,
    height=1,
    tile_width=tile_width,
    tile_height=tile_height,
    default_tile=0,
    x=(display.width - 32) // 2,
    y=display.height - 26
    )

splash.append(duck_sprite)

duck_sprite.direction = 0 #0: left, 1: right
duck_sprite.speed_x = 1


frame = 0

game_state = 0
colours = [000000, 229944]
#0: menu
#1: game
#2: game over

def change_bg():
    bg_sprite[0] = random.randint(0, 1)

def check_collision(sprite1, sprite2):
    return (
            sprite1.x < sprite2.x + 21 and
            sprite1.x + 26 > sprite2.x and
            sprite1.y < sprite2.y + 22 and
            sprite1.y + 26 > sprite2.y
           )

def change_speed(x_min, x_max, y_min, y_max):
    bread_sprite.speed_x = random.randint(x_min, x_max)
    bread_sprite.speed_y = random.randint(y_min, y_max)

previous_time = time.time()

def read_high_score():
    file = open("high_score.txt", "r")
    line = file.readlines()
    hs = int(line[0])
    file.close()
    return hs

def save_score(score_param):
    file = open("high_score.txt", "w")
    file.write(str(score_param))
    file.close()

def countdown():
    count = 3
    countdown_label = label.Label(font=bitmap_font.load_font("ter-u12.bdf"), text=str(count), color=colours[bg_sprite[0]],
                                      scale=5, x=53, y=64)
    splash.append(countdown_label)

    for i in range(0, 3):
        splash.remove(countdown_label)

        countdown_label = label.Label(font=bitmap_font.load_font("ter-u12.bdf"), text=str(count), color=colours[bg_sprite[0]],
                                          scale=5, x=53, y=64)
        splash.append(countdown_label)

        count -= 1
        time.sleep(0.5)
    splash.remove(countdown_label)

def change_bread_expression():
    if bread_sprite[0] == 0:
        bread_sprite[0] = 1
    else:
        bread_sprite[0] = 0


start_menu_sheet = displayio.OnDiskBitmap("start_menu_spritesheet.bmp")

start_menu_sprite = displayio.TileGrid(
    start_menu_sheet,
    pixel_shader=start_menu_sheet.pixel_shader,
    width=1,
    height=1,
    tile_width=128,
    tile_height=128,
    default_tile=0,
    x=0,
    y=0
)

splash.append(start_menu_sprite)

game_over_sheet = displayio.OnDiskBitmap("game_over_spritesheet.bmp")

game_over_sprite = displayio.TileGrid(
    game_over_sheet,
    pixel_shader=game_over_sheet.pixel_shader,
    width=1,
    height=1,
    tile_width=128,
    tile_height=128,
    default_tile=1,
    x=0,
    y=0
)

splash.append(game_over_sprite)

lives = 3
score = 0
change_bg()
score_label = label.Label(font=bitmap_font.load_font("ter-u12.bdf"), text=f"score: {str(score)}", color=colours[bg_sprite[0]], scale=1, x=20, y=4)
splash.append(score_label)

highscore = read_high_score()
highscore_label = label.Label(font=bitmap_font.load_font("ter-u12.bdf"), text=f"highscore: {str(highscore)}", color=colours[bg_sprite[0]], scale=1, x=20, y=15)
splash.append(highscore_label)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    if game_state == 0:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            start_menu_sprite[0] = 1
            game_state = 1
            countdown()

    if game_state == 1:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            duck_sprite.x -= 1
            duck_sprite.direction = 0
            duck_sprite[0] = duck_sprite.direction

        if keys[pygame.K_RIGHT]:
            duck_sprite.x += 1
            duck_sprite.direction = 1
            duck_sprite[0] = duck_sprite.direction

        if (bread_sprite.x <= 0 or bread_sprite.x >= 128) and bread_sprite.y <= 75:

            if bread_sprite.x <= 0:
                bread_sprite.x = 0
            elif bread_sprite.x >= 128:
                bread_sprite.x = 128

            change_bread_expression()

            bread_sprite.speed_x *= -1
            bread_sprite.speed_y = 1

        if bread_sprite.y <= 0:

            change_bread_expression()

            bread_sprite.y = 0
            bread_sprite.speed_y *= -1
            bread_sprite.speed_x = random.randint(1, 2)

        if check_collision(duck_sprite, bread_sprite):
            score += 1

            splash.remove(score_label)
            score_label = label.Label(font=bitmap_font.load_font("ter-u12.bdf"), text=f"score: {str(score)}", color=colours[bg_sprite[0]], scale=1,
                                      x=20, y=4)
            splash.append(score_label)

            change_bread_expression()

            bread_sprite.speed_y = -1
            bread_sprite.speed_x = random.randint(-2, -1)

        if bread_sprite.y >= 128 or bread_sprite.x <= -10 or bread_sprite.x >= 138:
            lives -= 1

            if lives <= 0:
                game_state = 2

            else:
                bread_sprite.x = display.width // 2
                bread_sprite.y = 2
                bread_sprite.speed_x = 1
                bread_sprite.speed_y = 1
                countdown()

        bread_sprite.x += bread_sprite.speed_x
        bread_sprite.y += bread_sprite.speed_y




    if game_state == 2:

        game_over_sprite[0] = 0

        if score > highscore:
            highscore = score
            save_score(score)


        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:

            change_bg()

            lives = 3
            score = 0

            splash.remove(score_label)
            score_label = label.Label(font=bitmap_font.load_font("ter-u12.bdf"), text=f"score: {str(score)}",
                                      color=colours[bg_sprite[0]], scale=1,
                                      x=20, y=4)
            splash.append(score_label)

            splash.remove(highscore_label)
            highscore_label = label.Label(font=bitmap_font.load_font("ter-u12.bdf"),
                                          text=f"highscore: {str(highscore)}",
                                          color=colours[bg_sprite[0]], scale=1, x=20, y=15)
            splash.append(highscore_label)

            bread_sprite.x = display.width // 2
            bread_sprite.y = 2
            game_over_sprite[0] = 1
            game_state = 1
            countdown()


    time.sleep(0.01)
