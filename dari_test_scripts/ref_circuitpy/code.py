import board
import displayio
import digitalio
import busio
import time
import adafruit_imageload
from adafruit_ssd1351 import SSD1351
import random

displayio.release_displays()
spi = busio.SPI(clock=board.SCK, MOSI=board.MOSI)
tft_cs = board.GP3
tft_dc = board.GP4
reset_pin = board.GP5

rbtn = digitalio.DigitalInOut(board.BTNR)
rbtn.pull = digitalio.Pull.UP

mbtn = digitalio.DigitalInOut(board.BTNM)
mbtn.pull = digitalio.Pull.UP

lbtn = digitalio.DigitalInOut(board.BTNL)
lbtn.pull = digitalio.Pull.UP

display_bus = displayio.FourWire(
    spi, command=tft_dc, chip_select=tft_cs, reset=reset_pin, baudrate=16000000
)

display = SSD1351(display_bus, width=128, height=128)
display.rotation=180

# Make the display context
group = displayio.Group()
display.root_group = group
# group.x = 128
# group.y = 128

forest_bg_file = open("/images/bg_forest.bmp", "rb")
forest_bg = displayio.OnDiskBitmap(forest_bg_file)
forest_bg_sprite = displayio.TileGrid(forest_bg, pixel_shader=getattr(forest_bg, 'pixel_shader', displayio.ColorConverter()))

group.append(forest_bg_sprite)

# cat!!!!!!!!

cat_filename = "/images/cat_sheet_pbg.bmp"

cat_img, cat_pal = adafruit_imageload.load(cat_filename)
cat_pal.make_transparent(1)

cat_tilegrid = displayio.TileGrid(
    cat_img,
    pixel_shader=cat_pal,
    width=1,
    height=1,
    tile_width=32,
    tile_height=32,
    default_tile=0,
    x=(display.width - 32) // 2,
    y=display.height - 32 - 10
)

group.append(cat_tilegrid)

# fireballs !!!!!!!!!

fireball_file = "/images/fireball.bmp"

fireball_img, fireball_pal = adafruit_imageload.load(fireball_file)

fireball_pal.make_transparent(1)

fireballs = []

def spawn_fireball():
    x_position = random.randint(0, 128 - 32)
    fireball = displayio.TileGrid(
        fireball_img,
        pixel_shader=fireball_pal,
        width=1,
        height=1,
        tile_width=32,
        tile_height=32,
        x=x_position,
        y=-32
    )
    fireballs.append(fireball)
    group.append(fireball)

def check_collision(sprite1, sprite2):
    return (
        sprite1.x < sprite2.x + 32 and
        sprite1.x + 32 > sprite2.x and
        sprite1.y < sprite2.y + 32 and
        sprite1.y + 32 > sprite2.y
    )

# game over ??????

restart_filename = open("/images/restart.bmp", "rb")
restart_file = displayio.OnDiskBitmap(restart_filename)

def display_game_over():
    global restart
    restart = displayio.TileGrid(
        restart_file,
        pixel_shader=restart_file.pixel_shader,
        width=1,
        height=1,
        tile_width=64,
        tile_height=32,
        default_tile=0,
        x=(display.width - 64) // 2,
        y=(display.height - 32) // 2
    )
    group.append(restart)
    for i in fireballs:
        group.remove(i)
    fireballs.clear()

frame = 0
frame_time = 0
speed = 2
game_over = False

while True:

    if game_over == False:
        if not lbtn.value:
            cat_tilegrid.x -= speed
        elif not rbtn.value:
            cat_tilegrid.x += speed

        if random.random() < 0.01:  # spawn rate
            spawn_fireball()

    if not mbtn.value and game_over == True:
        group.remove(restart)
        game_over = False

    for fireball in fireballs:
        fireball.y += 2
        if fireball.y > display.height:
            group.remove(fireball)
            fireballs.remove(fireball)
        elif check_collision(cat_tilegrid, fireball):
            game_over = True
            display_game_over()

    frame_time += 1
    if frame_time >= 10:
        cat_tilegrid[0] = frame
        frame = (frame + 1) % 9
        frame_time = 0

    time.sleep(0.01)

