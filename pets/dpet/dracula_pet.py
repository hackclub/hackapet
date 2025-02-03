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

backgrounds = ["desert.bmp", "desert2.bmp", "desert3.bmp"]
current_bg_index = 0
last_bg_change_time = time.time()

tile_width = 32
tile_height = 32

def show_game_over_screen():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        time.sleep(1)

        if show_start_menu():
            reset_game()
            break

start_menu = displayio.OnDiskBitmap("start_menu.bmp")
start_menu_sprite = displayio.TileGrid(start_menu, pixel_shader=start_menu.pixel_shader) 

quit_menu = displayio.OnDiskBitmap("quit_menu.bmp")
quit_menu_sprite = displayio.TileGrid(quit_menu, pixel_shader=quit_menu.pixel_shader) 




def show_start_menu():

    splash.append(start_menu_sprite)
    
    current_action = 1
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            if current_action == 1:
                splash.pop()
                splash.append(quit_menu_sprite)
                current_action = 2
            elif current_action == 2:
                splash.pop()
                splash.append(start_menu_sprite)
                current_action = 1
        elif keys[pygame.K_DOWN]:
            if current_action == 1:
                splash.pop()
                splash.append(quit_menu_sprite)
                current_action = 2
            elif current_action == 2:
                splash.pop()
                splash.append(start_menu_sprite)
                current_action = 1

        if keys[pygame.K_RIGHT]:
            if current_action == 1:
                return True
            elif current_action == 2:
                pygame.quit()        
                exit()   
        time.sleep(0.1)

dog_sheet = displayio.OnDiskBitmap("doggy.bmp")
dog_sprite = displayio.TileGrid(
    dog_sheet,
    pixel_shader=dog_sheet.pixel_shader,
    width=1,
    height=1,
    tile_width=tile_width,
    tile_height=tile_height,
    default_tile=0,
    x=(display.width - tile_width) // 2,
    y= display.height - tile_height - 10
)
splash.append(dog_sprite)


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

def change_background():
    global current_bg_index, bg_sprite
    current_bg_index = (current_bg_index + 1) % len(backgrounds)
    new_background = displayio.OnDiskBitmap(backgrounds[current_bg_index])
    new_bg_sprite = displayio.TileGrid(new_background, pixel_shader=new_background.pixel_shader)
    
    splash.insert(0, new_bg_sprite) 
    splash.pop(1)


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


grid_step = 4

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
    win_image = displayio.OnDiskBitmap("win.bmp")
    game_over_sprite = displayio.TileGrid(
        win_image,
        pixel_shader=win_image.pixel_shader
    )
    splash.append(game_over_sprite)
    global game_over
    game_over = True


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

    island_background = displayio.OnDiskBitmap(backgrounds[current_bg_index])
    bg_sprite = displayio.TileGrid(island_background, pixel_shader=island_background.pixel_shader) 
    splash.append(bg_sprite)
    splash.append(dog_sprite)
    splash.append(crab_sprite)

treasure_x, treasure_y = get_random_treasure_position()

fireball_bitmap = displayio.OnDiskBitmap("fireball.bmp")
fireballs = []

def get_proximity():
    distance_x = abs(dog_sprite.x - treasure_x)
    distance_y = abs(dog_sprite.y - treasure_y)
    distance = distance_x + distance_y

    if distance == 0:
        return "YOU FOUND IT!"
    elif distance <= 5:
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

frame = 0
speed = 3
game_over = False

wings_frames = 0

while True:
    if show_start_menu():

        reset_game()

        while True:
                    
            if time.time() - last_bg_change_time >= 15:
                change_background()
                last_bg_change_time = time.time()

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

                if keys[pygame.K_LEFT] and keys[pygame.K_RIGHT] and dog_sprite.y < display.height - tile_height - 10:
                    dog_sprite.y += speed
                if keys[pygame.K_UP] and dog_sprite.y > 0 :
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

                
                if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP]:
                    dog_sprite[0] = wings_frames

                if keys[pygame.K_LEFT] and keys[pygame.K_RIGHT] and dog_sprite.y > display.height - tile_height - 20 and dog_sprite.y < display.height - tile_height:
                    splash.remove(dog_sprite)
                    dog_sprite = displayio.TileGrid(
                    dog_sheet,
                        pixel_shader=dog_sheet.pixel_shader,
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
                if message == "HOT!":
                    print("a7aaa")
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
                if not restart_ready:
                    restart_ready = True

                if restart_ready:
                    show_game_over_screen()

            dog_sprite[0] = frame
            frame = (frame + 1) % (dog_sheet.width // tile_width)
            wings_frames = (wings_frames + 1) % 3
            
            time.sleep(0.1)
