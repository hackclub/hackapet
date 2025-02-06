import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
import pygame
import time
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font
import random
pygame.init()

# Initialize display
display = PyGameDisplay(width=128, height=128)
splash = displayio.Group()
display.show(splash)

# Load background and sprites
forest_background = displayio.OnDiskBitmap("ec61a5cc-3bf0-4149-8a18-6836238473a0_with_bgc.bmp")
bg_sprite = displayio.TileGrid(forest_background, pixel_shader=forest_background.pixel_shader)
splash.append(bg_sprite)

virtual_guy = displayio.OnDiskBitmap("Idle (32x32).bmp")

tile_width = 32
tile_height = 32

virtual_guy = displayio.TileGrid(
    virtual_guy,
    pixel_shader=virtual_guy.pixel_shader,
    width=1,
    height=1,
    tile_width=tile_width,
    tile_height=tile_height,
    default_tile=0,
    x=(display.width - tile_width) // 2,
    y=display.height - tile_height - 10
)



# Load font for text
font = bitmap_font.load_font("ib16x16u.bdf")
color = 0x000000  # Black color
text = "Feed"
text_area = label.Label(font, text=text, color=color)
text_area.x = (display.width - text_area.bounding_box[2]) // 2
text_area.y = 23

# Append text and sprites to the display
splash.append(text_area)
splash.append(virtual_guy)

frame = 0
total_frames = 11
frame_delay = 0.05
last_frame_time = time.time()
stats = {}
def load_stats():
    global stats  # Ensure we modify the global stats dictionary
    try:
        with open("data.txt", "r") as file:
            for line in file:
                key, value = line.strip().split(": ")
                stats[key] = int(value)
    except (FileNotFoundError, ValueError, KeyError):
        # File doesn't exist or is invalid, use default values
        stats = {
            "hunger": 50,
            "thirst": 50,
            "happiness": 50,
            "energy": 50
        }
load_stats()
actions = ["Feed", "Drink", "Play", "Sleep", "Stats"]
current_action_index = 0

def save_stats():
    with open("data.txt", "w") as file:
        for key, value in stats.items():
            file.write(f"{key}: {value}\n")

def feed():
    stats["hunger"] = min(stats["hunger"] + 10, 100)
    for (i) in range(8, 0, -1):
        text_area.text = f" {i}"
        text_area.x = (display.width - text_area.bounding_box[2]) // 2 -5

        time.sleep(1)
    text_area.text = f"{stats['hunger']}%"
    save_stats()

def drink():
    stats["thirst"] = min(stats["thirst"] + 10, 100)

    for (i) in range(3, 0, -1):
        text_area.text = f" {i}"
        text_area.x = (display.width - text_area.bounding_box[2]) // 2 -5

        time.sleep(1)
    text_area.text = f"{stats['thirst']}%"

    save_stats()
inGame = False
def play():
    global inGame  # Declare inGame as global so the main loop recognizes the change
    inGame = True

def sleep():
    stats["energy"] = min(stats["energy"] + 10, 100)
    for (i) in range(10, 0, -1):
        text_area.text = f" {i}"
        text_area.x = (display.width - text_area.bounding_box[2]) // 2 -5

        time.sleep(1)
    text_area.text = f"{stats['energy']}%"
    text_area.x = (display.width - text_area.bounding_box[2]) // 2 - 5

    save_stats()
def display_stats():
    text_area.text = f"HU:{stats['hunger']}%\nW:{stats['thirst']}%\nHA:{stats['happiness']}%\nEN:{stats['energy']}%"
    text_area.x = (display.width - text_area.bounding_box[2]) // 2
    time.sleep(5)
# Map actions to functions
action_functions = {
    "Feed": feed,
    "Drink": drink,
    "Play": play,
    "Sleep": sleep,
    "Stats": display_stats
}

# Main game loop
inGame = False
last_stat_update_time = time.time()  # Record the initial time

##Play Game Props
def check_collision(sprite1, sprite2):
    return (
        sprite1.x < sprite2.x + 32 and
        sprite1.x + 32 > sprite2.x and
        sprite1.y < sprite2.y + 32 and
        sprite1.y + 32 > sprite2.y
    )
