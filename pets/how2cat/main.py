import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
import pygame
import time
import random
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font

pygame.init()

# Initialize game state flags
minigame_active = False  # Assuming the game starts active
brushing_active = False
petting_active = False
feeding_active = False
minigame_over = False  # Initialize game_over variable
game_over = False
game_active = True

# Initialize display
display = PyGameDisplay(width=128, height=128)

# Create a display group
splash = displayio.Group()
display.show(splash)

# Load and display background
try:
    tabucat_bg = displayio.OnDiskBitmap("tabucat-bg.bmp")
    bg_sprite = displayio.TileGrid(tabucat_bg, pixel_shader=tabucat_bg.pixel_shader)
    splash.append(bg_sprite)
    print("Background loaded successfully.")
except Exception as e:
    print(f"Error loading background: {e}")


# Load the sprite sheet
try:
    tabucat_sheet = displayio.OnDiskBitmap("tabucat-sheet_cropped.bmp")
    print("Sprite sheet loaded successfully.")
    print(f"Sprite sheet dimensions: {tabucat_sheet.width}x{tabucat_sheet.height}")
except Exception as e:
    print(f"Error loading sprite sheet: {e}")

# Tile configuration
tile_width = 96
tile_height = 96
# num_frames = tabucat_sheet.width // tile_width  # Calculate total frames

# tabucat sprite
tabucat_sprite = displayio.TileGrid(
    tabucat_sheet,
    pixel_shader=tabucat_sheet.pixel_shader,
    width=1,
    height=1,
    tile_width=tile_width,
    tile_height=tile_height,
    default_tile=0,  # Start at frame 0
    x=(display.width - tile_width) // 2,  # Center horizontally
    y=(display.height - tile_height)  # Center vertically
)

splash.append(tabucat_sprite)

# update cat positions
def update_cat_position():
    """Update cat position with screen edge tolerance"""
    new_x = tabucat_sprite.x + x_speed
    # Allow partial off-screen movement (8px tolerance)
    min_x = -tile_width + 8
    max_x = display.width - 8
    tabucat_sprite.x = max(min_x, min(max_x, new_x))

# Load love bar images
love_bar_images = {
    100: displayio.OnDiskBitmap("lovebar-full.bmp"),
    75: displayio.OnDiskBitmap("lovebar-75.bmp"),  # Added love bar for 75 points
    50: displayio.OnDiskBitmap("lovebar-50.bmp"),
    25: displayio.OnDiskBitmap("lovebar-25.bmp"),
    "danger": displayio.OnDiskBitmap("lovebar-danger.bmp"),
    0: displayio.OnDiskBitmap("lovebar-0.bmp")
}

# Create love bar group (will hold current image)
love_bar_group = displayio.Group()

# Initial love state
love_points = 100
current_love_image = None

love_points = 10  # Value between danger (0-25) and 25
current_love_image = None

#love bar
def update_love_bar():
    global current_love_image
    # Determine which image to show
    if love_points >= 95:
        new_image = love_bar_images[100]
    elif love_points >= 65:  # Added condition for 75 points
        new_image = love_bar_images[75]
    elif love_points >= 55:
        new_image = love_bar_images[50]
    elif love_points >= 30:
        new_image = love_bar_images[25]
    elif love_points > 0:
        new_image = love_bar_images["danger"]
    else:
        new_image = love_bar_images[0]
    
    # Only update if the image has changed
    if new_image != current_love_image:
        # Clear previous image
        while len(love_bar_group) > 0:
            love_bar_group.pop()
        
        # Add new image
        love_bar_sprite = displayio.TileGrid(
            new_image,
            pixel_shader=new_image.pixel_shader,
            x=4,
            y=4
        )
        love_bar_group.append(love_bar_sprite)
        current_love_image = new_image

update_love_bar()

splash.append(love_bar_group)

# Create brush animation sprite
brush_sheet = displayio.OnDiskBitmap("brush-anim_cropped.bmp")
brush_animation = displayio.TileGrid(
    brush_sheet,
    pixel_shader=brush_sheet.pixel_shader,
    width=1,
    height=1,
    tile_width=128,  # Updated to match frame width (1664/13 ≈ 128)
    tile_height=128,  # Updated to match frame height
    default_tile=0,
    x=(display.width - 128) // 2,  # Center horizontally
    y=(display.height - 128) // 2  # Center vertically
)

