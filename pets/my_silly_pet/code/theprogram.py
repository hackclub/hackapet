import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
import pygame
import time


#pygame.init()
#display = PyGameDisplay(width=128, height=128)
#splash = displayio.Group()
#display.show(splash)

scale = 5
display_width = 128 * scale
display_height = 128 * scale
global offset
offset = 15


# initialize display
display = PyGameDisplay(width=display_width, height=display_height)
splash = displayio.Group(scale=scale)
display.show(splash)

hamster_background = displayio.OnDiskBitmap("background.bmp")
bg_sprite = displayio.TileGrid(hamster_background, pixel_shader=hamster_background.pixel_shader)
splash.append(bg_sprite)

cat_sheet = displayio.OnDiskBitmap("arifacespritesmile.bmp")

def load_cat_sprite(file):
    global cat_sheet
    try:
      cat_sheet = displayio.OnDiskBitmap(file)
      print("Bitmap loaded successfully.")
    except Exception as e:
     print(f"Failed to load bitmap: {e}")



tile_width = 64
tile_height = 64

hamsteroutfit_bitmap = displayio.OnDiskBitmap("arihamstersuit.bmp")

hamstersprite = displayio.TileGrid(
    hamsteroutfit_bitmap, pixel_shader=hamsteroutfit_bitmap.pixel_shader, 
    width=1, 
    height=1, 
    tile_width=tile_width, 
    tile_height=tile_height, 
    default_tile=0, 
    x=33, y=70-offset
)

splash.append(hamstersprite)


cat_sprite = displayio.TileGrid(
    cat_sheet,
    pixel_shader=cat_sheet.pixel_shader,
    width=1,
    height=1,
    tile_width=tile_width,
    tile_height=tile_height,
    default_tile=0,
    x=32,
    y=32-offset
   
   
)


splash.append(cat_sprite)

print("Display initialized and face sprite added.")



# Initialize hunger variable and decay rate
hunger = 100
decay_rate = 0.999999  # Adjust this value to control the decay rate
#decay_rate = 0.6
game_over=False


# Function to update hunger
def update_hunger():
    global hunger
    global game_over
    global cat_sprite
    global cat_sheet
    if hunger > 0:
        hunger *= decay_rate
        print(f"Hunger: {hunger:.2f}")
    if hunger < 50:
        try:
            cat_sheet = displayio.OnDiskBitmap("arifacesprite.bmp")
            print("Switched to neutral sprite.")
        except Exception as e:
            print(f"Failed to load neutral bitmap: {e}")
            pygame.quit()
            exit()
        # Update the sprite with the new bitmap
        cat_sprite = displayio.TileGrid(
            cat_sheet,
            pixel_shader=cat_sheet.pixel_shader,
            width=1,
            height=1,
            tile_width=tile_width,
            tile_height=tile_height,
            default_tile=0,
            x=32,
            y=32-offset
        )
        splash.append(cat_sprite)
    
    if hunger < 10:
        try:
            cat_sheet = displayio.OnDiskBitmap("arisad.bmp")
            print("Switched to SAD sprite.")
        except Exception as e:
            print(f"Failed to load SAD bitmap: {e}")
            pygame.quit()
            exit()
        # Update the sprite with the new bitmap
        cat_sprite = displayio.TileGrid(
            cat_sheet,
            pixel_shader=cat_sheet.pixel_shader,
            width=1,
            height=1,
            tile_width=tile_width,
            tile_height=tile_height,
            default_tile=0,
            x=32,
            y=32-offset
        )
        splash.append(cat_sprite)

    if hunger <= 0.05:
        game_over=True
        display_restart_screen()
        print("Game over! Press SPACE to restart.")



restart_sheet = displayio.OnDiskBitmap("restart.bmp")

def display_restart_screen():
    global restart_sprite

    restart_sprite = displayio.TileGrid(
        restart_sheet,
        pixel_shader=restart_sheet.pixel_shader,
        width=1,
        height=1,
        tile_width= 64,
        tile_height= 32,
        default_tile=0,
        x=32,
        y=32
    )
    splash.append(restart_sprite)

def feed_sprite():
    global hunger
    print("Feeding sprite")
    hunger = 100  # Reset hunger to 100 when fed
    try:
            cat_sheet = displayio.OnDiskBitmap("arifacespritesmile.bmp")
            print("Switched to smile sprite.")
    except Exception as e:
            print(f"Failed to load neutral bitmap: {e}")
            pygame.quit()
            exit()
        
    # Update the sprite with the new bitmap
    cat_sprite = displayio.TileGrid(
        cat_sheet,
        pixel_shader=cat_sheet.pixel_shader,
        width=1,
        height=1,
        tile_width=tile_width,
        tile_height=tile_height,
        default_tile=0,
        x=32,
        y=32-offset
    )
    splash.append(cat_sprite)

# Timer to update hunger every second
last_update_time = time.time()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    keys = pygame.key.get_pressed()



    # Move sprite left
    if keys[pygame.K_LEFT]:
        pass
    # Move sprite right
    if keys[pygame.K_RIGHT]:
        pass
    # Move sprite down
    if keys[pygame.K_SPACE]:
        if game_over == True:
            # Restart the game
            hunger = 100

            splash.remove(restart_sprite)      

            splash = displayio.Group(scale=scale)
            display.show(splash)
            #splash.append(bg_sprite)

            #cat_sprite = load_cat_sprite("arifacespritesmile.bmp")

            #splash.append(hamstersprite)


            cat_sheet = displayio.OnDiskBitmap("arifacesprite.bmp")
            print("Switched to neutral sprite.")

        # Update the sprite with the new bitmap
            cat_sprite = displayio.TileGrid(
            cat_sheet,
                pixel_shader=cat_sheet.pixel_shader,
                width=1,
                height=1,
                tile_width=tile_width,
                tile_height=tile_height,
                default_tile=0,
                x=32,
                y=32-offset
            )
            
            splash.append(bg_sprite)

            splash.append(hamstersprite)

            splash.append(cat_sprite)   
            game_over=False
            print("Game restarted")
        else:
            feed_sprite()

    # Update hunger every second
    current_time = time.time()
    if current_time - last_update_time >= 1:
        update_hunger()
        last_update_time = current_time



    # Update the display
    display.refresh()
    pygame.time.wait(100)

    