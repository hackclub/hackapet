import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
import pygame
import time
from adafruit_display_text import label
from datetime import datetime
import random
from adafruit_bitmap_font import bitmap_font

# -------------------------------------
# Variables
# -------------------------------------
selected = 0
current_screen = "menu"
fuel = 50
always_on = True
current_time = datetime.now().strftime("%H:%M")
first_open = True
plane_frame = 0
refuel_truck_frame = 0
time_elapsed = 0
fueled = False
animate = False
speed = 4
frame = 0
game_over = False
points = 0
lives = 3
ringes = []
nukes = []
ANIMATION_FRAMES = 24 
spawn_rate = {"nuke": random.randint(1, 70)/100,
            "ring": random.randint(1, 70)/100}
is_timer_on = False
FONT = bitmap_font.load_font("ter-u12.bdf") 

# Bitmaps
btn_bmp = displayio.OnDiskBitmap(open("button.bmp", "rb"))
plane_bmp = displayio.OnDiskBitmap(open("contyjet.bmp", "rb"))
background_bmp = displayio.OnDiskBitmap(open("idle_background.bmp", "rb"))
dice_bmp = displayio.OnDiskBitmap(open("dice.bmp", "rb"))
maintain_bmp = displayio.OnDiskBitmap(open("maintainance_truck.bmp", "rb"))
forest_background = displayio.OnDiskBitmap("game_background.bmp")
ring_sheet = displayio.OnDiskBitmap("ring.bmp")
nuke_sheet = displayio.OnDiskBitmap("nuke.bmp")
menu_background = displayio.OnDiskBitmap("menu_background.bmp")

# -------------------------------------
# THE GAME 
# -------------------------------------

display = PyGameDisplay(width=128, height=128)
game = displayio.Group()
game.hidden = True

text_group = displayio.Group()
# Create the score label
score_label = label.Label(
    FONT,
    text=f"Score: {points}",
    color=0xFFFFFF,  # White
    x=5,
    y=10
)

# Create the lives label
lives_label = label.Label(
    FONT,
    text=f"Lives: {lives}",
    color=0xFFFFFF,  # White
    x=5,
    y=25
)

text_group.append(score_label)
text_group.append(lives_label)
def update_text():
    score_label.text = f"Score: {points}"
    lives_label.text = f"Lives: {lives}"

bg_sprite = displayio.TileGrid(forest_background, pixel_shader=forest_background.pixel_shader)
game.append(bg_sprite)

plane_sheet = displayio.OnDiskBitmap("contyjet.bmp")
tile_width = 50
tile_height = 50

plane = displayio.TileGrid(
    plane_sheet,
    pixel_shader=plane_sheet.pixel_shader,
    width=1,
    height=1,
    tile_width=tile_width,
    tile_height=tile_height,
    default_tile=0,
    x=(display.width - tile_width) // 2,
    y=display.height - tile_height - 10,
)

game.append(plane)
game.append(text_group)

def spawn_ring():
    ring = displayio.TileGrid(
        ring_sheet,
        pixel_shader=ring_sheet.pixel_shader,
        width=1,
        height=1,
        tile_width=16,
        tile_height=16,
        default_tile=0,
        x=random.randint(0, display.width - 16),
        y=0
    )
    ringes.append(ring)
    game.append(ring)

def spawn_nuke():
    nuke = displayio.TileGrid(
        nuke_sheet,
        pixel_shader=ring_sheet.pixel_shader,
        width=1,
        height=1,
        tile_width=16,
        tile_height=16,
        default_tile=0,
        x=random.randint(0, display.width - 16),
        y=0
    )
    nukes.append(nuke)
    game.append(nuke)


def check_collision(sprite1, sprite2):
    return (
        sprite1.x < sprite2.x + 16 and
        sprite1.x + 16 > sprite2.x and
        sprite1.y < sprite2.y + 16 and
        sprite1.y + 16 > sprite2.y
    )

