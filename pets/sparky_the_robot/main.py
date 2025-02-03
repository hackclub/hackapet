import pygame
import time
import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
import adafruit_imageload
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font
import random
# import board
from PIL import Image

pygame.init()

display = PyGameDisplay(width=128, height=128)
splash = displayio.Group()
display.show(splash)

# Text
font = bitmap_font.load_font("Font.bdf")
fontColor = 0x0A133E



# Backgrounds
bg1 = displayio.OnDiskBitmap('Main_Background.bmp')
background1 = displayio.TileGrid(bg1, pixel_shader=bg1.pixel_shader)
splash.append(background1)

bg2 = displayio.OnDiskBitmap('Background_2.bmp')
background2 = displayio.TileGrid(bg2, pixel_shader=bg2.pixel_shader)

bg2Spritesheet = displayio.OnDiskBitmap('Background_2_Spritesheet.bmp')
background2Spritesheet = displayio.TileGrid(
    bg2Spritesheet,
    pixel_shader=bg2Spritesheet.pixel_shader,
    width=1,
    height=1,
    tile_width=128,
    tile_height=128,
)

# Buttons
buttons1 = displayio.OnDiskBitmap('Buttons.bmp')
upButtons = displayio.TileGrid(buttons1, pixel_shader=buttons1.pixel_shader, x=8, y=26)

buttons2 = displayio.OnDiskBitmap('Blue_Button.bmp')
blueButton = displayio.TileGrid(buttons2, pixel_shader=buttons2.pixel_shader, x=8, y=26)

buttons3 = displayio.OnDiskBitmap('Yellow_Button.bmp')
yellowButton = displayio.TileGrid(buttons3, pixel_shader=buttons3.pixel_shader, x=8, y=26)

buttons4 = displayio.OnDiskBitmap('Orange_Button.bmp')
orangeButton = displayio.TileGrid(buttons4, pixel_shader=buttons4.pixel_shader, x=8, y=26)

buttonsBackground = displayio.OnDiskBitmap('Game_Background.bmp')
buttonsBG = displayio.TileGrid(buttonsBackground, pixel_shader=buttonsBackground.pixel_shader, x=8, y=26)


# Sprite 1 (regular, resting)
robotSprite1, robotPal1 = adafruit_imageload.load('Resting_Spritesheet.bmp', bitmap=displayio.Bitmap, palette=displayio.Palette)
robotPal1.make_transparent(19)
robotTilegrid1 = displayio.TileGrid(
    robotSprite1,
    pixel_shader=robotPal1,
    width=1,
    height=1,
    tile_width=60,
    tile_height=66,
    x=33,
    y=50
)

# Sprite 2 (charging/sleeping)
robotSprite2, robotPal2 = adafruit_imageload.load('Sleeping_Spritesheet.bmp', bitmap=displayio.Bitmap, palette=displayio.Palette)
robotPal2.make_transparent(18)
robotTilegrid2 = displayio.TileGrid(
    robotSprite2,
    pixel_shader=robotPal2,
    width=1,
    height=1,
    tile_width=38,
    tile_height=44,
    x=83,
    y=70
)

# Sprite 3 (heart eyes)
robotSprite3, robotPal3 = adafruit_imageload.load('Heart_Eyes.bmp', bitmap=displayio.Bitmap, palette=displayio.Palette)
robotPal3.make_transparent(19)
robotTilegrid3 = displayio.TileGrid(
    robotSprite3,
    pixel_shader=robotPal3,
    width=1,
    height=1,
    tile_width=60,
    tile_height=66,
    x=33,
    y=50
)


# Sprite 4 (angry eyes)
robotSprite4, robotPal4 = adafruit_imageload.load('Angry_Eyes.bmp', bitmap=displayio.Bitmap, palette=displayio.Palette)
robotPal4.make_transparent(19)
robotTilegrid4 = displayio.TileGrid(
    robotSprite4,
    pixel_shader=robotPal4,
    width=1,
    height=1,
    tile_width=60,
    tile_height=66,
    x=33,
    y=50
)


# Sprite 5 (money eyes)
robotSprite5, robotPal5 = adafruit_imageload.load('Money_Eyes.bmp', bitmap=displayio.Bitmap, palette=displayio.Palette)
robotPal5.make_transparent(19)
robotTilegrid5 = displayio.TileGrid(
    robotSprite5,
    pixel_shader=robotPal5,
    width=1,
    height=1,
    tile_width=60,
    tile_height=66,
    x=33,
    y=50
)


