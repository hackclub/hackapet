import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
import pygame
import time
import random

pygame.init()

display = PyGameDisplay(width=128, height=128)
splash = displayio.Group()
display.show(splash)

forest_background = displayio.OnDiskBitmap("forestbackground.png")
bg_sprite = displayio.TileGrid(forest_background, pixel_shader=forest_background.pixel_shader)
splash.append(bg_sprite)

cat_sheet = displayio.OnDiskBitmap("cat-Sheet.png")

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
    y=display.height - tile_height - 24     
)

fireball_bitmap = displayio.OnDiskBitmap("fireball.bmp")

fireballs = []

def spawn_fireball():
    x_position = random.randint(0, display.width - fireball_bitmap.width)
    fireball = displayio.TileGrid(
        fireball_bitmap,
        pixel_shader=fireball_bitmap.pixel_shader,
        width=1,
        height=1,
        tile_width=fireball_bitmap.width,
        tile_height=fireball_bitmap.height,
        x=x_position,
        y=-32
    )
    fireballs.append(fireball)
    splash.append(fireball)

# Function to check for collisions
def check_collision(sprite1, sprite2):
    return (
        sprite1.x < sprite2.x + 32 and
        sprite1.x + 32 > sprite2.x and
        sprite1.y < sprite2.y + 32 and
        sprite1.y + 32 > sprite2.y
    )

death = displayio.OnDiskBitmap("restart.bmp")

def display_game_over():
    global death_hi
    death_hi = displayio.TileGrid(
        death,
        pixel_shader=cat_sheet.pixel_shader,
        width=1,
        height=1,
        tile_width=128,
        tile_height=128,
        default_tile=0,
        x=0,  
        y=0  
    )
    splash.append(death_hi)
    for i in fireballs:
        splash.remove(i)
    fireballs.clear()

def main():
    clock = pygame.time.Clock()
    delta = 0
    
    frame = 0

    hunger = 0
    main_menu = 0

    feeding = False

    frame_change = 0.25

    run = True

    while run:
        delta = clock.tick(15) / 1000

        frame_change -= delta

        if frame_change <= 0:
            frame_change += 0.25
            frame = (frame + 1) % 4
            cat_sprite[0] = frame

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if not feeding:
                        main_menu = max(-1, main_menu - 1)
                    else:
                        if cat_sprite.x == 64 - 16:
                            cat_sprite.x = 0
                        else:
                            cat_sprite.x = 64 - 16
                if event.key == pygame.K_RIGHT:
                    if not feeding:
                        main_menu = min(+1, main_menu + 1)
                    else:
                        if cat_sprite.x == 0:
                            cat_sprite.x = 64 - 16
                        else:
                            cat_sprite.x = 128 - 32
                if event.key == pygame.K_UP:
                    match main_menu:
                        case -1:
                            pass
                        case 0:
                            feeding = not feeding

                            if not feeding:
                                cat_sprite.x = 64 - tile_width // 2
                        case 1:
                            pass

        if not feeding and random.random() < 1.0e-4:
            hunger = min(3, hunger + 1)
        
        # clear screen
        for el in splash:
            splash.remove(el)

        # draw background
        match main_menu:
            case -1:
                pass
            case 0:
                splash.append(bg_sprite)
            case 1:
                pass
        
        # draw 'cat'
        splash.append(cat_sprite)
        
    pygame.quit()
    
main()