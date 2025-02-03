import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
import pygame
import time
import random
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font

# Load a custom font with a smaller size
font = bitmap_font.load_font("Arial-12.bdf")

# Initialize pygame and display
pygame.init()
pygame.mixer.init()  # Initialize the mixer module for sound
display = PyGameDisplay(width=128, height=128)
splash = displayio.Group()
display.show(splash)

# Helper function to load bitmaps
def load_bitmap(file_name):
    try:
        return displayio.OnDiskBitmap(file_name)
    except FileNotFoundError:
        print(f"Error: {file_name} not found")
        return None

# Load resources
cat_sheet = load_bitmap("uiia_spritesheet.png")
left_beat_bitmap = load_bitmap("beat_left.bmp")
mid_beat_bitmap = load_bitmap("beat_mid.bmp")
right_beat_bitmap = load_bitmap("beat_right.bmp")
line_map = load_bitmap("line.bmp")
line2_map = load_bitmap("line2.bmp")
welcome_bitmap = load_bitmap("welcome.bmp")

# Ensure all bitmaps are loaded
if not all([cat_sheet, left_beat_bitmap, mid_beat_bitmap, right_beat_bitmap, line_map, line2_map, welcome_bitmap]):
    print("Error: One or more bitmap files are missing.")
    pygame.quit()
    exit()

# Background colors for disco effect
disco_colors = [(139, 0, 0), (255, 69, 0), (255, 140, 0), (255, 215, 0), (0, 100, 0), (0, 0, 139), (75, 0, 130), (139, 0, 139)]

# Create a solid color bitmap for the background
background_bitmap = displayio.Bitmap(display.width, display.height, 1)
background_palette = displayio.Palette(1)
background_palette[0] = disco_colors[0]  # Initial color
background_sprite = displayio.TileGrid(background_bitmap, pixel_shader=background_palette)
splash.append(background_sprite)

# Function to change background color
def change_background_color():
    color = random.choice(disco_colors)
    background_palette[0] = color

