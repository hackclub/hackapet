import displayio
from adafruit_display_text import label
from blinka_displayio_pygamedisplay import PyGameDisplay
import pygame

pygame.init()
display = PyGameDisplay(width=128, height=128)
splash = displayio.Group()
display.show(splash)

def load_bitmap(filename):
    try:
        bitmap = displayio.OnDiskBitmap(filename)
        print(f"Loaded {filename} successfully!")
        return bitmap
    except Exception as e:
        print(f"Error loading {filename}: {e}")
        return None

def load_home_screen():
    splash = displayio.Group()

    background = load_bitmap("background.bmp")
    if background:
        splash.append(displayio.TileGrid(background, pixel_shader=background.pixel_shader))

    home_ninja_sheet = load_bitmap("ninjast.bmp")
    if home_ninja_sheet:
        tile_width = 32  
        tile_height = 32  
        frame_count_home_ninja = 2 

        home_ninja_sprite = displayio.TileGrid(
            home_ninja_sheet,
            pixel_shader=home_ninja_sheet.pixel_shader,
            width=1,
            height=1,
            tile_width=tile_width,
            tile_height=tile_height,
            default_tile=0,
            x=48,
            y=80
        )
        splash.append(home_ninja_sprite)

    return splash, home_ninja_sprite

def load_game_over_screen():
    splash = displayio.Group()

    background = load_bitmap("Over.bmp")
    if background:
        splash.append(displayio.TileGrid(background, pixel_shader=background.pixel_shader, x=0, y=0))
        
    return splash

def load_obstacle():
    obstacle = load_bitmap("obstacle.bmp")
    if obstacle:
        obstacle_sprite = displayio.TileGrid(
            obstacle,
            pixel_shader=obstacle.pixel_shader,
            width=1,
            height=1,
            tile_width=32,  
            tile_height=32,  
            default_tile=0,
            x=200, 
            y=85  
        )
        return obstacle_sprite
    return None

def load_game_screen():
    splash = displayio.Group()

    background2 = load_bitmap("background2.bmp")
    if background2:
        background2_sprite = displayio.TileGrid(background2, pixel_shader=background2.pixel_shader, x=0, y=0)
        splash.append(background2_sprite)

    cloud = load_bitmap("cloud.bmp")
    if cloud:
        cloud_sprite = displayio.TileGrid(cloud, pixel_shader=cloud.pixel_shader, x=0, y=10)
        splash.append(cloud_sprite)


    roof = load_bitmap("roof.bmp")
    if roof:
        roof_sprite = displayio.TileGrid(roof, pixel_shader=roof.pixel_shader, x=0, y=0)
        splash.append(roof_sprite)

    ninja_sheet = load_bitmap("run.bmp")
    ninja_sprite = None
    if ninja_sheet:
        tile_width = 32 
        tile_height = 32 
        ninja_sprite = displayio.TileGrid(
            ninja_sheet,
            pixel_shader=ninja_sheet.pixel_shader,
            width=1,
            height=1,
            tile_width=tile_width,
            tile_height=tile_height,
            default_tile=0,
            x=48,
            y=85
        )
        splash.append(ninja_sprite)

    obstacle_sprite = load_obstacle()
    if obstacle_sprite:
        splash.append(obstacle_sprite)

    return splash, ninja_sprite, cloud_sprite, roof_sprite, obstacle_sprite

home_screen = True
game_screen = False
game_over_screen = False

splash, home_ninja_sprite = load_home_screen()
display.show(splash)

clock = pygame.time.Clock()

# Jumping variables
is_jumping = False
jump_height = 3.4  
gravity = 0.1  
jump_velocity = 0  
ninja_y = 85  

frame_delay = 10  
frame_counter = 0

ninja_x = 10  
ninja_y = 81  
ninja_speed = 2  

cloud_speed = 0.2  


cloud_x = 0
roof_x = 0
background_x = 0

# Main loop
while True:
    clock.tick(60)  

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    keys = pygame.key.get_pressed()

    if home_screen and keys[pygame.K_RETURN]:
        home_screen = False
        game_screen = True
        splash, ninja_sprite, cloud_sprite, roof_sprite, obstacle_sprite = load_game_screen()
        display.show(splash)

    if game_screen and keys[pygame.K_a]:
        game_screen = False
        home_screen = True
        splash, home_ninja_sprite = load_home_screen()
        display.show(splash)

    if game_screen:
        if keys[pygame.K_SPACE] and not is_jumping: 
            is_jumping = True
            jump_velocity = -jump_height  

        if is_jumping:
            ninja_y += jump_velocity  
            jump_velocity += gravity  

            if ninja_y >= 80:  
                ninja_y = 80
                is_jumping = False
                jump_velocity = 0  

        if ninja_sprite:
            ninja_sprite.x = ninja_x
            ninja_sprite.y = int(ninja_y)

        frame_counter += 1
        if frame_counter >= frame_delay:
            if ninja_sprite:
                ninja_sprite[0] = (ninja_sprite[0] + 1) % 2  
            frame_counter = 0

        cloud_x -= cloud_speed  
        if cloud_x <= -128:  
            cloud_x = 128
        cloud_sprite.x = int(cloud_x)

        if obstacle_sprite:
            obstacle_sprite.x -= 1  
            if obstacle_sprite.x < -32:  
                obstacle_sprite.x = 200

            if (ninja_sprite.x < obstacle_sprite.x + 15 and ninja_sprite.x + 15 > obstacle_sprite.x and
                ninja_sprite.y < obstacle_sprite.y + 15 and ninja_sprite.y + 15 > obstacle_sprite.y):
                print("Collision detected!")
                game_screen = False
                game_over_screen = True
                splash = load_game_over_screen()
                display.show(splash)

    if home_screen and home_ninja_sprite:
        frame_counter += 1
        if frame_counter >= frame_delay:
            home_ninja_sprite[0] = (home_ninja_sprite[0] + 1) % 2  
            frame_counter = 0

    if game_over_screen:
        if keys[pygame.K_a]:  # If 'A' is pressed, go back to the home screen
            game_over_screen = False
            home_screen = True
            splash, home_ninja_sprite = load_home_screen()
            display.show(splash)

        if keys[pygame.K_RETURN]:  # If 'Enter' is pressed, restart the game
            game_over_screen = False
            game_screen = True
            splash, ninja_sprite, cloud_sprite, roof_sprite, obstacle_sprite = load_game_screen()
            display.show(splash)

    pygame.display.update()
