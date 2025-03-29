import os
import json

with open("data.json", "r") as f:
    data = json.load(f)
    timings = data.get("timings", None)
    colors = data.get("colors", None)
    print(colors)
files = os.listdir("Pet") + os.listdir("Extras") + os.listdir("Backdrops")
pngs = [file for file in files if file.endswith(".png")]
bmps = [file for file in files if file.endswith(".bmp")]
if pngs.sort() != bmps.sort() or None in [timings, colors]:
    print("Please run setup.py before you run this one. This program will not work without the necessary setup. Also run setup.py if you have changed any sprites in the Extras folder")

screen_width = 128
base_obj_speed = 50
pet_speed = 10
base_happy_increase = 20
base_hunger_increase = 20
base_exercise_increase = 20

os.environ["TIMINGS"] = json.dumps(timings)
os.environ["SCREEN_WIDTH"] = json.dumps(screen_width)
os.environ["BASE_OBJ_SPEED"] = json.dumps(base_obj_speed)
os.environ["BASE_HAPPY_INCREASE"] = json.dumps(base_happy_increase)
os.environ["BASE_HUNGER_INCREASE"] = json.dumps(base_hunger_increase)
os.environ["BASE_EXERCISE_INCREASE"] = json.dumps(base_exercise_increase)

import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
import time
from Classes.pet_class import Pet
#from Classes.game_class import Game
from misc import convert_all
import pygame
from PIL import Image

pygame.init()
convert_all()

def find_place(st, key, plc):
    last = -1
    if 0 > plc >= -st.count(key):
        plc = st.count(key) + plc
    if 0 <= plc < st.count(key):
        for _ in range(0, st.count(key)):
            last = st.find(key, last + 1) + len(key)
            plc -= 1
            if plc == -1:
                break
    return last

def find_color_index(palette, target_color):
    target_color = (target_color[0] << 16) | (target_color[1] << 8) | target_color[2]
    for index in range(len(palette)):
        if palette[index] == target_color:
            return index
    return -1

def load_bmp(file_path):
    img = Image.open(file_path)
    img = img.convert("RGB")  # Ensure the image is in RGB mode
    pixels = img.getdata()

    # Extract unique colors and maintain their order
    unique_colors = []
    color_to_index = {}
    for color in pixels:
        if color not in color_to_index:
            color_to_index[color] = len(unique_colors)
            unique_colors.append(color)

    # Create a palette and assign the unique colors
    palette = displayio.Palette(len(unique_colors))
    for index, color in enumerate(unique_colors):
        palette[index] = (color[0] << 16) | (color[1] << 8) | color[2]  # Convert RGB to 24-bit color

    # Create a bitmap and assign the indices
    bitmap = displayio.Bitmap(img.width, img.height, len(unique_colors))
    for y in range(img.height):
        for x in range(img.width):
            bitmap[x, y] = color_to_index[pixels[y * img.width + x]]
    try:
        file_data = colors[file_path[find_place(file_path, "/", -2) + 1:file_path.find(".")]]
        t_place = find_color_index(palette, file_data["t_color"])
        if t_place != -1:
            palette.make_transparent(t_place)
        else:
            print(f"{file_path}: Transparency color not found in palette")
    except KeyError as e:
        print(f"{file_path}: {e}")

    return bitmap, palette

display = PyGameDisplay(width=128, height=128)
splash = displayio.Group()
display.show(splash)

intro_sheet, intro_palette = load_bmp("Backdrops/Intro.bmp")
happy_idle_sheet, happy_idle_palette = load_bmp("Pet/HappyIdle.bmp")
open_back_sheet, open_back_palette = load_bmp("Backdrops/OpenBack.bmp")
neutral_idle_sheet, neutral_idle_palette = load_bmp("Pet/NeutralIdle.bmp")
sad_idle_sheet, sad_idle_palette = load_bmp("Pet/SadIdle.bmp")
petting_sheet, petting_palette = load_bmp("Pet/Petting.bmp")
eating_sheet, eating_palette = load_bmp("Pet/Eating.bmp")
playing_sheet, playing_palette = load_bmp("Pet/Playing (temp).bmp")

obj_to_name = {}

intro_animation = displayio.TileGrid(
    bitmap=intro_sheet,
    pixel_shader=intro_palette,
    width=1,
    height=1,
    tile_width=128,
    tile_height=128,
    default_tile=0,
    x=0,
    y=0
)

obj_to_name[intro_animation] = "intro"

happy_idle_animation = displayio.TileGrid(
    happy_idle_sheet,
    pixel_shader=happy_idle_palette,
    width=1,
    height=1,
    tile_width=128,
    tile_height=128,
    default_tile=0,
    x=0,
    y=0
)

obj_to_name[happy_idle_animation] = "happy_idle"