# Sprite 6 (X eyes)
robotSprite6, robotPal6 = adafruit_imageload.load('X_Eyes.bmp', bitmap=displayio.Bitmap, palette=displayio.Palette)
robotPal6.make_transparent(19)
robotTilegrid6 = displayio.TileGrid(
    robotSprite6,
    pixel_shader=robotPal6,
    width=1,
    height=1,
    tile_width=60,
    tile_height=66,
    x=33,
    y=50
)


# Sprite 7 (wide eyes)
robotSprite7, robotPal7 = adafruit_imageload.load('Wide_Eyes.bmp', bitmap=displayio.Bitmap, palette=displayio.Palette)
robotPal7.make_transparent(19)
robotTilegrid7 = displayio.TileGrid(
    robotSprite7,
    pixel_shader=robotPal7,
    width=1,
    height=1,
    tile_width=60,
    tile_height=66,
    x=33,
    y=50
)


# Sprite 8 (happy eyes)
robotSprite8, robotPal8 = adafruit_imageload.load('Happy_Eyes.bmp', bitmap=displayio.Bitmap, palette=displayio.Palette)
robotPal8.make_transparent(19)
robotTilegrid8 = displayio.TileGrid(
    robotSprite8,
    pixel_shader=robotPal8,
    width=1,
    height=1,
    tile_width=60,
    tile_height=66,
    x=33,
    y=50
)


# Import variables
sourceIndex = 0
specialEyeList = [robotTilegrid3, robotTilegrid4, robotTilegrid5, robotTilegrid6, robotTilegrid7, robotTilegrid8]
mainRoom = True
bedRoom = False
charging = False
playingGame = False
inMachine = False
gameOver = False
displayingFunEyes = False
eyeNum = None


# Important functions
# This is for converting my png images that need to have transparent backgrounds, for some reason converting them to bmps externally wasn't working with adafruit_imageload. I only use this once per spritesheet, and delete the code that calls it as soon as it's done.
def png_to_indexed(filename, filter_color=(0, 255, 0)):
    img = Image.open(filename)
    img = img.convert('RGB')

    palette = []
    palette.extend(filter_color)

    colors = img.getcolors(maxcolors=256)
    if colors:
        for count, rgb in colors:
            if rgb != filter_color:
                palette.extend(rgb)

    while len(palette) < 768:
        palette.extend(filter_color)

    palette_img = Image.new('P', (1, 1))
    palette_img.putpalette(palette)
    indexed = img.quantize(colors=256, palette=palette_img)

    output_name = filename.rsplit('.', 1)[0] + '.bmp'
    indexed.save(output_name, "BMP")

    return indexed





def displayBackground():
    if mainRoom and background1 not in splash:
        splash.append(background1)
        splash.remove(background2)
    elif bedRoom and charging is False and background2 not in splash and inMachine is False:
        splash.append(background2)
        if background1 in splash:
            splash.remove(background1)
        elif background2Spritesheet in splash:
            splash.remove(background2Spritesheet)
    elif bedRoom and charging and background2Spritesheet not in splash:
        splash.append(background2Spritesheet)
        splash.remove(background2)

def displayRobot():
    if robotTilegrid1 not in splash and charging is False and inMachine is False:
        splash.append(robotTilegrid1)
        if robotTilegrid2 in splash:
            splash.remove(robotTilegrid2)
    elif charging and robotTilegrid2 not in splash:
        splash.append(robotTilegrid2)
        if robotTilegrid1 in splash:
            splash.remove(robotTilegrid1)

def displayGameSequence(order):
    for i in range(len(order)):
        if order[i] == 0:
            splash.append(blueButton)
            time.sleep(0.2)
            splash.remove(blueButton)
        elif order[i] == 1:
            splash.append(yellowButton)
            time.sleep(0.2)
            splash.remove(yellowButton)
        elif order[i] == 2:
            splash.append(orangeButton)
            time.sleep(0.2)
            splash.remove(orangeButton)
        time.sleep(0.2)

