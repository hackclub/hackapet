import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
import time
import pygame

pygame.init()

# display settings
DISPLAY_WIDTH = 128
DISPLAY_HEIGHT = 128
display = PyGameDisplay(width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT)

tile_width = 32
tile_height = 32
icon_size = 16

splash = displayio.Group()
display.show(splash)

# load background
snowy_background = displayio.OnDiskBitmap("background.bmp")
bg_sprite = displayio.TileGrid(
    snowy_background, pixel_shader=snowy_background.pixel_shader)
splash.append(bg_sprite)

# load sprite sheets
fox_idle_sheet = displayio.OnDiskBitmap("fox-idle-sheet.bmp")
fox_walk_sheet = displayio.OnDiskBitmap("fox-walking-right-sheet.bmp")
fox_dead_sheet = displayio.OnDiskBitmap("fox-dead.bmp")
fox_happy_sheet = displayio.OnDiskBitmap("fox-happy.bmp")

# load stick and rabbit leg sprites
stick_sprite_sheet = displayio.OnDiskBitmap("stick.bmp")
rabbit_leg_sprite_sheet = displayio.OnDiskBitmap("rabbit-leg.bmp")

# calculate total frames
total_walk_frames = fox_walk_sheet.width // tile_width
total_idle_frames = fox_idle_sheet.width // tile_width

# create fox sprite
def create_fox_sprite(bitmap, x_position):
    return displayio.TileGrid(
        bitmap,
        pixel_shader=bitmap.pixel_shader,
        tile_width=tile_width,
        tile_height=tile_height,
        width=1,
        height=1,
        default_tile=0,
        x=x_position,
        y=DISPLAY_HEIGHT - tile_height - 10)

