import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
import pygame
import random
import time
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font
import random
import sys
import os

pygame.init()
display = PyGameDisplay(width=128, height=128)
splash = displayio.Group()
display.show(splash)
pygame.font.init()

font = bitmap_font.load_font("Arial-12.bdf")

programIcon = pygame.image.load('Erebus_Nightflitter.bmp')

pygame.display.set_icon(programIcon)

space_station_background = displayio.OnDiskBitmap("spacestationbackground.bmp")

bg_sprite = displayio.TileGrid(
	space_station_background, 
	pixel_shader=space_station_background.pixel_shader
)

tile_width = 32
tile_height = 32

# warning door 1 sprite

door_1 = displayio.OnDiskBitmap("door_1.bmp")

door_1_sprite = displayio.TileGrid(
	door_1, 
	pixel_shader=space_station_background.pixel_shader
)

# warning door 1 sprite

warning_door_1 = displayio.OnDiskBitmap("door_1_open.bmp")

warning_door_1_sprite = displayio.TileGrid(
	warning_door_1, 
	pixel_shader=space_station_background.pixel_shader
)

# door 2 sprite

door_2 = displayio.OnDiskBitmap("door_2.bmp")

door_2_sprite = displayio.TileGrid(
	door_2, 
	pixel_shader=space_station_background.pixel_shader
)

# warning door 2 sprite

warning_door_2 = displayio.OnDiskBitmap("door_2_open.bmp")

warning_door_2_sprite = displayio.TileGrid(
	warning_door_2, 
	pixel_shader=space_station_background.pixel_shader
)

# food dispenser sprite

food_dispenser = displayio.OnDiskBitmap("food_dispenser.bmp")

food_dispenser_sprite = displayio.TileGrid(
	food_dispenser, 
	pixel_shader=space_station_background.pixel_shader
)

# AME sprite

AME_normal = displayio.OnDiskBitmap("AME_normal.bmp")

AME_sprite = displayio.TileGrid(
	AME_normal, 
	pixel_shader=space_station_background.pixel_shader
)

# AME warning sprite

AME_warning = displayio.OnDiskBitmap("AME_warning.bmp")

AME_warning_sprite = displayio.TileGrid(
	AME_warning, 
	pixel_shader=space_station_background.pixel_shader
)

# singulo sprite

singulo_normal = displayio.OnDiskBitmap("singulo_normal.bmp")

singulo_sprite = displayio.TileGrid(
	singulo_normal, 
	pixel_shader=space_station_background.pixel_shader
)

# singulo warning sprite

singulo_warning = displayio.OnDiskBitmap("singulo_warning.bmp")

singulo_warning_sprite = displayio.TileGrid(
	singulo_warning, 
	pixel_shader=space_station_background.pixel_shader
)

# solar sprite

solar_normal = displayio.OnDiskBitmap("solar_normal.bmp")

solar_sprite = displayio.TileGrid(
	solar_normal, 
	pixel_shader=space_station_background.pixel_shader
)

# solar warning sprite

solar_warning = displayio.OnDiskBitmap("solar_warning.bmp")

solar_warning_sprite = displayio.TileGrid(
	solar_warning, 
	pixel_shader=space_station_background.pixel_shader
)


# door control menu sprite

door_control_menu = displayio.OnDiskBitmap("door_control.bmp")

door_control_menu_sprite = displayio.TileGrid(
	door_control_menu, 
	pixel_shader=space_station_background.pixel_shader
)

# AME control menu sprite

AME_control_menu = displayio.OnDiskBitmap("AME_control.bmp")

AME_control_menu_sprite = displayio.TileGrid(
	AME_control_menu, 
	pixel_shader=space_station_background.pixel_shader
)

# singulo control menu sprite

singulo_control_menu = displayio.OnDiskBitmap("singulo_control.bmp")

singulo_control_menu_sprite = displayio.TileGrid(
	singulo_control_menu, 
	pixel_shader=space_station_background.pixel_shader
)

# solar control menu sprite

solar_control_menu = displayio.OnDiskBitmap("solar_control.bmp")

solar_control_menu_sprite = displayio.TileGrid(
	solar_control_menu, 
	pixel_shader=space_station_background.pixel_shader
)

# game over menu sprite

game_over_menu = displayio.OnDiskBitmap("game_over.bmp")

