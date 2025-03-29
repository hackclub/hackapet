import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
import pygame
import time
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font
from random import randint

pygame.init()
pygame.mixer.init()
speaker_volume = 0.2

pygame.mixer.music.load("badapple.wav")
pygame.mixer.music.set_volume(speaker_volume)


# this is bad
original_spawn_events = {
    # time (seconds): lane (0,1,2)
    2: 0,
    3: 0,
    5: 0,
    7: 0,
    8: 1,
    9: 2,
    10: 1,
    11: 2,
    12: 0,
    13: 1,
    14: 0,
    15: 1,
    # thing
    16: 0,
    17: 2,
    18: 0,
    19: 1,
    20: 2,
    21: 0,
    22: 0,
    23: 1,
}


spawn_events = [
    randint(0, 2) if x % 4 == 0 else randint(0, 2) if x % 3 == 0 else 2
    for x in range(217)
]


display = PyGameDisplay(width=128, height=128)
splash = displayio.Group()
display.show(splash)

bg = displayio.OnDiskBitmap("bg.bmp")
bg_sprite = displayio.TileGrid(bg, pixel_shader=bg.pixel_shader)
splash.append(bg_sprite)

cat_sheet = displayio.OnDiskBitmap("cat.bmp")

tile_width = 32
tile_height = 32

cat_sprite = displayio.TileGrid(
    cat_sheet,
    pixel_shader=cat_sheet.pixel_shader,
    width=1,
    height=1,
    tile_width=tile_width,
    tile_height=tile_height,
    default_tile=0,
    x=(display.width - tile_width) // 2,
    y=display.height - tile_height - 4,
)

splash.append(cat_sprite)

fruit_bitmap = displayio.OnDiskBitmap("burger.bmp")

fruits = []

disabledfruits = []


def spawnfruit(lane):
    lanes = [0, display.width // 3, 2 * display.width // 3]  # Define 3 lanes
    x_position = lanes[lane]  # Randomly choose one of the lanes
    fruit = displayio.TileGrid(
        fruit_bitmap,
        pixel_shader=fruit_bitmap.pixel_shader,
        width=1,
        height=1,
        tile_width=fruit_bitmap.width,
        tile_height=fruit_bitmap.height,
        x=x_position,
        y=-32,
    )
    fruits.append(fruit)
    splash.append(fruit)


combofruit = displayio.TileGrid(
    fruit_bitmap,
    pixel_shader=fruit_bitmap.pixel_shader,
    width=1,
    height=1,
    tile_width=fruit_bitmap.width,
    tile_height=fruit_bitmap.height,
    x=32,
    y=display.height - (tile_height * 2),
)

splash.append(combofruit)


# Function to check for collisions
def check_collision(sprite1, sprite2):
    return (
        sprite1.x < sprite2.x + 32
        and sprite1.x + 32 > sprite2.x
        and sprite1.y < sprite2.y + 32
        and sprite1.y + 32 > sprite2.y
    )


frame = 0
speed = 8
game_over = False
started = False
combo = False

score = 0
start_time = time.time()
game_time = 0

start = displayio.OnDiskBitmap("start.bmp")

win = displayio.OnDiskBitmap("win.bmp")

displayed_score = False

font = bitmap_font.load_font("./helvR12.bdf")


def finished(score):
    global winscreen
    global displayed_score
    if displayed_score:
        return
    winscreen = displayio.TileGrid(
        win,
        pixel_shader=win.pixel_shader,
    )
    splash.append(
        winscreen,
    )
    text_area = label.Label(
        font,
        text=f"Missed: {217 - score}",
        color=0xFFFFFF,
        x=(display.width - 55) // 2,
        y=(display.height - 12) // 2,
    )
    splash.append(text_area)
    displayed_score = True


startscreen = displayio.TileGrid(
    start,
    pixel_shader=start.pixel_shader,
)
splash.append(
    startscreen,
)

text_area = label.Label(
    font,
    text="",
    color=0xFFFFFF,
    x=(10),
    y=(display.height - 12),
)
splash.append(text_area)


while True:
    game_time = int(time.time() - start_time)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    if combo:
        combofruit.x = cat_sprite.x
    else:
        combofruit.x = -32

    keys = pygame.key.get_pressed()

    if not started and keys[pygame.K_x]:
        splash.remove(startscreen)
        pygame.mixer.music.play()
        started = True

    if not game_over and started:
        if game_time > 217:
            game_over = True
        if keys[pygame.K_z] and cat_sprite.x - speed >= 0:
            cat_sprite.x -= speed
        if keys[pygame.K_c] and cat_sprite.x + speed <= (128 - tile_width):
            cat_sprite.x += speed
        if keys[pygame.K_x]:
            speed = 16
        else:
            speed = 8

        if game_time < len(spawn_events):
            lane = spawn_events[game_time]
            if lane != -1:
                spawnfruit(lane)
                spawn_events[game_time] = -1
    elif game_over and started:
        finished(score)

    for fruit in fruits:
        fruit.y += 5
        if fruit.y > display.height:
            splash.remove(fruit)
            fruits.remove(fruit)
        elif fruit.y > (display.height - 64):
            if fruit in disabledfruits:
                continue
            disabledfruits.append(fruit)
            combo = False
        elif check_collision(combofruit, fruit):
            if fruit in disabledfruits:
                continue
            splash.remove(fruit)
            fruits.remove(fruit)
            score += 1
            combo = True
            text_area.text = f"Score: {score}"
        elif check_collision(cat_sprite, fruit):
            if fruit in disabledfruits:
                continue
            splash.remove(fruit)
            fruits.remove(fruit)
            score += 1
            combo = True
            text_area.text = f"Score: {score}"

    cat_sprite[0] = frame
    frame = (frame + 1) % (cat_sheet.width // tile_width)

    time.sleep(0.1)
