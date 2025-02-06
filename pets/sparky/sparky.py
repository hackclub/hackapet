import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
import pygame
import time
import random

pygame.init()
display = PyGameDisplay(width=128, height=128)
splash = displayio.Group()
display.show(splash)

#===MAIN MENU===#
main_menu_background_bmp = displayio.OnDiskBitmap("assets/main_menu_background.bmp")
main_menu_bmp = displayio.OnDiskBitmap("assets/main_menu.bmp")
main_menu_decor_bmp = displayio.OnDiskBitmap("assets/main_menu_decor.bmp")



main_menu_background = displayio.TileGrid(main_menu_background_bmp, pixel_shader=main_menu_background_bmp.pixel_shader)
main_menu = displayio.TileGrid( main_menu_bmp, pixel_shader=main_menu_bmp.pixel_shader, tile_width=128, tile_height=128)

splash.append(main_menu_background)
splash.append(main_menu)

decor = []


def spawn_main_menu_decor():
    x_pos = random.randrange(0, 41) if random.randrange(0,2) == 1 else random.randrange(87,128)
    main_menu_decor = displayio.TileGrid(
        main_menu_decor_bmp,
        pixel_shader=main_menu_background_bmp.pixel_shader,
        width=1,
        height=1,
        tile_width=3,
        tile_height=3,
        default_tile=0,
        x=x_pos,
        y=display.height 
    )
    decor.append(main_menu_decor)
    splash.insert(1,main_menu_decor)



frame = 0
fps = 30
do_main_menu = True
while(do_main_menu):
    if display.check_quit():
        break
    if frame % 3 == 0:
        for main_menu_decor in decor:
            main_menu_decor.x += random.randrange(-1,2)
            main_menu_decor.y -= 1
    if frame % 6 == 0:
        spawn_main_menu_decor()
    if frame % 24 == 0:
        if main_menu[0] == 0:
            main_menu[0] = 1
        else:
            main_menu[0] = 0

    frame += 1
    keys = pygame.key.get_pressed()
    for main_menu_decor in decor:
        if main_menu_decor.y <= -2:
            splash.remove(main_menu_decor)
            decor.remove(main_menu_decor)

    if frame == 60:
        frame = 0
    if keys[pygame.K_UP]:
        do_main_menu = False
    if do_main_menu:
        time.sleep(1 / fps)


#===LOADING SCREEN===#
do_loading_screen = True
loading_screen_bmp = displayio.OnDiskBitmap("assets/loading_screen.bmp")
loading_screen = displayio.TileGrid( loading_screen_bmp, pixel_shader=loading_screen_bmp.pixel_shader, tile_width=128, tile_height=128)

splash.append(loading_screen)
while(do_loading_screen):
    if display.check_quit():
        break
    
    if frame % 6 == 0:
        if loading_screen[0] == 11:
            do_loading_screen = False
        else:
            loading_screen[0] +=1
        
    frame+=1
    if frame == 60:
        frame = 0
    if do_loading_screen:
        time.sleep(1 / fps)
    
