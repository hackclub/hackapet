import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
import pygame
import time
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font  # **Import bitmap font**
import random
import sys



# Load the bitmap font
font = bitmap_font.load_font("LeagueSpartan-Bold-16.bdf")  # **Make sure this matches your font file**


pygame.init()

display = PyGameDisplay(width=128, height=128)
splash = displayio.Group()
display.show(splash)

bathtub_background = displayio.OnDiskBitmap("bathtub.bmp")
lightsea = displayio.OnDiskBitmap("lightSea.bmp")
darksea = displayio.OnDiskBitmap("darkSea.bmp")
restart = displayio.OnDiskBitmap("restart.bmp")
seakingdom = displayio.OnDiskBitmap("seakingdom.bmp")
finalText = displayio.OnDiskBitmap("finaltext.bmp")
winText = displayio.OnDiskBitmap("wintext.bmp")
lostText = displayio.OnDiskBitmap("losttext.bmp")

bg_sprite1 = displayio.TileGrid(
    bathtub_background,
    pixel_shader=bathtub_background.pixel_shader,
    width=1,
    height=1,
    tile_width=128,
    tile_height=128,
    default_tile=0,
    x=(display.width - 128) // 2,  
    y=display.height - 128 - 10     
)
# bg_sprite1 = displayio.TileGrid(bathtub_background, pixel_shader=bathtub_background.pixel_shader)

bg_sprite2 = displayio.TileGrid(lightsea, pixel_shader=lightsea.pixel_shader)
# playButton = displayio.TileGrid(restart, pixel_shader=restart.pixel_shader)
bg_sprite3 = displayio.TileGrid(darksea, pixel_shader=darksea.pixel_shader)
bg_sprite4 = displayio.TileGrid(seakingdom, pixel_shader=seakingdom.pixel_shader)

splash.append(bg_sprite1)
# splash.append(playButton)




anglerfish_sheet = displayio.OnDiskBitmap("anglerfishV2red.bmp")

tile_width = 64
tile_height = 64

anglerfish_sprite = displayio.TileGrid(
    anglerfish_sheet,
    pixel_shader=anglerfish_sheet.pixel_shader,
    width=1,
    height=1,
    tile_width=tile_width,
    tile_height=tile_height,
    default_tile=0,
    x=(display.width - tile_width) // 2,  
    y=display.height - tile_height - 10     
)

winText_sprite = displayio.TileGrid(
    winText,
    pixel_shader=winText.pixel_shader,
    width=1,
    height=1,
    tile_width=tile_width,
    tile_height=tile_height,
    default_tile=0,
    x=(display.width - tile_width) // 2,  
    y=display.height - tile_height - 10     
)
lostText_sprite = displayio.TileGrid(
    lostText,
    pixel_shader=lostText.pixel_shader,
    width=1,
    height=1,
    tile_width=tile_width,
    tile_height=tile_height,
    default_tile=0,
    x=(display.width - tile_width) // 2,  
    y=display.height - tile_height - 10     
)

finalText_sprite = displayio.TileGrid(
    finalText,
    pixel_shader=finalText.pixel_shader,
    width=1,
    height=1,
    tile_width=tile_width,
    tile_height=tile_height,
    default_tile=0,
    x=(display.width - tile_width) // 2,  
    y=display.height - tile_height - 10     
)
restart_sprite = displayio.TileGrid(
    restart,
    pixel_shader=restart.pixel_shader,
    width=1,
    height=1,
    tile_width=tile_width,
    tile_height=tile_height,
    default_tile=0,
    x=(display.width - tile_width) // 2,  
    y=display.height - tile_height - 10     
)



fish_bitmap = displayio.OnDiskBitmap("fish.bmp")

fishs = []

# **1️⃣ Add a Score Label**
points = 0




def spawn_fish():
    x_position = random.randint(0, display.width - fish_bitmap.width)
    fish = displayio.TileGrid(
        fish_bitmap,
        pixel_shader=fish_bitmap.pixel_shader,
        width=1,
        height=1,
        tile_width=fish_bitmap.width,
        tile_height=fish_bitmap.height,
        x=x_position,
        y=-32
    )
    fishs.append(fish)
    splash.append(fish)

