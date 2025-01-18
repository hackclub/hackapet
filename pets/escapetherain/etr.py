import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
import pygame
import time
from adafruit_display_text import label
import random

# Initialize Pygame
pygame.init()

# Create the display object
display = PyGameDisplay(width=128, height=128)
splash = displayio.Group()
display.show(splash)

# Load and display the planet background
planet_background = displayio.OnDiskBitmap("planetbackground.bmp")
bg_sprite = displayio.TileGrid(planet_background, pixel_shader=planet_background.pixel_shader)
splash.append(bg_sprite)

# Load and display the robot sprite
robot_sheet = displayio.OnDiskBitmap("robot-Sheet.bmp")
tile_width = 32
tile_height = 32

# Initialize robot sprite at the bottom center of the screen
robot_sprite = displayio.TileGrid(
    robot_sheet,
    pixel_shader=robot_sheet.pixel_shader,
    width=1,
    height=1,
    tile_width=tile_width,
    tile_height=tile_height,
    default_tile=0,
    x=(display.width - tile_width) // 2,
    y=display.height - tile_height - 10     
)
splash.append(robot_sprite)

# Load the drop bitmap
drop_bitmap = displayio.OnDiskBitmap("drop.bmp")

# List to store active drops
drops = []

class PowerUp(displayio.TileGrid):
    def __init__(self, bitmap, x, y):
        super().__init__(
            bitmap,
            pixel_shader=bitmap.pixel_shader,
            width=1,
            height=1,
            tile_width=bitmap.width,
            tile_height=bitmap.height,
            x=x,
            y=y
        )
        self.active = False

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

# Load power-up bitmaps
shield_bitmap = displayio.OnDiskBitmap("shield.bmp")
boost_bitmap = displayio.OnDiskBitmap("boost.bmp")

# List to store active power-ups
power_ups = []

def spawn_drop():
    """Spawn a new drop at a random x position near the bottom of the screen."""
    x_position = random.randint(0, display.width - drop_bitmap.width)
    drop = displayio.TileGrid(
        drop_bitmap,
        pixel_shader=drop_bitmap.pixel_shader,
        width=1,
        height=1,
        tile_width=drop_bitmap.width,
        tile_height=drop_bitmap.height,
        x=x_position,
        y=-32
    )
    drops.append(drop)
    splash.append(drop)

def spawn_power_up():
    """Spawn a random power-up at a random x position near the bottom of the screen."""
    x_position = random.randint(0, display.width - shield_bitmap.width)
    if random.random() < 0.5:  # 50% chance of spawning a shield
        power_up = PowerUp(shield_bitmap, x_position, -32)
    else:  # 50% chance of spawning a boost
        power_up = PowerUp(boost_bitmap, x_position, -32)
    power_ups.append(power_up)
    splash.append(power_up)

def check_collision(sprite1, sprite2):
    """Check if two sprites collide."""
    return (
        sprite1.x < sprite2.x + 32 and
        sprite1.x + 32 > sprite2.x and
        sprite1.y < sprite2.y + 32 and
        sprite1.y + 32 > sprite2.y
    )

def check_collision_with_power_up(sprite1, sprite2):
    """Check if two sprites collide and apply power-up effects if they do."""
    return check_collision(sprite1, sprite2)

# Game variables
frame = 0
speed = 4 
game_over = False
death_hi = None  # Variable for game over text

# Function to display Game Over screen
def display_game_over():
    global death_hi
    game_over_text = "GAME OVER"
    text_area = label.Label(terminalio.FONT, text=game_over_text, x=10, y=60)
    splash.append(text_area)
    death_hi = text_area  # Save the label for future removal
    return text_area

# Function to display Welcome screen
def display_welcome_screen():
    welcome_text = "Escape The Rain!"
    text_area = label.Label(terminalio.FONT, text=welcome_text, x=10, y=60)
    splash.append(text_area)
    return text_area

# Show the welcome screen initially
welcome_screen = display_welcome_screen()

while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_over:
                # Reset the game when UP key is pressed during game over screen
                for i in drops:
                    splash.remove(i)
                drops.clear()
                for power_up in power_ups:
                    splash.remove(power_up)
                power_ups.clear()
                game_over = False
                splash.remove(death_hi)  # Remove the game over label
                death_hi = None  # Reset the death_hi variable to None
                # Reset the robot sprite
                robot_sprite.x = (display.width - tile_width) // 2
                robot_sprite.y = display.height - tile_height - 10
                # Clear the welcome screen
                splash.remove(welcome_screen)

    # Get the current key presses
    keys = pygame.key.get_pressed()

    if not game_over:
        # Move the robot left or right
        if keys[pygame.K_LEFT]:
            robot_sprite.x -= speed
        if keys[pygame.K_RIGHT]:
            robot_sprite.x += speed
        
        # Randomly spawn drops and power-ups
        if random.random() < 0.05:  # 5% chance of spawning a drop or power-up
            spawn_drop()
            spawn_power_up()

    # Update drops and power-ups
    for drop in drops[:]:  # Iterate through a copy to avoid modifying the list while iterating
        drop.y += 5 
        if drop.y > display.height:
            # Remove dropped objects that have gone off-screen
            splash.remove(drop)
            drops.remove(drop)
        elif check_collision_with_power_up(robot_sprite, drop):
            # Game over if robot collides with a drop
            game_over = True
            display_game_over()

    for power_up in power_ups[:]:  # Iterate through a copy to avoid modifying the list while iterating
        power_up.y += 5 
        if power_up.y > display.height:
            # Remove power-ups that have gone off-screen
            splash.remove(power_up)
            power_ups.remove(power_up)
        elif check_collision_with_power_up(robot_sprite, power_up):
            # Apply power-up effect when collected
            if isinstance(power_up, PowerUp):
                power_up.activate()
            # Remove the power-up from the screen and list
            splash.remove(power_up)
            power_ups.remove(power_up)

    # Handle active power-ups
    for power_up in power_ups[:]:
        if isinstance(power_up, PowerUp) and power_up.active:
            # Implement shield or boost effects here
            pass

    # Animate the robot sprite
    robot_sprite[0] = frame
    frame = (frame + 1) % (robot_sheet.width // tile_width)

    # Limit the frame rate to 10 FPS
    pygame.time.Clock().tick(10)
