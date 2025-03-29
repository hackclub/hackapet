import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
import pygame
import random
import time
import threading

pygame.init()

display = PyGameDisplay(width=128, height=128)
splash = displayio.Group()
display.show(splash)

lab_background = displayio.OnDiskBitmap("lab.bmp")
brain_sheet = displayio.OnDiskBitmap("brain.bmp")
brainRight_sheet = displayio.OnDiskBitmap("brainRight.bmp")
downArr = displayio.OnDiskBitmap("downArr.bmp")
leftArr = displayio.OnDiskBitmap("leftArr.bmp")
rightArr = displayio.OnDiskBitmap("rightArr.bmp")


bg_sprite = displayio.TileGrid(lab_background, pixel_shader=lab_background.pixel_shader)
splash.append(bg_sprite)

start_screen = displayio.OnDiskBitmap("start.bmp") 


brain_sprite = displayio.TileGrid(
    brain_sheet,
    pixel_shader=brain_sheet.pixel_shader,
    width=1,
    height=1,
    tile_width=32,
    tile_height=32,
    x=(display.width - 32) // 2,
    y=(display.height - 32) // 2,
)
splash.append(brain_sprite)

arrow_positions = {
    "DOWN": (48, 90),  
    "LEFT": (6, 48),
    "RIGHT": (90, 48),
}
arrow_sprites=[downArr, leftArr, rightArr]
arrows = {}
i=0
for direction, (x, y) in arrow_positions.items():
    arrow = displayio.TileGrid(
        arrow_sprites[i],
        pixel_shader=arrow_sprites[i].pixel_shader,
        width=1,
        height=1,
        tile_width=32,
        tile_height=32,
        x=x,
        y=y,
    )
    arrows[direction] = arrow
    splash.append(arrow)
    i+=1


start_sign = displayio.TileGrid(
    start_screen,
    pixel_shader=start_screen.pixel_shader,
    width=21,
    height=1,
    tile_width=128,
    tile_height=128,
    x=0,
    y=0
)
splash.append(start_sign)


sequence = []
player_input = []
waiting_for_input = False
game_state = "start"  
death_sign = None

def blink_arrow(direction):
    arrow = arrows[direction]
    splash.remove(arrow)
    time.sleep(0.15)  
    splash.insert(2,arrow)
    time.sleep(0.15)  
    
def blink_brain():
    global brain_sprite
    splash.remove(brain_sprite) 
    new_brain_sprite = displayio.TileGrid(
        brainRight_sheet ,
        pixel_shader=brainRight_sheet.pixel_shader ,
        width=1,
        height=1,
        tile_width=32,
        tile_height=32,
        x=(display.width - 32) // 2,
        y=(display.height - 32) // 2,
    )
    brain_sprite = new_brain_sprite 
    splash.append(brain_sprite) 
    time.sleep(0.15)
    splash.remove(brain_sprite)
    new_brain_sprite = displayio.TileGrid(
        brain_sheet ,
        pixel_shader=brain_sheet.pixel_shader ,
        width=1,
        height=1,
        tile_width=32,
        tile_height=32,
        x=(display.width - 32) // 2,
        y=(display.height - 32) // 2,
    )
    brain_sprite = new_brain_sprite
    splash.insert(1,brain_sprite) 
    time.sleep(.15)

def play_sequence():
    global waiting_for_input
    pygame.event.set_blocked(pygame.KEYDOWN)
    waiting_for_input = False
    time.sleep(0.5)
    for direction in sequence:
        blink_arrow(direction)
        time.sleep(0.2)
    waiting_for_input = True
    pygame.event.clear()
    pygame.event.set_allowed(pygame.KEYDOWN)



current_frame_start=0;
def display_game_over():
    global death_sign
    death = displayio.OnDiskBitmap("restart2.bmp")
    death_sign = displayio.TileGrid(
        death,
        pixel_shader=death.pixel_shader,
        width=8,
        height=1,
        tile_width=128,
        tile_height=128,
        x=0,
        y=0 
        
    )
    splash.append(death_sign)
    for k in range(8):
        death_sign[0] = k  
        time.sleep(.1)

def display_start():
    global current_frame_start
    current_frame_start = (current_frame_start + 1) % 21
    start_sign[0] = current_frame_start  
    time.sleep(.1)

waiting_for_input=False
while True:
    if game_state == "start":
        display_start()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if game_state == "start" and event.key == pygame.K_DOWN:
                splash.remove(start_sign)  # Hide start screen
                game_state = "playing"
                sequence.append(random.choice(list(arrows.keys())))  # Initial sequence
                play_sequence()
            
            elif game_state == "game_over" and event.key == pygame.K_DOWN:
                splash.remove(death_sign)  
                sequence.clear()  
                player_input.clear()
                game_state = "playing"
                waiting_for_input = False
                sequence.append(random.choice(list(arrows.keys())))
                play_sequence()
                continue
            
            elif event.key in [pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT] and waiting_for_input and game_state == "playing":
                if event.key == pygame.K_DOWN:
                    player_input.append("DOWN")
                    blink_brain_thread = threading.Thread(target=blink_brain, daemon=True)
                    blink_arrow_thread = threading.Thread(target=blink_arrow, args=("DOWN",), daemon=True)
                elif event.key == pygame.K_LEFT:
                    player_input.append("LEFT")
                    blink_brain_thread = threading.Thread(target=blink_brain, daemon=True)
                    blink_arrow_thread = threading.Thread(target=blink_arrow, args=("LEFT",), daemon=True)
                elif event.key == pygame.K_RIGHT:
                    player_input.append("RIGHT")
                    blink_brain_thread = threading.Thread(target=blink_brain, daemon=True)
                    blink_arrow_thread = threading.Thread(target=blink_arrow, args=("RIGHT",), daemon=True)

                blink_brain_thread.start()
                blink_arrow_thread.start()
            if player_input != sequence[:len(player_input)] and game_state == "playing":
                game_state = "game_over"
                display_game_over()
            elif len(player_input) == len(sequence):
                waiting_for_input = False
                player_input.clear()
                sequence.append(random.choice(list(arrows.keys())))
                play_sequence()
    if game_state == "playing" and not waiting_for_input:
        sequence.append(random.choice(list(arrows.keys())))
        play_sequence()
    