game_over_menu_sprite = displayio.TileGrid(
	game_over_menu, 
	pixel_shader=space_station_background.pixel_shader
)

# starvation menu sprite

starvation_menu = displayio.OnDiskBitmap("starvation.bmp")

starvation_menu_sprite = displayio.TileGrid(
	starvation_menu, 
	pixel_shader=space_station_background.pixel_shader
)

splash.append(bg_sprite)
splash.append(door_1_sprite)
splash.append(door_2_sprite)
splash.append(food_dispenser_sprite)
splash.append(AME_sprite)
splash.append(singulo_sprite)
splash.append(solar_sprite)

erebus_sheet = displayio.OnDiskBitmap("erebus_sheet.bmp")

tile_width = 32
tile_height = 32

erebus_sprite = displayio.TileGrid(
	erebus_sheet,
	pixel_shader=erebus_sheet.pixel_shader,
	width=1,
	height=1,
    tile_width=tile_width,
    tile_height=tile_height,
	default_tile=0,
	x=(display.width - tile_width) // 3,
	y=display.height - tile_height - 0
)

splash.append(erebus_sprite)

#food
#x = 96
#y = 64
#door_1
#x = 96
#Y = 96
#door_2
#x = 0
#Y = 96
#AME
#x = 0
#Y = 64
#Singulo
#x = 0
#Y = 32
#solar
#x = 0
#Y = 0

#here be warnings
game_over = False
power_outage = False
starvation_game_over = False
menu_open = False
write_mode = False
remove_splash = False
game_round = 0
score = 10
score_increment = 20
score_round_increment = 50
score_penalty = 50
score_overflow_reset_completed = False
food_price = 15#*round(game_round/2)
food_reduced_price = 10
hunger = 10
hunger_increment = 30
hunger_round_increment = 10
hunger_cost = 2
hunger_reset = False #ignore this, I am dum
ate = False
warning_select = random.randint(1, 2)
warning = False
warning_door_1 = False
penalty_door_1 = False
warning_door_2 = False
penalty_door_2 = False
warning_AME = False
penalty_AME = False
warning_Singulo = False
penalty_Singulo = False
warning_solar = False
penalty_solar = False
frame = 0
speed = 32

score_label = label.Label(font, text=f"Score: {score}", color=0xFFFFFF, x=34, y=10)
splash.append(score_label)

hunger_label = label.Label(font, text=f"Hunger: {hunger}", color=0xFFFFFF, x=34, y=32)
splash.append(hunger_label)

round_score_label = label.Label(font, text=f"income: {score_round_increment}", color=0xFFFFFF, x=34, y=54)
splash.append(round_score_label)