death_hi = label.Label(
    FONT,
    text="Game Over",
    color=0xFFFFFF,  # White
    x=display.width // 2 - 30,
    y=display.height // 2
)

death_hi.hidden = True
game.append(death_hi)

def show_death():
    score_label.x = display.width // 2 - 30
    score_label.y = display.height // 2 + 20

    death_hi.hidden = False
    lives_label.hidden = True
    bg_sprite.hidden = True
    plane.hidden = True
    time_elapsed = 0

def reset_game():
    global lives, points, game_over

    game.hidden = True
    plane.hidden = False
    bg_sprite.hidden = False
    lives = 3
    points = 0
    score_label.x = 5
    score_label.y = 10
    death_hi.hidden = True
    game_over = False


# -------------------------------------
# Display
# -------------------------------------
display = PyGameDisplay(width=128, height=128)
splash = displayio.Group()
display.show(splash)

# -------------------------------------
# Refueler Screen
# -------------------------------------
refuel_group = displayio.Group()
refuel_group.hidden = True 

refuel_truck = displayio.TileGrid(
    maintain_bmp,
    pixel_shader=plane_bmp.pixel_shader,
    width=1,
    height=1,
    tile_width=32,
    tile_height=32,
    default_tile=0,
    x=25,
    y=96
)

refuel_plane = displayio.TileGrid(
    plane_bmp,
    pixel_shader=plane_bmp.pixel_shader,
    width=1,
    height=1,
    tile_width=50,
    tile_height=50,
    default_tile=0,
    x=(display.width - 50) // 2,
    y=(display.height - 50) // 2 + 30,
)
background = displayio.TileGrid(
    background_bmp,
    pixel_shader=background_bmp.pixel_shader,
    width=1,
    height=1,
    tile_width=128,
    tile_height=128,
)

refuel_group.append(background)
refuel_group.append(refuel_truck)
refuel_group.append(refuel_plane)

refuel_success_group = displayio.Group()

refuel_success = label.Label(
    FONT,
    text="Refueled!",
    color=0xFFFFFF,
    x=(display.width - 32) // 2 - 5,
    y=(display.width - 32) // 2 
)

refuel_success_group.append(refuel_success)

refuel_success_group.hidden = True


# -------------------------------------
# Randomsizer Screen
# -------------------------------------
random_group = displayio.Group()
random_group.hidden = True  # Start hidden

dice = displayio.TileGrid(
    dice_bmp,
    pixel_shader=plane_bmp.pixel_shader,
    width=1,
    height=1,
    tile_width=64,
    tile_height=64,
    default_tile=0,
    x=(display.width - 64) // 2,
    y=(display.height - 64) // 2,
)

random_group.append(dice)



# -------------------------------------
# Idle Screen
# -------------------------------------

# Regular Idle Screen
idle_on_group = displayio.Group()
idle_on_group.hidden = True  # Start hidden



background = displayio.TileGrid(
    background_bmp,
    pixel_shader=background_bmp.pixel_shader,
    width=1,
    height=1,
    tile_width=128,
    tile_height=128,
)

on_plane = displayio.TileGrid(
    plane_bmp,
    pixel_shader=plane_bmp.pixel_shader,
    width=1,
    height=1,
    tile_width=50,
    tile_height=50,
    default_tile=0,
    x=(display.width - 50) // 2,
    y=(display.height - 50) // 2 + 20,
)

fuel_label = label.Label(
    FONT,
    text="Fuel: " + str(fuel) + "%",
    color=0xFFFFFF,
    x=(display.width - 32) // 2,
    y=16
)

idle_on_group.append(background)
idle_on_group.append(on_plane)
idle_on_group.append(fuel_label)

# Always On Mode
idle_always_on_group = displayio.Group()
idle_always_on_group.hidden = True  # Start hidden