neutral_idle_animation = displayio.TileGrid(
    neutral_idle_sheet,
    pixel_shader=neutral_idle_palette,
    width=1,
    height=1,
    tile_width=128,
    tile_height=128,
    default_tile=0,
    x=0,
    y=0
)

obj_to_name[neutral_idle_animation] = "neutral_idle"

sad_idle_animation = displayio.TileGrid(
    sad_idle_sheet,
    pixel_shader=sad_idle_palette,
    width=1,
    height=1,
    tile_width=128,
    tile_height=128,
    default_tile=0,
    x=0,
    y=0
)

obj_to_name[sad_idle_animation] = "sad_idle"

petting_animation = displayio.TileGrid(
    petting_sheet,
    pixel_shader=petting_palette,
    width=1,
    height=1,
    tile_width=128,
    tile_height=128,
    default_tile=0,
    x=0,
    y=0
)

obj_to_name[petting_animation] = "petting"

eating_animation = displayio.TileGrid(
    eating_sheet,
    pixel_shader=eating_palette,
    width=1,
    height=1,
    tile_width=128,
    tile_height=128,
    default_tile=0,
    x=0,
    y=0
)

obj_to_name[eating_animation] = "eating"

playing_animation = displayio.TileGrid(
    playing_sheet,
    pixel_shader=playing_palette,
    width=1,
    height=1,
    tile_width=128,
    tile_height=128,
    default_tile=0,
    x=0,
    y=0
)

obj_to_name[playing_animation] = "playing"

open_background = displayio.TileGrid(open_back_sheet, pixel_shader=open_back_palette)

obj_to_name[open_background] = "open_background"


splash.append(intro_animation)
display.refresh()
for i in range(intro_sheet.width // screen_width):
    print("intro", i)
    intro_animation[0] = i
    display.refresh()
    time.sleep(timings["intro"][i % len(timings["intro"])])

splash.remove(intro_animation)
splash.append(open_background)
display.refresh()

settings = {"game": [open_background, open_back_sheet], "inside": [open_background, open_back_sheet], "fridge": [open_background, open_back_sheet]}
setting = 1
#TO-DO: make eating, petting, and playing animations
anims = {"eating": [eating_animation, eating_sheet], "petting": [petting_animation, petting_sheet], "playing": [playing_animation, playing_sheet], "ko": [sad_idle_animation, sad_idle_sheet]}
busy = False
total_time = 0
game = None
idles = {"sad": [sad_idle_animation, sad_idle_sheet, "sad_idle"], "neutral": [neutral_idle_animation, neutral_idle_sheet, "neutral_idle"], "happy": [happy_idle_animation, happy_idle_sheet, "happy_idle"]}
pet = Pet(idles, splash, pet_speed, "Pet")

while True:
    up = False
    left = False
    right = False
    time_dif, ended_one_time = pet.run_frame()
    busy = busy and not ended_one_time
    total_time += time_dif
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_LEFT:
                    left = True
                case pygame.K_RIGHT:
                    right = True
                case pygame.K_UP:
                    up = True

    if right and setting < 2:
        if not busy:
            setting += 1
            print("New Setting:", setting)
            splash.remove(pet.anim)
            splash.remove(settings[list(settings.keys())[setting - 1]][0])
            splash.append(settings[list(settings.keys())[setting]][0])
            splash.append(pet.anim)
    elif left and setting > 0:
        if not busy:
            print("New Setting:", setting)
            setting -= 1
            splash.remove(pet.anim)
            splash.remove(settings[list(settings.keys())[setting + 1]][0])
            splash.append(settings[list(settings.keys())[setting]][0])
            splash.append(pet.anim)
    match setting:
        case 0:
            if up:
                if not busy:
                    busy = True
                    pet.set_anim(anims["playing"][0], anims["playing"][1], "playing", True)
                    pet.exercise += base_exercise_increase
                    #TO-DO: make game_background and ko_animation, fully implement game and mechanics
                    #game = Game(pet, settings["game"][0], settings["game"][1], anims["playing"][0], anims["playing"][1], anims["ko"][0], anims["ko"][1])
            if busy:
                pass
                #game.run(time_dif, left, right)
        case 1:
            if not busy and up:
                busy = True
                pet.set_anim(anims["petting"][0], anims["petting"][1], "petting", True)
                pet.happiness += base_happy_increase
            if (not pet.oneTime) and busy:
                print("busy off")
                busy = False
        case 2:
            if not busy and up:
                busy = True
                pet.set_anim(anims["eating"][0], anims["eating"][1], "eating", True)
                pet.hunger += base_hunger_increase
            if (not pet.oneTime) and busy:
                print("busy off")
                busy = False
    display.refresh()
    time.sleep(time_dif)
    for item in splash:
        if item in obj_to_name:
            print(obj_to_name[item])