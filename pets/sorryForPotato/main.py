import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
import pygame
import time
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font
from adafruit_display_shapes.rect import Rect
import random
from potato import Potato
from potato import growthStage


waterIncrese = 1
foodIncrese = 1
bugDecrese = 1

waterDecrese = 1
foodDecrese = 1
bugIncrese = 1

#Note: Higher number means lower chance
chanceOfDecrese = 200
chanceOfBug = 150
chanceOfDamg = 150
chanceOfHeal = 700
chanceOfGrowth = 550

def updateBar(splash, bar, maxBar, thing, maxThing, color):
    if bar:
        splash.remove(bar)
    if round((maxBar.width/maxThing)*thing) <= 0:
        return None
    bar = Rect(maxBar.x,maxBar.y,round((maxBar.width/maxThing)*thing),maxBar.height,fill=color)
    splash.append(bar)
    return bar

def spawnBug(splash, display, bugImage, bugs):
    x = random.randint(0, display.width-bugImage.width)
    y = random.randint(38, display.height - bugImage.height)
    
    bug = displayio.TileGrid(
        bugImage,
        pixel_shader=bugImage.pixel_shader,
        width=1,
        height=1,
        tile_width=bugImage.width,
        tile_height=bugImage.height,
        x=x,
        y=y
    )

    bugs.append(bug)
    splash.append(bug)

pygame.init()
scale = 1
try:
    display=PyGameDisplay(width=128*scale, height=128*scale,hw_accel=False)
except:
    display=PyGameDisplay(width=128*scale, height=128*scale)

splash = displayio.Group(scale=scale)
display.show(splash)

bgrImage = displayio.OnDiskBitmap("backgroundVer2.bmp")
bgrSprite = displayio.TileGrid(bgrImage,pixel_shader=bgrImage.pixel_shader)

font = bitmap_font.load_font("helvR12.bdf")
gameOverText = label.Label(font, text="Your Potato Died!",x=5,y=5,scale=1,line_spacing=0.7,color=0x0)
winText = label.Label(font, text="Congrats! Your\npotato is fully\ngrown and\nready to be\nbaked, mashed,\nboiled, or fryed!", x=5,y=5,scale=1,line_spacing=0.7,color=0x0)

splash.append(bgrSprite)

tile_width=32
tile_height=32
potatoImage = displayio.OnDiskBitmap("PotatoVer3.bmp")
deadPotatoImage = displayio.OnDiskBitmap("PotatoDead2.bmp")
potatoSprite = displayio.TileGrid(
    potatoImage,
    pixel_shader=potatoImage.pixel_shader,
    width=1,
	height=1,
	tile_width=32,
	tile_height=32,
	default_tile=0,
	x=(display.width - tile_width) // 2,
	y=display.height - tile_height - 10
)
deadPotatoSprite = displayio.TileGrid(
    deadPotatoImage,
    pixel_shader=deadPotatoImage.pixel_shader,
    width=1,
	height=1,
	tile_width=32,
	tile_height=32,
	default_tile=0,
	x=(display.width - tile_width) // 2,
	y=display.height - tile_height - 10
)

splash.append(potatoSprite)

bugImage = displayio.OnDiskBitmap("bug.bmp")
bugs = []

frame = 0
trueFrame = 0

#Dormant, Sprout, Plant, Flowers
# sproutImg = displayio.OnDiskBitmap("sprout.bmp")
# sproutSprite = displayio.TileGrid(
#     sproutImg,
#     pixel_shader=sproutImg.pixel_shader,
#     width=1,
# 	height=1,
# 	tile_width=32,
# 	tile_height=32,
# 	default_tile=0,
# 	x=(display.width - tile_width) // 2,
# 	y=display.height - tile_height - 10
# )
growthStages = [growthStage(None, 3), growthStage(None, 5), growthStage(None, 10), growthStage(None, 10)]

spud = Potato(10,10,10,10,growthStages)



waterOutline = Rect(10,10,32,6,outline=0x0)
foodOutline = Rect(10,18,32,6,outline=0x0)
bugOutline = Rect(10,26,32,6,outline=0x0)
healthOutline = Rect(10,34,32,6,outline=0x0)

waterBar = updateBar(splash, None, waterOutline,spud.water,spud.maxWater,0x0000FF)
foodBar = updateBar(splash, None, foodOutline, spud.food, spud.maxFood, 0xDAA06D)
bugBar = updateBar(splash, None, bugOutline, spud.bugs, spud.maxBugs, 0x94b21c)
healthBar = updateBar(splash, None, healthOutline, spud.health, spud.maxHealth, 0xFF0000)