play_dino_game = True
high_score = 0
#===DINO GAME===#
while(play_dino_game):
    
    do_main_game = True
    numbers_bmp = displayio.OnDiskBitmap("assets/numbers.bmp")
    score_labels_bmp = displayio.OnDiskBitmap("assets/score_labels.bmp")
    main_game_background_bmp = displayio.OnDiskBitmap("assets/main_game_background.bmp")
    obis_bmp = displayio.OnDiskBitmap("assets/obis.bmp")
    player_bmp = displayio.OnDiskBitmap("assets/player.bmp")


    high_score_number_1 = displayio.TileGrid(numbers_bmp,pixel_shader=numbers_bmp.pixel_shader,width=1,height=1,tile_width=3,tile_height= 7,default_tile=3,x = 48,y = 1)
    high_score_number_2 = displayio.TileGrid(numbers_bmp,pixel_shader=numbers_bmp.pixel_shader,width=1,height=1,tile_width=3,tile_height= 7,default_tile=3,x = 52,y = 1)
    high_score_number_3 = displayio.TileGrid(numbers_bmp,pixel_shader=numbers_bmp.pixel_shader,width=1,height=1,tile_width=3,tile_height= 7,default_tile=3,x = 56,y = 1)
    high_score_number_4 = displayio.TileGrid(numbers_bmp,pixel_shader=numbers_bmp.pixel_shader,width=1,height=1,tile_width=3,tile_height= 7,default_tile=3,x = 60,y = 1)
    high_score_number_5 = displayio.TileGrid(numbers_bmp,pixel_shader=numbers_bmp.pixel_shader,width=1,height=1,tile_width=3,tile_height= 7,default_tile=3,x = 64,y = 1)
    high_score_number_6 = displayio.TileGrid(numbers_bmp,pixel_shader=numbers_bmp.pixel_shader,width=1,height=1,tile_width=3,tile_height= 7,default_tile=3,x = 68,y = 1)

    current_score_number_1 = displayio.TileGrid(numbers_bmp,pixel_shader=numbers_bmp.pixel_shader,width=1,height=1,tile_width=3,tile_height= 7,default_tile=3,x = 48,y = 8)
    current_score_number_2 = displayio.TileGrid(numbers_bmp,pixel_shader=numbers_bmp.pixel_shader,width=1,height=1,tile_width=3,tile_height= 7,default_tile=3,x = 52,y = 8)
    current_score_number_3 = displayio.TileGrid(numbers_bmp,pixel_shader=numbers_bmp.pixel_shader,width=1,height=1,tile_width=3,tile_height= 7,default_tile=3,x = 56,y = 8)
    current_score_number_4 = displayio.TileGrid(numbers_bmp,pixel_shader=numbers_bmp.pixel_shader,width=1,height=1,tile_width=3,tile_height= 7,default_tile=3,x = 60,y = 8)
    current_score_number_5 = displayio.TileGrid(numbers_bmp,pixel_shader=numbers_bmp.pixel_shader,width=1,height=1,tile_width=3,tile_height= 7,default_tile=3,x = 64,y = 8)
    current_score_number_6 = displayio.TileGrid(numbers_bmp,pixel_shader=numbers_bmp.pixel_shader,width=1,height=1,tile_width=3,tile_height= 7,default_tile=3,x = 68,y = 8)
    main_game_background = displayio.TileGrid(main_game_background_bmp, pixel_shader=main_game_background_bmp.pixel_shader)

    player = displayio.TileGrid(
        player_bmp,
        pixel_shader=player_bmp.pixel_shader,
        x=10,
        y=75
    )

    score_labels = displayio.TileGrid(score_labels_bmp, pixel_shader=score_labels_bmp.pixel_shader,x=2,y=2)

    splash.append(main_game_background)
    splash.append(high_score_number_1)
    splash.append(high_score_number_2)
    splash.append(high_score_number_3)
    splash.append(high_score_number_4)
    splash.append(high_score_number_5)
    splash.append(high_score_number_6)
    splash.append(current_score_number_1)
    splash.append(current_score_number_2)
    splash.append(current_score_number_3)
    splash.append(current_score_number_4)
    splash.append(current_score_number_5)
    splash.append(current_score_number_6)
    splash.append(score_labels)
    splash.append(player)

    jump_timer = 0
    jump_muti = 30
    fall_muti = 1
    speed_muti = 1
    score = 0
    obis = []

    
    def get_value_at_index_of_int(int, idx) -> int:
        if idx > len(str(int)) - 1:
            return 0

        str_int = str(int)
        char_int = ord(str_int[idx])
        return char_int - 48

    def spawn_obi():
        obi = displayio.TileGrid(
            obis_bmp,
            pixel_shader=obis_bmp.pixel_shader,
            tile_width=12,
            tile_height=12,
            x=128 + 12,
            y =71
        )

        obis.append(obi)
        splash.append( obi)
    def check_collition(obj1, obj2):
        return(
            obj1.x < obj2.x + obj2.tile_width and
            obj1.x > obj2.x-3 and
            (obj1.y ==75) 
        )

    while(do_main_game):
        if display.check_quit():
            break
        for obi in obis:
            if check_collition(player,obi):
                do_main_game = False

        #===SCORE===#

        if frame % 4:
            score+=1 * int(speed_muti)
        if score >= high_score:
            high_score = score
        current_score_number_1[0] = get_value_at_index_of_int(score,0)
        current_score_number_2[0] = get_value_at_index_of_int(score,1)
        current_score_number_3[0] = get_value_at_index_of_int(score,2)
        current_score_number_4[0] = get_value_at_index_of_int(score,3)
        current_score_number_5[0] = get_value_at_index_of_int(score,4)
        current_score_number_6[0] = get_value_at_index_of_int(score,5)
        
        high_score_number_1[0] = get_value_at_index_of_int(high_score, 0)
        high_score_number_2[0] = get_value_at_index_of_int(high_score, 1)
        high_score_number_3[0] = get_value_at_index_of_int(high_score, 2)
        high_score_number_4[0] = get_value_at_index_of_int(high_score, 3)
        high_score_number_5[0] = get_value_at_index_of_int(high_score, 4)
        high_score_number_6[0] = get_value_at_index_of_int(high_score, 5)

        #===PLAYER===#

        keys = pygame.key.get_pressed()
        if jump_timer > 0:
            player.y-=int(jump_muti)
            jump_muti /= 1.6

            jump_timer-=1
        if player.y < 75:
            if player.y + fall_muti > 75:
                player.y = 75
            else:
                player.y+=int(fall_muti)
                fall_muti *= 1.1
        else:
            fall_muti = 1
        if keys[pygame.K_UP] and jump_timer == 0 and player.y == 75:
            jump_muti = 16
            jump_timer = 10


        #===OBJECTS===#

        if frame % int(60 / int(speed_muti)) == 0:
            spawn_obi()
        if frame % 120 == 0:
            speed_muti*=1.2
        for obi in obis:
            obi.x-=int(speed_muti)


        frame+=1
        if frame == 60:
            frame = 0
        if do_main_game:
            time.sleep(1 / fps)

    #===PLAY AGAIN===#
    do_play_again = True
    
    you_died_bmp = displayio.OnDiskBitmap("assets/dead.bmp")
    main_menu_background = displayio.TileGrid(main_menu_background_bmp, pixel_shader=main_menu_background_bmp.pixel_shader)
    you_died = displayio.TileGrid(you_died_bmp, pixel_shader=you_died_bmp.pixel_shader)
    splash.append(main_game_background)
    splash.append(you_died)
    while(do_play_again):
        if display.check_quit():
            break
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            for i in splash:
                splash.remove(i)
            do_play_again = False