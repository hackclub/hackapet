import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
import pygame
import time
from adafruit_display_text import label
import random

def text_to_sprite(text):
    if(text== "-"):
        return 29
    elif(text == "."):
        return 27
    elif(text == "?"):
        return 26
    elif(text == " "):
        return 47
    elif(text == "*"):
        return 28
    elif(text == "^"):
        return 44
    elif(text == ":"):
        return 43
    elif(text == "'"):
        return 30
    elif(text == "!"):
        return 55
    elif(ord(text) >= ord('0') and ord(text) <= ord('9')):
        return 33+ord(text)-ord('0')
    else:
        return ord(text)-ord('a')

pygame.init()

display = PyGameDisplay(width=128, height=128)
splash = displayio.Group()
display.show(splash)

room_sheet = displayio.OnDiskBitmap("room.bmp")
room_sprite = displayio.TileGrid(
    room_sheet,
    pixel_shader=room_sheet.pixel_shader,
    width=1,
    height=1,
    tile_width=128,
    tile_height=128,
    default_tile=0,
    x=0,  
    y=0     
)

chara_sheet = displayio.OnDiskBitmap("pet.bmp")
chara_width = 64
chara_height = 64

chara_sprite = displayio.TileGrid(
    chara_sheet,
    pixel_shader=chara_sheet.pixel_shader,
    width=1,
    height=1,
    tile_width=chara_width,
    tile_height=chara_height,
    default_tile=0,
    x=32-chara_width//2,  
    y=display.height - chara_height - 10     
)


prop_sheet = displayio.OnDiskBitmap("prop.bmp")
prop2_sheet = displayio.OnDiskBitmap("prop2.bmp")
text_sheet = displayio.OnDiskBitmap("text.bmp")

# 특정 타일 크기 설정 (예: 16x16 픽셀)
tile_width = 16
tile_height = 16

arrow_sprite = displayio.TileGrid(
    prop_sheet,
    pixel_shader=prop_sheet.pixel_shader,
    width=1,
    height=1,
    tile_width=tile_width,
    tile_height=tile_height,
)
prop_sprite = displayio.TileGrid(
    prop_sheet,
    pixel_shader=prop_sheet.pixel_shader,
    width=9,
    height=8,
    tile_width=tile_width,
    tile_height=tile_height,
    default_tile=3,
)
text_sprite = displayio.TileGrid(
    text_sheet,
    pixel_shader=text_sheet.pixel_shader,
    width=14,
    height=7,
    tile_width=8,
    tile_height=12,
    x=8,  
    y=12,
    default_tile=47,
)
game_back_sprite = displayio.TileGrid(
    prop2_sheet,
    pixel_shader=prop2_sheet.pixel_shader,
    width=11,
    height=7,
    tile_width=8,
    tile_height=8,
    x=24,  
    y=40,
    default_tile=23,
)
game_entity1_sprite = displayio.TileGrid(
    prop2_sheet,
    pixel_shader=prop2_sheet.pixel_shader,
    width=2,
    height=3,
    tile_width=8,
    tile_height=8,
    x=-128,  
    y=0,
    default_tile=23,
)
game_entity2_sprite = displayio.TileGrid(
    prop2_sheet,
    pixel_shader=prop2_sheet.pixel_shader,
    width=2,
    height=3,
    tile_width=8,
    tile_height=8,
    x=-128,  
    y=0,
    default_tile=23,
)
game_entity3_sprite = displayio.TileGrid(
    prop2_sheet,
    pixel_shader=prop2_sheet.pixel_shader,
    width=1,
    height=1,
    tile_width=8,
    tile_height=8,
    x=-128,  
    y=0,
    default_tile=23,
)
game_entity4_sprite = displayio.TileGrid(
    prop2_sheet,
    pixel_shader=prop2_sheet.pixel_shader,
    width=1,
    height=1,
    tile_width=8,
    tile_height=8,
    x=-128,  
    y=0,
    default_tile=23,
)
game_entity5_sprite = displayio.TileGrid(
    prop2_sheet,
    pixel_shader=prop2_sheet.pixel_shader,
    width=1,
    height=1,
    tile_width=8,
    tile_height=8,
    x=-128,  
    y=0,
    default_tile=23,
)
ladder_sheet = displayio.OnDiskBitmap("ladder.bmp")
ladder_sprite = displayio.TileGrid(ladder_sheet, pixel_shader=ladder_sheet.pixel_shader)

box_bitmap = displayio.Bitmap(120, 44, 1)
box_palette = displayio.Palette(1)
box_palette[0] = 0x222034
box_sprite = displayio.TileGrid(box_bitmap, pixel_shader=box_palette, x=-128, y=8)

box2_bitmap = displayio.Bitmap(88, 68, 1)
box2_palette = displayio.Palette(1)
box2_palette[0] = 0x222034
box2_sprite = displayio.TileGrid(box2_bitmap, pixel_shader=box2_palette, x=-128, y=32)
box3_bitmap = displayio.Bitmap(112, 80, 1)
box3_palette = displayio.Palette(1)
box3_palette[0] = 0x847e87
box3_sprite = displayio.TileGrid(box3_bitmap, pixel_shader=box3_palette, x=-128, y=26)
box4_bitmap = displayio.Bitmap(112, 114, 1)
box4_palette = displayio.Palette(1)
box4_palette[0] = 0x9badb7
box4_sprite = displayio.TileGrid(box4_bitmap, pixel_shader=box4_palette, x=-128, y=14)
fade_bitmap = displayio.Bitmap(128, 128, 1)
fade_palette = displayio.Palette(1)
fade_palette[0] = 0x222034
fade_sprite = displayio.TileGrid(fade_bitmap, pixel_shader=fade_palette, x=-128, y=0)
box5_bitmap = displayio.Bitmap(4, 60, 1)
box5_palette = displayio.Palette(1)
box5_palette[0] = 0x222034
box5_sprite = displayio.TileGrid(box5_bitmap, pixel_shader=box5_palette, x=-128, y=36)#20
box5_sprite2 = displayio.TileGrid(box5_bitmap, pixel_shader=box5_palette, x=-128, y=36)#104
box6_bitmap = displayio.Bitmap(4, 60, 1)
box6_palette = displayio.Palette(1)
box6_palette[0] = 0x847e87
box6_sprite = displayio.TileGrid(box6_bitmap, pixel_shader=box6_palette, x=-128, y=36)#16
box6_sprite2 = displayio.TileGrid(box6_bitmap, pixel_shader=box6_palette, x=-128, y=36)#108

arrow_sprite[0] = 9


prop_sprite.y = 15
prop_sprite.x = -2

splash.append(room_sprite)
splash.append(prop_sprite)
splash.append(ladder_sprite)
splash.append(chara_sprite)
splash.append(arrow_sprite)
splash.append(box_sprite)
splash.append(box4_sprite)
splash.append(box3_sprite)
splash.append(box2_sprite)
splash.append(fade_sprite)
splash.append(text_sprite)
splash.append(game_back_sprite)
splash.append(game_entity1_sprite)
splash.append(game_entity2_sprite)
splash.append(game_entity3_sprite)
splash.append(game_entity4_sprite)
splash.append(game_entity5_sprite)
splash.append(box5_sprite)
splash.append(box5_sprite2)
splash.append(box6_sprite)
splash.append(box6_sprite2)

frame = 0
frame_timer = 0
speed = 4
playerstate = "idle"
playerstate_his = "idle"
room = 1

talk = 0
talk_m = 0
talk_text = ""
talk_text_index = 0
choice = 1
ischoice = 0

read = 0
read_text = []
read_cursor = 0
read_once = 0
read_cursor_timer = 0

game = 0
game_clear = [0,0,0]
game_scene = 0
game_main_choice = 0
game_pong_pl_y = 0
game_pong_en_y = 0
game_pong_pl_ani = 0
game_pong_en_ani = 0
game_pong_m = 0
game_pong_ball = [0,0]
game_pong_ball_g = 0
game_pong_ball_sp = 0
game_pong_ball_ai = [0,0,0,0,0]
game_pong_score = [0,0]
game_gala_pl_x = 0
game_gala_en = [0 for i in range(40)]
game_gala_bullet = 0
game_gala_ef = 0
game_gala_en_time =0
game_gala_time =0
game_gala_cooltime =0
game_gala_m =0
game_gala_score = 0
game_mario_pl = [0,0,0]
game_mario_pl_ani = 0
game_mario_pl_m = 0
game_mario_en = [0,0]
game_mario_powerup = [0,0]
game_mario_coin = 0
game_mario_cam_x= 0
game_mario_map = [
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [1,1,1,1,1,1,1,1,1,1],
]
game_mario_m = 0

inventory = ""

ladder = 0
figure = 0
password = 0
box = 0
power = 0
paper = 0

up_once = 0
up_once2 = 0
left_once = 0
left_once2 = 0
right_once = 0
right_once2 = 0

chara_sprite.flip_x = True