fox_sprite = create_fox_sprite(fox_idle_sheet, (DISPLAY_WIDTH - tile_width) // 2)
splash.append(fox_sprite)

# load icons
hunger_full_icon = displayio.OnDiskBitmap("meat-full.bmp")
hunger_halfway_icon = displayio.OnDiskBitmap("meat-halfway.bmp")
hunger_empty_icon = displayio.OnDiskBitmap("meat-empty.bmp")

happiness_full_icon = displayio.OnDiskBitmap("smiling.bmp")
happiness_halfway_icon = displayio.OnDiskBitmap("serious.bmp")
happiness_empty_icon = displayio.OnDiskBitmap("sad.bmp")

health_full_icon = displayio.OnDiskBitmap("heart-full.bmp")
health_halfway_icon = displayio.OnDiskBitmap("heart-halfway.bmp")
health_empty_icon = displayio.OnDiskBitmap("heart-empty.bmp")

# icon sprites
hunger_sprite = displayio.TileGrid(hunger_full_icon, pixel_shader=hunger_full_icon.pixel_shader, x=5, y=DISPLAY_HEIGHT - icon_size - 5)
happiness_sprite = displayio.TileGrid(happiness_full_icon, pixel_shader=happiness_full_icon.pixel_shader, x=20, y=DISPLAY_HEIGHT - icon_size - 5)
health_sprite = displayio.TileGrid(health_full_icon, pixel_shader=health_full_icon.pixel_shader, x=35, y=DISPLAY_HEIGHT - icon_size - 5)

splash.append(hunger_sprite)
splash.append(happiness_sprite)
splash.append(health_sprite)

# stats
hunger = 5
happiness = 5
health = 5

HAPPY_DISPLAY_TIME = 2  # seconds for happy fox sprite
time_happy_activated = 0  # store the time when happy sprite was activated

# UPDATING ICONS BASED ON LEVELS
def update_icons():
    splash.remove(hunger_sprite)
    if hunger >= 4:
        hunger_sprite.bitmap = hunger_full_icon
    elif 1 <= hunger < 4:
        hunger_sprite.bitmap = hunger_halfway_icon
    else:
        hunger_sprite.bitmap = hunger_empty_icon
    splash.append(hunger_sprite)

    splash.remove(happiness_sprite)
    if happiness >= 4:
        happiness_sprite.bitmap = happiness_full_icon
    elif 2 <= happiness < 4:
        happiness_sprite.bitmap = happiness_halfway_icon
    else:
        happiness_sprite.bitmap = happiness_empty_icon
    splash.append(happiness_sprite)

    splash.remove(health_sprite)
    if happiness >= 4 and hunger >= 4:
        health_sprite.bitmap = health_full_icon
    elif 2 <= happiness < 4 and 2 <= hunger < 4:
        health_sprite.bitmap = health_halfway_icon
    else:
        health_sprite.bitmap = health_empty_icon
    splash.append(health_sprite)

def change_fox_sprite(new_bitmap):
    global fox_sprite
    current_x_position = fox_sprite.x
    splash.remove(fox_sprite)
    fox_sprite = create_fox_sprite(new_bitmap, current_x_position)
    splash.append(fox_sprite)

# Function to display happy fox for a limited time
def display_fox_happy():
    global time_happy_activated
    time_happy_activated = time.monotonic()
    change_fox_sprite(fox_happy_sheet)

state = "idle"
frame = 0
last_state_change = time.monotonic()
walk_direction = 1  # 1 for right, -1 for left

IDLE_TIME = 3
WALK_TIME = 5
FRAME_DELAY = 0.2

HUNGER_DECAY = 10
HAPPINESS_DECAY = 14

last_hunger_time = time.monotonic()
last_happiness_time = time.monotonic()

update_icons()

while True:
    current_time = time.monotonic()

    # Handle happy sprite duration
    if time_happy_activated and current_time - time_happy_activated > HAPPY_DISPLAY_TIME:
        change_fox_sprite(fox_walk_sheet)
        time_happy_activated = 0  # reset timer

    # decrease hunger and happiness over time
    if current_time - last_hunger_time > HUNGER_DECAY:
        hunger = max(0, hunger - 1)
        last_hunger_time = current_time

    if current_time - last_happiness_time > HAPPINESS_DECAY:
        happiness = max(0, happiness - 1)
        last_happiness_time = current_time

    # health depends on hunger and happiness
    health = (hunger + happiness) // 2
    update_icons()

    if health == 0:
        change_fox_sprite(fox_dead_sheet)
    else:
        if state == "idle" and current_time - last_state_change > IDLE_TIME:
            state = "walking"
            last_state_change = current_time
            frame = 0
            change_fox_sprite(fox_walk_sheet)

        elif state == "walking" and current_time - last_state_change > WALK_TIME:
            if abs(fox_sprite.x - (DISPLAY_WIDTH - tile_width) // 2) < 2:
                state = "idle"
                last_state_change = current_time
                frame = 0
                change_fox_sprite(fox_idle_sheet)

        if state == "walking":
            fox_sprite.x += walk_direction * 2
            if fox_sprite.x <= 0 or fox_sprite.x >= DISPLAY_WIDTH - tile_width:
                walk_direction *= -1
            fox_sprite[0] = frame % total_walk_frames
            frame += 1
        else:
            fox_sprite[0] = frame % total_idle_frames
            frame += 1

    # handle keyboard events for rabbit leg and stick
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:  # press 'R' to spawn rabbit leg and regenerate hunger
                hunger = min(5, hunger + 2)
                rabbit_leg_sprite = displayio.TileGrid(rabbit_leg_sprite_sheet, pixel_shader=rabbit_leg_sprite_sheet.pixel_shader, x=50, y=50)
                splash.append(rabbit_leg_sprite)
                update_icons()
                display_fox_happy()  # Display happy fox
                print("Rabbit leg fed! Hunger increased.")
                time.sleep(0.5)  # debounce delay
                splash.remove(rabbit_leg_sprite)  # remove the sprite after a delay

            if event.key == pygame.K_s:  # Press 'S' to spawn stick and regenerate happiness
                happiness = min(5, happiness + 2)
                stick_sprite = displayio.TileGrid(stick_sprite_sheet, pixel_shader=stick_sprite_sheet.pixel_shader, x=70, y=50)
                splash.append(stick_sprite)
                update_icons()
                display_fox_happy()  # Display happy fox
                print("Stick thrown! Happiness increased.")
                time.sleep(0.5)  # debounce delay
                splash.remove(stick_sprite)  # remove the sprite after a delay

    time.sleep(FRAME_DELAY)