def funEyes():
    global displayingFunEyes
    displayingFunEyes = True
    global eyeNum
    if eyeNum is None:
        eyeNum = random.randint(0, len(specialEyeList)-1)

    specialEyeList[eyeNum].x = robotTilegrid1.x
    splash.append(specialEyeList[eyeNum])
    splash.remove(robotTilegrid1)
    i = 0
    while i != 7:
        global sourceIndex
        sourceIndex += 1
        specialEyeList[eyeNum][0] = sourceIndex % 4
        time.sleep(0.2)
        i += 1

    splash.append(robotTilegrid1)
    splash.remove(specialEyeList[eyeNum])
    displayingFunEyes = False
    eyeNum = None





# Game loop
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if mainRoom and displayingFunEyes is False:
                    funEyes()
                elif bedRoom and robotTilegrid1.x > 60 and charging is False:
                    inMachine = True
                    charging = True
                    if robotTilegrid1 in splash:
                        splash.remove(robotTilegrid1)
                elif charging:
                    playingGame = True

            if event.key == pygame.K_LEFT:
                if robotTilegrid1.x > -6 and displayingFunEyes is False:
                    robotTilegrid1.x -= 5
                elif bedRoom and robotTilegrid1.x <= -5:
                    splash.remove(robotTilegrid1)
                    robotTilegrid1.x = 74
                    mainRoom = True
                    bedRoom = False

                if inMachine and charging is False:
                    inMachine = False

            elif event.key == pygame.K_RIGHT:
                if robotTilegrid1.x < 75 and displayingFunEyes is False:
                    robotTilegrid1.x += 5
                if mainRoom and robotTilegrid1.x >= 75:
                    splash.remove(robotTilegrid1)
                    robotTilegrid1.x = -8
                    bedRoom = True
                    mainRoom = False

    displayBackground()
    displayRobot()

    # Memory game
    if charging:
        if "gameIntroTextArea" not in globals():
            gameIntroTextArea = label.Label(font, text="Play Game?", color=fontColor, x=26, y=64)
            gameOverTextArea = label.Label(font, text="Game Over", color=fontColor, x=28, y=48)

        if buttonsBG not in splash and gameIntroTextArea not in splash and playingGame is False:
            splash.append(buttonsBG)
            if gameIntroTextArea not in splash:
                splash.append(gameIntroTextArea)

        sequence = [random.randint(0, 2)]
        playerSequence = []
        sequenceDisplayed = False

        while playingGame:
            if upButtons not in splash and gameOver is False:
                splash.append(upButtons)

            if playerSequence == sequence and gameOver is False:
                playerSequence = []
                sequence.append(random.randint(0, 2))
                sequenceDisplayed = False

            if sequenceDisplayed is False and gameOver is False:
                time.sleep(0.3)
                displayGameSequence(sequence)
                sequenceDisplayed = True

            for x in range(len(playerSequence)):
                if len(playerSequence) > len(sequence) or playerSequence[x] != sequence[x]:
                    gameOver = True

            if gameOver and gameOverTextArea not in splash:
                splash.append(buttonsBG)
                splash.remove(upButtons)
                scoreText = label.Label(font, text=f"Score = {len(sequence)-1}", color=fontColor, x=26, y=74)
                splash.append(scoreText)
                splash.append(gameOverTextArea)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    run = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and gameOver is False:
                        playerSequence.append(0)
                        splash.append(blueButton)
                        time.sleep(0.2)
                        splash.remove(blueButton)
                    elif event.key == pygame.K_UP and gameOver is False:
                        playerSequence.append(1)
                        splash.append(yellowButton)
                        time.sleep(0.2)
                        splash.remove(yellowButton)
                    elif event.key == pygame.K_UP and gameOver:
                        splash.remove(gameOverTextArea)
                        splash.remove(scoreText)
                        splash.remove(buttonsBG)
                        charging = False
                        gameOver = False
                        playingGame = False
                    elif event.key == pygame.K_RIGHT and gameOver is False:
                        playerSequence.append(2)
                        splash.append(orangeButton)
                        time.sleep(0.2)
                        splash.remove(orangeButton)

    if charging is False and buttonsBG in splash:
        splash.remove(gameIntroTextArea)
        del gameIntroTextArea
        del gameOverTextArea
        splash.remove(buttonsBG)


    # Animations
    if robotTilegrid1 in splash:
        robotTilegrid1[0] = sourceIndex % 4
    elif robotTilegrid2 in splash:
        robotTilegrid2[0] = sourceIndex % 4
    if background2Spritesheet in splash:
        background2Spritesheet[0] = sourceIndex % 8

    sourceIndex += 1
    time.sleep(0.2)
