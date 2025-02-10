import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
import pygame
import time
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font
# from machine import Timer
# import terminalio
import random









# import bitmaptools

# def bitmar_from_on_disk(on_disk_bitmap):
#     width, height = on_disk_bitmap.width, on_disk_bitmap.height
#     new_bitmap = displayio.Bitmap(width, height, 256)
#     bitmaptools.blit(new_bitmap, on_disk_bitmap, 0, 0)
#     return new_bitmap

# def resize_bitmap(source_bitmap, scale_factor):
#     new_width = max(1, int(source_bitmap.width * scale_factor))
#     new_height = max(1, int(source_bitmap.height * scale_factor))

#     new_bitmap = displayio.Bitmap(new_width, new_height, 256)

#     for y in range(new_height):
#         for x in range(new_width):
#             src_x = int(x / scale_factor)
#             src_y = int(y / scale_factor)
#             new_bitmap[x, y] = source_bitmap[src_x, src_y]
#     return new_bitmap

pygame.init()

display = PyGameDisplay(width=128, height=128)
splash = displayio.Group()

tile_width = 32
tile_height = 32

game_over = False

gamesPlayed = 0

golden = False
droopy = False

hungry = False

timer_durtaion = 120
start_time = time.monotonic()


def notGolden(gamesPlayed):
    if gamesPlayed > 0:
        gamesPlayed -= 1

# timer = Timer(0)

# timer.init(period=120000, mode=Timer.PERIODIC, callback=notGolden)


# scale = 3
# display_width = 128 * scale
# display_height = 128 * scale
# display = PyGameDisplay(width=384, height=384)
# splash = displayio.Group(scale=scale)

display.show(splash)

castle_background = displayio.OnDiskBitmap("castle.bmp")

bg_castle_sprite = displayio.TileGrid(
    castle_background,
    pixel_shader=castle_background.pixel_shader
)

splash.append(bg_castle_sprite)

grassy_background = displayio.OnDiskBitmap("grassy-field.bmp")

bg_grassy_sprite = displayio.TileGrid(
    grassy_background,
    pixel_shader=grassy_background.pixel_shader
)

eat_icon = displayio.OnDiskBitmap("eat.bmp")

eat_icon_highlighted = displayio.OnDiskBitmap("eat-highlighted.bmp")

game_icon = displayio.OnDiskBitmap("game.bmp")

game_icon_highlighted = displayio.OnDiskBitmap("game-highlighted.bmp")

# eat_icon_original = bitmar_from_on_disk(eat_icon)

# scaled_eat_icon = resize_bitmap(eat_icon, 0.5)

eat_sprite = displayio.TileGrid(
    eat_icon,
    pixel_shader=eat_icon.pixel_shader,
    width=1,
    height=1,
    tile_width=16,
    tile_height=16,
    default_tile=0,
    x=10,
    y=10
)

eat_sprite_highlighted = displayio.TileGrid(
    eat_icon_highlighted,
    pixel_shader=eat_icon_highlighted.pixel_shader,
    width=1,
    height=1,
    tile_width=16,
    tile_height=16,
    default_tile=0,
    x=10,
    y=10
)

game_sprite = displayio.TileGrid(
    game_icon,
    pixel_shader=game_icon.pixel_shader,
    width=1,
    height=1,
    tile_width=16,
    tile_height=16,
    default_tile=0,
    x=31,
    y=10
)

game_sprite_highlighted = displayio.TileGrid(
    game_icon_highlighted,
    pixel_shader=game_icon_highlighted.pixel_shader,
    width=1,
    height=1,
    tile_width=16,
    tile_height=16,
    default_tile=0,
    x=31,
    y=10
)

play_meter0_bitmap = displayio.OnDiskBitmap("playMeter0.bmp")
play_meter25_bitmap = displayio.OnDiskBitmap("playMeter25.bmp")
play_meter50_bitmap = displayio.OnDiskBitmap("playMeter50.bmp")
play_meter75_bitmap = displayio.OnDiskBitmap("playMeter75.bmp")
play_meter100_bitmap = displayio.OnDiskBitmap("playMeter100.bmp")

play_meter0 = displayio.TileGrid(
    play_meter0_bitmap,
    pixel_shader=play_meter0_bitmap.pixel_shader,
    width=1,
    height=1,
    tile_width=64,
    tile_height=16,
    default_tile=0,
    x=128-66,
    y=2
)

