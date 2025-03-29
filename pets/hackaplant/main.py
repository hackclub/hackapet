# This is the main Python script for the Tamagotchi-like game.

# --- Required Libraries ---
from adafruit_display_text import label as adafruit_label
from adafruit_bitmap_font import bitmap_font
import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
import time
import random
import pygame

# --- Load Font ---
font_file = "Roboto-Medium-8pt.bdf"  # Replace with a compatible BDF font file path
font = bitmap_font.load_font(font_file)

# --- Setup PyGameDisplay ---
display = PyGameDisplay(width=128, height=128)

# --- Global Variables ---
current_screen = "menu"
selected_button = 0

# --- Create Display Groups ---
splash = displayio.Group()
display.show(splash)

# --- Load Background Image ---
image_file = "mainmenuv2.bmp"
image = displayio.OnDiskBitmap(open(image_file, "rb"))
menu_bg = displayio.TileGrid(image, pixel_shader=image.pixel_shader)
splash.append(menu_bg)

# --- Load Character Sprite (64x64) ---
character_file = "idle.bmp"
character_image = displayio.OnDiskBitmap(open(character_file, "rb"))
character_sprite = displayio.TileGrid(character_image, pixel_shader=character_image.pixel_shader, x=29, y=25)
splash.append(character_sprite)

# --- Create Buttons ---
button_labels = ["Play", "Water", "Shake"]
buttons = []
for i, label in enumerate(button_labels):
    button_group = displayio.Group(x=6 + (i * 38), y=100)
    button_bitmap = displayio.Bitmap(40, 22, 1)
    button_palette = displayio.Palette(1)
    button_palette[0] = 0x222222
    button_rect = displayio.TileGrid(button_bitmap, pixel_shader=button_palette)
    button_group.append(button_rect)
    button_text = adafruit_label.Label(font, text=label, color=0xFFFFFF, x=4, y=10)
    button_group.append(button_text)
    buttons.append(button_group)
    splash.append(button_group)

# --- Functions ---
def draw_menu():
    """Update the menu with highlighted buttons."""
    for i, button in enumerate(buttons):
        rect = button[0]  # Background rectangle
        rect.pixel_shader[0] = 0x444444 if i == selected_button else 0x222222  # Highlight selected

def mini_game():
    """Mini-game: Ball rolling down the slope with a jumping character."""
    global current_screen

    # Load the game background
    image_file = "game1_4bit.bmp"
    image = displayio.OnDiskBitmap(open(image_file, "rb"))
    background = displayio.TileGrid(image, pixel_shader=image.pixel_shader)
    splash.append(background)

    # Create ball sprite
    image_log = "log.bmp"
    ball_bitmap = displayio.OnDiskBitmap(open(image_log, "rb"))
    ball_sprite = displayio.TileGrid(ball_bitmap, pixel_shader=image.pixel_shader)
    splash.append(ball_sprite)

    # Load character sprite (32x32)
    character_file = "idlesmall.bmp"  # Replace with your 32x32 character sprite file
    character_image = displayio.OnDiskBitmap(open(character_file, "rb"))
    character_sprite = displayio.TileGrid(character_image, pixel_shader=character_image.pixel_shader, x=10, y=96)
    splash.append(character_sprite)

    # Points Counter
    points = 0
    points_label = adafruit_label.Label(font, text=f"Points: {points}", color=0xFFFFFF, x=80, y=120)
    splash.append(points_label)

    # Jump Mechanic Variables
    character_y = 70  # Initial Y position
    jump_active = False
    jump_speed = 0
    gravity = 0.3
    jump_strength = -6  # Initial upward velocity for jump
    ground_level = 70  # Character's Y position when on the ground

    # Animation timing
    clock = pygame.time.Clock()  # Pygame clock for frame timing

    # Ball movement parameters
    ball_x = 110
    ball_y = random.uniform(65, 70)  # Corrected starting position
    ball_speed = random.uniform(1.5, 1.9)

    # Game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:  # Exit to menu
                    splash.remove(background)
                    splash.remove(ball_sprite)
                    splash.remove(character_sprite)
                    splash.remove(points_label)
                    current_screen = "menu"
                    return
                if event.key == pygame.K_UP and not jump_active:  # Jump
                    jump_active = True
                    jump_speed = jump_strength

        # Check if the display is closed
        if display.check_quit():
            exit()

        slope_angle = 0.27

        # Ball movement
        ball_x -= ball_speed
        ball_y += slope_angle * ball_speed

        if ball_x < -8 or ball_y > display.height:
            # Ball leaves screen, reset position and increment points
            ball_x = 110
            ball_y = random.uniform(65, 70)
            ball_speed = random.uniform(1.5, 3.0)
            points += 1
            points_label.text = f"Points: {points}"

        # Update ball position
        ball_sprite.x = int(ball_x)
        ball_sprite.y = int(ball_y)

        # Jump logic
        if jump_active:
            character_y += jump_speed
            jump_speed += gravity
            if character_y >= ground_level:  # Character lands back
                character_y = ground_level
                jump_active = False

        character_sprite.y = int(character_y)

        # Collision detection
        if (
            ball_x < character_sprite.x + 32 and ball_x + 8 > character_sprite.x and
            ball_y < character_sprite.y + 32 and ball_y + 8 > character_sprite.y
        ):
            # Game over
            splash.remove(background)
            splash.remove(ball_sprite)
            splash.remove(character_sprite)
            splash.remove(points_label)
            current_screen = "menu"
            print("Game Over!")
            return

        # Frame delay for smoother animations
        clock.tick(60)  # Target 60 FPS

def water_fill():


    """Simulate the screen progressively filling with water."""
    clock = pygame.time.Clock()
    # Create a transparent blue bitmap
    water_bitmap = displayio.Bitmap(display.width, display.height, 1)
    water_palette = displayio.Palette(1)
    water_palette[0] = 0x0000FF  # Blue color
    water_layer = displayio.TileGrid(water_bitmap, pixel_shader=water_palette, x=0, y=display.height)

    # Add the water layer to the display
    splash.append(water_layer)

    # Animate the water rising
    water_height = 0  # Start from the bottom
    while True:
        # Check for user input to return to menu
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:  # Escape key to go back
                    splash.remove(water_layer)
                    return

        # Check if the display is closed
        if display.check_quit():
            exit()

        # Increment water height until the screen is filled
        if water_height < display.height:
            water_height += 1  # Increase water height
            water_layer.y = display.height - water_height  # Adjust position to "rise"
            clock.tick(60)  # Control animation speed
        else:
            # Optionally, loop the animation or keep it filled
            break

    # Keep the screen filled until user exits
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    splash.remove(water_layer)


                    return
        if display.check_quit():
            exit()
def handle_menu_input():
    """Handle arrow key navigation and Enter key selection."""
    global current_screen, selected_button
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                selected_button = (selected_button - 1) % len(button_labels)
                draw_menu()
            elif event.key == pygame.K_RIGHT:
                selected_button = (selected_button + 1) % len(button_labels)
                draw_menu()
            elif event.key == pygame.K_UP:
                if selected_button == 0:  # Play Mini-Game
                    current_screen = "game"
                elif selected_button == 1:  # Water Fill
                    water_fill()
                elif selected_button == 2:  # Shake
                    print("Shake action coming soon!")

# --- Main Loop ---
draw_menu()  # Initial menu rendering
while True:
    if current_screen == "menu":
        handle_menu_input()
    elif current_screen == "game":
        mini_game()
        draw_menu()  # Redraw menu after returning from game