round_label = label.Label(font, text=f"round: {game_round}", color=0xFFFFFF, x=35, y=74)
splash.append(round_label)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
            elif event.key == pygame.K_LEFT and game_over == False and menu_open == False:
                erebus_sprite.x -= speed
                hunger += hunger_cost
                print ("x:", erebus_sprite.x)
                print ("y:", erebus_sprite.y)
                print ("Hunger: ", hunger)
            elif event.key == pygame.K_RIGHT and game_over == False and menu_open == False:
                erebus_sprite.x += speed
                hunger += hunger_cost
                print ("x:", erebus_sprite.x)
                print ("y:", erebus_sprite.y)
                print ("Hunger: ", hunger)
            elif event.key == pygame.K_UP and game_over == False and menu_open == False:
                erebus_sprite.y -= speed
                hunger += hunger_cost
                print ("x:", erebus_sprite.x)
                print ("y:", erebus_sprite.y)
                print ("Hunger: ", hunger)
            elif event.key == pygame.K_UP and game_over == True:
                if power_outage == True:
                    splash.remove(game_over_menu_sprite)
                    power_outage = False
                if starvation_game_over == True:
                    splash.remove(starvation_menu_sprite)
                    starvation_game_over = False
                game_over = False
                menu_open = False
                write_mode = False
                remove_splash = False
                game_round = 0
                score = 10
                score_increment = 20
                score_round_increment = 50
                score_penalty = 50
                score_overflow_reset_completed = False
                food_price = 15#*round(game_round/2)
                food_reduced_price = 10
                hunger = 10
                hunger_increment = 30
                hunger_round_increment = 10
                hunger_cost = 2
                hunger_reset = False #ignore this, I am dum
                ate = False
                warning_select = random.randint(1, 2)
                warning = False
                warning_door_1 = False
                penalty_door_1 = False
                warning_door_2 = False
                penalty_door_2 = False
                warning_AME = False
                penalty_AME = False
                warning_Singulo = False
                penalty_Singulo = False
                warning_solar = False
                penalty_solar = False
                frame = 0
                speed = 32
                x=(display.width - tile_width) // 3,
                y=display.height - tile_height - 0

    # side walls
    if erebus_sprite.x < 0:
        erebus_sprite.x = 0
    elif erebus_sprite.x > display.width - tile_width:
        erebus_sprite.x = display.width - tile_width

    erebus_sprite.x = erebus_sprite.x
    
    # wrap around the top and round progression
    if erebus_sprite.y < 0:
        erebus_sprite.y = display.height - tile_height
        score += score_round_increment
        game_round += 1
        hunger += hunger_round_increment
        ate = False
        print ("Round: ", game_round)
        print ("Score: ", score)
        print ("Hunger: ", hunger)
        if write_mode == True:
            file_object = open(r'score.txt', 'w')
            file_object.write(f'{str(score)}\n')
            file_object.close()
            file_object = open(r'round.txt', 'w')
            file_object.write(f'{str(game_round)}\n')
            file_object.close()
        # this needs to be randomised! done!
        if warning_door_1 == False and warning_select == random.randint(1, 2):
            warning_door_1 = True
            #score_round_increment -= score_penalty
        if warning_door_2 == False and warning_select == random.randint(1, 2):
            warning_door_2 = True
            #score_round_increment -= score_penalty
        if warning_AME == False and warning_select == random.randint(1, 2):
            warning_AME = True
            #score_round_increment -= score_penalty
        if warning_Singulo == False and warning_select == random.randint(1, 2):
            warning_Singulo = True
            #score_round_increment -= score_penalty
        if warning_solar == False and warning_select == random.randint(1, 2):
            warning_solar = True
            #score_round_increment -= score_penalty

    # food
    # btw, that's not rice, 
    # it's cloth, 
    # because that's what moths eat,
    # in this game,
    # and Erebus is a moth

    if erebus_sprite.x == 96 and erebus_sprite.y == 64 and hunger >= 1 and ate == False and hunger >= 30 and score >= food_price:
        hunger -= hunger_increment
        score -= food_price
        print ("Hunger: ", hunger)
        print ("Score: ", score)
        ate = True
    if erebus_sprite.x == 96 and erebus_sprite.y == 64 and hunger >= 1 and ate == False and hunger <= 30 and score >> food_reduced_price:
        hunger = 0
        score -= food_reduced_price
        print ("Hunger: ", hunger)
        print ("Score: ", score)
        ate = True

    # door_1

    if warning_door_1 == True:
        splash.append(warning_door_1_sprite)
        if door_1_sprite in splash:
            splash.remove(door_1_sprite)
        if penalty_door_1 == False:
            score_round_increment -= score_penalty
            penalty_door_1 = True
    else:
        if warning_door_1_sprite in splash:
            splash.remove(warning_door_1_sprite)
        if door_1_sprite not in splash:
            splash.append(door_1_sprite)
        if erebus_sprite in splash:
            splash.remove(erebus_sprite)
        if erebus_sprite not in splash:
            splash.append(erebus_sprite)

    if erebus_sprite.x == 96 and erebus_sprite.y == 96 and warning_door_1 == True:
        if menu_open == False:
            splash.append(door_control_menu_sprite)
        menu_open = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if door_control_menu_sprite in splash:
                    splash.remove(door_control_menu_sprite)
                if warning_door_1_sprite in splash:
                    splash.remove(warning_door_1_sprite)
                splash.append(door_1_sprite)
                warning_door_1 = False
                menu_open = False
                penalty_door_1 = False
                score += score_increment
                score_round_increment += score_penalty

    # door_2

    if warning_door_2 == True:
        splash.append(warning_door_2_sprite)
        if door_2_sprite in splash:
            splash.remove(door_2_sprite)
        if penalty_door_2 == False:
            score_round_increment -= score_penalty
            penalty_door_2 = True
    else:
        if warning_door_2_sprite in splash:
            splash.remove(warning_door_2_sprite)
        if door_2_sprite not in splash:
            splash.append(door_2_sprite)
        if erebus_sprite in splash:
            splash.remove(erebus_sprite)
        if erebus_sprite not in splash:
            splash.append(erebus_sprite)

    if erebus_sprite.x == 0 and erebus_sprite.y == 96 and warning_door_2 == True:
        if menu_open == False:
            splash.append(door_control_menu_sprite)
        menu_open = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if door_control_menu_sprite in splash:
                    splash.remove(door_control_menu_sprite)
                if warning_door_2_sprite in splash:
                    splash.remove(warning_door_2_sprite)
                splash.append(door_2_sprite)
                warning_door_2 = False
                menu_open = False
                penalty_door_2 = False
                score += score_increment
                score_round_increment += score_penalty

    # AME

    if warning_AME == True:
        splash.append(AME_warning_sprite)
        if AME_sprite in splash:
            splash.remove(AME_sprite)
        if penalty_AME == False:
            score_round_increment -= score_penalty
            penalty_AME = True
    else:
        if AME_warning_sprite in splash:
            splash.remove(AME_warning_sprite)
        if AME_sprite not in splash:
            splash.append(AME_sprite)
        if erebus_sprite in splash:
            splash.remove(erebus_sprite)
        if erebus_sprite not in splash:
            splash.append(erebus_sprite)

    if erebus_sprite.x == 0 and erebus_sprite.y == 64 and warning_AME == True:
        if menu_open == False:
            splash.append(AME_control_menu_sprite)
        menu_open = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if AME_control_menu_sprite in splash:
                    splash.remove(AME_control_menu_sprite)
                if AME_warning_sprite in splash:
                    splash.remove(AME_warning_sprite)
                splash.append(AME_sprite)
                warning_AME = False
                menu_open = False
                penalty_AME = False
                score += score_increment
                score_round_increment += score_penalty

    # Singulo

    if warning_Singulo == True:
        splash.append(singulo_warning_sprite)
        if singulo_sprite in splash:
            splash.remove(singulo_sprite)
        if penalty_Singulo == False:
            score_round_increment -= score_penalty
            penalty_Singulo = True
    else:
        if singulo_warning_sprite in splash:
            splash.remove(singulo_warning_sprite)
        if singulo_sprite not in splash:
            splash.append(singulo_sprite)
        if erebus_sprite in splash:
            splash.remove(erebus_sprite)
        if erebus_sprite not in splash:
            splash.append(erebus_sprite)

    if erebus_sprite.x == 0 and erebus_sprite.y == 32 and warning_Singulo == True:
        if menu_open == False:
            splash.append(singulo_control_menu_sprite)
        menu_open = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if singulo_control_menu_sprite in splash:
                    splash.remove(singulo_control_menu_sprite)
                if singulo_warning_sprite in splash:
                    splash.remove(singulo_warning_sprite)
                splash.append(singulo_sprite)
                warning_Singulo = False
                menu_open = False
                penalty_Singulo = False
                score += score_increment
                score_round_increment += score_penalty

    # solar

    if warning_solar == True:
        splash.append(solar_warning_sprite)
        if solar_sprite in splash:
            splash.remove(solar_sprite)
        if penalty_solar == False:
            score_round_increment -= score_penalty
            penalty_solar = True
    else:
        if solar_warning_sprite in splash:
            splash.remove(solar_warning_sprite)
        if solar_sprite not in splash:
            splash.append(solar_sprite)
        if erebus_sprite in splash:
            splash.remove(erebus_sprite)
        if erebus_sprite not in splash:
            splash.append(erebus_sprite)

    if erebus_sprite.x == 0 and erebus_sprite.y == 0 and warning_solar == True:
        if menu_open == False:
            splash.append(solar_control_menu_sprite)
        menu_open = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if solar_control_menu_sprite in splash:
                    splash.remove(solar_control_menu_sprite)
                if solar_warning_sprite in splash:
                    splash.remove(solar_warning_sprite)
                splash.append(solar_sprite)
                warning_solar = False
                menu_open = False
                penalty_solar = False
                score += score_increment
                score_round_increment += score_penalty

    # why is it crashing ffs
    # fixed it, I am literally a god

    if door_control_menu_sprite in splash and menu_open == True:
        splash.append(door_control_menu_sprite)
    elif door_control_menu_sprite in splash:
        splash.remove(door_control_menu_sprite)

    if AME_control_menu_sprite in splash and menu_open == True:
        splash.append(AME_control_menu_sprite)
    elif AME_control_menu_sprite in splash:
        splash.remove(AME_control_menu_sprite)

    if singulo_control_menu_sprite in splash and menu_open == True:
        splash.append(singulo_control_menu_sprite)
    elif singulo_control_menu_sprite in splash:
        splash.remove(singulo_control_menu_sprite)

    if solar_control_menu_sprite in splash and menu_open == True:
        splash.append(solar_control_menu_sprite)
    elif solar_control_menu_sprite in splash:
        splash.remove(solar_control_menu_sprite)

    if score <= 0 and game_over == False:
        game_over = True
        power_outage = True
        print("Game Over")
        splash.append(game_over_menu_sprite)

    #if score <= 0 and score_overflow_reset_completed == False:
        #score = 0
        #score_overflow_reset_completed = True

    if hunger >= 150 and game_over == False:
        game_over = True
        starvation_game_over = True
        print("Game Over")
        splash.append(starvation_menu_sprite)

    if game_over_menu_sprite in splash and game_over == True:
        splash.append(game_over_menu_sprite)
    elif game_over_menu_sprite in splash:
        splash.remove(game_over_menu_sprite)

    if starvation_menu_sprite in splash and game_over == True:
        splash.append(starvation_menu_sprite)
    elif starvation_menu_sprite in splash:
        splash.remove(starvation_menu_sprite)

    score_label.text = f"Score: {score}"
    display.refresh()

    hunger_label.text = f"Hunger: {hunger}"
    display.refresh()

    round_score_label.text = f"income: {score_round_increment}"
    display.refresh()

    round_label.text = f"round: {game_round}"
    display.refresh()

    # score overflow reset (why is this even here? can't be bothered to find where it should be)

    # I HAVE NO IDEA WHAT I'M DOING! :D

    #if hunger <= 0 and hunger_reset == False:
        #hunger = 0
        #print ("Hunger: ", hunger)
        #hunger_reset = True

    erebus_sprite[0] = frame
    frame = (frame + 1) % (erebus_sheet.width // tile_width)

    pygame.time.wait(100)

    #let him cook

    # ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠿⠿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
    # ⣿⣿⣿⣿⣿⣿⣿⣿⠟⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠉⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
    # ⣿⣿⣿⣿⣿⣿⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢺⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
    # ⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠆⠜⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
    # ⣿⣿⣿⣿⠿⠿⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠻⣿⣿⣿⣿⣿
    # ⣿⣿⡏⠁⠀⠀⠀⠀⠀⣀⣠⣤⣤⣶⣶⣶⣶⣶⣦⣤⡄⠀⠀⠀⠀⢀⣴⣿⣿⣿⣿⣿
    # ⣿⣿⣷⣄⠀⠀⠀⢠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⡧⠇⢀⣤⣶⣿⣿⣿⣿⣿⣿⣿
    # ⣿⣿⣿⣿⣿⣿⣾⣮⣭⣿⡻⣽⣒⠀⣤⣜⣭⠐⢐⣒⠢⢰⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿
    # ⣿⣿⣿⣿⣿⣿⣿⣏⣿⣿⣿⣿⣿⣿⡟⣾⣿⠂⢈⢿⣷⣞⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿
    # ⣿⣿⣿⣿⣿⣿⣿⣿⣽⣿⣿⣷⣶⣾⡿⠿⣿⠗⠈⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
    # ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠻⠋⠉⠑⠀⠀⢘⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
    # ⣿⣿⣿⣿⣿⣿⣿⡿⠟⢹⣿⣿⡇⢀⣶⣶⠴⠶⠀⠀⢽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
    # ⣿⣿⣿⣿⣿⣿⡿⠀⠀⢸⣿⣿⠀⠀⠣⠀⠀⠀⠀⠀⡟⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
    # ⣿⣿⣿⡿⠟⠋⠀⠀⠀⠀⠹⣿⣧⣀⠀⠀⠀⠀⡀⣴⠁⢘⡙⢿⣿⣿⣿⣿⣿⣿⣿⣿
    # ⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⢿⠗⠂⠄⠀⣴⡟⠀⠀⡃⠀⠉⠉⠟⡿⣿⣿⣿⣿
    #⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢷⠾⠛⠂⢹⠀⠀⠀⢡⠀⠀⠀⠀⠀⠙⠛⠿⢿