play_meter25 = displayio.TileGrid(
    play_meter25_bitmap,
    pixel_shader=play_meter25_bitmap.pixel_shader,
    width=1,
    height=1,
    tile_width=64,
    tile_height=16,
    default_tile=0,
    x=128-66,
    y=2
)

play_meter50 = displayio.TileGrid(
    play_meter50_bitmap,
    pixel_shader=play_meter50_bitmap.pixel_shader,
    width=1,
    height=1,
    tile_width=64,
    tile_height=16,
    default_tile=0,
    x=128-66,
    y=2
)

play_meter75 = displayio.TileGrid(
    play_meter75_bitmap,
    pixel_shader=play_meter75_bitmap.pixel_shader,
    width=1,
    height=1,
    tile_width=64,
    tile_height=16,
    default_tile=0,
    x=128-66,
    y=2
)

play_meter100 = displayio.TileGrid(
    play_meter100_bitmap,
    pixel_shader=play_meter100_bitmap.pixel_shader,
    width=1,
    height=1,
    tile_width=64,
    tile_height=16,
    default_tile=0,
    x=128-66,
    y=2
)

splash.append(play_meter0)

# splash.append(eat_sprite)

# scale_factor = 0.5

# eat_group = displayio.Group(scale=)
fontFile = "fonts/PressStart2P-Regular-5pt.bdf"
fontToUse = bitmap_font.load_font(fontFile)

arrow_left = displayio.OnDiskBitmap("arrow-left.bmp")

arrow_right = displayio.OnDiskBitmap("arrow-right.bmp")

arrow_left_sprite = displayio.TileGrid(
    arrow_left,
    pixel_shader=arrow_left.pixel_shader,
    width=1,
    height=1,
    tile_width=16,
    tile_height=16,
    default_tile=0,
    x=10,
    y=100
)

arrow_right_sprite = displayio.TileGrid(
    arrow_right,
    pixel_shader=arrow_right.pixel_shader,
    width=1,
    height=1,
    tile_width=16,
    tile_height=16,
    default_tile=0,
    x=100,
    y=100
)

fish_bitmap = displayio.OnDiskBitmap("fish.bmp")





def play_fish_game(splash):
    print("Playing game")
    fishies = []

    def spawn_fish():
        x_position = random.randint(0, display_width - fish_bitmap.width)
        fish = displayio.TileGrid(
            fish_bitmap,
            pixel_shader=fish_bitmap.pixel_shader,
            width=1,
            height=1,
            tile_width=fish_bitmap.width,
            tile_height=fish_bitmap.height,
            x=x_position,
            y=-32
        )
        fishies.append(fish)
        splash.append(fish)

    def check_collision(sprite1, sprite2):
        return (
            sprite1.x < sprite2.x + 32 and
            sprite1.x + 32 > sprite2.x and
            sprite1.y < sprite2.y + 32 and
            sprite1.y + 32 > sprite2.y
        )

    score = 0

    score_display = label.Label(font=fontToUse, color=0x581845, text="Score:"+str(score))

    score_display.x = 10
    score_display.y = 40

    splash.append(score_display)

    if droopy == True and golden == False:
        princess_sheet_droopy.x = 64 - 16
    elif golden == False:
        princess_sprite.x = 64 - 16
    elif golden == True:
        princess_sprite_golden.x = 64 - 16
    while score < 10:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        keys = pygame.key.get_pressed()
        if droopy == True and golden == False:
            if keys[pygame.K_LEFT]:
                princess_sprite_droopy.x -= speed
            if keys[pygame.K_RIGHT]:
                princess_sprite_droopy.x += speed
        elif golden == False:
            if keys[pygame.K_LEFT]:
                princess_sprite.x -= speed
            if keys[pygame.K_RIGHT]:
                princess_sprite.x += speed
        elif golden == True:
            if keys[pygame.K_LEFT]:
                princess_sprite_golden.x -= speed
            if keys[pygame.K_RIGHT]:
                princess_sprite_golden.x += speed
        if random.random() < 0.05:
            spawn_fish()
        
        for fish in fishies:
            if droopy == True and golden == False:
                fish.y += 5
                if fish.y > display.height:
                    splash.remove(fish)
                    fishies.remove(fish)
                    score -= 1
                    score_display.text = "Score:"+str(score)
                elif check_collision(princess_sprite_droopy, fish):
                    splash.remove(fish)
                    fishies.remove(fish)
                    score += 1
                    score_display.text = "Score:"+str(score)
            elif golden == False:
                fish.y += 5
                if fish.y > display.height:
                    splash.remove(fish)
                    fishies.remove(fish)
                    score -= 1
                    score_display.text = "Score:"+str(score)
                elif check_collision(princess_sprite, fish):
                    splash.remove(fish)
                    fishies.remove(fish)
                    score += 1
                    score_display.text = "Score:"+str(score)
            elif golden == True:
                fish.y += 5
                if fish.y > display.height:
                    splash.remove(fish)
                    fishies.remove(fish)
                    score -= 1
                    score_display.text = "Score:"+str(score)
                elif check_collision(princess_sprite_golden, fish):
                    splash.remove(fish)
                    fishies.remove(fish)
                    score += 1
                    score_display.text = "Score:"+str(score)
        time.sleep(0.1)

        

    try:
        splash.remove(score_display)
    except:
        pass
    print("Game over")

    
