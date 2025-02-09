import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
import pygame
import random
import time
import ntplib
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import label

pygame.init()

# hw_accel=False
# Set to disabled if on Linux using https://github.com/CyrilSLi/Blinka_Displayio_PyGameDisplay
display = PyGameDisplay(width=128, height=128, hw_accel=False)
splash = displayio.Group()
display.show(splash)

bg_state = "sun_mnt"

try:
    c = ntplib.NTPClient()
    response = c.request("pool.ntp.org")
    currentHour = time.localtime(response.tx_time).tm_hour
    if currentHour > 19 or currentHour < 6:
        bg_state = "night_mnt"
except:
    print("No internet")

if bg_state == "sun_mnt":
    sun_bg_sheet = displayio.OnDiskBitmap("sun_bg.bmp")

    sun_bg_sprite = displayio.TileGrid(
        sun_bg_sheet,
        pixel_shader=sun_bg_sheet.pixel_shader,
        width=1,
        height=1,
        tile_width=128,
        tile_height=128,
        default_tile=0,
    )

    splash.append(sun_bg_sprite)

if bg_state == "night_mnt":
    night_bg_sheet = displayio.OnDiskBitmap("night_bg.bmp")

    night_bg_sprite = displayio.TileGrid(
        night_bg_sheet,
        pixel_shader=night_bg_sheet.pixel_shader,
        width=1,
        height=1,
        tile_width=128,
        tile_height=128,
        default_tile=0,
    )

    splash.append(night_bg_sprite)

bear_sheet = displayio.OnDiskBitmap("bear.bmp")

bear_sprite = displayio.TileGrid(
    bear_sheet,
    pixel_shader=bear_sheet.pixel_shader,
    width=1,
    height=1,
    tile_width=32,
    tile_height=32,
    default_tile=0,
    x=int((display.width / 2)) - 16,
    y=display.height - 29,
)

splash.append(bear_sprite)

timer_sheet = displayio.OnDiskBitmap("timer.bmp")

timer_sprite = displayio.TileGrid(
    timer_sheet,
    pixel_shader=timer_sheet.pixel_shader,
    width=1,
    height=1,
    tile_width=128,
    tile_height=128,
    default_tile=0,
)

splash.append(timer_sprite)

if bg_state == "night_mnt":
    start_sheet = displayio.OnDiskBitmap("night_start.bmp")

    start_sprite = displayio.TileGrid(
        start_sheet,
        pixel_shader=start_sheet.pixel_shader,
        width=1,
        height=1,
        tile_width=128,
        tile_height=128,
        default_tile=0,
    )

    splash.append(start_sprite)

if bg_state == "sun_mnt":
    start_sheet = displayio.OnDiskBitmap("sun_start.bmp")

    start_sprite = displayio.TileGrid(
        start_sheet,
        pixel_shader=start_sheet.pixel_shader,
        width=1,
        height=1,
        tile_width=128,
        tile_height=128,
        default_tile=0,
    )

    splash.append(start_sprite)

score_label_text = label.Label(
    bitmap_font.load_font("font.bdf"),
    text="Score:",
    color=0xFFFFFF,
    y=int(display.height / 2) - 20,
    x=20,
)

splash.append(score_label_text)
score_label_text.text = ""

score_text = label.Label(
    bitmap_font.load_font("font.bdf"),
    text="Start",
    color=0xFFFFFF,
    y=int(display.height / 2),
    x=20,
)

splash.append(score_text)

bomb_sheet = displayio.OnDiskBitmap("bomb.bmp")
blueberry_sheet = displayio.OnDiskBitmap("blueberry.bmp")
acorn_sheet = displayio.OnDiskBitmap("acorn.bmp")
fish_sheet = displayio.OnDiskBitmap("fish.bmp")

fallingObjects = {
    "bomb": [],
    "blueberry": [],
    "acorn": [],
    "fish": [],
}


def addFallingObject(type):
    bitmaps = {
        "bomb": bomb_sheet,
        "blueberry": blueberry_sheet,
        "acorn": acorn_sheet,
        "fish": fish_sheet,
    }
    bitmap = bitmaps[type]
    x_position = random.randint(0, display.width - bitmap.width)
    display_object = displayio.TileGrid(
        bitmap,
        pixel_shader=bitmap.pixel_shader,
        width=1,
        height=1,
        tile_width=bitmap.width,
        tile_height=bitmap.height,
        x=x_position,
        y=bitmap.height * -1,
    )
    fallingObjects[type].append(display_object)
    splash.append(display_object)


sun_bg_frame = 0
night_bg_frame = 0
bear_frame = 0

night_bg_timer = 0

windowState = "title"
gameTimer = 0
score = 0

initial = True

timer_timer = 0
timer_frame = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and windowState == "title":
                windowState = "game"
                if initial == True:
                    splash.remove(start_sprite)
                    initial = False
                score_text.text = ""
                score_label_text.text = ""
                score = 0

    if gameTimer >= 25:
        windowState = "title"
        gameTimer = 0
        for objectType in fallingObjects:
            for individual in fallingObjects[objectType][:]:
                fallingObjects[objectType].remove(individual)
                splash.remove(individual)
        bear_sprite.x = int((display.width / 2)) - 16
        bear_sprite.y = display.height - 29
        score_label_text.text = "Score:"
        score_text.text = str(score)

    keys = pygame.key.get_pressed()

    if windowState == "game":
        if keys[pygame.K_LEFT]:
            if bear_sprite.x != -16:
                bear_sprite.x -= 4
        if keys[pygame.K_RIGHT]:
            if bear_sprite.x != (display.width - 16):
                bear_sprite.x += 4
        tickChance = random.random()
        if tickChance < 0.025:
            addFallingObject("fish")
        elif tickChance < 0.05:
            addFallingObject("blueberry")
        elif tickChance < 0.075:
            addFallingObject("acorn")
        elif tickChance < 0.1:
            addFallingObject("bomb")
        for objectType in fallingObjects:
            for individual in fallingObjects[objectType]:
                individual.y += 5
                if individual.y > display.height:
                    splash.remove(individual)
                    fallingObjects[objectType].remove(individual)
                elif (
                    individual.x < bear_sprite.x + 32
                    and individual.x + 32 > bear_sprite.x
                    and individual.y < bear_sprite.y + 32
                    and individual.y + 32 > bear_sprite.y
                ):
                    if objectType == "bomb":
                        score -= 4
                    elif objectType == "fish":
                        score += 2
                    elif objectType == "acorn":
                        score += 4
                    elif objectType == "blueberry":
                        score += 6
                    splash.remove(individual)
                    fallingObjects[objectType].remove(individual)

    if bg_state == "sun_mnt":
        sun_bg_sprite[0] = sun_bg_frame
        sun_bg_frame = (sun_bg_frame + 1) % (sun_bg_sheet.width // 128)
    elif bg_state == "night_mnt":
        if night_bg_timer % 4 == 0:
            night_bg_sprite[0] = night_bg_frame
            night_bg_frame = (night_bg_frame + 1) % (night_bg_sheet.width // 128)
        night_bg_timer += 1

    bear_frame += 1
    if bear_frame % 60 == 0:
        bear_sprite[0] = 1
    else:
        bear_sprite[0] = 0

    if windowState == "game":
        if (timer_timer / 10).is_integer() and timer_timer % 5 == 0:
            timer_sprite[0] = timer_frame
            timer_frame = (timer_frame + 1) % (timer_sheet.width // 128)
        timer_timer += 1
        gameTimer += 0.1
    time.sleep(0.1)