apple_bitmap = displayio.OnDiskBitmap("New-Piskel.bmp")
apples = []
def spawn_apple():
    x_position = random.randint(0, display.width - apple_bitmap.width)
    fireball = displayio.TileGrid(
        apple_bitmap,
        pixel_shader=apple_bitmap.pixel_shader,
        width=1,
        height=1,
        tile_width=apple_bitmap.width,
        tile_height=apple_bitmap.height,
        x=x_position,
        y=-32
    )
    apples.append(fireball)
    splash.append(fireball)
game_start_time = None

while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    if inGame:
        if game_start_time is None:
            game_start_time = time.time()

        text_area.text = f"{30 - int(time.time() - game_start_time)}s"
        text_area.x = (display.width - text_area.bounding_box[2]) // 2 + 5

        # Check for game over conditions
        if time.time() - game_start_time >= 30:
            inGame = False
            text_area.text = "Game \nOver"
            text_area.x = (display.width - text_area.bounding_box[2]) // 2 + 10
            display.refresh()
            for apple in apples:
                splash.remove(apple)
            apples.clear()
            time.sleep(3)
            text_area.text = actions[current_action_index]


        # Update apple positions and check collisions
        for apple in apples:
            apple.y += 5
            if apple.y > display.height:
                splash.remove(apple)
                apples.remove(apple)
            elif check_collision(virtual_guy, apple):
                stats["happiness"] = min(stats["happiness"] + 1, 100)
                save_stats()
                splash.remove(apple)
                apples.remove(apple)

        # Randomly spawn apples
        if random.randint(0, 100) < 5:
            spawn_apple()

        # Handle key presses
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            print("LEFT")
            virtual_guy.x = max(0, virtual_guy.x - 4)  # Move left
        if keys[pygame.K_RIGHT]:
            print("RIGHT")
            virtual_guy.x = min(display.width - virtual_guy.width, virtual_guy.x + 4)  # Move right

        # Update display
        if keys[pygame.K_LEFT]:
            virtual_guy.x -= 4
        if keys[pygame.K_RIGHT]:
            virtual_guy.x += 4
        if keys[pygame.K_RETURN]:
            inGame = False
            text_area.text = "Game \nOver"
            text_area.x = (display.width - text_area.bounding_box[2]) // 2 + 10
            display.refresh()
            for apple in apples:
                splash.remove(apple)
            apples.clear()
            time.sleep(3)
            text_area.text = actions[current_action_index]


        display.refresh()
        time.sleep(0.05)
    else:
        if stats["hunger"] <= 0 or stats["thirst"] <= 0 or stats["happiness"] <= 0 or stats["energy"] <= 0:
            text_area.text = f"Game \nOver"
            text_area.x = ((display.width - text_area.bounding_box[2]) // 2) + 10

            virtual_guy[0] = 0
            time.sleep(5)
            stats = {
                "hunger": 50,
                "thirst": 50,
                "happiness": 50,
                "energy": 50
            }
            save_stats()
            pygame.quit()
            exit()

        keys = pygame.key.get_pressed()


        if keys[pygame.K_LEFT]:
            current_action_index = (current_action_index - 1) % len(actions)
            text_area.text = actions[current_action_index]
            text_area.x = (display.width - text_area.bounding_box[2]) // 2
            time.sleep(0.2)

        if keys[pygame.K_RIGHT]:
            current_action_index = (current_action_index + 1) % len(actions)
            text_area.text = actions[current_action_index]
            text_area.x = (display.width - text_area.bounding_box[2]) // 2
            time.sleep(0.2)

        if keys[pygame.K_RETURN]:
            current_action = actions[current_action_index]
            action_functions[current_action]()
            text_area.x = (display.width - text_area.bounding_box[2]) // 2
            time.sleep(0.5)
            text_area.text = actions[current_action_index]
            text_area.x = (display.width - text_area.bounding_box[2]) // 2

        current_time = time.time()
        if current_time - last_frame_time >= frame_delay:
            frame = (frame + 1) % total_frames
            virtual_guy[0] = frame
            last_frame_time = current_time

        if current_time - last_stat_update_time >= 20:
            stats["energy"] -= 10
            stats["thirst"] -= 3
            stats["hunger"] -= 3
            stats["happiness"] -= 2
            last_stat_update_time = current_time
            save_stats()

        display.refresh()
        time.sleep(0.01)