def play_arrow_game(splash):
    print("Playing game")
    score = 0
    round = 0

    score_display = label.Label(font=fontToUse, color=0x581845, text="Score:"+str(score))
    round_display = label.Label(font=fontToUse, color=0x581845, text="Round:"+str(round))

    score_display.x = 10
    score_display.y = 40

    round_display.x = 10
    round_display.y = 50

    splash.append(score_display)
    splash.append(round_display)

    if droopy == True and golden == False:
        princess_sheet_droopy.x = 64 - 16
    elif golden == False:
        princess_sprite.x = 64 - 16
    elif golden == True:
        princess_sprite_golden.x = 64 - 16

    while round < 5:

        pygame.event.clear()

        event = pygame.event.wait()

        # if event.type == pygame.KEYDOWN:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
        # while True:
        #     for event in pygame.event.get():
        #         if event.type == KEYDOWN:
        #             return

            left = False
            right = False

            left_selected = False
            right_selected = False

            number = random.randint(0, 1)

            print(number)

            if number == 0:
                left_selected = True
                right_selected = False
            elif number == 1:
                left_selected = False
                right_selected = True

            

            

            
            
            if keys[pygame.K_LEFT]:
                left = True
                right = False
            elif keys[pygame.K_RIGHT]:
                left = False
                right = True

            time.sleep(0.1)

            if left_selected == True:
                splash.append(arrow_left_sprite)
                try:
                    splash.remove(arrow_right_sprite)
                except:
                    pass

            if right_selected == True:
                splash.append(arrow_right_sprite)
                try:
                    splash.remove(arrow_left_sprite)
                except:
                    pass

            print("Left:", left, "Right:", right)

            if left == left_selected or right == right_selected:
                score += 1
                score_display.text = "Score:"+str(score)

            round = round + 1
            round_display.text = "Round:"+str(round)
            print("Round:", round)

        time.sleep(0.5)
        try:
            splash.remove(arrow_left_sprite)
        except:
            pass
        
        try:
            splash.remove(arrow_right_sprite)
        except:
            pass
    
    try:
        splash.remove(arrow_left_sprite)
    except:
        pass

    try:
        splash.remove(arrow_right_sprite)
    except:
        pass

    try:
        splash.remove(score_display)
    except:
        pass

    try:
        splash.remove(round_display)
    except:
        pass


princess_sheet = displayio.OnDiskBitmap("princess_kitty_sheet.bmp")

princess_sheet_golden = displayio.OnDiskBitmap("princess_kitty_golden_sheet.bmp")

princess_sheet_droopy = displayio.OnDiskBitmap("princess_kitty_droopy_sheet.bmp")

princess_sprite = displayio.TileGrid(
    princess_sheet,
    pixel_shader=princess_sheet.pixel_shader,
    width=1,
    height=1,
    tile_width=32,
    tile_height=32,
    default_tile=0,
    x=(display.width - tile_width) // 2,
    y=display.height - tile_height - 10
)

princess_sprite_golden = displayio.TileGrid(
    princess_sheet_golden,
    pixel_shader=princess_sheet_golden.pixel_shader,
    width=1,
    height=1,
    tile_width=32,
    tile_height=32,
    default_tile=0,
    x=(display.width - tile_width) // 2,
    y=display.height - tile_height - 10
)

princess_sprite_droopy = displayio.TileGrid(
    princess_sheet_droopy,
    pixel_shader=princess_sheet_droopy.pixel_shader,
    width=1,
    height=1,
    tile_width=32,
    tile_height=32,
    default_tile=0,
    x=(display.width - tile_width) // 2,
    y=display.height - tile_height - 10
)