splash.append(waterOutline)
splash.append(foodOutline)
splash.append(bugOutline)
splash.append(healthOutline)

while True:

    
    for event in pygame.event.get():

        #For some reason it often errors when quiting, particerly after
        #win condition is me. Not to conserend, becuase the program quits either way
        #but probably should investigate at some point
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if spud.alive == True:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    spud.water+= waterIncrese
                    if spud.water > spud.maxWater:
                        spud.water = spud.maxWater
                if event.key == pygame.K_2:
                    spud.food += foodIncrese
                    if spud.food > spud.maxFood:
                        spud.food = spud.maxFood
                if event.key == pygame.K_3:
                    spud.bugs -= bugDecrese
                    if spud.bugs < 0:
                        spud.bugs = 0
                    else:
                        splash.remove(bugs[0])
                        bugs.pop(0)
    if spud.alive == False:
        continue
    
    #decrese water and food
    randNum = random.randint(0, chanceOfDecrese)
    if randNum == 0:
        spud.water -= waterDecrese
        if spud.water < 0:
            spud.water = 0
    if randNum == 1:
        spud.food -= foodDecrese
        if spud.food < 0:
            spud.food = 0
    
    #add bugs
    if spud.water > (spud.maxWater*0.75) or spud.food > (spud.maxFood*0.75):
        if spud.water > (spud.maxWater*0.75) and spud.food < (spud.maxFood*0.75):
            tmpChanceOfBug = chanceOfBug//2
        else:
            tmpChanceOfBug = chanceOfBug
        if random.randint(0, tmpChanceOfBug) == 0:
            spud.bugs+=1
            if spud.bugs > spud.maxBugs:
                spud.bugs = spud.maxBugs
            else:
                spawnBug(splash, display, bugImage, bugs)
    
    if spud.water < (spud.maxWater*0.25) or spud.food < (spud.maxFood*0.25):
        if spud.water < (spud.maxWater*0.25) and spud.food < (spud.maxFood*0.25):
            tmpChanceOfDamg = chanceOfDamg//2
        else:
            tmpChanceOfDamg = chanceOfDamg
        if random.randint(0, chanceOfDamg) == 0:
            spud.health -= 1
    
    if spud.bugs > 0:
        if spud.bugs > (spud.maxBugs*0.75):
            tmpChanceOfDamg = chanceOfDamg//2
        else:
            tmpChanceOfDamg = chanceOfDamg
        if random.randint(0, chanceOfDamg) == 0:
            spud.health -= 1
        #TODO: potato image should get sadder as health drops

    if spud.water > (spud.maxWater*0.25) and spud.food > (spud.maxFood*0.25) and spud.bugs == 0:
        if random.randint(0, chanceOfHeal) == 0:
            spud.health += 1
            if spud.health > spud.maxHealth:
                spud.health = spud.maxHealth 

    if spud.health < 0:
        spud.alive = False
        
        splash.remove(potatoSprite)
        splash.append(deadPotatoSprite)
        
        splash.append(gameOverText)
        continue
    
    if spud.health > (spud.maxHealth*0.5):
        if random.randint(0,chanceOfGrowth) == 0:

            spud.stageProg += 1
            if spud.stageProg >= spud.growthStages[spud.curentStage].length:
                spud.curentStage += 1
                spud.stageProg = 0
                if spud.curentStage >= len(spud.growthStages):
                    spud.alive = False

                    splash.append(winText)
                    continue
                if spud.growthStages[spud.curentStage].image:
                    splash.append(spud.growthStages[spud.curentStage].image)

        
    waterBar = updateBar(splash, waterBar, waterOutline, spud.water, spud.maxWater, 0x0000FF)
    foodBar = updateBar(splash, foodBar,foodOutline,spud.food,spud.maxFood,0xDAA06D)
    bugBar = updateBar(splash, bugBar, bugOutline, spud.bugs, spud.maxBugs, 0x94b21c)
    healthBar = updateBar(splash, healthBar, healthOutline, spud.health, spud.maxHealth, 0xFF0000)

    potatoSprite[0] = frame
    trueFrame = (trueFrame + 0.03) % ((potatoImage.width // tile_width)-2)
    frame = round(trueFrame)

    time.sleep(0.01)