# Create overlay grid for brushing (replace the existing overlay code)
overlay = displayio.Bitmap(128, 128, 2)
overlay_palette = displayio.Palette(2)
overlay_palette[0] = 0x808080  # White
overlay_palette[1] = 0xFFFFFF  # Transparent
overlay_palette.make_transparent(1)
overlay_palette[0] = (255, 255, 255, 0x80)  # 50% opacity white

overlay_grid = displayio.TileGrid(
    overlay,
    pixel_shader=overlay_palette,
    x=0,
    y=0
)

# brushing
try:
    brush_icon = displayio.OnDiskBitmap("brush.bmp")  # Changed from brush-icon.bmp to match your files
    print(f"Brush icon loaded successfully. Size: {brush_icon.width}x{brush_icon.height}")
    brush_sprite = displayio.TileGrid(
        brush_icon,
        pixel_shader=brush_icon.pixel_shader,
        x=display.width - 30,  # Adjusted for scaled size
        y=display.height - 30  # Adjusted for scaled size
    )
    splash.append(brush_sprite)
    print("Brush sprite added to display")
except Exception as e:
    print(f"Error loading brush icon: {e}")

def start_brushing():
    global brushing_active, animation_start_time
    brushing_active = True
    animation_start_time = time.monotonic()
    
    # First remove the elements if they're in any group
    try:
        if overlay_grid.parent_group:
            overlay_grid.parent_group.remove(overlay_grid)
        if brush_animation.parent_group:
            brush_animation.parent_group.remove(brush_animation)
    except (AttributeError, ValueError):
        pass
    
    # Now add them to splash
    try:
        splash.append(overlay_grid)
        splash.append(brush_animation)
    except ValueError:
        pass
    
    # Hide UI elements by moving them off-screen
    love_bar_group.x = -200  # Move off-screen instead of removing
    brush_sprite.x = -200

def stop_brushing():
    global brushing_active, brush_frame, love_points
    brushing_active = False
    brush_frame = 0
    
    # Remove animation elements
    try:
        if overlay_grid in splash:
            splash.remove(overlay_grid)
        if brush_animation in splash:
            splash.remove(brush_animation)
    except ValueError:
        pass
    
    # Restore UI elements by moving them back on-screen
    love_bar_group.x = 4  # Original x position
    brush_sprite.x = display.width - 30  # Original x position
    
    love_points = min(100, love_points + 25)  # Ensure love points do not exceed 100
    update_love_bar()  # Update the love bar display

# Load the petting sheet
petting_sheet = displayio.OnDiskBitmap("tabucat-pet.bmp")  # Ensure this file exists

# Create the petting animation sprite
petting_animation = displayio.TileGrid(
    petting_sheet,
    pixel_shader=petting_sheet.pixel_shader,
    width=1,
    height=1,
    tile_width=128,  # Width of each frame
    tile_height=128,  # Height of each frame
    default_tile=0,
    x=(display.width - 128) // 2,  # Center horizontally
    y=(display.height - 128) // 2  # Center vertically
)

def start_petting():
    global petting_active, animation_start_time
    petting_active = True
    animation_start_time = time.monotonic()
    
    # First remove the elements if they're in any group
    try:
        if overlay_grid.parent_group:
            overlay_grid.parent_group.remove(overlay_grid)
        if petting_animation.parent_group:
            petting_animation.parent_group.remove(petting_animation)
    except (AttributeError, ValueError):
        pass

    # Now add them to splash
    try:
        splash.append(overlay_grid)
        splash.append(petting_animation)
    except ValueError:
        pass
    
    # Hide UI elements by moving them off-screen
    love_bar_group.x = -200  # Move off-screen instead of removing
    brush_sprite.x = -200
    
    print("Petting started.")  # Debugging output

def stop_petting():
    global petting_active, pet_frame, love_points
    petting_active = False
    pet_frame = 0

    # Remove animation elements
    try:
        if overlay_grid in splash:
            splash.remove(overlay_grid)
        if petting_animation in splash:
            splash.remove(petting_animation)
    except ValueError:
        pass
    
    # Restore UI elements by moving them back on-screen
    love_bar_group.x = 4  # Original x position
    brush_sprite.x = display.width - 30  # Original x position
    
    love_points = min(100, love_points + 25)  # Ensure love points do not exceed 100
    update_love_bar()  # Update the love bar display

#feed
#load food sprite
food_sprite = displayio.OnDiskBitmap("pet-food_cropped.bmp")
food_tilegrid = displayio.TileGrid(
    food_sprite,
    pixel_shader=food_sprite.pixel_shader,
    width=1,
    height=1,
    tile_width=30,
    tile_height=32,
    default_tile=0,
    x=10,
    y=display.height - 60
)
splash.append(food_tilegrid)
splash.append(tabucat_sprite)