always_on_plane = displayio.TileGrid(
    plane_bmp,
    pixel_shader=plane_bmp.pixel_shader,
    width=1,
    height=1,
    tile_width=50,
    tile_height=50,
    default_tile=0,
    x=(display.width - 50) // 2,
    y=(display.height - 50) // 2,
)

clock_label = label.Label(
    FONT,
    text=current_time,
    color=0xFFFFFF,
    x=(display.width - 32) // 2,
    y=16,
    scale=1
)

idle_always_on_group.append(always_on_plane)
idle_always_on_group.append(clock_label)

# -------------------------------------
# Menu
# -------------------------------------

menu_group = displayio.Group()
menu_group.hidden = False  

# Background for menu
menu_background_sprite = displayio.TileGrid(
    menu_background,
    pixel_shader=menu_background.pixel_shader,
    width=1,
    height=1,
    tile_width=128,
    tile_height=128,
    default_tile=0
)

menu_group.append(menu_background_sprite)

# Text for menu
text_menu_group = displayio.Group()

refuel_label = label.Label(
    FONT,
    text="Refuel",
    color=0xFFFFFF,
    x=(display.width - 32) // 2,
    y=16
)
text_menu_group.append(refuel_label)

random_label = label.Label(
    FONT,
    text="Random",
    color=0xFFFFFF,
    x=(display.width - 32) // 2,
    y=48
)
text_menu_group.append(random_label)

walk_label = label.Label(
    FONT,
    text="Fly",
    color=0xFFFFFF,
    x=(display.width - 16) // 2,
    y=80
)
text_menu_group.append(walk_label)

idle_label = label.Label(
    FONT,
    text="Idle",
    color=0xFFFFFF,
    x=(display.width - 24) // 2,
    y=112
)
text_menu_group.append(idle_label)

menu_group.append(text_menu_group)

# Buttons for menu
buttons_menu_group = displayio.Group()

btn_random_sprite = displayio.TileGrid(
    btn_bmp, 
    pixel_shader=displayio.ColorConverter(),
    width=1,
    height=1,
    tile_width=120,
    tile_height=30,
    default_tile=0,
    x=(display.width - 120) // 2,
    y=2
)
buttons_menu_group.append(btn_random_sprite)

btn_refuel_sprite = displayio.TileGrid(
    btn_bmp, 
    pixel_shader=displayio.ColorConverter(),
    width=1,
    height=1,
    tile_width=120,
    tile_height=30,
    default_tile=0,
    x=(display.width - 120) // 2,
    y=34
)
buttons_menu_group.append(btn_refuel_sprite)

btn_game_sprite = displayio.TileGrid(
    btn_bmp, 
    pixel_shader=displayio.ColorConverter(),
    width=1,
    height=1,
    tile_width=120,
    tile_height=30,
    default_tile=0,
    x=(display.width - 120) // 2,
    y=66
)
buttons_menu_group.append(btn_game_sprite)

btn_back_sprite = displayio.TileGrid(
    btn_bmp, 
    pixel_shader=displayio.ColorConverter(),
    width=1,
    height=1,
    tile_width=120,
    tile_height=30,
    default_tile=0,
    x=(display.width - 120) // 2,
    y=98
)
buttons_menu_group.append(btn_back_sprite)

menu_group.append(buttons_menu_group)

# -------------------------------------
# Fuel Error Message 
# -------------------------------------
fuel_error_group = displayio.Group()
fuel_error_group.hidden = True

fuel_error = label.Label(
    FONT,
    text="Not enough fuel!",
    color=0xFFFFFF,
    x=(display.width - 32) // 2 - 30,
    y=(display.height - 32) // 2
)

fuel_error_group.append(fuel_error)

# Add all groups to splash at startup
splash.append(menu_group)
splash.append(idle_on_group)
splash.append(idle_always_on_group)
splash.append(random_group)
splash.append(refuel_group)
splash.append(refuel_success_group)
splash.append(game)
splash.append(fuel_error_group)

