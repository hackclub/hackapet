import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
import pygame
import time

pygame.init()
display = PyGameDisplay(width=128, height=128)
splash = displayio.Group()
display.show(splash)

# Background Setup
background_sheet = displayio.OnDiskBitmap("background.bmp")
bg_frame_count = background_sheet.width // 128 
bg_sprite = displayio.TileGrid(
    background_sheet,
    pixel_shader=background_sheet.pixel_shader,
    width=1,
    height=1,
    tile_width=128,
    tile_height=128,
    default_tile=0
)
splash.append(bg_sprite)

# Blob Setup
blob_states = {
    "idle": ["default_idle.bmp", "default_idle_90.bmp", "default_idle_180.bmp", "default_idle_270.bmp"],
    "squish": ["default_squish.bmp", "default_squish_90.bmp", "default_squish_180.bmp", "default_squish_270.bmp"],
    "glitter_idle": ["glitter_idle.bmp", "glitter_idle_90.bmp", "glitter_idle_180.bmp", "glitter_idle_270.bmp"],
    "glitter_squish": ["glitter_squish.bmp", "glitter_squish_90.bmp", "glitter_squish_180.bmp", "glitter_squish_270.bmp"]
}

current_mode = "idle"  # Tracks state
rotation_index = 0  # 0° (0), 90° (1), 180° (2), 270° (3)
tile_width, tile_height = 64, 64

def create_blob_sprite():
    blob_sheet = displayio.OnDiskBitmap(blob_states[current_mode][rotation_index])
    return displayio.TileGrid(
        blob_sheet,
        pixel_shader=blob_sheet.pixel_shader,
        width=1,
        height=1,
        tile_width=tile_width,
        tile_height=tile_height,
        default_tile=0,
        x=(display.width - tile_width) // 2,
        y=display.height - tile_height - 10
    )

blob_sprite = create_blob_sprite()
splash.append(blob_sprite)

# Cookie Mode Setup
cookie_mode = False
cookie_sprite = None
cookie_image = "cookie.bmp"

# Konami Code: Down, Down, Down, Down, Left, Right, Left, Right, Down, Down
konami_code = [pygame.K_DOWN, pygame.K_DOWN, pygame.K_DOWN, pygame.K_DOWN,
               pygame.K_LEFT, pygame.K_RIGHT, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_DOWN]
konami_index = 0

frame = 0
bg_frame = 0

def update_blob():
    global blob_sprite, frame
    print(f"Updating blob: mode={current_mode}, rotation={rotation_index}")
    splash.remove(blob_sprite)
    blob_sprite = create_blob_sprite()
    splash.append(blob_sprite)
    frame = 0  # Reset frame count when updating the blob sprite

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                # Toggle Glitter Mode
                if "glitter_" in current_mode:
                    current_mode = current_mode.replace("glitter_", "")
                else:
                    current_mode = "glitter_" + current_mode
                update_blob()

            elif event.key == pygame.K_DOWN:
                # Toggle Squish Mode
                print("DOWN key pressed")
                if "_squish" in current_mode:
                    current_mode = current_mode.replace("_squish", "_idle")
                else:
                    current_mode = current_mode.replace("_idle", "_squish")
                print(f"New mode: {current_mode}")
                update_blob()

            elif event.key == pygame.K_RIGHT:
                # Cycle Rotations: 0° → 90° → 180° → 270° → 0°
                rotation_index = (rotation_index + 1) % 4
                update_blob()

            # Konami Code Detection
            if konami_index < len(konami_code) and event.key == konami_code[konami_index]:
                konami_index += 1
                if konami_index == len(konami_code):  # Full sequence completed
                    if not cookie_mode:
                        cookie_mode = True
                        cookie_sprite = displayio.TileGrid(
                            displayio.OnDiskBitmap(cookie_image),
                            pixel_shader=blob_sheet.pixel_shader,
                            x=(display.width - 64) // 2,
                            y=(display.height - 64) // 2
                        )
                        splash.append(cookie_sprite)
            else:
                konami_index = 0  # Reset if wrong key is pressed

    # Background Frame Cycling
    bg_sprite[0] = bg_frame
    bg_frame = (bg_frame + 1) % bg_frame_count

    # Blob Animation
    blob_sheet = displayio.OnDiskBitmap(blob_states[current_mode][rotation_index])
    blob_sprite[0] = frame
    frame = (frame + 1) % (blob_sheet.width // tile_width)

    time.sleep(0.1)
