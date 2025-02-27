import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
import pygame
import time
from adafruit_display_text import label
import random


pygame.init()


display = PyGameDisplay(width=128, height=128)
splash = displayio.Group()
display.show(splash)


background = displayio.OnDiskBitmap("background.bmp")
backgroundSprite = displayio.TileGrid(background, pixel_shader=background.pixel_shader)
splash.append(backgroundSprite)

wizardSheet = displayio.OnDiskBitmap("player.bmp")
wizard = displayio.TileGrid(
    wizardSheet,
    pixel_shader=wizardSheet.pixel_shader,
    width=1,
    height=1,
    tile_width=32,
    tile_height=32,
    default_tile=0,
    x=0,  
    y=128 - 64 - 1    
)
splash.append(wizard)

goblinSheet = displayio.OnDiskBitmap("goblin.bmp")
goblin1 = displayio.TileGrid(
    goblinSheet,
    pixel_shader=goblinSheet.pixel_shader,
    width=1,
    height=1,
    tile_width=32,
    tile_height=32,
    default_tile=0,
    x=8,  
    y=1     
)
splash.append(goblin1)

goblin2 = displayio.TileGrid(
    goblinSheet,
    pixel_shader=goblinSheet.pixel_shader,
    width=1,
    height=1,
    tile_width=32,
    tile_height=32,
    default_tile=0,
    x=8 + 8 + 32,  
    y=1     
)
splash.append(goblin2)

goblin3 = displayio.TileGrid(
    goblinSheet,
    pixel_shader=goblinSheet.pixel_shader,
    width=1,
    height=1,
    tile_width=32,
    tile_height=32,
    default_tile=0,
    x=8 + 8 + 8 + 32 + 32,  
    y=1     
)
splash.append(goblin3)

zapSheet = displayio.OnDiskBitmap("zap.bmp")
zap = displayio.TileGrid(
    zapSheet,
    pixel_shader=zapSheet.pixel_shader,
    width=1,
    height=1,
    tile_width=32,
    tile_height=64,
    default_tile=0,
    x= 128/2 -16,  
    y=-64    
)
splash.append(zap)

fireBallSheet = displayio.OnDiskBitmap("fireBall.bmp")
fireBall = displayio.TileGrid(
    fireBallSheet,
    pixel_shader=fireBallSheet.pixel_shader,
    width=1,
    height=1,
    tile_width=32 * 3,
    tile_height=64,
    default_tile=0,
    x=16,  
    y=-64     
)
splash.append(fireBall)

cards = displayio.OnDiskBitmap("cards.bmp")
chargeCard = displayio.TileGrid(
    cards,
    pixel_shader=cards.pixel_shader,
    width=1,
    height=1,
    tile_width=22,
    tile_height=32,
    default_tile=0,
    x=3,  
    y=128 - 32
)
splash.append(chargeCard)

zapCard = displayio.TileGrid(
    cards,
    pixel_shader=cards.pixel_shader,
    width=1,
    height=1,
    tile_width=22,
    tile_height=32,
    default_tile=2,
    x=3 * 2 + 22,  
    y=128 - 32
)
splash.append(zapCard)

fireBallCard = displayio.TileGrid(
    cards,
    pixel_shader=cards.pixel_shader,
    width=1,
    height=1,
    tile_width=22,
    tile_height=32,
    default_tile=4,
    x=3 * 3 + 22 * 2,  
    y=128 - 32
)
splash.append(fireBallCard)

healCard = displayio.TileGrid(
    cards,
    pixel_shader=cards.pixel_shader,
    width=1,
    height=1,
    tile_width=22,
    tile_height=32,
    default_tile=6,
    x=3 * 4 + 22 * 3,  
    y=128 - 32
)
splash.append(healCard)

counterCard = displayio.TileGrid(
    cards,
    pixel_shader=cards.pixel_shader,
    width=1,
    height=1,
    tile_width=22,
    tile_height=32,
    default_tile=8,
    x=3 * 5 + 22 * 4,  
    y=128 - 32
)
splash.append(counterCard)

