import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
import displayio._ondiskbitmap
import pygame
import time
import random

pygame.init()
display = PyGameDisplay(width=128,height=128)
splash = displayio.Group()
display.show(splash)

currentbg = 0
backgrounds = [displayio.OnDiskBitmap("assets/winterforest.bmp"), displayio.OnDiskBitmap("assets/springforest.bmp"),displayio.OnDiskBitmap("assets/summerforest.bmp"),displayio.OnDiskBitmap("assets/fallforest.bmp")]
bg = displayio.OnDiskBitmap("assets/winterforest.bmp")
bgs = displayio.TileGrid(
    bg,
    pixel_shader=bg.pixel_shader
)
splash.append(bgs)

sleepingbit = displayio.OnDiskBitmap("assets/sleep.bmp")
sleepingScreen = displayio.TileGrid(
    sleepingbit,
    pixel_shader=sleepingbit.pixel_shader
)
splash.append(sleepingScreen)
sleepingScreen.hidden = True

dog = displayio.OnDiskBitmap("assets/blizzard.bmp")
moredog = displayio.OnDiskBitmap("assets/blizzard2.bmp")
blizzard_sprite = displayio.TileGrid(
    dog,
    pixel_shader=dog.pixel_shader,
    width=1,
    height=1,
    tile_height=96,
    tile_width=96,
    default_tile=0,
    x=(display.width - 96) // 2,
    y=display.height - 96 - 15
)
splash.append(blizzard_sprite)

dogminigame = displayio.OnDiskBitmap("assets/bMinigame.bmp")
bminigame_sprite = displayio.TileGrid(
    dogminigame,
    pixel_shader=dogminigame.pixel_shader,
    width=1,
    height=1,
    tile_height=128,
    tile_width=97,
    default_tile=0,
    x=display.width-97,
)
splash.append(bminigame_sprite)
bminigame_sprite.hidden = True

lowH = displayio.OnDiskBitmap("assets/lowHunger.bmp")
lowT = displayio.OnDiskBitmap("assets/lowThirst.bmp")
warning = displayio.TileGrid(
    lowH,
    pixel_shader=lowH.pixel_shader,
    x=(display.width - 96) // 2,
)
splash.append(warning)
warning.hidden = True

balls = []
def makeBall():
    ballBitmap = displayio.OnDiskBitmap("assets/ball.bmp")
    ball = displayio.TileGrid(
        ballBitmap,
        pixel_shader=ballBitmap.pixel_shader,
        x= -20,
        y= display.height / 2 - 9 # there may be a better way to center the ball to the press region on the bminigame sprite but i feel like this is good for now
    )
    balls.append(ball)
    splash.append(ball)

def cleanUpBalls():
    for ball in balls:
        splash.remove(ball)
    balls.clear()

frame = 0
hunger = 25.0
thirst = 35.0

ticks = 0
eat_cooldown = 0
drink_cooldown = 0
ball_cooldown = 0

minigames = False
minigameWon = 0 # 0 - no state 1 - won 2 - lost
totalBalls = 0

sleeping = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT and minigames:
            for ball in balls:
                if ball.x <= 65 and ball.x >= 30:
                    balls.remove(ball)
                    splash.remove(ball)
                    bminigame_sprite[0] = 1
                    totalBalls += 1
                    time.sleep(.2)
                    break
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP and sleeping:
            hunger = 25.0
            thirst = 35.0
            sleeping = False
    
    if sleeping:
        blizzard_sprite.bitmap = dog
        warning.hidden = True
        bminigame_sprite.hidden = True
        blizzard_sprite.hidden = True
        bgs.hidden = True
        sleepingScreen.hidden = False
        time.sleep(.01)
    else:
        sleepingScreen.hidden = True
        bgs.hidden = False

        ticks += 1
        if eat_cooldown <= 0: 
            eat_cooldown = 0
        else:
            eat_cooldown -= 1
        
        if drink_cooldown <= 0: 
            drink_cooldown = 0
        else:
            drink_cooldown -= 1

        if ball_cooldown <= 0: 
            ball_cooldown = 0
        else:
            ball_cooldown -= 1

        if ticks >= 240:
            ticks = 0
            currentbg = (currentbg + 1) % 4
        
        bgs.bitmap = backgrounds[currentbg]
        keys = pygame.key.get_pressed()
        if minigames:
            warning.hidden = True
            bminigame_sprite.hidden = False
            blizzard_sprite.hidden = True
            bminigame_sprite[0] = 0

            if random.random() < .05 and ball_cooldown <= 0:
                makeBall()
                ball_cooldown = 6

            for ball in balls:
                ball.x += 2
                if ball.x >= 75:
                    bminigame_sprite[0] = 2
                    balls.remove(ball)
                    splash.remove(ball)
                    totalBalls -= 1
                    time.sleep(.2)
            
            if totalBalls >= 10:
                cleanUpBalls()
                minigames = False
                totalBalls = 0
                minigameWon = 1
            
            if totalBalls <= -5:
                cleanUpBalls()
                minigames = False
                totalBalls = 0
                minigameWon = 2             
        else:
            bminigame_sprite.hidden = True
            blizzard_sprite.hidden = False

            if minigameWon == 1:
                minigameWon = 0
                blizzard_sprite.bitmap = moredog
                blizzard_sprite[0] = 0
                time.sleep(1)
                blizzard_sprite.bitmap = dog
            elif minigameWon == 2:
                minigameWon = 0
                blizzard_sprite.bitmap = moredog
                blizzard_sprite[0] = 1
                time.sleep(1)
                blizzard_sprite.bitmap = dog

            if keys[pygame.K_UP] and eat_cooldown <= 0:
                blizzard_sprite[0] = 8
                hunger += 15
                time.sleep(1)
                eat_cooldown = 6
            elif keys[pygame.K_LEFT] and drink_cooldown <= 0:
                blizzard_sprite[0] = 9
                thirst += 20
                time.sleep(1)
                drink_cooldown = 4
            elif keys[pygame.K_RIGHT] and not minigames:
                minigames = True
                continue

            if hunger <= 20:
                warning.bitmap = lowH
                warning.hidden = False
                blizzard_sprite[0] = frame
                frame = ((frame + 1) % 4) + 4
            elif thirst <= 20:
                warning.bitmap = lowT
                warning.hidden = False
            else:
                warning.hidden = True
                blizzard_sprite[0] = frame
                frame = (frame + 1) % 4
            
            hunger -= hunger < 75 and .15 or .3
            thirst -= hunger < 75 and .25 or .5

            if thirst <= 0: thirst = 0
            if hunger >= 100: hunger = 100
            if thirst >= 100: thirst = 100

            if hunger <= 0: 
                hunger = 0
                warning.hidden = True
                blizzard_sprite.bitmap = moredog
                blizzard_sprite[0] = 2
                for i in range(3,8):
                    blizzard_sprite[0] = i
                    time.sleep(.3)
                
                sleeping = True
                continue

            print(hunger,thirst)

        time.sleep(minigames and .03 or .25)