#load tabucat eat sprite
tabucat_chomp_sheet = displayio.OnDiskBitmap("tabucat-chomp.bmp")
feeding_animation = displayio.TileGrid(
    tabucat_chomp_sheet,
    pixel_shader=tabucat_chomp_sheet.pixel_shader,
    width=1,
    height=1,
    tile_width=128,  
    tile_height=128,
    default_tile=0,
    x=display.width - 128,
    y=display.height - 128
)

def start_feeding():
    global feeding_active, animation_start_time
    feeding_active = True
    animation_start_time = time.monotonic()

    # First remove the elements if they're in any group
    try:
        if overlay_grid.parent_group:
            overlay_grid.parent_group.remove(overlay_grid)
        if feeding_animation.parent_group:
            feeding_animation.parent_group.remove(feeding_animation)
    except (AttributeError, ValueError):
        pass

    # Now add them to splash
    try:
        splash.append(overlay_grid)
        splash.append(feeding_animation)
    except ValueError:
        pass

    # Hide UI elements by moving them off-screen
    love_bar_group.x = -200  # Move off-screen instead of removing
    brush_sprite.x = -200
    
    print("Feeding started.")  # Debugging output

def stop_feeding():
    global feeding_active, chomp_frame, love_points
    feeding_active = False
    chomp_frame = 0
    
     # Remove animation elements
    try:
        if overlay_grid in splash:
            splash.remove(overlay_grid)
        if feeding_animation in splash:
            splash.remove(feeding_animation)    
    except ValueError:
        pass
    

    # Restore UI elements by moving them back on-screen
    love_bar_group.x = 4  # Original x position
    brush_sprite.x = display.width - 30  # Original x position
    
    love_points = min(100, love_points + 25)  # Ensure love points do not exceed 100
    update_love_bar()  # Update the love bar display

# Load yarn sprite outside of play
yarn_bitmap = displayio.OnDiskBitmap("yarnball.bmp")  # Ensure this file exists
yarn_sprite = displayio.TileGrid(
    yarn_bitmap,
    pixel_shader=yarn_bitmap.pixel_shader,
    width=1,
    height=1,
    tile_width=32,
    tile_height=32,
    default_tile=0,
    x=display.width - 32,  # Adjusted for scaled size
    y=display.height - 32  # Adjusted for scaled size
)
splash.append(yarn_sprite)
# Load tabucat play sprite outside of play
tabucat_play_sheet = displayio.OnDiskBitmap("tabucat-play_cropped.bmp")
tabucat_play_sprite = displayio.TileGrid(
    tabucat_play_sheet,
    pixel_shader=tabucat_play_sheet.pixel_shader,
    width=1,
    height=1,
    tile_width=96,  # Updated to match the width of a single frame
    tile_height=96,          # Height of the sprite
    default_tile=0,
    x=display.width - 96,  # Adjusted for scaled size
    y=display.height - 96  # Adjusted for scaled size
)