healthSheet = displayio.OnDiskBitmap("healthBar.bmp")
healthBar = displayio.TileGrid(
    healthSheet,
    pixel_shader=healthSheet.pixel_shader,
    width=1,
    height=1,
    tile_width=35,
    tile_height=5,
    default_tile=0,
    x=0,  
    y=0
)
splash.append(healthBar)

manaSheet = displayio.OnDiskBitmap("mana.bmp")
manaBar = displayio.TileGrid(
    manaSheet,
    pixel_shader=manaSheet.pixel_shader,
    width=1,
    height=1,
    tile_width=27,
    tile_height=6,
    default_tile=0,
    x=0,  
    y=5
)
splash.append(manaBar)

state = 1
HP = 25
mana = 2
card = 0
goblinHP1 = 2
goblinHP2 = 2
goblinHP3 = 2
atack1 = False
atack2 = True
atack3 = False
wizardFrame = 0
goblin1Frame = 0
goblin2Frame = 0
goblin3Frame = 0
playerPos = 1
spellFrame = 0
goblinY = 0

while True:
    time.sleep(0.1)

    manaBar[0] = mana

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        if state == 2:
            playerPos -= 1
        else:
            card -= 1
    if keys[pygame.K_RIGHT]:
        if state == 2:
            playerPos += 1
        else:
            card += 1
    if card > 4:
         card = 0
    if card < 0:
         card = 4
    if playerPos > 2:
         playerPos = 2
    if playerPos < 0:
         playerPos = 0

    if state >= 6 or state == 1:
        playerPos = 1

    if playerPos == 0:
        wizard.x = 8
        zap.x = 8
    elif playerPos == 1:
        wizard.x = 8 * 2 + 32
        zap.x = 8 * 2 + 32
    elif playerPos == 2:
        wizard.x = 8 * 3 + 32 * 2
        zap.x = 8 * 3 + 32 * 2

    if state == 3:
        zap.y = 0
        spellFrame += 1
        zap[0] = spellFrame
        if spellFrame > 18:
            state = 6
            wizardFrame = 1
            if playerPos == 0:
                goblinHP1 -= 1
            elif playerPos == 1:
                goblinHP2 -= 1
            elif playerPos == 2:
                goblinHP3 -= 1
    else:
        zap.y = 64

    if state == 4:
        fireBall.y = 0
        spellFrame += 1
        fireBall[0] = spellFrame
        if spellFrame > 22:
            state = 6
            wizardFrame = 1
            goblinHP1 -= 1
            goblinHP2 -= 1
            goblinHP3 -= 1
    else:
        fireBall.y = 64

    if keys[pygame.K_UP] and state == 2:
        state = 3
        wizardFrame = 8

    if keys[pygame.K_UP] and state == 1:
        if card == 0 and mana < 4:
            mana += 1
            state = 5
            wizardFrame = 8
        if card == 1 and mana >= 1:
            mana -= 1
            state = 2
            spellFrame = -1
        if card == 2 and mana >= 2:
            mana -= 2
            state = 4
            wizardFrame = 8
            spellFrame = -1
        if card == 3 and mana >= 1:
            mana -= 1
            state = 5
            HP += 10
            wizardFrame = 8
        # if card == 4 and mana >= 2:
        #     mana -= 2

    if card == 0:
        chargeCard[0] = 1
        zapCard[0] = 2
        fireBallCard[0] = 4
        healCard[0] = 6
        counterCard[0] = 8
    if card == 1:
        chargeCard[0] = 0
        zapCard[0] = 3
        fireBallCard[0] = 4
        healCard[0] = 6
        counterCard[0] = 8
    if card == 2:
        chargeCard[0] = 0
        zapCard[0] = 2
        fireBallCard[0] = 5
        healCard[0] = 6
        counterCard[0] = 8
    if card == 3:
        chargeCard[0] = 0
        zapCard[0] = 2
        fireBallCard[0] = 4
        healCard[0] = 7
        counterCard[0] = 8
    if card == 4:
        chargeCard[0] = 0
        zapCard[0] = 2
        fireBallCard[0] = 4
        healCard[0] = 6
        counterCard[0] = 9
   
    if state == 1 or state == 2:
        wizardFrame += 1
        if wizardFrame < 2:
            wizard[0] = 0
        elif wizardFrame < 4:
            wizard[0] = 1
        else:
            wizard[0] = 0
            wizardFrame = 0
    elif state == 3 or state == 4 or state == 5:
        if wizardFrame != 0:
            wizardFrame += 1
        if wizardFrame > 15:
            wizardFrame = 0
            if state == 5:
                state = 6
                wizardFrame = 1
        wizard[0] = wizardFrame

    if goblinHP1 <= 0:
        goblin1.y = -32
    else:
        goblin1.y = 0

    if goblinHP2 <= 0:
        goblin2.y = -32
    else:
        goblin2.y = 0

    if goblinHP3 <= 0:
        goblin3.y = -32
    else:
        goblin3.y = 0

    if state == 6:
        if goblinHP1 > 0:
            if atack1:
                if goblinY < 15:
                    goblinY += 1
                if goblinY >= 15:
                    wizardFrame += 1
                    if wizardFrame > 8:
                        HP -= 5
                        atack1 = False
                    wizard[0] = wizardFrame
            else:
                if goblinY > 0:
                    goblinY -= 1
                if goblinY <= 0:
                    state = 7
                    wizardFrame = 1
            goblin1.y = goblinY
        else:
            goblin1.y = goblinY - 32
            if goblinY < 32: 
                goblinY += 1
            else:
                goblinHP1 = 2
                goblinY = 0
                state = 7
                wizardFrame = 1 

    if state == 7:
        if goblinHP2 > 0:
            if atack2:
                if goblinY < 15:
                    goblinY += 1
                if goblinY >= 15:
                    wizardFrame += 1
                    if wizardFrame > 8:
                        HP -= 5
                        atack2 = False
                    wizard[0] = wizardFrame
            else:
                if goblinY > 0:
                    goblinY -= 1
                if goblinY == 0:
                    state = 8
                    wizardFrame = 1
            goblin2.y = goblinY
        else:
            goblin2.y = goblinY - 32
            if goblinY < 32: 
                goblinY += 1
            else:
                goblinHP2 = 2
                goblinY = 0
                state = 8
                wizardFrame = 1 

    if state == 8:
        if goblinHP3 > 0:
            if atack3:
                if goblinY < 15:
                    goblinY += 1
                if goblinY >= 15:
                    wizardFrame += 1
                    if wizardFrame > 8:
                        HP -= 5
                        atack3 = False
                    wizard[0] = wizardFrame
            else:
                if goblinY > 0:
                    goblinY -= 1
                if goblinY == 0:
                    state = 9
                    wizardFrame = 1
            goblin3.y = goblinY
        else:
            goblin3.y = goblinY - 32
            if goblinY < 32: 
                goblinY += 1
            else:
                goblinHP3 = 2
                goblinY = 0
                state = 9
                wizardFrame = 1 

    if atack1:
        goblin1Frame += 2
    else:
        goblin1Frame += 1
    if goblin1Frame < 2:
        goblin1[0] = 0
    elif goblin1Frame < 4:
        goblin1[0] = 1
    else:
        goblin1[0] = 0
        goblin1Frame = 0

    if atack2:
        goblin2Frame += 2
    else:
        goblin2Frame += 1
    if goblin2Frame < 2:
         goblin2[0] = 0
    elif goblin2Frame < 4:
         goblin2[0] = 1
    else:
         goblin2[0] = 0
         goblin2Frame = 0

    if atack3:
        goblin3Frame += 2
    else:
        goblin3Frame += 1
    if goblin3Frame < 2:
         goblin3[0] = 0
    elif goblin3Frame < 4:
         goblin3[0] = 1
    else:
         goblin3[0] = 0
         goblin3Frame = 0

    if HP > 25:
        HP = 25
    
    if HP <= 0:
        pygame.quit()

    healthBar[0] = 25 - HP

    if state == 9:
        atack1 = random.randint(0, 2) == 0
        atack2 = random.randint(0, 2) == 0
        atack3 = random.randint(0, 2) == 0
        state = 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