# Function to check for collisions
def check_collision(sprite1, sprite2):
    return (
        sprite1.x < sprite2.x + 20 and
        sprite1.x + 20 > sprite2.x and
        sprite1.y < sprite2.y + 20 and
        sprite1.y + 20 > sprite2.y
    )

death = displayio.OnDiskBitmap("restart.bmp")

def display_game_over():
    global death_hi
    death_hi = displayio.TileGrid(
        lostText,
        pixel_shader=lostText.pixel_shader,
        width=1,
        height=1,
        tile_width=64,
        tile_height=64,
        default_tile=0,
        x=(display.width - 64) // 2,  
        y=(display.height - 64) // 2  
    )
    splash.append(death_hi)
    for i in fishs:
        splash.remove(i)
    fishs.clear()
    splash.remove(anglerfish_sprite)
    splash.remove(score_label)
    splash.remove(timer_label)
    time.sleep(3)


    # show score on screen


def winSequence():
    for i in fishs:
        splash.remove(i)
    fishs.clear()
    splash.remove(anglerfish_sprite)
    splash.append(bg_sprite4)
    time.sleep(3)
    splash.append(winText_sprite)
    time.sleep(3)
    splash.append(finalText_sprite)
    splash.remove(winText_sprite)
    # show score on screen
    time.sleep(3)
    splash.remove(finalText_sprite)
    time.sleep(1)
    splash.append(restart_sprite)




frame = 0
speed = 4 
game_over = True





while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN and game_over == True:
                for i in fishs:
                    splash.remove(i)
                fishs.clear()
                # splash.remove(death_hi)
                splash.append(bg_sprite2)
                time.sleep(1)
                if anglerfish_sprite not in splash:
                    splash.append(anglerfish_sprite)
                # splash.remove(playButton)
                points=0
                # score_label.text = f"Score: {points}"  # **2️⃣ Reset score on restart**
                game_over = False
                score_label = label.Label(font, text=f"Score: {points}", color=0000, x=5, y=5)
                splash.append(score_label)
                start_time = pygame.time.get_ticks()  # Start the timer
                timer_duration = 90000  # 90 seconds (in milliseconds)
                timer_label = label.Label(font, text="Time: 60", color=0x0000, x=5, y=20)
                splash.append(timer_label)


            


               

            


    keys = pygame.key.get_pressed()
        
    if game_over == False:
        elapsed_time = pygame.time.get_ticks() - start_time
        remaining_time = max(0, (timer_duration - elapsed_time) // 1000)

        # Update the timer label instead of appending new ones
        timer_label.text = f"Time: {remaining_time}"

        if points == 100:
            # score_label = label.Label(font, text=f"Score: {points}", color=0000, x=5, y=5)
            # splash.remove(bg_sprite1)
            splash.insert(2, bg_sprite3)	
            # splash.append(score_label)
            # start_time = pygame.time.get_ticks()



        if points == 300:
            winSequence()
            game_over = True
            points=0

        if keys[pygame.K_LEFT]: 
            anglerfish_sprite.x -= speed
        if keys[pygame.K_RIGHT]:
            anglerfish_sprite.x += speed
        if random.random() < 0.7:  # spawn rate
            spawn_fish()
        if remaining_time == 0:
            display_game_over()
            game_over = True
            splash.append(bg_sprite1)


    # while game_over == False:
    #     clock=pygame.time.Clock()

    #     t=0
    #     # creating a loop for 5 iterations
    #     while t<5:
            
    #         # setting fps of program to max 1 per second
    #         clock.tick(1)
            
    #         # printing time used in the previous tick
    #         print(clock.get_time())
            
    #         # printing compute the clock framerate
    #         print(clock.get_fps())
    #         t=t+1



    for fish in fishs:
        fish.y += 5 
        if fish.y > display.height:
            splash.remove(fish)
            fishs.remove(fish)
        elif check_collision(anglerfish_sprite, fish):
            points=points+1
            score_label.text = f"Score: {points}"  # **3️⃣ Update score when collecting fish**
            print("Points: ", points)
            splash.remove(fish)
            fishs.remove(fish)



    anglerfish_sprite[0] = frame
    frame = (frame + 1) % (anglerfish_sheet.width // 64)
    bg_sprite1[0] = frame
    frame = (frame + 1) % (bathtub_background.width // 128)


    
    time.sleep(0.1)
