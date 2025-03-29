import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
import pygame
import time
from random import randint
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import label

pygame.init()
display = PyGameDisplay(width=128, height=128)
screen = displayio.Group()
display.show(screen)

background_bitmap = displayio.OnDiskBitmap("background.bmp")
background = displayio.TileGrid(background_bitmap, pixel_shader=background_bitmap.pixel_shader)
screen.append(background)

edgeA_group = displayio.Group()
edgeB_group = displayio.Group()
edgeC_group = displayio.Group()
floating_edgeA_group = displayio.Group()
floating_edgeB_group = displayio.Group()
floating_edgeC_group = displayio.Group()
edge_group = displayio.Group()
edge_group.append(edgeA_group)
edge_group.append(edgeB_group)
edge_group.append(edgeC_group)
edge_group.append(floating_edgeA_group)
edge_group.append(floating_edgeB_group)
edge_group.append(floating_edgeC_group)
screen.append(edge_group)

pet_bitmap = displayio.OnDiskBitmap("pet.bmp")
pet_frames = 6 # the total amount of frames in the pet bitmap
pet_palette = displayio.Palette(8)
pet_palette.make_transparent(0)
pet_palette[7] = 0xFE6C90
pet_palette[6] = 0xE74D91
pet_palette[5] = 0x80307A
pet_palette[4] = 0xD03791
pet_palette[3] = 0xAA2F7E
pet_palette[2] = 0x942C75
pet_palette[1] = 0x532C6B

pet = displayio.TileGrid(
    pet_bitmap,
    pixel_shader = pet_palette,
    width = 1,
    height = 1,
    tile_width = 32,
    tile_height = 32,
    default_tile = 0,
    x = 48,
    y = 48,
)
screen.append(pet)

restart_bitmap = displayio.OnDiskBitmap("restart.bmp")
restart_palette = displayio.Palette(2)
restart_palette.make_transparent(0)
restart_palette[1] = 0x000000
restart = displayio.TileGrid(
    restart_bitmap,
    pixel_shader = restart_palette,
    width = 1,
    height = 1,
    x = 48,
    y = 48,
)
screen.append(restart)

edgeA_bitmap = displayio.OnDiskBitmap("edgeA.bmp")
def edgeA(x, y, color):
    palette = displayio.Palette(2)
    palette.make_transparent(0)
    palette[1] = color
    return displayio.TileGrid(edgeA_bitmap, pixel_shader = palette, x = x, y = y)

edgeB_bitmap = displayio.OnDiskBitmap("edgeB.bmp")
def edgeB(x, y, color):
    palette = displayio.Palette(2)
    palette.make_transparent(0)
    palette[1] = color
    return displayio.TileGrid(edgeB_bitmap, pixel_shader = palette, x = x, y = y)


edgeC_bitmap = displayio.OnDiskBitmap("edgeC.bmp")
def edgeC(x, y, color):
    palette = displayio.Palette(2)
    palette.make_transparent(1)
    palette[0] = color
    return displayio.TileGrid(edgeC_bitmap, pixel_shader = palette, x = x, y = y)