btn_random_sprite[0] = 1

# -------------------------------------
# Main Loop
# -------------------------------------

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    keys = pygame.key.get_pressed()

    if current_screen == "menu":
        if keys[pygame.K_DOWN]:
            if selected == 0:
                btn_random_sprite[0] = 0
                btn_refuel_sprite[0] = 1
                btn_game_sprite[0] = 0
                btn_back_sprite[0] = 0
                selected = 1
            elif selected == 1:
                btn_random_sprite[0] = 0
                btn_refuel_sprite[0] = 0
                btn_game_sprite[0] = 1
                btn_back_sprite[0] = 0
                selected = 2
            elif selected == 2:
                btn_random_sprite[0] = 0
                btn_refuel_sprite[0] = 0
                btn_game_sprite[0] = 0
                btn_back_sprite[0] = 1
                selected = 3
            elif selected == 3:
                btn_random_sprite[0] = 1
                btn_refuel_sprite[0] = 0
                btn_game_sprite[0] = 0
                btn_back_sprite[0] = 0
                selected = 0
        elif keys[pygame.K_UP]:
            if selected == 0:
                btn_random_sprite[0] = 0
                btn_refuel_sprite[0] = 0
                btn_game_sprite[0] = 0
                btn_back_sprite[0] = 1
                selected = 3
            elif selected == 1:
                btn_random_sprite[0] = 1
                btn_refuel_sprite[0] = 0
                btn_game_sprite[0] = 0
                btn_back_sprite[0] = 0
                selected = 0
            elif selected == 2:
                btn_random_sprite[0] = 0
                btn_refuel_sprite[0] = 1
                btn_game_sprite[0] = 0
                btn_back_sprite[0] = 0
                selected = 1
            elif selected == 3:
                btn_random_sprite[0] = 0
                btn_refuel_sprite[0] = 0
                btn_game_sprite[0] = 1
                btn_back_sprite[0] = 0
                selected = 2
        elif keys[pygame.K_SPACE]:
            if selected == 3:
                menu_group.hidden = True 
                current_screen = "idle"
                if not always_on:
                    idle_on_group.hidden = False 
                    idle_always_on_group.hidden = True
                else:
                    idle_always_on_group.hidden = False 
                    idle_on_group.hidden = True
                fuel_label.text = "Fuel: " + str(fuel) + "%"
            elif selected == 1:
                menu_group.hidden = True 
                current_screen = "random"
                random_group.hidden = False
            elif selected == 0:
                menu_group.hidden = True
                current_screen = "refuel"
                refuel_group.hidden = False 
                refuel_truck_frame = 0
                refuel_truck[0] = refuel_truck_frame
            elif selected == 2:
                if fuel >= 10:
                    menu_group.hidden = True
                    current_screen = "game"
                    game.hidden = False
                    plane.hidden = False
                    bg_sprite.hidden = False
                    death_hi.hidden = True
                    lives_label.hidden = False
                    score_label.x = 5
                    score_label.y = 10
                    lives = 3
                    points = 0
                else:
                    fuel_error_group.hidden = False
                    menu_group.hidden = True
                    is_timer_on = True


    elif current_screen == "idle":
        if keys[pygame.K_SPACE]:
            idle_on_group.hidden = True
            idle_always_on_group.hidden = True
            menu_group.hidden = False  # Show menu
            current_screen = "menu"
            btn_random_sprite[0] = 1
            selected = 0
            btn_back_sprite[0] = 0
        elif keys[pygame.K_LEFT]:
            if always_on:
                always_on = False
                idle_always_on_group.hidden = True
                idle_on_group.hidden = False
                animate = True
                on_plane[0] = 0
                plane_frame = 0
            else:
                animate = False
                always_on_plane[0] = 0
                always_on = True
                idle_always_on_group.hidden = False
                idle_on_group.hidden = True
        elif keys[pygame.K_RIGHT]:
            animate = True


        if animate:
            if always_on:
                always_on_plane[0] = plane_frame
                print(plane_frame)
                if plane_frame == 23:
                    plane_frame = 0
                    always_on_plane[0] = plane_frame

                    animate = False


        if not always_on:
            on_plane[0] = plane_frame
            if plane_frame == 22:
                plane_frame = 0
                on_plane[0] = 0

    elif current_screen == "random":
        if keys[pygame.K_LEFT]:
            random_group.hidden = False
            print("randomising")
            dice[0] = random.randint(0, 5)
            for _ in range(13):
                dice[0] = random.randint(0, 5)
                display.refresh()
                time.sleep(0.1)
                
        elif keys[pygame.K_SPACE]:
            random_group.hidden = True
            menu_group.hidden = False
            current_screen = "menu"
    elif current_screen == "refuel":
        if refuel_truck_frame != 33:
            refuel_truck_frame += 1
            refuel_truck[0] = refuel_truck_frame
        else:
            is_timer_on = False
            time_elapsed += 1
            print(time_elapsed)
            if time_elapsed == 25:
                refuel_group.hidden = True
                refuel_success_group.hidden = False
                fueled = True
                time_elapsed = 0


        if fueled:
            if time_elapsed == 10:
                if fuel + 5 <= 100:
                    fuel = fuel + 5
                refuel_success_group.hidden = True
                refuel_group.hidden = True
                menu_group.hidden = False
                fueled = False
                time_elapsed = 0
                current_screen = "menu"
                fuel_label.text = "Fuel: " + str(fuel) + "%"


    elif current_screen == "game":
        update_text()
        keys = pygame.key.get_pressed()
                

        if game_over == False:
            for ringe in ringes:
                ringe.y += 5 
                if ringe.y > display.height:
                    game.remove(ringe)
                    ringes.remove(ringe)
                elif check_collision(plane, ringe):
                    points += 1
                    ringes.remove(ringe)
                    game.remove(ringe)
                
        
            for nuke in nukes:
                if not game_over:
                    nuke.y += 5 
                    if nuke.y > display.height:
                        game.remove(nuke)
                        nukes.remove(nuke)
                    elif check_collision(plane, nuke):
                        lives -= 1
                        nukes.remove(nuke)
                        game.remove(nuke)
                        if lives == 0:
                            for i in ringes:
                                game.remove(i)

                            for i in nukes:
                                game.remove(i)

                            ringes.clear()
                            nukes.clear()

                            show_death()

                            game_over = True
                            break
                

            if keys[pygame.K_LEFT]:
                if plane.x - speed >= 0:
                    plane.x -= speed
                else:
                    plane.x = 0
            if keys[pygame.K_RIGHT]:
                if plane.x + speed <= 78:
                    plane.x += speed                        

            if random.random() < spawn_rate["ring"]:
                spawn_ring()
                spawn_rate["ring"] = random.randint(1, 70) / 100 
            
            if random.random() < spawn_rate["nuke"]:
                spawn_nuke()
                spawn_rate["nuke"] = random.randint(1, 40) / 100
        else:
            show_death()
            fuel = fuel - 10
            time.sleep(1)
 
            time_elapsed = 0
            game.hidden = True
            menu_group.hidden = False
            death_hi.hidden = True
            game_over = False

            current_screen = "menu"
            
    


        plane_frame = (plane_frame + 1) % ANIMATION_FRAMES 
        plane[0] = plane_frame

    time.sleep(0.1)
    if datetime.now().strftime("%H:%M") != current_time:
        current_time = datetime.now().strftime("%H:%M")
        clock_label.text = current_time

    if animate:
        plane_frame += 1
        
    if is_timer_on:
        time_elapsed += 1
        if time_elapsed == 10:
            time_elapsed = 0
            fuel_error_group.hidden = True
            menu_group.hidden = False
            is_timer_on = False

    display.refresh()