talk = 1
talk_m = 76
talk_text_index = -1
up_once=0

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    keys = pygame.key.get_pressed()

    playerstate = "idle"
    if not (talk or read or game):
        if keys[pygame.K_LEFT] and keys[pygame.K_RIGHT]:
            pass
        else:
            if keys[pygame.K_LEFT]:
                chara_sprite.x -= speed
                chara_sprite.flip_x = False
                playerstate = "walk"
            if keys[pygame.K_RIGHT]:
                chara_sprite.x += speed
                chara_sprite.flip_x = True
                playerstate = "walk"

    up_once = 0
    if keys[pygame.K_UP]:
        if(up_once2):
            up_once = 1
        up_once2 = 0
    else:
        up_once2 = 1
    left_once= 0
    if keys[pygame.K_LEFT]:
        if(left_once2):
            left_once = 1
        left_once2 = 0
    else:
        left_once2 = 1
    right_once = 0
    if keys[pygame.K_RIGHT]:
        if(right_once2):
            right_once = 1
        right_once2 = 0
    else:
        right_once2 = 1

    if not (talk or read or game):
        if(chara_sprite.x+chara_width//2 < 32):
            if(room != 2):
                chara_sprite.x = 32-chara_width//2
            else:
                if(chara_sprite.x+chara_width//2 <= 0):
                    room = 1
                    room_sprite[0] = room-1
                    chara_sprite.x =  display.width-32-chara_width//2
        if(chara_sprite.x+chara_width//2 > display.width-32):
            if(room != 1):
                chara_sprite.x =  display.width-32-chara_width//2
            else:
                if(chara_sprite.x+chara_width//2 >= display.width):
                    room = 2
                    room_sprite[0] = room-1
                    chara_sprite.x = 32-chara_width//2
        
        if(chara_sprite.x+chara_width//2 < 48):
            if(room == 3):
                chara_sprite.x = 48-chara_width//2

        if(chara_sprite.x+chara_width//2 >= display.width-32-16 and chara_sprite.x+chara_width//2 <= display.width-32):
            if(room != 1):
                if up_once:
                    up_once = 0
                    if(ladder):
                        room = 3-(room == 3)*1
                        room_sprite[0] = room-1
                        chara_sprite.x = display.width-32-chara_width//2
                    else:
                        if(inventory == "ladder"):
                            talk = 1
                            talk_m = 19
                            talk_text_index = -1
                        else:
                            talk = 1
                            talk_m = 22
                            talk_text_index = -1


    arrow_sprite.x = -128
    box_sprite.x = -128
    box2_sprite.x = -128
    box3_sprite.x = -128
    box4_sprite.x = -128

    prop_sprite[2*9+4+1] = 3
    prop_sprite[3*9+4+1] = 3

    prop_sprite[4*9+6+1] = 3
    prop_sprite[5*9+6+1] = 3
    prop_sprite[5*9+7+1] = 3

    prop_sprite[4*9+0+1] = 3
    prop_sprite[4*9+1+1] = 3

    prop_sprite[5*9+5+1] = 3
    prop_sprite[5*9+6+1] = 3

    prop_sprite[5*9+0] = 3

    prop_sprite[3*9+3+1] = 3
    prop_sprite[4*9+2+1] = 3
    prop_sprite[4*9+3+1] = 3
    prop_sprite[4*9+4+1] = 3
    
    prop_sprite[1*9+0+1] = 3
    prop_sprite[2*9+0+1] = 3

    ladder_sprite.x = -128

    if(room == 1):
        if(power):
            prop_sprite[4*9+6+1] = 2
            prop_sprite[5*9+6+1] = 6
            prop_sprite[5*9+7+1] = 7
        if(not figure):
            prop_sprite[2*9+4+1] = 8
            prop_sprite[3*9+4+1] = 12
        else:
            prop_sprite[5*9+5+1] = 4
            prop_sprite[5*9+6+1] = 5

        if not (talk or read or game):
            if(chara_sprite.x+chara_width//2 < 40):
                arrow_sprite.x = 8
                arrow_sprite.y = 32
                
                if(up_once):
                    talk = 1
                    talk_m = 67
                    talk_text_index = -1
                    up_once=0
            if(chara_sprite.x+chara_width//2 >= 40 and chara_sprite.x+chara_width//2 <= 40+32):
                arrow_sprite.x = 40+16-8+1
                arrow_sprite.y = 32
                if(up_once):
                    talk = 1
                    talk_m = 1
                    talk_text_index = -1
                    up_once=0
            elif(chara_sprite.x+chara_width//2 >= 72 and chara_sprite.x+chara_width//2 <= 72+24):
                arrow_sprite.x = 77-8+1
                arrow_sprite.y = 24
                
                if(up_once):
                    talk = 1
                    if(figure):
                        talk_m = 56
                    else:
                        talk_m = 49
                    talk_text_index = -1
                    up_once=0
            elif(chara_sprite.x+chara_width//2 >= 96 and chara_sprite.x+chara_width//2 <= 96+32):
                arrow_sprite.x = 112-8+1
                arrow_sprite.y = 64-8
                if(up_once):
                    talk = 1
                    talk_m = 40
                    talk_text_index = -1
                    up_once=0
    if(room == 2):
        if(ladder):
            ladder_sprite.x = 16*6
        if(power):
            prop_sprite[5*9+0] = 7
        if(box):
            prop_sprite[3*9+4] = 10
            prop_sprite[4*9+3] = 13
            prop_sprite[4*9+4] = 14
            prop_sprite[4*9+5] = 15

        if not (talk or read or game):
            if(chara_sprite.x+chara_width//2 >= display.width-32-16 and chara_sprite.x+chara_width//2 <= display.width-32):
                arrow_sprite.x = display.width-32
                arrow_sprite.y = 32
            elif(chara_sprite.x+chara_width//2 >= 16 and chara_sprite.x+chara_width//2 <= 16+32):
                arrow_sprite.x = 161-128-8+1
                arrow_sprite.y = 16
                if(up_once):
                    talk = 1
                    talk_m = 44
                    talk_text_index = -1
                    up_once=0
            elif(chara_sprite.x+chara_width//2 >= 64 and chara_sprite.x+chara_width//2 <= 64+16):
                arrow_sprite.x = 64+1
                arrow_sprite.y = 48
                if(up_once):
                    talk = 1
                    if(box):
                        talk_m = 66
                    else:
                        talk_m = 57
                    talk_text_index = -1
                    up_once=0

    if(room == 3):
        if(paper):
            prop_sprite[4*9+1] = 0
            prop_sprite[4*9+2] = 1

        if not (talk or read or game):
            if(chara_sprite.x+chara_width//2 >= display.width-32-16 and chara_sprite.x+chara_width//2 <= display.width-32):
                arrow_sprite.x = display.width-32
                arrow_sprite.y = 64
            elif(chara_sprite.x+chara_width//2 >= 48 and chara_sprite.x+chara_width//2 <= 48+8):
                arrow_sprite.x = 32-8
                arrow_sprite.y = 32
                if(up_once):
                    talk = 1
                    talk_m = 23
                    talk_text_index = -1
                    up_once=0
            elif(chara_sprite.x+chara_width//2 >= 64-8 and chara_sprite.x+chara_width//2 <= 64+8):
                arrow_sprite.x = 64-8
                arrow_sprite.y = 0
                if(up_once):
                    talk = 1
                    talk_m = 35
                    talk_text_index = -1
                    up_once=0

    if(playerstate == "idle"):
        if(playerstate_his != playerstate):
            frame_timer= 0
        if(frame == 0):
            frame_timer+=1
            if(frame_timer == 30):
                frame = 1
                frame_timer= 0
        elif(frame == 1):
            frame = 0
        else:
            frame = 0
    if(playerstate == "walk"):
        if(playerstate_his != playerstate):
            frame_timer= 0
        frame_timer+=1
        if(frame == 0):
            if(frame_timer == 2):
                frame = 2
                frame_timer= 0
        elif(frame == 2):
            if(frame_timer == 2):
                frame = 0
                frame_timer= 0
        else:
            frame = 0

    if(talk or read or game):
        playerstate = "idle"

    chara_sprite[0] = frame
    playerstate_his = playerstate
    while 1:
        ischoice = 0
        if(talk):
            if(talk_m == 1): talk_text = "a two-tiered drawer."
            elif(talk_m == 2): talk_text = "which tier should i open?"
            elif(talk_m == 3): talk_text = "top/bottom"
            elif(talk_m == 4): talk_text = "a ladder is here. take it?" #사다리가있다. 얻을까?
            elif(talk_m == 5): talk_text = "a paper is here. take it?" #종이가있다. 얻을까?
            elif(talk_m == 6): talk_text = "yes/no"
            elif(talk_m == 7): talk_text = "yes/no"
            elif(talk_m == 8): talk_text = "you already have the "+inventory+"."#당신은이미''를갖고있다
            elif(talk_m == 9): talk_text = "you got the ladder."#사다릴를얻었다
            elif(talk_m == 10): talk_text = "you got the paper.something written on it."#를얻었다
            elif(talk_m == 11): talk_text = "it's empty."#비어있다
            elif(talk_m == 12): talk_text = "it's empty."#비어있다
            elif(talk_m == 13): talk_text = "put the ladder back?"#사다리다시넣어둘까?
            elif(talk_m == 14): talk_text = "yes/no"
            elif(talk_m == 15): talk_text = "ladder put back."#사다리다시넣었다
            elif(talk_m == 16): talk_text = "put the paper back?"#종이다시넣어둘까?
            elif(talk_m == 17): talk_text = "yes/no"
            elif(talk_m == 18): talk_text = "paper put back."#종이다시넣었다
            elif(talk_m == 19): talk_text = "set up the ladder?"#사다리설치?
            elif(talk_m == 20): talk_text = "yes/no"
            elif(talk_m == 21): talk_text = "ladder set up."#사다리설치
            elif(talk_m == 22): talk_text = "you need something to climb up."#뭔가필요함
            elif(talk_m == 23): talk_text = "a desk."
            elif(talk_m == 24): talk_text = "open the desk drawer?"
            elif(talk_m == 25): talk_text = "yes/no"
            elif(talk_m == 26): talk_text = "a power cord here. take it?"
            elif(talk_m == 27): talk_text = "yes/no"
            elif(talk_m == 28): talk_text = "you got the power cord."
            elif(talk_m == 29): talk_text = "place the paper on the desk?"
            elif(talk_m == 30): talk_text = "yes/no"
            elif(talk_m == 31): talk_text = "paper placed."
            elif(talk_m == 32): talk_text = "read the paper?"
            elif(talk_m == 33): talk_text = "yes/no"
            elif(talk_m == 34): talk_text = "maybe you can rearrange the letters."
            elif(talk_m == 35): talk_text = "trees visible outside the window."
            elif(talk_m == 36): talk_text = "it's empty."#비어있다
            elif(talk_m == 37): talk_text = "put the power cord back?"
            elif(talk_m == 38): talk_text = "yes/no"
            elif(talk_m == 39): talk_text = "power cord put back."
            elif(talk_m == 40): talk_text = "a power outlet."
            elif(talk_m == 41): talk_text = "connect the power cord to the console?"
            elif(talk_m == 42): talk_text = "yes/no"
            elif(talk_m == 43): talk_text = "power cord connected to the console."
            elif(talk_m == 44): talk_text = "a game console."
            elif(talk_m == 45): talk_text = "doesn't seem to work."
            elif(talk_m == 46): talk_text = "start the game console?"
            elif(talk_m == 47): talk_text = "yes/no"
            elif(talk_m == 48): talk_text = "figured something out!"
            elif(talk_m == 49): talk_text = "a wooden figure."
            elif(talk_m == 50): talk_text = "break the figure?"
            elif(talk_m == 51): talk_text = "yes/no"
            elif(talk_m == 52): talk_text = "a key inside the figure!"
            elif(talk_m == 53): talk_text = "take the key?"
            elif(talk_m == 54): talk_text = "yes/no"
            elif(talk_m == 55): talk_text = "key obtained."
            elif(talk_m == 56): talk_text = "a broken figure."
            elif(talk_m == 57): talk_text = "a wooden box."
            elif(talk_m == 58): talk_text = "it's locked."
            elif(talk_m == 59): talk_text = "use the key to open the box?"
            elif(talk_m == 60): talk_text = "yes/no"
            elif(talk_m == 61): talk_text = "box opened."
            elif(talk_m == 62): talk_text = "an axe inside the box."
            elif(talk_m == 63): talk_text = "take the axe?"
            elif(talk_m == 64): talk_text = "yes/no"
            elif(talk_m == 65): talk_text = "axe obtained."
            elif(talk_m == 66): talk_text = "an open box."
            elif(talk_m == 67): talk_text = "a door."
            elif(talk_m == 68): talk_text = "it won't open."
            elif(talk_m == 69): talk_text = "break the door with the axe?"
            elif(talk_m == 70): talk_text = "yes/no"
            elif(talk_m == 71): talk_text = "door destroyed."
            elif(talk_m == 72): talk_text = "escaped through the broken door."
            elif(talk_m == 73): talk_text = "finally... escaped."
            elif(talk_m == 74): talk_text = "-end-"
            elif(talk_m == 75): talk_text = "thank you for playing!!!"
            elif(talk_m == 76): talk_text = "where am i?"
            elif(talk_m == 77): talk_text = "i came to my senses and found myself here."
            elif(talk_m == 78): talk_text = "letters visible on the console."
            elif(talk_m == 79): 
                talk_text = list("              --------------")#breakthefigure
                talk_text[4] = "*"
                talk_text[8] = "*"
                talk_text[9] = "*"
                if(game_clear[0]):
                    talk_text[4] = "^"
                    talk_text[4+14] = "k"
                if(game_clear[1]):
                    talk_text[8] = "^"
                    talk_text[8+14] = "f"
                if(game_clear[2]):
                    talk_text[9] = "^"
                    talk_text[9+14] = "i"
                talk_text = "".join(talk_text)

            if(talk_text.find('/') != -1):
                talk_text = talk_text.split('/')
                talk_text = talk_text[0].ljust(6," ")+talk_text[1].ljust(6," ")
                ischoice =1

            box_sprite.x = 4

            if(talk_text_index != len(talk_text)):
                for i in range(1+(up_once or ischoice)*(len(talk_text)-talk_text_index-1)):
                    if(talk_text_index > -1):
                        text_sprite[talk_text_index+ischoice*15] = text_to_sprite(talk_text[talk_text_index])
                    talk_text_index+=1
                if(up_once):up_once=0
            else:
                if(ischoice):
                    if(keys[pygame.K_LEFT]):
                        choice = 1
                    elif(keys[pygame.K_RIGHT]):
                        choice = 0
                    if(not choice):
                        text_sprite[14+6] = 28
                        text_sprite[14] = 47
                    else:
                        text_sprite[14] = 28
                        text_sprite[14+6] = 47
                if(up_once):
                    up_once=0
                    talk_text_index = -1
                    if(talk_m == 1): talk_m = 2
                    elif(talk_m == 2): talk_m = 3
                    elif(talk_m == 3): 
                        if(choice):
                            if(inventory == "ladder" or ladder):
                                talk_m = 11
                            else:
                                talk_m = 4
                        else:
                            if(inventory == "paper" or paper):
                                talk_m = 12
                            else:
                                talk_m = 5
                    elif(talk_m == 4): 
                        talk_m = 6
                    elif(talk_m == 5):
                        talk_m = 7
                    elif(talk_m == 6): 
                        if(choice):
                            if(inventory ==""):
                                talk_m = 9
                            else:
                                talk_m = 8
                        else:
                            talk_m = 0
                    elif(talk_m == 7): 
                        if(choice):
                            if(inventory == ""):
                                talk_m = 10
                            else:
                                talk_m = 8
                        else:
                            talk_m = 0
                    elif(talk_m == 8): 
                        talk_m = 0
                    elif(talk_m == 9): 
                        inventory = "ladder"
                        talk_m = 0
                    elif(talk_m == 10): 
                        inventory = "paper"
                        talk_m = 0
                    elif(talk_m == 11): 
                        if(inventory == "ladder"):
                            talk_m = 13
                        else:
                            talk_m = 0
                    elif(talk_m == 12): 
                        if(inventory == "paper"):
                            talk_m = 16
                        else:
                            talk_m = 0
                    elif(talk_m == 13): 
                        talk_m = 14
                    elif(talk_m == 14): 
                        if(choice):
                            talk_m = 15
                        else:
                            talk_m = 0
                    elif(talk_m == 15):
                        inventory = ""
                        talk_m = 0
                    elif(talk_m == 16): 
                        talk_m = 17
                    elif(talk_m == 17): 
                        if(choice):
                            talk_m = 18
                        else:
                            talk_m = 0
                    elif(talk_m == 18):
                        inventory = ""
                        talk_m = 0
                    elif(talk_m == 19):
                        talk_m = 20
                    elif(talk_m == 20):
                        if(choice):
                            talk_m = 21
                        else:
                            talk_m = 0
                    elif(talk_m == 21):
                        inventory = ""
                        ladder = 1
                        talk_m = 0
                    elif(talk_m == 23):
                        if(inventory == "paper"):
                            talk_m = 29
                        else:
                            if(paper):
                                talk_m = 32
                            else:
                                talk_m = 24
                    elif(talk_m == 24):
                        talk_m = 25
                    elif(talk_m == 25):
                        if(choice):
                            if(inventory == "power" or power):
                                talk_m = 36
                            else:
                                talk_m = 26
                        else:
                            talk_m = 0
                    elif(talk_m == 26):
                        talk_m = 27
                    elif(talk_m == 27):
                        if(choice):
                            if(inventory == ""):
                                talk_m = 28
                            else:
                                talk_m = 8
                        else:
                            talk_m = 0
                    elif(talk_m == 28):
                        inventory = "power"
                        talk_m = 0
                    elif(talk_m == 29):
                        talk_m = 30
                    elif(talk_m == 30):
                        if(choice):
                            talk_m = 31
                        else:
                            talk_m = 24
                    elif(talk_m == 31):
                        inventory = ""
                        paper = 1
                        talk_m = 0
                    elif(talk_m == 32):
                        talk_m = 33
                    elif(talk_m == 33):
                        if(choice):
                            read = 1
                            read_once = 1
                            talk_m = 0
                        else:
                            talk_m = 24
                    elif(talk_m == 34):
                        read = 1
                        read_once = 1
                        talk_m = 0
                    elif(talk_m == 36):
                        if(inventory == "power"):
                            talk_m = 37
                        else:
                            talk_m = 0
                    elif(talk_m == 37):
                        talk_m = 38
                    elif(talk_m == 38):
                        if(choice):
                            talk_m = 39
                        else:
                            talk_m = 0
                    elif(talk_m == 39):
                        inventory = ""
                        talk_m = 0
                    elif(talk_m == 40):
                        if(inventory == "power"):
                            talk_m = 41
                        else:
                            talk_m = 0
                    elif(talk_m == 41):
                        talk_m = 42
                    elif(talk_m == 42):
                        if(choice):
                            talk_m = 43
                        else:
                            talk_m = 0
                    elif(talk_m == 43):
                        inventory = ""
                        power =1
                        talk_m = 0
                    elif(talk_m == 44):
                        if(power):
                            talk_m = 46
                        else:
                            talk_m = 45
                    elif(talk_m == 45):
                        talk_m = 0
                    elif(talk_m == 46):
                        talk_m = 47
                    elif(talk_m == 47):
                        if(choice):
                            game = 1
                            game_scene = 0
                            game_main_choice = 0
                            talk_m = 0
                        else:
                            talk_m = 0
                    elif(talk_m == 48):
                        talk_m = 0
                    elif(talk_m == 49):
                        if(password and (not figure)):
                            talk_m = 50
                        else:
                            talk_m = 0
                    elif(talk_m == 50):
                        talk_m = 51
                    elif(talk_m == 51):
                        if(choice):
                            figure = 1
                            talk_m = 52
                        else:
                            talk_m = 0
                    elif(talk_m == 52):
                        talk_m = 53
                    elif(talk_m == 53):
                        talk_m = 54
                    elif(talk_m == 54):
                        if(choice):
                            if(inventory == ""):
                                talk_m = 55
                            else:
                                talk_m = 8
                        else:
                            talk_m = 0
                    elif(talk_m == 55):
                        inventory = "key"
                        talk_m = 0
                    elif(talk_m == 56):
                        if(inventory == "key" or box):
                            talk_m = 0
                        else:
                            talk_m = 53
                    elif(talk_m == 57):
                        talk_m = 58
                    elif(talk_m == 58):
                        if(inventory == "key"):
                            talk_m = 59
                        else:
                            talk_m = 0
                    elif(talk_m == 59):
                        talk_m = 60
                    elif(talk_m == 60):
                        if(choice):
                            talk_m = 61
                        else:
                            talk_m = 0
                    elif(talk_m == 61):
                        inventory = ""
                        box = 1
                        talk_m = 62
                    elif(talk_m == 62):
                        talk_m = 63
                    elif(talk_m == 63):
                        talk_m = 64
                    elif(talk_m == 64):
                        if(choice):
                            if(inventory == ""):
                                talk_m = 65
                            else:
                                talk_m = 8
                        else:
                            talk_m = 0
                    elif(talk_m == 65):
                        inventory = "axe"
                        talk_m = 0
                    elif(talk_m == 66):
                        if(inventory == "axe"):
                            talk_m = 0
                        else:
                            talk_m = 62
                    elif(talk_m == 67):
                        talk_m = 68
                    elif(talk_m == 68):
                        if(inventory == "axe"):
                            talk_m = 69
                        else:
                            talk_m = 0
                    elif(talk_m == 69):
                        talk_m = 70
                    elif(talk_m == 70):
                        if(choice):
                            talk_m = 71
                        else:
                            talk_m = 0
                    elif(talk_m == 71):
                        fade_sprite.x = 0
                        talk_m = 72
                    elif(talk_m == 72):
                        talk_m = 73
                    elif(talk_m == 73):
                        talk_m = 74
                    elif(talk_m == 74):
                        talk_m = 75
                    elif(talk_m == 75):
                        talk_m = 75
                    elif(talk_m == 76):
                        talk_m = 77
                    elif(talk_m == 77):
                        talk_m = 0
                    elif(talk_m == 78):
                        talk_m = 79
                    elif(talk_m == 79):
                        talk_m = 0

                    else: 
                        talk_m = 0


                    if(talk_m == 0):
                        talk = 0
                    
                    choice = 1
                    for i in range(3*14):
                        text_sprite[i] = 47
            if(not talk):
                box_sprite.x = -128
        if(read):
            box_sprite.x = 4

            if(read_once):
                read_text = list("hugefreaktribe")
                for i in range(len(read_text)):
                    text_sprite[i+14] = ord(read_text[i])-ord('a')
                text_sprite[0] = 31
                read_once = 0
                read_cursor = 0
            read_cursor_timer += 1
            if(read_cursor_timer > 2):read_cursor_timer =2
            if(read_cursor_timer == 2):
                if(keys[pygame.K_LEFT]):
                    read_cursor_timer = 0
                    if(read_cursor != 0):
                        if(read_cursor == 14):
                            text_sprite[41] = 47
                        else:
                            text_sprite[read_cursor] = 47
                        read_cursor -= 1
                        text_sprite[read_cursor] = 31
                if(keys[pygame.K_RIGHT]):
                    read_cursor_timer = 0
                    if(read_cursor != 14):
                        text_sprite[read_cursor] = 47
                        read_cursor += 1
                        if(read_cursor == 14):
                            text_sprite[41] = 31
                        else:
                            text_sprite[read_cursor] = 31
            if(up_once):
                up_once= 0
                if(read_cursor == 14):
                    read = 0
                else:
                    read_text.append(read_text.pop(read_cursor))
                    for i in range(len(read_text)):
                        text_sprite[i+14] = ord(read_text[i])-ord('a')

            if(not read):
                for i in range(3*14):
                    text_sprite[i] = 47
                box_sprite.x = -128

                if(read_text == list("breakthefigure")):
                    if(not password):
                        talk = 1
                        talk_m = 48
                        talk_text_index = -1
                        password =1
                        continue
    
        if(game):
            box2_sprite.x = 20
            box3_sprite.x = 8
            box4_sprite.x = 8
            box5_sprite.x = 20
            box5_sprite2.x = 104
            box6_sprite.x = 16
            box6_sprite2.x = 108

            if(game_scene == 0):
                for i in range(4):
                    text_sprite[32+i+14+14] = ord("pong"[i])-ord('a')
                for i in range(6):
                    text_sprite[32+i+14] = ord("galaga"[i])-ord('a')
                for i in range(5):
                    text_sprite[32+i+28+14] = ord("mario"[i])-ord('a')
                for i in range(3):
                    if(game_clear[i] == 1):text_sprite[32+6+14*i+14] = 44
                text_sprite[31+14*game_main_choice+14] = 32
                text_sprite[32+5+42+14] = 45
                text_sprite[32+6+42+14] = 46
                game_scene = 1
            if(game_scene == 1):
                if(left_once):
                    if(game_main_choice == 3):
                        text_sprite[32+4+42+14] = 47
                    text_sprite[31+14*game_main_choice+14] = 47
                    game_main_choice -= 1
                    if(game_main_choice == -1):game_main_choice = 0
                    text_sprite[31+14*game_main_choice+14] = 32
                if(right_once):
                    text_sprite[31+14*game_main_choice+14] = 47
                    game_main_choice += 1
                    if(game_main_choice == 4): game_main_choice = 3
                    if(game_main_choice == 3):
                        text_sprite[32+4+42+14] = 32
                    else:
                        text_sprite[31+14*game_main_choice+14] = 32
                if(up_once):
                    up_once= 0
                    if(game_main_choice == 3):
                        game = 0
                    elif(game_main_choice == 1): #pong
                        game_scene = 2
                        for i in range(2*14,7*14):
                            text_sprite[i] = 47
                        game_back_sprite[60+6] = 57
                        game_back_sprite[61+6] = 58
                        game_back_sprite[62+6] = 59
                        game_back_sprite[63+6] = 59
                        game_back_sprite[64+6] = 58
                        game_back_sprite[65+6] = 60
                        game_back_sprite[66+6] = 59
                        game_back_sprite[67+6] = 59
                        game_back_sprite[68+6] = 60
                        game_back_sprite[69+6] = 61
                        game_back_sprite[54+5] = 62
                        game_back_sprite[55+5] = 63
                        game_entity1_sprite[0] = 23
                        game_entity1_sprite[1] = 34
                        game_entity1_sprite[2] = 23
                        game_entity1_sprite[3] = 42
                        game_entity1_sprite[4] = 23
                        game_entity1_sprite[5] = 50
                        game_entity1_sprite.x = 88
                        game_entity2_sprite[0] = 23
                        game_entity2_sprite[1] = 34
                        game_entity2_sprite[2] = 23
                        game_entity2_sprite[3] = 42
                        game_entity2_sprite[4] = 23
                        game_entity2_sprite[5] = 50
                        game_entity2_sprite.x = 24
                        game_entity2_sprite.flip_x = True
                        game_pong_pl_y = 48
                        game_pong_en_y = 48
                        game_pong_pl_ani = 0
                        game_pong_en_ani = 0
                        game_pong_m = 0
                        game_entity3_sprite[0] = 56
                        game_pong_ball_g = 0
                        game_pong_ball = [60,56]
                        game_pong_ball_sp = 0
                        game_pong_ball_ai = [0,0,0,0,0,0,0]
                        game_pong_score = [0,0]
                        text_sprite[30] = 33
                        text_sprite[39] = 33
                    elif(game_main_choice == 0):
                        game_scene = 3
                        for i in range(2*14,7*14):
                            text_sprite[i] = 47
                        game_gala_en = [0 for i in range(40)]
                        for i in range(0,10):
                            game_gala_en[i]= 1
                        game_entity1_sprite[0] = 23
                        game_entity1_sprite[1] = 23
                        game_entity1_sprite[2] = 35
                        game_entity1_sprite[3] = 36
                        game_entity1_sprite[4] = 43
                        game_entity1_sprite[5] = 44
                        game_entity1_sprite.y =72
                        game_entity3_sprite[0] = 39
                        game_entity4_sprite[0] = 45
                        game_gala_pl_x = 56
                        game_gala_bullet = 0
                        game_gala_en_time = 10
                        game_gala_time =0
                        game_gala_m =0
                        game_gala_score= 0
                        game_gala_cooltime =10
                        game_gala_ef = 0
                        game_gala_ef_ani = 0
                    elif(game_main_choice == 2):
                        game_scene = 4
                        game_mario_m = 0

            if(game_scene == 4):
                if(game_mario_m == 0):
                    for i in range(2*14,7*14):
                        text_sprite[i] = 47

                    game_entity1_sprite[0] = 23
                    game_entity1_sprite[1] = 23
                    game_entity1_sprite[2] = 23
                    game_entity1_sprite[3] = 23
                    game_entity1_sprite[4] = 16
                    game_entity1_sprite[5] = 23
                    game_entity3_sprite[0] = 19#coin,score
                    game_entity4_sprite[0] = 27#powerup
                    game_entity5_sprite[0] = 25#enemy

                    game_mario_pl = [8,32,0]
                    game_mario_pl_ani_m = 0
                    game_mario_pl_ani_m_his = 0
                    game_mario_pl_m_ani = 0
                    game_mario_pl_m_ani_r = 0
                    game_mario_pl_ani = 0
                    game_mario_pl_m = 0
                    game_mario_pl_m2 = 0
                    game_mario_pl_ani = 0
                    game_mario_pl_stat = 0
                    game_mario_en = [0,0,0,0,0,0,0]#enable,x,y,g,flip,ani,m
                    game_mario_powerup = [0,0,0,0,0]
                    game_mario_coin = 0
                    game_mario_coin_g = 0
                    game_mario_score = 0
                    game_mario_score_t = 0
                    game_mario_map = [
  [0,0,0,0,0,0,0,0,0,0,0,8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8,0,0,0,0,0,0,0,0,0,0,8,8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,10,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8,8,8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,7,0,0,0,0,9,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,3,0,0,0,2,6,2,3,2,0,0,0,0,0,0,0,0,0,0,0,0,5,5,0,0,0,0,0,5,5,0,0,0,0,8,8,0,0,0,0,2,6,2,0,0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,3,0,3,0,3,0,0,0,0,0,0,0,5,0,0,5,0,0,0,0,0,0,0,0,0,0,0,5,5,0,0,0,0,9,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,5,0,0,0,0,0,5,5,0,0,0,0,0,5,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,5,0,0,5,5,0,0,0,8,8,8,0,0,0,5,5,5,0,0,0,0,9,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,7,0,0,0,0,0,5,5,0,0,0,0,7,5,5,0,0,0,0,0,5,5,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,5,5,0,0,5,5,5,0,0,0,0,0,0,0,5,5,5,5,0,0,0,0,9,0,0,0,0,0,0,0,0,0,0,0],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]
                    game_mario_map_rf = 1
                    
                    game_mario_cam_x= 0
                    game_mario_cam_x_his= 0
                    game_mario_gr= [1,2,3,4,5,6]
                    game_mario_ongr= 0
                    game_mario_j= 0
                    game_mario_m = 1
                    game_mario_score_real = 0
                    game_mario_score_real_his = 0

                    text_sprite[39] = text_to_sprite("0")
                if(game_mario_m == 1):
                    game_mario_score_real_his = game_mario_score_real
                    game_mario_pl_ani_m_his = game_mario_pl_ani_m
                    game_mario_cam_x_his = game_mario_cam_x
                    game_mario_pl_stat = 0
                    if(keys[pygame.K_LEFT]):
                        game_mario_pl[0] -= 2
                        game_mario_pl_stat = 1
                        game_entity1_sprite.flip_x = True
                        if(game_mario_pl[0] < 0):
                            game_mario_pl[0] = 0
                            game_mario_pl_stat = 0
                        if(game_mario_pl[1] > 0):
                            if(game_mario_map[(game_mario_pl[1]+7)//8][(game_mario_pl[0])//8] in game_mario_gr or game_mario_map[(game_mario_pl[1])//8][(game_mario_pl[0])//8] in game_mario_gr or (game_mario_pl_m == 1 and (game_mario_pl[1]-8 > 0) and game_mario_map[(game_mario_pl[1]-8)//8][(game_mario_pl[0])//8] in game_mario_gr )):
                                
                                game_mario_pl[0] += 2
                                game_mario_pl_stat = 0
                        
                    if(keys[pygame.K_RIGHT]):
                        game_mario_pl[0] += 2
                        game_entity1_sprite.flip_x = False
                        game_mario_pl_stat = 1
                        if(game_mario_pl[1] > 0):
                            if(game_mario_map[(game_mario_pl[1]+7)//8][(game_mario_pl[0]+7)//8] in game_mario_gr or game_mario_map[(game_mario_pl[1])//8][(game_mario_pl[0]+7)//8] in game_mario_gr or (game_mario_pl_m == 1 and (game_mario_pl[1]-8 > 0) and game_mario_map[(game_mario_pl[1]-8)//8][(game_mario_pl[0]+7)//8] in game_mario_gr )):
                                game_mario_pl[0] -= 2
                                game_mario_pl_stat = 0
                            if(game_mario_map[(game_mario_pl[1]+7)//8][(game_mario_pl[0]+7)//8] in [9,10]):
                                game_mario_m = 6

                    if(keys[pygame.K_UP]):
                        if(game_mario_ongr and game_mario_j):
                            game_mario_pl[2] = -8
                    else:
                        game_mario_j = 1

                    game_mario_pl[2] += 1
                    if(game_mario_pl[2] > 7):
                        game_mario_pl[2] = 7
                    game_mario_pl[1] += game_mario_pl[2]
                    game_mario_ongr = 0
                    if(game_mario_pl[1] >= 40):
                        game_mario_m = 2
                        game_mario_pl[1] = 40
                    else:
                        if(game_mario_pl[2] > 0):
                            if(game_mario_pl[1] > 0):
                                if(game_mario_map[(game_mario_pl[1]+8)//8][game_mario_pl[0]//8] in game_mario_gr or game_mario_map[(game_mario_pl[1]+8)//8][(game_mario_pl[0]+7)//8] in game_mario_gr):
                                    game_mario_pl[2] = 0
                                    game_mario_pl[1] = game_mario_pl[1]//8*8
                                    game_mario_ongr = 1

                    
                        else:
                            if(game_mario_pl[1]-game_mario_pl_m*8 > 0):
                                dum,dum1 = game_mario_map[(game_mario_pl[1]-game_mario_pl_m*8)//8][game_mario_pl[0]//8],game_mario_map[(game_mario_pl[1]-game_mario_pl_m*8)//8][(game_mario_pl[0]+7)//8]
                                if(dum in game_mario_gr or dum1 in game_mario_gr):
                                    game_mario_pl[2] = 0
                                    game_mario_pl[1] = game_mario_pl[1]//8*8+8
                                    game_mario_ongr = 0
                                    if(game_mario_pl_m):
                                        if(dum == 2 or dum1 == 2):
                                            game_mario_map_rf = 1
                                            if(dum == 2):
                                                game_mario_map[(game_mario_pl[1])//8-1-game_mario_pl_m][game_mario_pl[0]//8] = 0
                                            else:
                                                game_mario_map[(game_mario_pl[1])//8-1-game_mario_pl_m][game_mario_pl[0]//8+1] = 0
                                    if(dum == 3 or dum1 == 3):
                                        game_mario_coin =1
                                        game_entity3_sprite[0] = 19
                                        game_entity3_sprite.y = game_mario_pl[1]+48-8-game_mario_pl_m*8
                                        game_mario_map_rf = 1
                                        game_mario_coin_g = 4
                                        if(dum == 3):
                                            game_entity3_sprite.x = game_mario_pl[0]//8*8+24-game_mario_cam_x
                                            game_mario_map[(game_mario_pl[1])//8-1-game_mario_pl_m][game_mario_pl[0]//8] = 4
                                        else:
                                            game_entity3_sprite.x = (game_mario_pl[0])//8*8+24-game_mario_cam_x+8
                                            game_mario_map[(game_mario_pl[1])//8-1-game_mario_pl_m][(game_mario_pl[0])//8+1] = 4
                                    if(dum == 6 or dum1 == 6):
                                        game_mario_map_rf = 1
                                        game_mario_powerup[0] = 1
                                        game_mario_powerup[3] = 0
                                        game_mario_powerup[4] = 0
                                        game_mario_powerup[2] = game_mario_pl[1]-16-game_mario_pl_m*8
                                        if(dum == 6):
                                            game_mario_powerup[1] = game_mario_pl[0]//8*8
                                            game_mario_map[(game_mario_pl[1])//8-1-game_mario_pl_m][game_mario_pl[0]//8] = 4
                                        else:
                                            game_mario_powerup[1] = (game_mario_pl[0])//8*8+8
                                            game_mario_map[(game_mario_pl[1])//8-1-game_mario_pl_m][(game_mario_pl[0])//8+1] = 4

                        for i in range(2):
                            for j in range(2):
                                if(game_mario_pl[1]+7*j >= 0):
                                    if(game_mario_map[(game_mario_pl[1]+7*j)//8][(game_mario_pl[0]+i*7)//8] == 8):
                                        game_mario_map_rf = 1
                                        game_mario_map[(game_mario_pl[1]+7*j)//8][(game_mario_pl[0]+i*7)//8] = 0
                                        game_mario_score = 1
                                        game_mario_score_t = 0
                                        game_entity3_sprite[0] = 31
                                        game_entity3_sprite.y = (game_mario_pl[1]+7*j)//8*8+40
                                        game_entity3_sprite.x = (game_mario_pl[0]+i*7)//8*8+24-game_mario_cam_x
                                        game_mario_score_real += 100
                            if((game_mario_pl_m == 1 and (game_mario_pl[1]-8 >= 0) and game_mario_map[(game_mario_pl[1]-8)//8][(game_mario_pl[0]+i*7)//8] == 8 )):
                                
                                game_mario_map_rf = 1
                                game_mario_map[(game_mario_pl[1]-8)//8][(game_mario_pl[0]+i*7)//8] = 0
                                game_mario_score = 1
                                game_mario_score_t = 0
                                game_entity3_sprite[0] = 31
                                game_entity3_sprite.y = (game_mario_pl[1]-8)//8*8+40
                                game_entity3_sprite.x= (game_mario_pl[0]+i*7)//8*8+24-game_mario_cam_x
                                game_mario_score_real += 100


                    if(game_mario_ongr == 0):
                        game_mario_pl_stat = 2
                    if(game_mario_coin):
                        if(game_mario_coin_g == 0):
                            game_mario_coin = 0
                            game_mario_score = 1
                            game_mario_score_t = 0
                            game_entity3_sprite[0] = 31
                            game_mario_score_real += 100
                        game_entity3_sprite.y -= max(game_mario_coin_g,1)
                        game_mario_coin_g= game_mario_coin_g//2
                    if(game_mario_score):
                        game_mario_score_t += 1
                        game_entity3_sprite.y -= 1
                        if(game_mario_score_t == 4):
                            game_mario_score = 0
                            game_entity3_sprite.x = -128
                    if(game_mario_powerup[0]):
                        if(game_mario_powerup[4] == 0):
                            game_mario_powerup[1] += 1
                            if(game_mario_pl[0] < 0):
                                game_mario_powerup[1] -= 1
                                game_mario_powerup[4] = 1
                            if(game_mario_map[(game_mario_powerup[2]+7)//8][(game_mario_powerup[1]+7)//8] in game_mario_gr):
                                game_mario_powerup[1] -= 1
                                game_mario_powerup[4] = 1
                        else:
                            game_mario_powerup[1] += -1
                            if(game_mario_map[(game_mario_powerup[2]+7)//8][(game_mario_powerup[1])//8] in game_mario_gr):
                                game_mario_powerup[1] += 1
                                game_mario_powerup[4] = 0

                        game_mario_powerup[3] += 1
                        if(game_mario_powerup[3] > 7):
                            game_mario_powerup[3] = 7
                        game_mario_powerup[2] += game_mario_powerup[3]

                        if(game_mario_map[(game_mario_powerup[2]+8)//8][game_mario_powerup[1]//8] in game_mario_gr or game_mario_map[(game_mario_powerup[2]+8)//8][(game_mario_powerup[1]+7)//8] in game_mario_gr):
                            game_mario_powerup[2]= game_mario_powerup[2]//8*8
                            game_mario_powerup[3] = 0
                        if(game_mario_powerup[1]-8 < game_mario_pl[0] and game_mario_powerup[1]+8 > game_mario_pl[0]):
                            if(game_mario_powerup[2]-8 < game_mario_pl[1] and game_mario_powerup[2]+8 > game_mario_pl[1]):
                                if(game_mario_pl_m == 0):
                                    game_mario_pl_m = 1
                                    game_mario_pl_m2 = 1 
                                    game_mario_pl_m_ani = 0
                                game_mario_powerup[0] = 0

                                game_mario_score_real += 500
                                game_mario_score = 1
                                game_mario_score_t = 0
                                game_entity3_sprite[0] = 30
                                game_entity3_sprite.x = game_mario_powerup[1]+24-game_mario_cam_x
                                game_entity3_sprite.y = game_mario_powerup[2]+48
                    if(game_mario_en[0]):
                        if(game_mario_en[6] == 0):
                            game_mario_en[5] += 1
                            if(game_mario_en[5] == 4):game_mario_en[5] = 0
                            if(game_mario_en[5]<2):game_entity5_sprite.flip_x = True
                            else:game_entity5_sprite.flip_x = False

                            if(game_mario_en[4] == 0):
                                game_mario_en[1] += 1
                                if(game_mario_en[0] < 0):
                                    game_mario_en[1] -= 1
                                    game_mario_en[4] = 1
                                if(game_mario_map[(game_mario_en[2]+7)//8][(game_mario_en[1]+7)//8] in game_mario_gr):
                                    game_mario_en[1] -= 1
                                    game_mario_en[4] = 1
                            else:
                                game_mario_en[1] += -1
                                if(game_mario_map[(game_mario_en[2]+7)//8][(game_mario_en[1])//8] in game_mario_gr):
                                    game_mario_en[1] += 1
                                    game_mario_en[4] = 0

                            game_mario_en[3] += 1
                            if(game_mario_en[3] > 7):
                                game_mario_en[3] = 7
                            game_mario_en[2] += game_mario_en[3]

                            if(game_mario_map[(game_mario_en[2]+8)//8][game_mario_en[1]//8] in game_mario_gr or game_mario_map[(game_mario_en[2]+8)//8][(game_mario_en[1]+7)//8] in game_mario_gr):
                                game_mario_en[2]= game_mario_en[2]//8*8
                                game_mario_en[3] = 0

                            if(game_mario_en[1]-8 < game_mario_pl[0] and game_mario_en[1]+8 > game_mario_pl[0]):
                                if(game_mario_en[2]-8 < game_mario_pl[1] and game_mario_en[2]+8 > game_mario_pl[1]):
                                    if(game_mario_pl[2] > 0):
                                        game_mario_pl[2] = -6
                                        game_mario_en[6] = 1
                                        game_entity5_sprite[0] = 26
                                        game_mario_en[5] = 0
                                        game_mario_score = 1
                                        game_mario_score_t = 0
                                        game_entity3_sprite[0] = 30
                                        game_entity3_sprite.x = game_mario_en[1]+24-game_mario_cam_x
                                        game_entity3_sprite.y = game_mario_en[2]+48
                                        game_mario_score_real += 500


                                    else:
                                        if(game_mario_pl_m2 == 0):
                                            if(game_mario_pl_m == 1):
                                                game_mario_pl_m = 0
                                                game_mario_pl_m2 = 1 
                                                game_mario_pl_m_ani = 0
                                            else:
                                                game_mario_m = 2
                        else:
                            game_mario_en[5] += 1
                            if(game_mario_en[5] == 8):game_mario_en[0] = 0

                    if(game_mario_pl_m2):
                        game_mario_pl_m_ani += 1
                        if(game_mario_pl_m_ani == 8):
                            game_mario_pl_m2 = 0

                    if(game_mario_pl[0]-32 > game_mario_cam_x):
                        game_mario_cam_x = game_mario_pl[0]-32
                    if(game_mario_pl[0]-16 < game_mario_cam_x):
                        game_mario_cam_x = game_mario_pl[0]-16
                    if(game_mario_cam_x//8+11 > len(game_mario_map[0])):
                        game_mario_cam_x = (len(game_mario_map[0])-10)*8
                    if(game_mario_cam_x//8 < 0):
                        game_mario_cam_x = 0
                    if(game_mario_pl_stat == 0):
                        game_mario_pl_ani_m = 0
                    if(game_mario_pl_stat == 2):
                        game_mario_pl_ani_m = 2
                    if(game_mario_pl_stat == 1):
                        game_mario_pl_ani+=1
                        if(game_mario_pl_ani == 4):
                            game_mario_pl_ani = 0
                        if(game_mario_pl_ani < 2):
                            game_mario_pl_ani_m = 1
                        else:
                            game_mario_pl_ani_m = 0
                    else:
                        game_mario_pl_ani = 0
                    
                    if(game_mario_score_real != game_mario_score_real_his):
                        for i in range(len(str(game_mario_score_real))):
                            text_sprite[40-len(str(game_mario_score_real))+i] = text_to_sprite(str(game_mario_score_real)[i])

                    if(game_mario_pl_ani_m_his != game_mario_pl_ani_m or game_mario_pl_m2):
                        if((game_mario_pl_m == 0 and game_mario_pl_m2 == 0) or (game_mario_pl_m == 1 and game_mario_pl_m2 and game_mario_pl_m_ani%2 < 1) or (game_mario_pl_m == 0 and game_mario_pl_m2 and game_mario_pl_m_ani%2 >= 1)):
                            game_mario_pl_m_ani_r = 0
                            if(game_mario_pl_ani_m == 0):
                                game_entity1_sprite[0] = 23
                                game_entity1_sprite[1] = 23
                                game_entity1_sprite[2] = 23
                                game_entity1_sprite[3] = 23
                                game_entity1_sprite[4] = 16
                                game_entity1_sprite[5] = 23
                            elif(game_mario_pl_ani_m == 1):
                                game_entity1_sprite[0] = 23
                                game_entity1_sprite[1] = 23
                                game_entity1_sprite[2] = 23
                                game_entity1_sprite[3] = 23
                                game_entity1_sprite[4] = 17
                                game_entity1_sprite[5] = 23
                            elif(game_mario_pl_ani_m == 2):
                                game_entity1_sprite[0] = 23
                                game_entity1_sprite[1] = 23
                                game_entity1_sprite[2] = 23
                                game_entity1_sprite[3] = 23
                                game_entity1_sprite[4] = 18
                                game_entity1_sprite[5] = 23
                        elif((game_mario_pl_m == 1 and game_mario_pl_m2 == 0)  or (game_mario_pl_m == 0 and game_mario_pl_m2 and game_mario_pl_m_ani%2 < 1) or (game_mario_pl_m ==1 and game_mario_pl_m2 and game_mario_pl_m_ani%2 >= 1)):
                            game_mario_pl_m_ani_r = 1
                            if(game_mario_pl_ani_m == 0):
                                game_entity1_sprite[0] = 23
                                game_entity1_sprite[1] = 23
                                game_entity1_sprite[2] = 0
                                game_entity1_sprite[3] = 23
                                game_entity1_sprite[4] = 8
                                game_entity1_sprite[5] = 23
                            elif(game_mario_pl_ani_m == 1):
                                game_entity1_sprite[0] = 23
                                game_entity1_sprite[1] = 23
                                game_entity1_sprite[2] = 1
                                game_entity1_sprite[3] = 23
                                game_entity1_sprite[4] = 9
                                game_entity1_sprite[5] = 23
                            elif(game_mario_pl_ani_m == 2):
                                game_entity1_sprite[0] = 23
                                game_entity1_sprite[1] = 23
                                game_entity1_sprite[2] = 2
                                game_entity1_sprite[3] = 23
                                game_entity1_sprite[4] = 10
                                game_entity1_sprite[5] = 23
                    if(game_entity1_sprite.flip_x):
                        game_entity1_sprite.x = game_mario_pl[0]+24-game_mario_cam_x-8
                    else:
                        game_entity1_sprite.x = game_mario_pl[0]+24-game_mario_cam_x
                    if(game_mario_pl[1] < -16+game_mario_pl_m_ani_r*8):
                        game_entity1_sprite.x = -128
                    game_entity1_sprite.y = game_mario_pl[1]+48-16

                    game_back_sprite.x = 24-game_mario_cam_x%8

                    game_entity4_sprite.x = -128
                    if(game_mario_powerup[0] and game_mario_powerup[1] >= game_mario_cam_x-8 and game_mario_powerup[1] <=game_mario_cam_x+8*10):
                        game_entity4_sprite.x = game_mario_powerup[1]+24-game_mario_cam_x
                        game_entity4_sprite.y = game_mario_powerup[2]+48
                    game_entity5_sprite.x = -128
                    if(game_mario_en[0] and game_mario_en[1] >= game_mario_cam_x-8 and game_mario_en[1] <=game_mario_cam_x+8*10):
                        game_entity5_sprite.x = game_mario_en[1]+24-game_mario_cam_x
                        game_entity5_sprite.y = game_mario_en[2]+48


                    if(game_mario_cam_x_his//8 != game_mario_cam_x//8 or game_mario_map_rf):
                        game_mario_map_rf = 0
                        for i in range(6):
                            for j in range(11-(game_mario_cam_x//8+10 == len(game_mario_map[0]))*1):
                                if(game_mario_map[i][game_mario_cam_x//8+j] == 0):
                                    game_back_sprite[11+i*11+j] = 23
                                elif(game_mario_map[i][game_mario_cam_x//8+j] == 1):
                                    game_back_sprite[11+i*11+j] = 7
                                elif(game_mario_map[i][game_mario_cam_x//8+j] == 2):
                                    game_back_sprite[11+i*11+j] = 15
                                elif(game_mario_map[i][game_mario_cam_x//8+j] == 3):
                                    game_back_sprite[11+i*11+j] = 14
                                elif(game_mario_map[i][game_mario_cam_x//8+j] == 4):
                                    game_back_sprite[11+i*11+j] = 13
                                elif(game_mario_map[i][game_mario_cam_x//8+j] == 5):
                                    game_back_sprite[11+i*11+j] = 20
                                elif(game_mario_map[i][game_mario_cam_x//8+j] == 6):
                                    game_back_sprite[11+i*11+j] = 14
                                elif(game_mario_map[i][game_mario_cam_x//8+j] == 8):
                                    game_back_sprite[11+i*11+j] = 19
                                elif(game_mario_map[i][game_mario_cam_x//8+j] == 9):
                                    game_back_sprite[11+i*11+j] = 22
                                elif(game_mario_map[i][game_mario_cam_x//8+j] == 10):
                                    game_back_sprite[11+i*11+j] = 21
                                elif(game_mario_map[i][game_mario_cam_x//8+j] == 7):
                                    game_entity5_sprite[0] = 25#enemy
                                    game_mario_map[i][game_mario_cam_x//8+j] = 0
                                    game_mario_en[0] =1
                                    game_mario_en[1] =(game_mario_cam_x//8+j)*8
                                    game_mario_en[2] =i*8
                                    game_mario_en[3] = 0
                                    game_mario_en[4] = 1
                                    game_mario_en[5] = 0
                                    game_mario_en[6] = 0

                if(game_mario_m == 2):
                    game_entity1_sprite[0] = 23
                    game_entity1_sprite[1] = 23
                    game_entity1_sprite[2] = 23
                    game_entity1_sprite[3] = 23
                    game_entity1_sprite[4] = 18
                    game_entity1_sprite[5] = 23

                    game_mario_pl_ani = 0
                    game_mario_m = 3
                if(game_mario_m == 3):
                    game_mario_pl_ani += 1
                    if(game_mario_pl_ani == 10):
                        game_mario_pl[2] = -6
                        game_mario_m = 4
                if(game_mario_m == 4):
                    game_mario_pl[2] += 1
                    if(game_mario_pl[2] > 7):
                        game_mario_pl[2] = 7
                    game_entity1_sprite.y += game_mario_pl[2]
                    if(game_entity1_sprite.y > 72):
                        game_entity1_sprite.x = -128
                        game_mario_m = 5
                        game_mario_pl_ani = 0
                if(game_mario_m == 5):
                    game_mario_pl_ani += 1
                    if(game_mario_pl_ani == 10):
                        for i in range(14):
                            text_sprite[28+i] = 47
                        game_mario_m = 0
                if(game_mario_m == 6):
                    game_mario_pl_ani = 0
                    game_mario_m = 7
                    game_entity1_sprite.x = game_entity1_sprite.x//8*8
                if(game_mario_m == 7):
                    game_mario_pl_ani += 1
                    if(game_mario_pl_ani == 10):
                        game_entity1_sprite.flip_x = True
                        game_entity1_sprite.x += 8
                        game_mario_m = 8
                        game_mario_pl_ani = 0
                if(game_mario_m == 8):
                    game_entity1_sprite.y += 1
                    if(game_entity1_sprite.y >= 64):
                        game_entity1_sprite.y = 64
                        game_mario_pl_ani+=1
                        if(game_mario_pl_ani == 10):
                            game_mario_m = 9
                            for i in range(7*11):
                                game_back_sprite[i] = 23
                            game_entity5_sprite.flip_x = False
                            game_entity1_sprite.flip_x = False
                            game_back_sprite.x = 24
                            game_entity4_sprite.x = -128
                            game_entity3_sprite.x = -128
                            game_entity1_sprite.x = -128
                            for i in range(14):
                                text_sprite[28+i] = 47
                            for i in range(len("score:"+str(game_mario_score_real))):
                                text_sprite[44+i+(game_mario_score_real==0)*1] = text_to_sprite(("score:"+str(game_mario_score_real))[i])
                            for i in range(10):
                                text_sprite[58+i] = text_to_sprite("clear game"[i])
                                
                            text_sprite[58+4] =52
                            text_sprite[58+7] = 53
                            text_sprite[58+8] = 54


                if(game_mario_m == 9):
                    if(up_once):
                        up_once = 0
                        game_clear[2] = 1
                        for i in range(28):
                            text_sprite[44+i] = 47
                        game_scene = 0

            if(game_scene == 3):
                if(game_gala_m == 0):
                    if(keys[pygame.K_LEFT]):
                        game_gala_pl_x -= 2
                        if(game_gala_pl_x < 24):
                            game_gala_pl_x =24
                    if(keys[pygame.K_RIGHT]):
                        game_gala_pl_x += 2
                        if(game_gala_pl_x > 88):
                            game_gala_pl_x =88
                    game_gala_time += 1
                    if(game_gala_time == 20):
                        game_gala_time = 0
                    if(game_gala_en_time != 0):game_gala_en_time -= 1
                    if(game_gala_en_time == 0):
                        game_gala_en_time = game_gala_cooltime
                        if(random.randrange(0,4) == 0):
                            game_gala_en.insert(0,0)
                        else:
                            game_gala_en.insert(0,1)
                        if(game_gala_en.pop()):
                            game_gala_m = 1
                            for i in range(40):
                                game_back_sprite[10+i+i//10+1] = 23
                            game_entity1_sprite.x = -128
                            game_entity3_sprite.x = -128
                            game_entity4_sprite.x = -128
                            for i in range(10):
                                text_sprite[30+i] = 47
                            for i in range(len("score:"+str(game_gala_score))):
                                text_sprite[44+i+(len(str(game_gala_score))<3)*1] = text_to_sprite(("score:"+str(game_gala_score))[i])
                            for i in range(10):
                                text_sprite[58+i] = text_to_sprite("alien win."[i])
                                
                            text_sprite[58] = 48
                            text_sprite[58+8] = 49
                            
                    if(game_gala_bullet):
                        game_entity3_sprite.y -= 4
                        if(game_entity3_sprite.y >= 48):
                            if((game_entity3_sprite.y - 48)//8)%2 == 0:
                                dum = (game_entity3_sprite.x - 24)//8+(game_entity3_sprite.y - 48)//8*10
                            else:
                                dum = 9-(game_entity3_sprite.x - 24)//8+(game_entity3_sprite.y - 48)//8*10
                            if game_gala_en[dum]:
                                game_gala_en[dum] = 0
                                game_gala_ef = 1
                                game_entity4_sprite.x = game_entity3_sprite.x//8*8
                                game_entity4_sprite.y = game_entity3_sprite.y//8*8
                                game_gala_ef_ani = 0
                                game_gala_score += 1
                                if(game_gala_score%10 == 0):
                                    game_gala_cooltime -= 1
                                    if(game_gala_cooltime == 0):
                                        game_gala_cooltime =1
                                game_gala_bullet = 0
                                game_entity3_sprite.x = -128
                        if(game_entity3_sprite.y < 48):
                            game_gala_bullet = 0
                            game_entity3_sprite.x = -128
                    if(game_gala_ef):
                        game_gala_ef_ani += 1
                        if(game_gala_ef_ani == 3):
                            game_gala_ef = 0
                            game_entity4_sprite.x = -128
                        game_entity4_sprite[0] = 45+game_gala_ef_ani
                    else:
                        game_gala_ef_ani = 0
                if(up_once):
                    up_once = 0
                    if(game_gala_m == 0):
                        if(game_gala_bullet == 0):
                            game_gala_bullet =1
                            game_entity3_sprite.x = game_gala_pl_x+7
                            game_entity3_sprite.y = 72+4
                    elif(game_gala_m == 1):
                        if(game_gala_score >= 80):
                            game_clear[0] = 1
                        for i in range(28):
                            text_sprite[44+i] = 47
                        game_scene = 0
                if(game_gala_m == 0):
                    game_entity1_sprite.x =game_gala_pl_x
                    for i in range(len("score:"+str(game_gala_score))):
                        text_sprite[30+i] = text_to_sprite(("score:"+str(game_gala_score))[i])
                    for i in range(40):
                        game_back_sprite[10+i+i//10+1] = 23
                        if((i//10) % 2 == 0):
                            if game_gala_en[i]:
                                game_back_sprite[10+i+i//10+1] = 37+(game_gala_time<10)
                        else:
                            if game_gala_en[i//10*10+9-i%10]:
                                game_back_sprite[10+i+i//10+1] = 37+(game_gala_time<10)
            if(game_scene == 2):
                if(game_pong_m == 0 and game_pong_ball_sp != 0):
                    game_pong_ball_g = 0
                    game_pong_ball = [60,56]
                    game_pong_ball_sp = 0
                    game_pong_pl_y = 48
                    game_pong_en_y = 48
                    game_pong_pl_ani = 0
                    game_pong_en_ani = 0
                if(game_pong_m == 1):
                    if(game_pong_pl_ani != 0): 
                        game_pong_pl_ani -= 1
                        if(game_pong_pl_ani == 0):
                            game_entity1_sprite[0] = 23
                            game_entity1_sprite[1] = 34
                            game_entity1_sprite[2] = 23
                            game_entity1_sprite[3] = 42
                            game_entity1_sprite[4] = 23
                            game_entity1_sprite[5] = 50
                    if(game_pong_en_ani != 0): 
                        game_pong_en_ani -= 1
                        if(game_pong_en_ani == 0):
                            game_entity2_sprite[0] = 23
                            game_entity2_sprite[1] = 34
                            game_entity2_sprite[2] = 23
                            game_entity2_sprite[3] = 42
                            game_entity2_sprite[4] = 23
                            game_entity2_sprite[5] = 50

                    game_pong_ball_g += 1
                    game_pong_ball[1]+=game_pong_ball_g
                    if(game_pong_ball[1] >= 80):
                        game_pong_ball[1] = 80
                        game_pong_ball_g += 1
                        game_pong_ball_g *= -1
                        if(game_pong_ball_g < -9):game_pong_ball_g = -9
                    game_pong_ball[0]+=game_pong_ball_sp
                    if(game_pong_ball[0] >= 56 and game_pong_ball[0] <= 64 and game_pong_ball[1] > 72):
                        if(game_pong_ball_sp > 0):
                            game_pong_score[1] += 1
                        else:
                            game_pong_score[0] += 1
                        game_pong_m = 2
                    if(game_pong_ball[0] <= 32):
                        if(game_pong_ball[1] > game_pong_en_y-8 and game_pong_ball[1] < game_pong_en_y+16):
                            game_pong_ball[0] = 32
                            game_pong_ball_sp = 2
                    if(game_pong_ball[0] >= 88):
                        if(game_pong_ball[1] > game_pong_pl_y-8 and game_pong_ball[1] < game_pong_pl_y+16):
                            game_pong_ball[0] = 88
                            game_pong_ball_sp = -2
                    if(game_pong_ball[0] <= 24):
                        game_pong_ball[0] = 24
                        game_pong_score[1] += 1
                        game_pong_m = 2
                    if(game_pong_ball[0] >= 96):
                        game_pong_ball[0] = 96
                        game_pong_score[0] += 1
                        game_pong_m = 2

                    if(game_pong_ball[1] <= game_pong_en_y-8):
                        game_pong_en_y -= 1
                        if(game_pong_en_y < 48):
                            game_pong_en_y =48
                    if(game_pong_ball[1] >= game_pong_en_y+16):
                        game_pong_en_y += 1
                        if(game_pong_en_y > 64):
                            game_pong_en_y =64

                    if(game_pong_ball[0] < 40):
                        if(game_pong_ball[1] > game_pong_en_y-8 and game_pong_ball[1] < game_pong_en_y+16):
                            if(game_pong_ball_ai[0] == 0):
                                game_pong_ball_ai[0] = 1
                                game_pong_ball_ai[1] = game_pong_ball[0]
                                game_pong_ball_ai[2] = game_pong_ball[1]
                                game_pong_ball_ai[3] = game_pong_ball_g
                                game_pong_ball_ai[4] = 0
                                game_pong_ball_ai[5] = 0
                                game_pong_ball_ai[6] = 0
                                for i in range(30):
                                    if(game_pong_ball_ai[5] == 0):
                                        game_pong_ball_ai[1] += game_pong_ball_sp
                                    else:
                                        game_pong_ball_ai[1] += 2
                                    game_pong_ball_ai[3] += 1
                                    game_pong_ball_ai[2]+=game_pong_ball_ai[3]
                                    if(game_pong_ball_ai[2] >= 80):
                                        game_pong_ball_ai[2] = 80
                                        game_pong_ball_ai[3] += 1
                                        game_pong_ball_ai[3] *= -1
                                        if(game_pong_ball_ai[3] < -9):game_pong_ball_ai[3] = -9
                                    if(game_pong_ball_ai[1] <= 32):
                                        game_pong_ball_ai[1] = 32
                                        game_pong_ball_ai[5] = 1
                                        
                                    if(game_pong_ball_ai[1] >= 56 and game_pong_ball_ai[1] <= 64 and game_pong_ball_ai[2] > 72):
                                        game_pong_ball_ai[6] = 1
                                        
                            if(game_pong_ball_ai[0] == 1):
                                game_pong_ball_ai[0] = 3
                                game_pong_ball_ai[1] = 40
                                game_pong_ball_ai[2] = game_pong_ball[1]-game_pong_ball_g+6
                                game_pong_ball_ai[3] = 6
                                game_pong_ball_ai[4] = 0
                                for i in range(10):
                                    game_pong_ball_ai[1] += 5
                                    game_pong_ball_ai[3] += 1
                                    game_pong_ball_ai[2]+=game_pong_ball_ai[3]
                                    if(game_pong_ball_ai[2] >= 80):
                                        game_pong_ball_ai[2] = 80
                                        game_pong_ball_ai[3] += 1
                                        game_pong_ball_ai[3] *= -1
                                        if(game_pong_ball_ai[3] < -9):game_pong_ball_ai[3] = -9
                                    if(game_pong_ball_ai[1] >= 56 and game_pong_ball_ai[1] <= 64 and game_pong_ball_ai[2] > 72):
                                        game_pong_ball_ai[4] = 1
                                    if(game_pong_ball_ai[4] == 0 and game_pong_ball_ai[1] >= 88):
                                        if(game_pong_ball_ai[2] > game_pong_pl_y-8 and game_pong_ball_ai[2] < game_pong_pl_y+16):
                                            if(game_pong_ball_ai[6] == 0):
                                                game_pong_ball_ai[4] = 2
                                if(game_pong_ball_ai[4] == 0):
                                    game_pong_en_ani = 2
                                    game_entity2_sprite[0] = 32
                                    game_entity2_sprite[1] = 33
                                    game_entity2_sprite[2] = 40
                                    game_entity2_sprite[3] = 41
                                    game_entity2_sprite[4] = 48
                                    game_entity2_sprite[5] = 49
                                    game_pong_ball[0] = 40
                                    game_pong_ball_sp = +random.randrange(4,7)
                                    game_pong_ball[1]+=-game_pong_ball_g+6
                                    game_pong_ball_g = 6

                    else:
                        game_pong_ball_ai[0] = 0
                    if(game_pong_ball_ai[0] > 1):
                        game_pong_ball_ai[0] -= 1

                    if(keys[pygame.K_LEFT]):
                        game_pong_pl_y -= 2
                        if(game_pong_pl_y < 48):
                            game_pong_pl_y =48
                    if(keys[pygame.K_RIGHT]):
                        game_pong_pl_y += 2
                        if(game_pong_pl_y > 64):
                            game_pong_pl_y =64
                if(game_pong_m == 2):
                    if(game_pong_score[0] == 3 or game_pong_score[1] == 3):
                        if(game_pong_score[1] == 3):
                            game_clear[1] = 1
                            
                            for i in range(8):
                                text_sprite[45+i] = text_to_sprite("you win!"[i])
                        else:
                            for i in range(8):
                                text_sprite[45+i] = text_to_sprite("you lose"[i])
                        game_entity1_sprite.x = -128
                        game_entity2_sprite.x = -128
                        game_entity3_sprite.x = -128
                        for i in range(7*11):
                            game_back_sprite[i] = 23
                        game_pong_m = 3
                        text_sprite[30] = 47
                        text_sprite[39] = 47
                        game_entity2_sprite.flip_x = False
                        for i in range(10):
                            text_sprite[58+i] = text_to_sprite("try again?"[i])
                        text_sprite[58+4] = 50
                        text_sprite[58+5] = 51
                    else:
                        game_pong_m = 0
                        text_sprite[30] = 33+game_pong_score[0]
                        text_sprite[39] = 33+game_pong_score[1]
                if(game_pong_m == 3):
                    pass
                if(up_once):
                    up_once = 0
                    if(game_pong_m == 0):
                        game_pong_m = 1
                        game_pong_ball_sp = -2
                        if(game_pong_score[0]+game_pong_score[1])%2 == 1:
                            game_pong_ball_sp = 2
                    elif(game_pong_m == 1):
                        game_pong_pl_ani = 2
                        game_entity1_sprite[0] = 32
                        game_entity1_sprite[1] = 33
                        game_entity1_sprite[2] = 40
                        game_entity1_sprite[3] = 41
                        game_entity1_sprite[4] = 48
                        game_entity1_sprite[5] = 49
                        if(game_pong_ball[0] >= 80):
                            if(game_pong_ball[1] > game_pong_pl_y-8 and game_pong_ball[1] < game_pong_pl_y+16):
                                game_pong_ball[0] = 80
                                game_pong_ball_sp = -random.randrange(4,7)
                                game_pong_ball[1]+=-game_pong_ball_g+6
                                game_pong_ball_g = 6
                    else:
                        for i in range(28):
                            text_sprite[44+i] = 47
                        game_scene = 0


                if(game_pong_m != 3):
                    game_entity1_sprite.y = game_pong_pl_y
                    game_entity2_sprite.y = game_pong_en_y
                    game_entity3_sprite.x = game_pong_ball[0]
                    game_entity3_sprite.y = game_pong_ball[1]
            if(not game):
                for i in range(2*14,7*14):
                    text_sprite[i] = 47
                box2_sprite.x = -128
                box3_sprite.x = -128
                box4_sprite.x = -128
                box5_sprite.x = -128
                box5_sprite2.x =-128
                box6_sprite.x = -128
                box6_sprite2.x =-128


                talk = 1
                talk_m = 78
                talk_text_index = -1
                continue
                
        break

    time.sleep(0.1)