#game
def play():
    global love_points, minigame_active, minigame_over, frame  # Added 'frame' to the global variables
    # Reset game state on start
    minigame_active = True
    minigame_over = False
    hearts = 3
    score = 0
    minigame_paused = False
    minigame_over =   False
    start_time = time.monotonic()
    minigame_duration = 20
    
    up = False
    left = False
    right = False

    # Initialize frame variable
    frame = 0  # Ensure frame is initialized

    # Move love bar and brush sprite off-screen
    love_bar_group.x = -200  # Move off-screen
    brush_sprite.x = -200  # Move off-screen

    class FallingObject:
        def __init__(self, sprite, is_mouse=True):
            self.sprite = sprite
            self.x = sprite.x
            self.y = -32
            self.speed = random.uniform(2, 4)
            self.is_mouse = is_mouse
            self.active = True
            
        def update(self):
            if self.active:
                self.y += self.speed
                self.sprite.y = int(self.y)
                if self.y > display.height:
                    self.active = False
                    return True
            return False
    
    # Create game objects group
    minigame_group = displayio.Group()
    
    # Create grey background
    game_bg = displayio.Bitmap(display.width, display.height, 1)
    bg_palette = displayio.Palette(1)
    bg_palette[0] = 0x808080  # Grey
    bg_sprite = displayio.TileGrid(game_bg, pixel_shader=bg_palette)
    minigame_group.append(bg_sprite)
    
    try:
        # Load mouse sprite
        mouse_bitmap = displayio.OnDiskBitmap("mousetoy.bmp")
        mouse_sprite = displayio.TileGrid(
            mouse_bitmap,
            pixel_shader=mouse_bitmap.pixel_shader,
            width=1,
            height=1,
            tile_width=32,
            tile_height=32
        )
        
        # Load heart states
        heart_images = {
            3: displayio.OnDiskBitmap("fullhealth.bmp"),
            2: displayio.OnDiskBitmap("2-hearts.bmp"),
            1: displayio.OnDiskBitmap("1-heart.bmp")
        }
        
        # Create heart display
        heart_sprite = displayio.TileGrid(
            heart_images[3],
            pixel_shader=heart_images[3].pixel_shader,
            x=4,  # Set the x position
            y=4  # Set the y position
        )
        minigame_group.append(heart_sprite)
        print("Heart sprite added to game group.")
            
        # Create a label for the score within the game at the top right corner
        if font:
            game_score_label = label.Label(
                font,
                text=f"Score: {score}",
                color=0xFFFF00,  # Optional: Different color for visibility
                x=display.width - 55,  # Position near the right edge
                y=4  # Position near the top
            )
            minigame_group.append(game_score_label)
            print("Game score label created and added to game group.")
            print("Created game_score_label:", game_score_label)
        
    except Exception as e:
        print(f"Error loading game sprites: {e}")
        return
    
    # Initialize game
    falling_objects = []
    spawn_timer = 0
    score = 0
    
    # Store original positions
    original_y = tabucat_sprite.y
    original_x = tabucat_sprite.x
    
    # Move tabucat to game group and position at bottom
    try:
        if tabucat_sprite in splash:
            splash.remove(tabucat_sprite)
    except ValueError:
        pass
    
    tabucat_play_sprite.y = display.height - 96  # Position the new sprite at the bottom
    minigame_group.append(tabucat_play_sprite)
    
    # Show game UI
    splash.append(minigame_group)
    print("Game group added to splash.")
    
    # Game loop
    while hearts > 0 and not minigame_over:
        #time
        current_time = time.monotonic()

        if current_time - start_time >= minigame_duration:
            minigame_over = True
            continue
                
    # Continuous animation like main screen
        tabucat_play_sprite[0] = frame
        frame = (frame + 1) % (tabucat_play_sheet.width // tile_width)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                minigame_over = True
                minigame_active = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    up = True
                if event.key == pygame.K_LEFT:
                    left = True
                if event.key == pygame.K_RIGHT:
                    right = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    up = False
                if event.key == pygame.K_LEFT:
                    left = False
                if event.key == pygame.K_RIGHT:
                    right = False
                
        if minigame_paused:
            keys = pygame.key.get_pressed()

            if keys[pygame.K_LEFT] and keys[pygame.K_RIGHT]:
                minigame_paused = False
                
            if keys[pygame.K_UP] and keys[pygame.K_LEFT]:
                minigame_over = True
                hearts = 0
                break
        
        if not minigame_paused:
            # Move cat
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                tabucat_play_sprite.x = max(-32, tabucat_play_sprite.x - speed)
                tabucat_play_sprite[0] = frame  # Use left-facing frames
            if keys[pygame.K_RIGHT]:
                tabucat_play_sprite.x = min(display.width - 32, tabucat_play_sprite.x + speed)
                tabucat_play_sprite[0] = frame  # Use right-facing frames
            if keys[pygame.K_LEFT] and keys[pygame.K_RIGHT]:
                minigame_paused = True

            # Spawn new objects
            spawn_timer += 1
            if spawn_timer >= 30:
                spawn_timer = 0
                if random.random() < 0.5:
                    new_sprite = displayio.TileGrid(
                        mouse_bitmap,
                        pixel_shader=mouse_bitmap.pixel_shader,
                        width=1,
                        height=1,
                        tile_width=32,
                        tile_height=32,
                        x=random.randint(0, display.width - 32)
                    )
                    is_mouse = True
                else:
                    new_sprite = displayio.TileGrid(
                        yarn_bitmap,
                        pixel_shader=yarn_bitmap.pixel_shader,
                        width=1,
                        height=1,
                        tile_width=32,
                        tile_height=32,
                        x=random.randint(0, display.width - 32)
                    )
                    is_mouse = False
                minigame_group.append(new_sprite)
                falling_objects.append(FallingObject(new_sprite, is_mouse))
            
            # Update falling objects
            for obj in falling_objects[:]:
                if obj.update():  # Object was missed
                    hearts -= 1
                    print(f"Heart lost! Remaining hearts: {hearts}")
                    if hearts in heart_images:
                        heart_sprite.bitmap = heart_images[hearts]
                    falling_objects.remove(obj)
                    minigame_group.remove(obj.sprite)
                elif obj.active:
                    # Improved collision detection with a smaller hitbox
                    cat_hitbox = {
                        'x': tabucat_play_sprite.x + 20,       # Adjusted x position for smaller hitbox
                        'y': tabucat_play_sprite.y + 12,       # Adjusted y position for smaller hitbox
                        'width': 20,                       # Reduced width from 24 to 20
                        'height': 40                       # Reduced height from 48 to 40
                    }
                    
                    if (obj.y + 32 > cat_hitbox['y'] and
                        obj.y < cat_hitbox['y'] + cat_hitbox['height'] and
                        obj.x + 32 > cat_hitbox['x'] and
                        obj.x < cat_hitbox['x'] + cat_hitbox['width']):
                        score += 10 if obj.is_mouse else 5
                        print(f"Collision detected! Score increased to {score}")
                        if font and game_score_label:
                            game_score_label.text = f"Score: {score}"
                        falling_objects.remove(obj)
                        minigame_group.remove(obj.sprite)
            
            time.sleep(0.1)
        if minigame_paused:
            if up and left:
                minigame_over = True
                hearts = 0

    print(f"Final Score: {score}")
    
    # Add love points based on score
    love_points = min(100, love_points + (score))  # Add love points based on score
    update_love_bar()  # Update the love bar display
    
    # Wait for a moment before returning
    time.sleep(1)
    
    # Clean up and restore sprites
    try:
        splash.remove(minigame_group)
        print("Game group removed from splash.")
    except ValueError:
        pass
    
    # Restore tabucat position and add back to splash
    tabucat_play_sprite.x = original_x
    tabucat_play_sprite.y = original_y
    
    try:
        if tabucat_sprite not in splash:
            splash.append(tabucat_sprite)
        if love_bar_group not in splash:
            splash.append(love_bar_group)
        if brush_sprite not in splash:
            splash.append(brush_sprite)
        print("Main UI elements restored to splash.")
    except ValueError:
        pass

    # Clean up and remove the game_score_label after the game ends
    try:
        minigame_group.remove(game_score_label)
        print("Game score label removed from game group.")
    except ValueError:
        pass

    minigame_active = False  # Indicate that the game has ended

    # After the game ends, restore UI elements to their original positions
    try:
        love_bar_group.x = 4  # Original x position for love bar
        brush_sprite.x = display.width - 30  # Original x position for brush sprite
        splash.append(love_bar_group)  # Restore love bar group
        splash.append(brush_sprite)  # Restore brush sprite
        print("Love bar and brush sprite restored to splash.")  # Debugging output
    except ValueError:
        pass

# Animation variables
frame = 0

# Movement variables
x_speed = 0  # Horizontal movement speed
speed = 4  # Pixels per frame for walking

# Animation control
brush_frame = 0  # Renamed from current_brush_frame
animation_start_time = 0
pet_frame = 0
chomp_frame = 0

# Load the bitmap font
font = bitmap_font.load_font("ter-u12.bdf")

# Debugging output to check variable states
print(f"brushing_active: {brushing_active}, petting_active: {petting_active}, game_active: {game_active}")

# Animation control variables
frame_delay = 0.15  # Delay in seconds between frames
last_frame_time = time.monotonic()  # Track the last frame update time

# Function to display the game over screen
def show_game_over_screen():
    global game_over, running, love_points, minigame_active, brushing_active, petting_active, feeding_active
    # Create a new display group for the game over screen
    game_over_group = displayio.Group()

    # Create a background for the game over screen
    game_over_bg = displayio.Bitmap(display.width, display.height, 1)
    bg_palette = displayio.Palette(1)
    bg_palette[0] = 0x000000  # Black background
    game_over_bg_sprite = displayio.TileGrid(game_over_bg, pixel_shader=bg_palette)
    game_over_group.append(game_over_bg_sprite)

    # Update the game over label creation
    game_over_label = label.Label(
        font,
        text="Game Over!",
        color=0xFFFFFF,
        x=(display.width // 2) - 30,  # Centered based on text width
        y=(display.height // 2) - 20
    )
    game_over_group.append(game_over_label)
    # Update the restart label creation
    restart_label = label.Label(
        font,
        text='  LEFT+RIGHT to \n    Restart\n   UP to Quit',
        color=0xFFFFFF,
        x=(display.width // 2) - 45,  # Centered based on text width
        y=(display.height // 2) + 10
    )
    game_over_group.append(restart_label)

    # Show the game over screen
    splash.append(game_over_group)
    # Wait for restart input
    while running:
        keys = pygame.key.get_pressed()
        
        # Handle restart
        if keys[pygame.K_LEFT] and keys[pygame.K_RIGHT]:
            # Reset all game states
            love_points = 10
            game_over = False
            minigame_active = False
            brushing_active = False
            petting_active = False
            feeding_active = False
            
            # Remove game over screen
            try:
                splash.remove(game_over_group)
            except ValueError:
                pass
            
            # Restore initial UI elements
            love_bar_group.x = 4
            brush_sprite.x = display.width - 30
            update_love_bar()
            break
            
        # Handle quit
        if keys[pygame.K_UP]:
            running = False
            break
            
        # Process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                return
            
        time.sleep(0.1)


# Main loop
running = True
up = False
left = False
right = False
while running:
    # Get current key states once per frame
    keys = pygame.key.get_pressed()
    
    # Handle game over restart
    if game_over:
        show_game_over_screen()
        continue  # Skip to next iteration

    current_time = time.monotonic()
    # Process Pygame events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Quit if window is closed
            pygame.quit()
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP: 
                up = True
            if event.key == pygame.K_LEFT:
                left = True
            if event.key == pygame.K_RIGHT:
                right = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                up = False
            if event.key == pygame.K_LEFT:
                left = False
            if event.key == pygame.K_RIGHT:
                right = False
        
        # Handle game over
        if left:
            if minigame_active:
                if up:
                    minigame_over = True  # Set minigame_over to True
                    continue
            if game_over:
                if up:
                    print("Game Over condition met")  # Debugging output
                    game_active = False
                    show_game_over_screen()  # Show the game over screen
                    love_points = 10
                    # Reset game state variables for restart
                    score = 0
                    hearts = 3
                    minigame_over = True
                    running = True  # Keep running to allow restart
                    # Do not start the minigame automatically
                    continue  # Skip to the next iteration of the loop

        # Handle other actions only if the game is active
        if up:
            if not minigame_active:
                if not right and not left and not brushing_active:
                    start_brushing()
                if right and not petting_active:
                    start_petting()
                if left and not feeding_active:
                    start_feeding()
        if right:
            if not minigame_active:
                if left:
                    play()

    if running:  # Only update if running is still True
        update_love_bar()
        # Check for keyboard inputs
        if keys[pygame.K_LEFT]:
            x_speed = -speed
        elif keys[pygame.K_RIGHT]:
            x_speed = speed
        else:
            x_speed = 0

        update_cat_position()

        tabucat_sprite[0] = frame
        frame = (frame + 1) % (tabucat_sheet.width // tile_width) 

        # love_points = love_points - 0.5  # Uncomment for auto-decay
        # update_love_bar()

        # Handle brushing animation
        if brushing_active:
            brush_animation[0] = brush_frame
            brush_frame = (brush_frame + 1) % 13  # 13 frames total

            # Auto-stop after full animation cycle
            if time.monotonic() - animation_start_time >= 2.6:  # 13 frames * 0.2s
                stop_brushing()

        if not (brushing_active or petting_active or feeding_active or minigame_active):
            love_points = max(0, love_points - 0.1)  # Ensure doesn't go below 0
            update_love_bar()
            if love_points <= 0 and not game_over:
                game_over = True
                show_game_over_screen()

        # Handle petting animation
        if petting_active:
            petting_animation[0] = pet_frame
            pet_frame = (pet_frame + 1) % 16  # Ensure this wraps correctly

            if time.monotonic() - animation_start_time >= 1.2:  # 16 frames * 0.2s
                stop_petting()  # Ensure this is called only after the full animation cycle

        # Handle feeding animation
        if feeding_active:
            feeding_animation[0] = chomp_frame
            chomp_frame = (chomp_frame + 1) % 16  # Ensure this wraps correctly
            
            if time.monotonic() - animation_start_time >= 1.6:
                stop_feeding()

    # Adjust the sleep time to slow down the animation      
    time.sleep(0.1)

# Quit Pygame after the main loop ends
pygame.quit()