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

forest_background = displayio.OnDiskBitmap("desert.bmp")
bg_sprite = displayio.TileGrid(forest_background, pixel_shader=forest_background.pixel_shader)
splash.append(bg_sprite)

def display_found_it():
    yellow_background = displayio.Bitmap(display.width, display.height, 1)
    yellow_palette = displayio.Palette(1)
    yellow_palette[0] = 0xFFFF00
    yellow_bg_sprite = displayio.TileGrid(yellow_background, pixel_shader=yellow_palette)
    splash.append(yellow_bg_sprite)
    font = bitmap_font.load_font("./helvR12.bdf")
    text_area = label.Label(font, text="YOU FOUND IT!", color=0x000000, x=(display.width - 100) // 2,
                            y=(display.height - 10))
    splash.append(text_area)
    game_over_image = displayio.OnDiskBitmap("restart.bmp")
    game_over_sprite = displayio.TileGrid(
        game_over_image,
        pixel_shader=game_over_image.pixel_shader
    )
    splash.append(game_over_sprite)
    global game_over
    game_over = True

dog_sheet = displayio.OnDiskBitmap("doggy.bmp")
tile_width = 32
tile_height = 32
dog_sprite = displayio.TileGrid(
    dog_sheet,
    pixel_shader=dog_sheet.pixel_shader,
    width=1,
    height=1,
    tile_width=tile_width,
    tile_height=tile_height,
    default_tile=0,
    x=(display.width - tile_width) // 2,
    y=display.height - tile_height - 10
)
splash.append(dog_sprite)

grid_step = 4

def get_random_treasure_position():
    x = random.randint(0, (display.width - tile_width) // grid_step) * grid_step
    possible_y_values = list(range(-2, 99, grid_step))
    y = random.choice(possible_y_values)
    return x, y

restart_ready = False
game_over_time = 0

def reset_game():
    global dog_sprite, treasure_x, treasure_y, fireballs, game_over, frame, restart_ready, crab_sprite, crab_direction

    dog_sprite.x = (display.width - tile_width) // 2
    dog_sprite.y = display.height - tile_height - 10
    treasure_x, treasure_y = get_random_treasure_position()
    fireballs = []
    game_over = False
    frame = 0
    restart_ready = False

    crab_sprite.x = 0
    crab_sprite.y = display.height - crab_height - 10
    crab_direction = 1

    while len(splash) > 0:
        splash.pop()

    splash.append(bg_sprite)
    splash.append(dog_sprite)
    splash.append(crab_sprite)

treasure_x, treasure_y = get_random_treasure_position()

fireball_bitmap = displayio.OnDiskBitmap("fireball.bmp")
fireballs = []

def spawn_fireball():
    x_position = random.randint(0, display.width - tile_width)
    fireball = displayio.TileGrid(
        fireball_bitmap,
        pixel_shader=fireball_bitmap.pixel_shader,
        width=1,
        height=1,
        tile_width=tile_width,
        tile_height=tile_height,
        x=x_position,
        y=-tile_height
    )
    fireballs.append(fireball)
    splash.append(fireball)

def get_proximity():
    distance_x = abs(dog_sprite.x - treasure_x)
    distance_y = abs(dog_sprite.y - treasure_y)
    distance = distance_x + distance_y

    if distance == 0:
        return "YOU FOUND IT!"
    elif distance <= 10:
        return "HOT!"
    elif distance <= 30:
        return "WARM!"
    else:
        return "COLD!"

def display_proximity_message(message):
    for sprite in splash:
        if isinstance(sprite, label.Label):
            splash.remove(sprite)
    font = bitmap_font.load_font("./helvR12.bdf")
    text_area = label.Label(font, text=message, color=0x000000, x=display.width - 5 - len(message) * 8,
                            y=display.height - 20)
    splash.append(text_area)

crab_bitmap = displayio.OnDiskBitmap("crab.bmp")
crab_width = 32
crab_height = 32

crab_sprite = displayio.TileGrid(
    crab_bitmap,
    pixel_shader=crab_bitmap.pixel_shader,
    width=1,
    height=1,
    tile_width=crab_width,
    tile_height=crab_height,
    x=0,
    y=(display.height - crab_height - 2)
)
splash.append(crab_sprite)

crab_speed = 2
crab_direction = 1

frame = 0
speed = 4
game_over = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    keys = pygame.key.get_pressed()

    if not game_over:
        if keys[pygame.K_LEFT] and dog_sprite.x > 0:
            dog_sprite.x -= speed
        if keys[pygame.K_RIGHT] and dog_sprite.x < display.width - tile_width:
            dog_sprite.x += speed

        if keys[pygame.K_LEFT] and keys[pygame.K_RIGHT] and dog_sprite.y < display.height - tile_height:
            dog_sprite.y += speed
        if keys[pygame.K_UP] and dog_sprite.y > 0:
            dog_sprite.y -= speed
            splash.remove(dog_sprite)
            dog_wings_sheet = displayio.OnDiskBitmap("doggy_wings.bmp")
            dog_sprite = displayio.TileGrid(
                dog_wings_sheet,
                pixel_shader=dog_wings_sheet.pixel_shader,
                width=1,
                height=1,
                tile_width=tile_width,
                tile_height=tile_height,
                default_tile=0,
                x=dog_sprite.x,
                y=dog_sprite.y
            )
            splash.append(dog_sprite)

        crab_sprite.x += crab_speed * crab_direction
        if crab_sprite.x <= 0 or crab_sprite.x >= display.width - crab_width:
            crab_direction *= -1

        if abs(dog_sprite.x - crab_sprite.x) < tile_width and abs(dog_sprite.y - crab_sprite.y) < tile_height:
            display_proximity_message("DOG HIT CRAB!")
            time.sleep(2)

        message = get_proximity()
        display_proximity_message(message)

        if dog_sprite.x == treasure_x and dog_sprite.y == treasure_y:
            display_found_it()

        if random.random() < 0.02:
            spawn_fireball()

        for fireball in fireballs[:]:
            fireball.y += 4

            if fireball.y > display.height:
                splash.remove(fireball)
                fireballs.remove(fireball)
            elif (
                dog_sprite.x < fireball.x + tile_width
                and dog_sprite.x + tile_width > fireball.x
                and dog_sprite.y < fireball.y + tile_height
                and dog_sprite.y + tile_height > fireball.y
            ):
                game_over = True
                game_over_time = time.time()
                display_proximity_message("GAME OVER!")
                game_over_image = displayio.OnDiskBitmap("restart.bmp")
                game_over_sprite = displayio.TileGrid(
                    game_over_image,
                    pixel_shader=game_over_image.pixel_shader
                )
                splash.append(game_over_sprite)

    else:
        if not restart_ready and time.time() - game_over_time >= 1.5:
            restart_ready = True

        if restart_ready and keys[pygame.K_UP]:
            reset_game()

    dog_sprite[0] = frame
    frame = (frame + 1) % (dog_sheet.width // tile_width)

    time.sleep(0.1)