def update_display():
    display.show(splash)
    pygame.display.update()

splash.append(princess_sprite)

grass = False
castle = True
playing_arrow_game = False
playing_fish_game = False

frame = 0
speed = 4
display_width = 128
play_meter100there = False
play_meter75there = False
play_meter50there = False
play_meter25there = False
play_meter0there = False
# display_needs_update = False

count = 0
# princess_sprite.x = 64

while True:

    current_time = time.monotonic()

    elapsed_time = current_time - start_time
    print(f"Elapsed time: {elapsed_time:.2f} seconds")

    if elapsed_time >= timer_durtaion:
        print("2 minutes have passed")
        count += 1

        if count == 2:
            hungry = True
            droopy = True
            count = 0
            print("Princess is hungry")

        if gamesPlayed > 0:
            gamesPlayed -= 1
        print(gamesPlayed)
        start_time = time.monotonic()

    if gamesPlayed == 0:
        golden = False
        if play_meter25there == True:
            try:
                splash.remove(play_meter25)
                print("removed play_meter25")
            except:
                print("could not remove play_meter25")
            play_meter25there = False
        
    
        try:
            splash.append(play_meter0)
            play_meter0there = True
        except:
            print("could not append play_meter0")
        # golden = False
        # try:
        #     splash.remove(play_meter25)
        # except:
        #     print("could not remove play_meter0")
        # try:
        #     splash.append(play_meter0)
        # except:
        #     print("could not append play_meter0")
        # display_needs_update = True
       
    if gamesPlayed == 1:
        golden = False
        if play_meter50there == True:
            try:
                splash.remove(play_meter50)
                print("removed play_meter50")
            except:
                print("could not remove play_meter50")
            play_meter50there = False
        
        if not play_meter25there:
            try:
                splash.append(play_meter25)
                play_meter25there = True
            except:
                print("could not append play_meter25")
        # try:
        #     splash.remove(play_meter50)
        # except:
        #     print("could not remove play_meter50")
        # try:
        #     splash.append(play_meter25)
        # except:
        #     print("could not append play_meter25")
        # display_needs_update = True
        
    if gamesPlayed == 2:
        golden = False
        if play_meter75there == True:
            try:
                splash.remove(play_meter75)
                print("removed play_meter75")
            except:
                print("could not remove play_meter75")
            play_meter75there = False
        
        if not play_meter50there:
            try:
                splash.append(play_meter50)
                play_meter50there = True
            except:
                print("could not append play_meter50")
        # try:
        #     splash.remove(play_meter75)
        # except:
        #     print("could not remove play_meter75")
        # try:
        #     splash.append(play_meter50)
        # except:
        #     print("could not append play_meter50")
        # display_needs_update = True
        
    if gamesPlayed == 3:
        golden = False
        if play_meter100there == True:
            try:
                splash.remove(play_meter100)
                print("removed play_meter100")
            except:
                print("could not remove play_meter100")
            play_meter100there = False
        
        if not play_meter75there:
            try:
                splash.append(play_meter75)
                play_meter75there = True
            except:
                print("could not append play_meter75")
        
    if gamesPlayed == 4:
        golden = True
        if not play_meter100there:
            try:
                splash.append(play_meter100)
                play_meter100there = True
            except:
                print("could not append play_meter100")
        # display_needs_update = True
    if droopy == True and golden == False:
        try:
            splash.remove(princess_sprite)
            splash.append(princess_sprite_droopy)
        except:
            print("could not remove princess_sprite")
    elif golden == True:
        try:
            splash.remove(princess_sprite)
            splash.append(princess_sprite_golden)
        except:
            print("could not remove princess_sprite")
        
        # display_needs_update = True
    # else:
    #     try:
    #         splash.remove(princess_sprite_golden)
    #     except:
    #         print("could not remove princess_sprite_golden")
    #     splash.append(princess_sprite)
        # display_needs_update = True
    elif golden == False:
        try:
            splash.remove(princess_sprite_golden)
            splash.append(princess_sprite)
        except:
            print("could not remove princess_sprite_golden")
        

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    if droopy == True and golden == False:
        princess_sprite_droopy[0] = frame
        frame = (frame + 1) % (princess_sheet_droopy.width // tile_width)
    elif golden == False:
        princess_sprite[0] = frame
        frame = (frame + 1) % (princess_sheet.width // tile_width)
    elif golden == True:
        princess_sprite_golden[0] = frame
        frame = (frame + 1) % (princess_sheet_golden.width // tile_width)

    time.sleep(0.1)

    keys = pygame.key.get_pressed()

    if game_over == False and playing_arrow_game == False and playing_fish_game == False:
        if droopy == True and golden == False:
            if keys[pygame.K_LEFT]:
                princess_sprite_droopy.x -= speed
            if keys[pygame.K_RIGHT]:
                princess_sprite_droopy.x += speed
        elif golden == False:
            if keys[pygame.K_LEFT]:
                princess_sprite.x -= speed
            if keys[pygame.K_RIGHT]:
                princess_sprite.x += speed
        elif golden == True:
            if keys[pygame.K_LEFT]:
                princess_sprite_golden.x -= speed
            if keys[pygame.K_RIGHT]:
                princess_sprite_golden.x += speed

    
        if droopy == True and golden == False:
            if (castle_background.width - 32 < princess_sprite_droopy.x):
                if grass == False:
                    splash.remove(bg_castle_sprite)
                    splash.append(bg_grassy_sprite)
                    if droopy == True:
                        splash.append(princess_sprite_droopy)
                    if golden == False:
                        splash.append(princess_sprite)
                    elif golden == True:
                        splash.append(princess_sprite_golden)
                    splash.append(eat_sprite)
                    splash.append(game_sprite)
                    princess_sprite.x = -4
                    grass = True
                    castle = False
                else:
                    princess_sprite_droopy.x = castle_background.width - 32
        elif golden == False:
            if (castle_background.width - 32 < princess_sprite.x):
                if grass == False:
                    splash.remove(bg_castle_sprite)
                    splash.append(bg_grassy_sprite)
                    if golden == False:
                        splash.append(princess_sprite)
                    elif golden == True:
                        splash.append(princess_sprite_golden)
                    splash.append(eat_sprite)
                    splash.append(game_sprite)
                    princess_sprite.x = -4
                    grass = True
                    castle = False
                else:
                    princess_sprite.x = castle_background.width - 32
        elif golden == True:
            if (castle_background.width - 32 < princess_sprite_golden.x):
                if grass == False:
                    splash.remove(bg_castle_sprite)
                    splash.append(bg_grassy_sprite)
                    if golden == False:
                        splash.append(princess_sprite)
                    elif golden == True:
                        splash.append(princess_sprite_golden)
                    splash.append(eat_sprite)
                    splash.append(game_sprite)
                    princess_sprite_golden.x = -4
                    grass = True
                    castle = False
                else:
                    princess_sprite_golden.x = castle_background.width - 32

        if droopy == True and golden == False:
            if princess_sprite_droopy.x == -8:
                if grass == True:
                    # print("out of bounds - right")
                    splash.remove(bg_grassy_sprite)
                    splash.append(bg_castle_sprite)
                    if droopy == True:
                        splash.append(princess_sprite_droopy)
                    if golden == False:
                        splash.append(princess_sprite)
                    if golden == True:
                        splash.append(princess_sprite_golden)
                    splash.remove(eat_sprite)
                    splash.remove(game_sprite)
                    princess_sprite_droopy.x = display_width - 32
                    grass = False
                    castle = True
                else:
                    princess_sprite.x = -4
        elif golden == False:
            if princess_sprite.x == -8:
                if grass == True:
                    # print("out of bounds - right")
                    splash.remove(bg_grassy_sprite)
                    splash.append(bg_castle_sprite)
                    if golden == False:
                        splash.append(princess_sprite)
                    if golden == True:
                        splash.append(princess_sprite_golden)
                    splash.remove(eat_sprite)
                    splash.remove(game_sprite)
                    princess_sprite.x = display_width - 32
                    grass = False
                    castle = True
                else:
                    princess_sprite.x = -4
        elif golden == True:
            if princess_sprite_golden.x == -8:
                if grass == True:
                    # print("out of bounds - right")
                    splash.remove(bg_grassy_sprite)
                    splash.append(bg_castle_sprite)
                    if golden == False:
                        splash.append(princess_sprite)
                    if golden == True:
                        splash.append(princess_sprite_golden)
                    splash.remove(eat_sprite)
                    splash.remove(game_sprite)
                    princess_sprite_golden.x = display_width - 32
                    grass = False
                    castle = True
                else:
                    princess_sprite_golden.x = -4

        # if (princess_sprite.x == -4):
        #     if grass == True:
        #         # print("out of bounds - right")
        #         splash.remove(bg_grassy_sprite)
        #         splash.append(bg_castle_sprite)
        #         splash.append(princess_sprite)

        if droopy == True and golden == False:
            if princess_sprite_droopy.x > 0 and princess_sprite_droopy.x < 16 and grass == True:
                try:
                    splash.remove(eat_sprite)
                except:
                    pass
                splash.append(eat_sprite_highlighted)

                if keys[pygame.K_UP]:
                    print("Game started")
                    playing_fish_game = True
                    play_fish_game(splash=splash)
                    playing_fish_game = False
                    hungry = False
                    droopy = False
                    print("Game ended")
                    gamesPlayed += 1
                    # display_needs_update = True


            elif grass == True:
                try:
                    splash.remove(eat_sprite_highlighted)
                except:
                    pass
                splash.append(eat_sprite)
                # display_needs_update = True
        elif golden == False:
            if princess_sprite.x > 0 and princess_sprite.x < 16 and grass == True:
                try:
                    splash.remove(eat_sprite)
                except:
                    pass
                splash.append(eat_sprite_highlighted)

                if keys[pygame.K_UP]:
                    print("Game started")
                    playing_fish_game = True
                    play_fish_game(splash=splash)
                    playing_fish_game = False
                    print("Game ended")
                    gamesPlayed += 1
                    # display_needs_update = True


            elif grass == True:
                try:
                    splash.remove(eat_sprite_highlighted)
                except:
                    pass
                splash.append(eat_sprite)
                # display_needs_update = True
        elif golden == True:
            if princess_sprite_golden.x > 0 and princess_sprite_golden.x < 16 and grass == True:
                try:
                    splash.remove(eat_sprite)
                except:
                    pass
                splash.append(eat_sprite_highlighted)

                if keys[pygame.K_UP]:
                    print("Game started")
                    playing_fish_game = True
                    play_fish_game(splash=splash)
                    playing_fish_game = False
                    print("Game ended")
                    gamesPlayed += 1
                    # display_needs_update = True


            elif grass == True:
                try:
                    splash.remove(eat_sprite_highlighted)
                except:
                    pass
                splash.append(eat_sprite)
                # display_needs_update = True
        
        if droopy == True and golden == False:
            if princess_sprite_droopy.x > 16 and princess_sprite_droopy.x < 31 and grass == True:
                try:
                    splash.remove(game_sprite)
                except:
                    pass
                splash.append(game_sprite_highlighted)

                if keys[pygame.K_UP]:
                    playing_arrow_game = True
                    print("Game started")
                    play_arrow_game(splash=splash)
                    print("Game ended")
                    playing_arrow_game = False
                    gamesPlayed += 1
                    # display_needs_update = True

            elif grass == True:
                try:
                    splash.remove(game_sprite_highlighted)
                except:
                    pass
                splash.append(game_sprite)
                # display_needs_update = True
        elif golden == False:
            if princess_sprite.x > 16 and princess_sprite.x < 31 and grass == True:
                try:
                    splash.remove(game_sprite)
                except:
                    pass
                splash.append(game_sprite_highlighted)

                if keys[pygame.K_UP]:
                    playing_arrow_game = True
                    print("Game started")
                    play_arrow_game(splash=splash)
                    print("Game ended")
                    playing_arrow_game = False
                    gamesPlayed += 1
                    # display_needs_update = True

            elif grass == True:
                try:
                    splash.remove(game_sprite_highlighted)
                except:
                    pass
                splash.append(game_sprite)
                # display_needs_update = True
        elif golden == True:
            if princess_sprite_golden.x > 16 and princess_sprite_golden.x < 31 and grass == True:
                try:
                    splash.remove(game_sprite)
                except:
                    pass
                splash.append(game_sprite_highlighted)

                if keys[pygame.K_UP]:
                    playing_arrow_game = True
                    print("Game started")
                    play_arrow_game(splash=splash)
                    print("Game ended")
                    playing_arrow_game = False
                    gamesPlayed += 1
                    # display_needs_update = True

            elif grass == True:
                try:
                    splash.remove(game_sprite_highlighted)
                except:
                    pass
                splash.append(game_sprite)
                # display_needs_update = True

    # if display_needs_update:
    #     update_display()
    #     display_needs_update = False
