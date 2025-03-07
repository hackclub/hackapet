import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay, time
import pygame
import random
import time

def get_time() -> str:
    return ':'.join(str(e).removeprefix('0') if i == 0 else str(e) for i, e in enumerate(time.ctime().split(' ')[3].split(':')[:2]))

pygame.init()

display = PyGameDisplay(width=128, height=128)
splash = displayio.Group()
display.show(splash)

forest_background_left = displayio.OnDiskBitmap("forestbackgroundleft.png")
forest_background_center = displayio.OnDiskBitmap("forestbackgroundcenter.png")
forest_background_right = displayio.OnDiskBitmap("forestbackgroundright.png")
bg_sprite_left = displayio.TileGrid(forest_background_left, pixel_shader=forest_background_left.pixel_shader)
bg_sprite_center = displayio.TileGrid(forest_background_center, pixel_shader=forest_background_center.pixel_shader)
bg_sprite_right = displayio.TileGrid(forest_background_right, pixel_shader=forest_background_right.pixel_shader)

cat_sheet = displayio.OnDiskBitmap("cat-Sheet.png")
numbers_sheet = displayio.OnDiskBitmap("numbers.png")

fruit = displayio.OnDiskBitmap("fruit.png")
bomb = displayio.OnDiskBitmap("bomb.png")

def draw_char(char, x, y):
    spr = displayio.TileGrid(
        numbers_sheet,
        pixel_shader=numbers_sheet.pixel_shader,
        width=1,
        height=1,
        tile_width=8,
        tile_height=9,
        default_tile=0,
        x=x,  
        y=y     
    )

    if char == ':':
        spr[0] = 10
    else:
        spr[0] = int(char)

    return spr

def new_fruit(x, y):
    return displayio.TileGrid(
        fruit,
        pixel_shader=fruit.pixel_shader,
        width=1,
        height=1,
        tile_width=32,
        tile_height=32,
        default_tile=0,
        x=x,  
        y=y     
    )

def new_bomb(x, y):
    return displayio.TileGrid(
        bomb,
        pixel_shader=bomb.pixel_shader,
        width=1,
        height=1,
        tile_width=32,
        tile_height=32,
        default_tile=0,
        x=x,  
        y=y     
    )

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

# Function to check for collisions
def check_collision(sprite1, sprite2):
    return (
        sprite1.x < sprite2.x + 32 and
        sprite1.x + 32 > sprite2.x and
        sprite1.y < sprite2.y + 32 and
        sprite1.y + 32 > sprite2.y
    )

def main():
    clock = pygame.time.Clock()
    delta = 0
    
    frame = 0

    hunger = 0
    main_menu = 0

    feeding = False

    dead = False

    frame_change = 0.35

    direction = 1

    score = 0

    last_minute = 0

    feed_timer = 0

    run = True

    obs = []

    while run:
        delta = clock.tick(15) / 1000

        if feeding:
            feed_timer -= delta

            if feed_timer <= 0:
                feed_timer += 2

                obs.append([
                    random.randint(0, 1),
                    random.choice([0, 48, 96]),
                    -32
                ])

        frame_change -= delta

        if frame_change <= 0:
            frame_change += 0.35
            frame += direction
            if frame in [0, 3]:
                direction *= -1
            cat_sprite[0] = frame
        

        if dead:
            cat_sprite[0] = 4

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
                    if not dead:
                        match main_menu:
                            case -1:
                                pass
                            case 0:
                                feeding = not feeding

                                if not feeding:
                                    cat_sprite.x = 64 - tile_width // 2
                                else:
                                    feed_timer = 0
                                    obs = []

                                    if not hunger:
                                        feeding = False
                                        cat_sprite.x = 64 - tile_width // 2
                            
                            case 1:
                                pass
                    else:
                        dead = False
                        hunger = 0
                        score = 0

        if not feeding and random.random() < 1.0e-3:
            if hunger == 3:
                dead = True

            hunger = min(3, hunger + 1)
        
        # clear screen
        for el in splash:
            splash.remove(el)

        timestr = get_time()

        # draw background
        match main_menu:
            case -1:
                splash.append(bg_sprite_left)
            
                x, y = display.width // 2 - 5 * len(timestr), 8
                for c in timestr:
                    splash.append(draw_char(c, x, y))
                    x += 10
            case 0:
                splash.append(bg_sprite_center)
            case 1:
                splash.append(bg_sprite_right)
        
        if not dead:
            # update score

            minute = int(timestr.split(':')[1])
            if minute != last_minute:
                if last_minute != 0:
                    score += 1
                last_minute = minute

        if feeding:
            # draw obstacles
            for o in obs[::-1]:
                o[2] += delta * 35
                
                if o[0]:
                    splash.append(n := new_fruit(o[1], o[2]))
                    
                    if check_collision(cat_sprite, n):
                        hunger -= 1
                        obs.remove(o)
                        if hunger == 0:
                            feeding = False
                            cat_sprite.x = 64 - tile_width // 2
                            continue
                else:
                    splash.append(n := new_bomb(o[1], o[2]))

                    if check_collision(cat_sprite, n):
                        feeding = False
                        cat_sprite.x = 64 - tile_width // 2

        # draw 'cat'
        splash.append(cat_sprite)

        # draw score
        x, y = 0, 0
        for c in str(score):
            splash.append(draw_char(c, x, y))
            x += 10

        # draw hunger
        splash.append(draw_char(str(hunger)[0], 120, 0))

    pygame.quit()
    
main()