def rotate_left_dict(x, y):
    if x < 48:
        return (48, ((((43 - x) // 6) * 8) + 75))
    elif x > 48:
        return (108 - x, y)
    elif x == 48:
        return ((65 + (((y - 75) // 8) * 6)), (43 - (((y - 75) // 8) * 6)))

def rotate_right_dict(x, y):
    if x < 48:
        return (108 - x, y)
    elif x > 48:
        return (48, ((((x - 65) // 6) * 8) + 75))
    elif x == 48:
        return ((43 - (((y - 75) // 8) * 6)), (43 - (((y - 75) // 8) * 6)))

def rotate_edges_left(edge_group: displayio.Group):
    edge_group_0 = edge_group[0]
    edge_group_1 = edge_group[1]
    edge_group_2 = edge_group[2]

    for i in range(0, len(edge_group_0)):
        temp = edge_group_0.pop(0)
        (x, y) = rotate_left_dict(temp.x, temp.y)
        edge_group_0.append(edgeC(x, y, temp.pixel_shader[1]))

    for i in range(0, len(edge_group_1)):
        temp = edge_group_1.pop(0)
        (x, y) = rotate_left_dict(temp.x, temp.y)
        edge_group_1.append(edgeA(x, y, temp.pixel_shader[1]))

    for i in range(0, len(edge_group_2)):
        temp = edge_group_2.pop(0)
        (x, y) = rotate_left_dict(temp.x, temp.y)
        edge_group_2.append(edgeB(x, y, temp.pixel_shader[0]))

    edge_group[0] = edge_group_1
    edge_group[1] = edge_group_2
    edge_group[2] = edge_group_0

def rotate_edges_right(edge_group: displayio.Group):
    edge_group_0 = edge_group[0]
    edge_group_1 = edge_group[1]
    edge_group_2 = edge_group[2]

    for i in range(0, len(edge_group_0)):
        temp = edge_group_0.pop(0)
        (x, y) = rotate_right_dict(temp.x, temp.y)
        edge_group_0.append(edgeB(x, y, temp.pixel_shader[1]))

    for i in range(0, len(edge_group_1)):
        temp = edge_group_1.pop(0)
        (x, y) = rotate_right_dict(temp.x, temp.y)
        edge_group_1.append(edgeC(x, y, temp.pixel_shader[1]))

    for i in range(0, len(edge_group_2)):
        temp = edge_group_2.pop(0)
        (x, y) = rotate_right_dict(temp.x, temp.y)
        edge_group_2.append(edgeA(x, y, temp.pixel_shader[0]))

    edge_group[0] = edge_group_2
    edge_group[1] = edge_group_0
    edge_group[2] = edge_group_1

edge_colors = [0x29ADFF, 0XFFA300, 0XFF77A8]

global pet_frame
pet_frame = 0
game_over = False
rotate_left = False
rotate_right = False
cooldown = 0
speed = 2 # number of pixels edges move per tick
rate = 4 # rate of edges spawned (per 100 ticks)
ticks = 0 # counter for ticks since last spawn
edges_sent = 0 # number of edges sent since last speed-up
global score
score = 0 # number of pairs of edges cleared
score_label = label.Label(bitmap_font.load_font("Munro.bdf"), x = 44, y = 4, text = f"score: 0", color = 0x000000)
screen.append(score_label)

def process_collision(edge_group):
    # floating_edgeA_group
    if edge_group[3].__len__() > 0:
        len = edge_group[0].__len__()
        edge = edge_group[3][0]
        if edge.x >= (43 - (6 * len)) and edge.y >= (43 - (6 * len)):
            edge_group[3][0].x = (43 - (6 * len))
            edge_group[3][0].y = (43 - (6 * len))
            edge_group[0].append(edge_group[3].pop(0))
    # floating_edgeB_group
    if edge_group[4].__len__() > 0:
        len = edge_group[1].__len__()
        edge = edge_group[4][0]
        if edge.x <= (65 + (6 * len)) and edge.y >= (43 - (6 * len)):
            edge_group[4][0].x = (65 + (6 * len))
            edge_group[4][0].y = (43 - (6 * len))
            edge_group[1].append(edge_group[4].pop(0))
    # floating_edgeC_group
    if edge_group[5].__len__() > 0:
        len = edge_group[2].__len__()
        edge = edge_group[5][0]
        if  edge.y <= (75 + (8 * len)):
            edge_group[5][0].y = (75 + (8 * len))
            edge_group[2].append(edge_group[5].pop(0))

def process_clears(edge_group, score, score_label):
    for i in range(0, 3):
        for j in range(0, edge_group[i].__len__() - 1):
            if edge_group[i][j].pixel_shader[1] == edge_group[i][j + 1].pixel_shader[1] and edge_group[i][j].pixel_shader[0] == edge_group[i][j + 1].pixel_shader[0]:
                score += 1
                edge_group[i].pop(j)
                edge_group[i].pop(j)
                score_label.text = f"score: {score}"
                if edge_group[0].__len__() == 0 and edge_group[1].__len__() == 0 and edge_group[2].__len__() == 0:
                    score += 2
                    score_label.text = f"score: {score}\n all clear!\n     +3"
    return score
            
def process_game_over(edge_group):
    output = False
    for i in range(0, 3):
        if edge_group[i].__len__() >= 7:
            output = True
    return output

def play():
    pet_frame = 0
    pet.hidden = False
    restart_palette.make_transparent(1)
    game_over = False
    rotate_left = False
    rotate_right = False
    cooldown = 0
    speed = 2 # number of pixels edges move per tick
    rate = 4 # rate of edges spawned (per 100 ticks)
    ticks = 0 # counter for ticks since last spawn
    edges_sent = 0 # number of edges sent since last speed-up
    score = 0 # number of pairs of edges cleared
    score_label.x = 44
    score_label.text = f"score: {score}"


    for i in range(6):
        for j in range(edge_group[i].__len__()):
            edge_group[i].pop(0)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        keys = pygame.key.get_pressed()

        for edge in floating_edgeA_group:
            edge.x += speed
            edge.y += speed
        for edge in floating_edgeB_group:
            edge.x -= speed
            edge.y += speed
        for edge in floating_edgeC_group:
            edge.y -= speed    

        process_collision(edge_group)
        score = process_clears(edge_group, score, score_label)
        game_over = process_game_over(edge_group)
        if game_over: break

        if ticks == (100 // rate):
            ticks = 0
            edges_sent += 1
            i = randint(3, 5)
            color = edge_colors[randint(0, 2)]
            if i == 3: 
                edge = edgeA(3, 3, color)
            if i == 4:
                edge = edgeB(105, 3, color)
            if i == 5:
                edge = edgeC(48, 115, color)
            edge_group[i].append(edge)

        if edges_sent == int(10 + rate):
            score_label.text = f"score: {score}\nspeed up!"
            edges_sent = 0
            rate += 1

        if game_over == False:
            if keys[pygame.K_LEFT] and cooldown == 0:
                rotate_edges_left(edge_group)
                rotate_left = True
                rotate_right = False
                pet_frame -= 1
                cooldown = 3
                if pet_frame == -1:
                    pet_frame = pet_frames - 1
            if keys[pygame.K_RIGHT] and cooldown == 0:
                rotate_edges_right(edge_group)
                rotate_right = True
                rotate_left = False
                pet_frame += 1
                cooldown = 3
                if pet_frame == pet_frames:
                    pet_frame = 0

        if cooldown > 0:
            cooldown -= 1

        if rotate_left == True and not (pet_frame % pet_frames) == 0:
            pet_frame -= 1
        if rotate_right == True and not (pet_frame % pet_frames) == 0:
            pet_frame += 1
        if (pet_frame % pet_frames) == 0:
            rotate_left = False
            rotate_right = False

        if pet_frame == pet_frames:
            pet_frame = 0
        if pet_frame == -1:
            pet_frame = pet_frames - 1
        pet[0] = pet_frame

        ticks += 1
        time.sleep(0.1)
    return score

score = play()
score_label.x = 40
score_label.text = f"game over!\n    score:\n      {score}"
restart_palette.make_opaque(1)
pet.hidden = True
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    if pygame.key.get_pressed()[pygame.K_UP]:
        score = play()
        score_label.x = 40
        score_label.text = f"game over!\n    score:\n      {score}"