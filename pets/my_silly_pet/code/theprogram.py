import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
import pygame
import time


global state
state = "smiling"
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

hungerbarspritesheet = displayio.OnDiskBitmap("hungerbarspritesheet.bmp")
hungerbar_sprite = displayio.TileGrid(
    hungerbarspritesheet, pixel_shader=hungerbarspritesheet.pixel_shader,
    width=1, height=1, 
    tile_width=19, 
    tile_height=25, 
    default_tile=0, 
    x=4, 
    y=0,
)

splash.append(hungerbar_sprite)

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
#decay_rate = 0.999999  # Adjust this value to control the decay rate
decay_rate = 0.999993 # after exactly two weeks, it drops below 0.05
#decay_rate = 0.6
game_over=False


# Function to update hunger
def update_hunger():
    global hunger
    global game_over
    global cat_sprite
    global cat_sheet
    global state
    if hunger > 0:
        hunger *= decay_rate
        print(f"Hunger: {hunger:.4f}")

    if hunger < 10:
        try:
            if state != "sad":
                try:
                    splash.remove(cat_sprite)
                    print("Removed neutral sprite.")
                except:
                    print("neutral sprite removal failed")
                cat_sheet = displayio.OnDiskBitmap("arisad.bmp")
                is_sad = True
                print("Switched to SAD sprite.")
                state = "sad"
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
        #update hungerbar sprite sheet
        hungerbar_sprite[0] = 2  # Set tile to the 10% sprite

    
    elif hunger < 50:
        try:
            if state != "neutral":
                try: 
                    splash.remove(cat_sprite)
                    print("Removed happy sprite.")
                except:
                    print("happy sprite removal failed")
                cat_sheet = displayio.OnDiskBitmap("arifacesprite.bmp")
                print("Switched to neutral sprite.")
                state = "neutral"
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
        #update hungerbar sprite sheet
        hungerbar_sprite[0] = 1  # Set tile to the 50% sprite
    


    if hunger <= 0.05:
        game_over=True
        display_restart_screen()
        print("Game over! Press SPACE to restart.")



restart_sheet = displayio.OnDiskBitmap("restart.bmp")

def display_restart_screen():
    global restart_sprite

    restart_sprite = displayio.TileGrid(
        restart_sheet,
        pixel_shader=restart_sheet.pixel_shader
    )
    splash.append(restart_sprite)

def feed_sprite():
    global hunger
    print("Feeding sprite")
    hunger = 100  # Reset hunger to 100 when fed
    #try:
    #    splash.remove(cat_sprite)
    #    print("feed removed face sprite.")
    #except:
    #    print("sprite removal failed")

    # Load the star sprite
    star_sheet = displayio.OnDiskBitmap("starsprite.bmp")
    star_sprite = displayio.TileGrid(
        star_sheet,
        pixel_shader = star_sheet.pixel_shader,
        x = 5,
        y = -3
    )
    splash.append(star_sprite)

    # Timer to remove the star sprite after 0.5 seconds
    start_time = time.time()

    while time.time() - start_time < 0.5:
        # Move the star sprite upwards
        star_sprite.y -= 1  # Adjust the speed of movement as needed
        display.refresh()
        pygame.time.wait(50)  # Small delay for smooth animation

    # Remove the star sprite after 0.5 seconds
    splash.remove(star_sprite)

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
    # feed pet
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
    if current_time - last_update_time >= 1 and game_over == False:
        update_hunger()
        last_update_time = current_time



    # Update the display
    display.refresh()
    pygame.time.wait(100)

    