# Load the bitmap image
cat_sheet = displayio.OnDiskBitmap("uiia_spritesheet.png")
cat_sprite = displayio.TileGrid(
    cat_sheet,
    pixel_shader=cat_sheet.pixel_shader,
    width=1,
    height=1,
    tile_width=cat_sheet.width // 6,  # Assuming 6 frames in the sprite sheet
    tile_height=cat_sheet.height,
    x=(display.width - cat_sheet.width // 6) // 2,
    y=display.height - cat_sheet.height - 40
)

# Load beat bitmaps
left_beat_bitmap = displayio.OnDiskBitmap("beat_left.bmp")
mid_beat_bitmap = displayio.OnDiskBitmap("beat_mid.bmp")
right_beat_bitmap = displayio.OnDiskBitmap("beat_right.bmp")
beats = []

# Load the sound effect
score_sound = pygame.mixer.Sound("snare.wav")

# Load and play the background song
pygame.mixer.music.load("oiia.mp3")


# Variables to control the rate of beats being spawned and speed of beats falling down
spawn_interval = 0.5  # Time interval between spawns in seconds
fall_speed = 12  # Speed of beats falling down (pixels per frame)
score = 0  # Initialize score
total_beats_spawned = 0  # Initialize total beats spawned
collision_tolerance = 10  # Tolerance for collision detection

# Animation variables
animation_interval = 0.1  # Time interval between animation frames in seconds
last_animation_time = time.time()
current_frame = 0
num_frames = 6  # Number of frames in the sprite sheet

# Function to spawn a random beat
def spawn_beat():
    global total_beats_spawned
    beat_bitmap = random.choice([left_beat_bitmap, mid_beat_bitmap, right_beat_bitmap])
    if beat_bitmap == left_beat_bitmap:
        x_position = 9
    elif beat_bitmap == mid_beat_bitmap:
        x_position = 61
    else:
        x_position = 113
    beat = displayio.TileGrid(
        beat_bitmap,
        pixel_shader=beat_bitmap.pixel_shader,
        width=1,
        height=1,
        tile_width=beat_bitmap.width,
        tile_height=beat_bitmap.height,
        x=x_position,
        y=-32
    )
    beats.append(beat)
    splash.append(beat)
    total_beats_spawned += 1

# Load the bitmap image of beatline
line_map = displayio.OnDiskBitmap("line.bmp")

# Create a TileGrid to hold the image
linemap = displayio.TileGrid(
    line_map,
    pixel_shader=line_map.pixel_shader,
    width=1,
    height=1,
    tile_width=line_map.width,  # Ensure this matches the bitmap's width
    tile_height=line_map.height,  # Ensure this matches the bitmap's height
    x=(display.width - line_map.width) // 2,
    y=display.height - line_map.height - 20
)

# Create a TileGrid to hold the second line image
line2map = displayio.TileGrid(
    line2_map,
    pixel_shader=line2_map.pixel_shader,
    width=1,
    height=1,
    tile_width=line2_map.width,  # Ensure this matches the bitmap's width
    tile_height=line2_map.height,  # Ensure this matches the bitmap's height
    x=(display.width - line2_map.width) // 2,
    y=display.height - 8
)
splash.append(line2map)

# Create a label to display the score during the game
score_label = label.Label(font, text=f"Score: {score}", color=0xFFFFFF, x=10, y=10)
splash.append(score_label)


def main_loop():
    global running, paused, last_spawn_time, score, total_beats_spawned, last_animation_time, current_frame
    while running:
        current_time = time.time()

        if not paused and current_time - last_spawn_time > spawn_interval:
            spawn_beat()
            last_spawn_time = current_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                paused = True
                pygame.mixer.music.pause()
            elif event.type == pygame.KEYDOWN:
                if paused:
                    if event.key == pygame.K_RIGHT:
                        paused = False
                        pygame.mixer.music.unpause()
                    elif event.key == pygame.K_LEFT:
                        running = False
                else:
                    print(f"Key pressed: {pygame.key.name(event.key)}")  # Print the key pressed for debugging
                    correct_key_pressed = False
                    for beat in beats:
                        if abs(beat.y - linemap.y) <= collision_tolerance or abs(beat.y - line2map.y) <= collision_tolerance:
                            if (event.key == pygame.K_LEFT and beat.x == 9) or \
                               (event.key == pygame.K_DOWN and beat.x == 61) or \
                               (event.key == pygame.K_RIGHT and beat.x == 113):
                                score += 1
                                beats.remove(beat)
                                splash.remove(beat)
                                score_sound.play()  # Play the sound effect
                                print(f"Score: {score}")
                                correct_key_pressed = True
                                break
                    if not correct_key_pressed and abs(beat.y - line2map.y) > collision_tolerance:
                        score -= 1
                        print(f"Score: {score}")

        if not paused:
            # Move beats down
            for beat in beats:
                beat.y += fall_speed
                if beat.y > display.height:
                    beats.remove(beat)
                    splash.remove(beat)

            # Update the display
            score_label.text = f"Score: {score}/{total_beats_spawned}"
            display.refresh()

            # Check if the music has stopped
            if not pygame.mixer.music.get_busy():
                running = False

            # Update animation
            if current_time - last_animation_time > animation_interval:
                current_frame = (current_frame + 1) % num_frames
                cat_sprite[0] = current_frame
                last_animation_time = current_time

        # Delay to control frame rate
        time.sleep(0.1)

# Display the welcome screen
welcome_sprite = displayio.TileGrid(
    welcome_bitmap,
    pixel_shader=welcome_bitmap.pixel_shader,
    width=1,
    height=1,
    tile_width=welcome_bitmap.width,
    tile_height=welcome_bitmap.height,
    x=(display.width - welcome_bitmap.width) // 2,
    y=(display.height - welcome_bitmap.height) // 2
)
splash.append(welcome_sprite)
display.refresh()

# Wait for the down key press to start the game
start_game = False
while not start_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                start_game = True

# Remove the welcome screen and start the game
splash.remove(welcome_sprite)
splash.append(cat_sprite)
splash.append(linemap)
splash.append(line2map)
pygame.mixer.music.play()

while True:
    running = True
    paused = False
    last_spawn_time = time.time()
    score = 0
    total_beats_spawned = 0
    beats.clear()
    splash = displayio.Group()
    display.show(splash)
    splash.append(background_sprite)
    splash.append(cat_sprite)
    splash.append(linemap)
    splash.append(line2map)
    pygame.mixer.music.rewind()
    pygame.mixer.music.play()

    time.sleep(5)  # Delay
    main_loop()

    # Clear the screen and display the final score
    splash = displayio.Group()
    display.show(splash)
    final_score_text = f"Final Score: \n{score}/{total_beats_spawned}Replay?\nRight for Yes\nLeft for No"
    final_score_label = label.Label(font, text=final_score_text, color=0xFFFFFF, x=10, y=display.height // 2 - 40, scale=1)
    splash.append(final_score_label)
    display.refresh()

    # Wait for user input for replay
    replay = None
    while replay is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                replay = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    replay = True
                elif event.key == pygame.K_LEFT:
                    replay = False

    if replay:
        # Re-add elements to the group
        cat_sprite[0] = 0
        splash = displayio.Group()
        display.show(splash)
        splash.append(background_sprite)
        splash.append(cat_sprite)
        splash.append(linemap)
        splash.append(line2map)
        pygame.mixer.music.rewind()
        pygame.mixer.music.play()
    else:
        break

pygame.quit()
