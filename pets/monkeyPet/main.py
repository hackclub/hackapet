# Imports
import displayio
import pygame
import time
import random
from blinka_displayio_pygamedisplay import PyGameDisplay
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import label

# Vars
frame = 0
playerSpeed = 3
stuffSpeed = 2
canMove = True
gameOver = False
score = 0
spawnedlvl2 = False
spawnedlvl3 = False

# Start
pygame.init()

display = PyGameDisplay(width=128, height=128)
splash = displayio.Group()
display.show(splash)

# Background
background = displayio.OnDiskBitmap("sprites/background.bmp")
bg_sprite = displayio.TileGrid(background, pixel_shader=background.pixel_shader)
splash.append(bg_sprite)

# Monkey stuff
monkey_sheet = displayio.OnDiskBitmap("sprites/monkeyPet.bmp")
tile_width = 48
tile_height = 41
monkey_sprite = displayio.TileGrid(
    monkey_sheet,
    pixel_shader=monkey_sheet.pixel_shader,
    width=1,
    height=1,
    tile_width=tile_width,
    tile_height=tile_height,
    default_tile=0,
    x=(display.width - tile_width) // 2,  
    y=display.height - tile_height - 10     
)
splash.append(monkey_sprite)

# Banna stuff
banna_bitmap = displayio.OnDiskBitmap("sprites/banna.bmp")
bannas = []
trash_bitmap = displayio.OnDiskBitmap("sprites/trash.bmp")
trashs = []
def spawn():
    if gameOver == False:
        x_position = random.randint(0, display.width - banna_bitmap.width)
        banna_sprite = displayio.TileGrid(
            banna_bitmap,
            pixel_shader=banna_bitmap.pixel_shader,
            width=1,
            height=1,
            tile_width=banna_bitmap.width,
            tile_height=banna_bitmap.height,
            x=x_position,
            y=0
        )

        x_position = random.randint(0, display.width - trash_bitmap.width)
        trash_sprite = displayio.TileGrid(
            trash_bitmap,
            pixel_shader=trash_bitmap.pixel_shader,
            width=1,
            height=1,
            tile_width=trash_bitmap.width,
            tile_height=trash_bitmap.height,
            x=x_position,
            y=0
        )

        bannas.append(banna_sprite)
        splash.append(banna_sprite)

        trashs.append(trash_sprite)
        splash.append(trash_sprite)
    else:
        pass

# Collisions check
def checkCollision(sprite1, sprite2):
    return (sprite1.x + 4 < sprite2.x + 4 and 
            sprite1.x + 48 > sprite2.x + 8 and 

            sprite1.y + 4 < sprite2.y + 18 and 
            sprite1.y + 32 > sprite2.y + 8
            )


# Game loop
spawn()
# more text stuff
font = bitmap_font.load_font("Helvetica-Bold-16.bdf") 
scoretext = label.Label(font, text="Score: ", color=0xffffff, x=5 , y=10)
splash.append(scoretext)

font = bitmap_font.load_font("Helvetica-Bold-16.bdf") 
scoreArea = label.Label(font, text=("     0"), color=0xffffff, x=20 , y=10)
splash.append(scoreArea)

font = bitmap_font.load_font("Helvetica-Bold-16.bdf") 
gameoverScreen = label.Label(font, text=("   Gameover \n  Press down\n to play again \n "), color=0xffffff, x=5 , y=10)
gameoverScreen.background_color = 0x000000
splash.append(gameoverScreen)
gameoverScreen.hidden = True

while True:

    key = pygame.key.get_pressed()

    if key[pygame.K_LEFT] and canMove == True:
        monkey_sprite[0] = frame
        frame = (frame + 1) % (monkey_sheet.width // tile_width)
        monkey_sprite.flip_x = False
        monkey_sprite.x -= playerSpeed

    if key[pygame.K_RIGHT] and canMove == True:
        monkey_sprite[0] = frame
        frame = (frame + 1) % (monkey_sheet.width // tile_width)
        monkey_sprite.flip_x = True
        monkey_sprite.x += playerSpeed

    if key[pygame.K_DOWN] and gameOver == True:
        canMove = True
        gameOver = False
        spawn()
        gameoverScreen.hidden = True

    if display.check_quit():
        break

    if score == 10 and spawnedlvl2 == False:
        spawn()
        spawnedlvl2 = True
    elif score == 20 and spawnedlvl3 == False:
        spawn()
        spawnedlvl3 = True
    

    for i in bannas:
        i.y += stuffSpeed
        if i.y > display.height:
            splash.remove(i)
            bannas.remove(i)
            spawn()
        elif checkCollision(monkey_sprite, i):
            splash.remove(i)
            bannas.remove(i)
            spawn()
            score = score + 1
            scoreArea.text = "     " + score.__str__()

    for i in trashs:
        i.y += random.randint(1, (3 + stuffSpeed))
        if i.y > display.height:
            splash.remove(i)
            trashs.remove(i)
        elif checkCollision(monkey_sprite, i):
            splash.remove(i)
            trashs.remove(i)
            for i in bannas:
                splash.remove(i)
                bannas.remove(i)
            canMove = False
            gameOver = True
            gameoverScreen.hidden = False
            score = 0
            scoreArea.text = "     " + score.__str__()

        if monkey_sprite.x >= 128:
            monkey_sprite.x = -20
        elif monkey_sprite.x <= -20:
            monkey_sprite.x = 128

    time.sleep(0.1)