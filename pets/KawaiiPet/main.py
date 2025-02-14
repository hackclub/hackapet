import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import label
from displayio import Bitmap
import pygame as pg
from random import random,randint
import time

## Initializing pygame and display
HEIGHT=128
WIDTH=128
pg.init()
pg.event.set_allowed([pg.QUIT,pg.KEYDOWN,pg.KEYUP])
screen =  PyGameDisplay(width=WIDTH,height=HEIGHT,hw_accel=False)
splash = displayio.Group()
screen.show(splash)

############################## menu ####################################################
menuType=0
menuBgImg=displayio.OnDiskBitmap("images/bg/bg.bmp")
menuBg=displayio.TileGrid(
    menuBgImg,
    pixel_shader=menuBgImg.pixel_shader,
    width=1,
    height=1,
    tile_width=128,
    tile_height=128,
    default_tile=0,
    x=0,
    y=0
)
bg_img=displayio.OnDiskBitmap("images/bg/Garden.bmp")
bg=displayio.TileGrid(
    bg_img,
    pixel_shader=bg_img.pixel_shader,
)

gameOverImg=displayio.OnDiskBitmap("images/bg/Menu.bmp")
gameOverBg=displayio.TileGrid(
    gameOverImg,
    pixel_shader=gameOverImg.pixel_shader,
)

petImg=displayio.OnDiskBitmap("images/Pets/KawaiiDog/KawaiiDog_scaled.bmp")
pet=displayio.TileGrid(
    petImg,
    pixel_shader=petImg.pixel_shader,
    width=1,
    height=1,
    tile_width=51,
    tile_height=64,
    default_tile=0,
    x=(128-51)//2,
    y=128-64-15
)

b_img=displayio.OnDiskBitmap("images/Collectibles/Bone.bmp")
bomb_img=displayio.OnDiskBitmap("images/Collectibles/Bomb.bmp")
sword_img=displayio.OnDiskBitmap("images/Collectibles/Sword.bmp")

splash.append(menuBg)

framePet=0
bombFrame=0
swordFrame=0
bones=[]
bombs=[]
swords=[]

def checkHs():
    with open("highscore","r") as f:
        return int(f.read())
def saveHs():
    hsText.text="H.S:"+str(highscore)
    with open("highscore","w") as f:
        f.write(str(highscore))

bone_speed=3 
player_speed=5
bone_speed_max=30
points=0
highscore=checkHs()
allFrames=0

## Texts -----------------------------------------------------------------------------------------------
font=bitmap_font.load_font("fonts/Chroma48Medium-8.bdf", Bitmap)
## menu
title= label.Label(font, text="KawaiiPet", color=0xCDD6F4)
title.x=64-title.width//2
title.y=20

## Score and highscore texts
scoreText= label.Label(font, text="Score:"+str(points), color=0x000000)
scoreText.x=5
scoreText.y=5
hsText=label.Label(font, text="H.S:"+str(highscore), color=0x000000)
hsText.x=5
hsText.y=20
helpText=label.Label(font, text="Press enter", color=0xCDD6F4)
helpText.x=64-title.width//2
helpText.y=64-title.height//2
splash.append(title)
splash.append(helpText)

## Functions -------------------------------------------------------------------------------------------

def check_collision(sprite1, sprite2):
    return (
        sprite1.x < sprite2.x + 32 and
        sprite1.x + 32 > sprite2.x and
        sprite1.y < sprite2.y + 32 and
        sprite1.y + 32 > sprite2.y
    )

def spawnBone():
    xPos=randint(0,screen.width-b_img.width)
    b=displayio.TileGrid(
        b_img,
        pixel_shader=petImg.pixel_shader,
        width=1,
        height=1,
        tile_width=29,
        tile_height=30,
        x=xPos,
        y=-30
    )
    bones.append(b)
    splash.append(b)

def spawnBomb():
    xPos=randint(0,screen.width-b_img.width)
    bo=displayio.TileGrid(
        bomb_img,
        pixel_shader=bomb_img.pixel_shader,
        width=1,
        height=1,
        tile_width=32,
        tile_height=32,
        x=xPos,
        y=-30
    )
    bombs.append(bo)
    splash.append(bo)
def spawnSword():
    xPos=randint(0,screen.width-b_img.width)
    sw=displayio.TileGrid(
        sword_img,
        pixel_shader=sword_img.pixel_shader,
        width=1,
        height=1,
        tile_width=32,
        tile_height=32,
        x=xPos,
        y=-30
    )
    swords.append(sw)
    splash.append(sw)

f=0
bgFrame=0
while True:
    for event in pg.event.get():
        if event.type==pg.QUIT:
            pg.quit()
            exit()
    keys=pg.key.get_pressed()
    if menuType==1:
        if keys[pg.K_LEFT] or keys[pg.K_h]:
            pet.x -= player_speed 
        if keys[pg.K_RIGHT] or keys[pg.K_l]:
            pet.x += player_speed
        if random() < 0.08:
            spawnBone()

        for bone in bones:
            bone.y += bone_speed 
            if bone.y > screen.height-15:
                splash.remove(bone)
                bones.remove(bone)
                points-=20
                scoreText.text="Score:"+str(points)
            elif check_collision(pet,bone):
                points+=10
                if highscore<points:
                    highscore=points
                    saveHs()
                splash.remove(bone)
                bones.remove(bone)
                scoreText.text="Score:"+str(points)
        for bomb in bombs:
            bomb[0]=bombFrame
            bomb.y+=bone_speed
            if check_collision(pet,bomb):
                points-=100
                splash.remove(bomb)
                bombs.remove(bomb)
                scoreText.text="Score:"+str(points)

        for sword in swords:
            sword[0]=swordFrame
            sword.y+=bone_speed
            if check_collision(pet,sword):
                points=0
                splash.remove(sword)
                swords.remove(sword)
                scoreText.text="Score:"+str(points)
                menuType=2
                splash.append(gameOverBg)

        pet[0]=framePet
        
        framePet=(framePet+1) % 10
        allFrames=(allFrames+1)%200
        bombFrame=(framePet+1)%4
        swordFrame=(framePet+1)%4

        if allFrames==1:
            spawnBomb()
            bone_speed+=2
            if bone_speed>=30:
                bone_speed=40
        elif allFrames==100:
            spawnSword()

    elif menuType==0:
        if keys[pg.K_RETURN]:
            menuType=1
            splash.remove(menuBg)
            splash.remove(title)
            splash.remove(helpText)
            splash.append(bg)
            splash.append(pet)
            splash.append(scoreText)
            splash.append(hsText)
    else:
        if keys[pg.K_RETURN]:
            menuType=1
            splash.remove(gameOverBg)
    f+=1
    if f%5==0:
        bgFrame=(bgFrame+1)%12
    menuBg[0]=bgFrame
    time.sleep(0.1)

