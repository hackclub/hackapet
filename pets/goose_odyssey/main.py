import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay

import pygame
import time

from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import label

from instances.goose import Goose
from instances.stella import Stella
from instances.greygoose import GreyGoose
from instances.greygoosebossfight import GreyGooseBossfight
from instances.mushroom_scavenging import MushroomScavenging

from map import Map, Interactable, updateMaps, Trigger
from instances.parallax import Parallax, ParallaxFrame
from instances.button_indicator import ButtonIndicator
from instances.fade import Fade

import timer
import random
from dialogue import Dialogue

pygame.init()

display = PyGameDisplay(width=128, height=128)
splash = displayio.Group()
display.show(splash)

fade = Fade()
dialogue = Dialogue()

global currentMap

currentMap = "outside_hotel"
currentState = "start"

def enterHotel():
    def afterFade():
        global currentMap
        
        fade.direction = -1
        currentMap = "inside_hotel"
        goose.x = 0
    
    fade.direction = 1
    timer.createAndStartTimer(6, afterFade)

def winBossfight():
    global currentState
    currentState = "won_bossfight"
    fade.direction = 1

    def afterFade():
        global currentMap
        greygooseBossfight.angerSprite.hidden = True
        fade.direction = -1
        currentMap = "outside_hotel"
        goose.x = 700
        goose.cameraFollow = True
        goose.showHealth = False
        goose.sprite.flip_x = True
        goose.SPEED = 5
        goose.frozen = True
        
        greygooseBossfight.sprite.hidden = True
        greygooseBossfight.healthBar.hidden = True
        
        goose.sprite.y = 64
        
        greygoose.x = 790
        greygoose.walking = False
        greygoose.map = "outside_hotel"
        greygoose.sprite.flip_x = False
        greygoose.direction = 0
        
        greygoose.passingOut = 1
        
        def afterWait():
            stella.map = "outside_hotel"
            stella.x = 500
            stella.direction = 5
            stella.walking = True
            stella.sleeping = False
            stella.sprite.flip_x = False
            stella.customUpdate = stella.foughtGreygoose

            greygoose.passingOut = 2

            def afterWait2():
                def afterSpeak():
                    stella.direction = -5
                    stella.walking = True
                    stella.sprite.flip_x = True
                    goose.frozen = False
                    
                    goose.afterGatherX = goose.x + 250

                    maps["outside_hotel"].parallax.appendFrame(ParallaxFrame(
                        "assets/big_tree.bmp", 1, False, goose.x + 300
                    ), splash)

                    maps["outside_hotel"].leftBound = goose.x - 20

                    maps["outside_hotel_sunset"].parallax.appendFrame(ParallaxFrame(
                        "assets/big_tree.bmp", 1, False, goose.x + 300
                    ), splash)
                    
                    maps["outside_hotel_sunset"].rightBound = goose.x + 260
                    
                    maps["outside_hotel"].triggers.append(Trigger(
                        goose.x + 250, True, startGathering
                    ))
                
                dialogue.speak("stella", stella.dialogues["afterFight"], afterSpeak, False)

            timer.createAndStartTimer(50, afterWait2)
        
        timer.createAndStartTimer(25, afterWait)
    
    timer.createAndStartTimer(6, afterFade)

def failBossfight():
    global currentState
    currentState = "failed_bossfight"
    fade.direction = 1

    def afterFade():
        global currentMap
        
        fade.direction = -1
        currentMap = "outside_hotel"
        goose.x = 700
        goose.cameraFollow = True
        goose.frozen = True
        goose.showHealth = False
        goose.sprite.flip_x = True
        greygooseBossfight.sprite.hidden = True
        greygooseBossfight.healthBar.hidden = True
        
        goose.sprite.y = 64
        
        greygoose.x = 790
        greygoose.walking = False
        greygoose.map = "outside_hotel"
        greygoose.sprite.flip_x = False
        greygoose.direction = 0
        
        goose.passingOut = 1
        
        def afterWait():
            goose.passingOut = 2

            def afterWait2():
                greygoose.walking = True
                greygoose.sprite.flip_x = True
                greygoose.direction = 3

                def afterWait3():
                    fade.direction = 1
                    
                    def afterWait4():
                        greygooseBossfight.health = greygooseBossfight.MAX_HEALTH
                        greygooseBossfight.parryFeatherCount = 0
                        greygooseBossfight.parryFeatherRequiredCount = 6

                        goose.health = goose.MAX_HEALTH
                        goose.passingOut = 0
                        encounter()

                    timer.createAndStartTimer(10, afterWait4)
                
                timer.createAndStartTimer(20, afterWait3)
            
            timer.createAndStartTimer(25, afterWait2)
    
        timer.createAndStartTimer(25, afterWait)
    
    timer.createAndStartTimer(6, afterFade)

def startFight():
    global currentMap
    global currentState
    fade.direction = -1
    greygooseBossfight.sprite.hidden = False
    greygooseBossfight.healthBar.hidden = False
    goose.cameraFollow = False
    goose.x = 40
    goose.showHealth = True
    goose.SPEED = 10
    goose.hidden = False
    goose.frozen = False
    goose.sprite.y = 64+24
    
    currentMap = "void"
    currentState = "bossfight"
    
    def startAttacks():
        def attackLeft():
            if goose.health <= 0 or greygooseBossfight.health <= 0:
                return
            
            greygooseBossfight.attackLeft(goose.x, splash)
            
            minTime = 7 if greygooseBossfight.health <= int(greygooseBossfight.MAX_HEALTH / 2) else 10
            maxTime = 15 if greygooseBossfight.health <= int(greygooseBossfight.MAX_HEALTH / 2) else 30

            timer.createAndStartTimer(random.randint(minTime, maxTime), attackLeft)

        def attackRight():
            if goose.health <= 0 or greygooseBossfight.health <= 0:
                return
            
            greygooseBossfight.attackRight(goose.x, splash)

            minTime = 7 if greygooseBossfight.health <= int(greygooseBossfight.MAX_HEALTH / 2) else 10
            maxTime = 16 if greygooseBossfight.health <= int(greygooseBossfight.MAX_HEALTH / 2) else 30

            timer.createAndStartTimer(random.randint(minTime,maxTime), attackRight)

        timer.createAndStartTimer(random.randint(20,30), attackLeft)
        timer.createAndStartTimer(random.randint(20,30), attackRight)
    
    dialogue.speak(None, [
        "Avoid red feathers\nParry blue feathers\nby holding the\nmiddle button."
    ], startAttacks, True)

    

def encounter():
    def frame1():
        global currentMap
        fade.direction = -1
        currentMap = "encounter_1"
        goose.x = 0
        goose.hidden = True

        def afterWait():
            def frame2():
                global currentMap
                fade.direction = -1
                currentMap = "encounter_2"
                
                def afterWait2():
                    fade.direction = 1
                    timer.createAndStartTimer(6, startFight)

                timer.createAndStartTimer(15, afterWait2)
                
            

            fade.direction = 1
            timer.createAndStartTimer(6, frame2)
        
        timer.createAndStartTimer(15, afterWait)

    fade.direction = 1
    timer.createAndStartTimer(6, frame1)

def startGathering():
    fade.direction = 1

    def afterFade():
        global currentMap
        
        currentMap = "void"
        goose.frozen = True
        goose.hidden = True

        mushroomScavenging.sprite.hidden = False
        fade.direction = -1
    
        def afterDialogue():
            global currentState
            currentState = "mushroom_gathering"
            mushroomScavenging.bladeSprite.hidden = False
            mushroomScavenging.spawnMushroom(splash)
            mushroomScavenging.label.hidden = False
            mushroomScavenging.timerLabel.hidden = False
            mushroomScavenging.started = True
        
        dialogue.speak(None, [
        "Harvest mushrooms\nby pressing the\nmiddle button",
        "Discard poisonous\nspotted mushrooms\nwith the right\nbutton",
        "Score at least\n15 points to\ncontinue"
        ], afterDialogue, True)
    
    timer.createAndStartTimer(6, afterFade)

def finishedGathering():
    fade.direction = 1

    def afterFade():
        global currentMap
        
        mushroomScavenging.bladeSprite.hidden = True
        mushroomScavenging.sprite.hidden = True
        mushroomScavenging.mushroom.sprite.hidden = True
        mushroomScavenging.mushroom.spritePoision.hidden = True
        mushroomScavenging.label.hidden = True
        mushroomScavenging.timerLabel.hidden = True

        currentMap = "outside_hotel_sunset"
        fade.direction = -1

        print(currentMap)
        
        goose.x = goose.afterGatherX
        goose.hidden = False
        goose.frozen = False
        
        stella.x = 260
        stella.sleeping = True
        stella.direction = 0
        stella.walking = False
        stella.map = "outside_hotel_sunset"
    
    timer.createAndStartTimer(6, afterFade)

def exitHotel():
    def afterFade():
        global currentMap
        global currentState

        fade.direction = -1
        currentMap = "outside_hotel"
        goose.x = 120
        
        if currentState == "metStella":
            def afterSpeak():
                def stellaScare():
                    
                    goose.frozen = True
                    goose.sprite.flip_x = True
                    greygoose.x = stella.x + 100
                    greygoose.direction = -5

                    greygoose.map = "outside_hotel"
                    stella.customUpdate = None
                    stella.direction = -15
                    stella.sprite.flip_x = True
                    dialogue.speak("stella", stella.dialogues["meetOutside3"], None, True)

                    timer.createAndStartTimer(15, encounter)

                dialogue.speak("stella", stella.dialogues["meetOutside2"], stellaScare, True)
                
                stella.direction = 5
                stella.walking = True
                stella.sprite.flip_x = False
                stella.customUpdate = stella.metStellaOutside
            
            dialogue.speak("stella", stella.dialogues["meetOutside"], afterSpeak, True)
    
    fade.direction = 1
    timer.createAndStartTimer(6, afterFade)

def upstairsHotel():
    global currentMap
    
    def afterFade():
        global currentMap
        global currentState

        fade.direction = -1
        currentMap = "inside_hotel_floor2"
        goose.x = 400
        goose.sprite.flip_x = False
    
    fade.direction = 1
    timer.createAndStartTimer(6, afterFade)

def downstairsHotel():
    global currentMap

    def afterFade():
        global currentMap
        global currentState

        fade.direction = -1
        currentMap = "inside_hotel"
        goose.x = 390
        goose.sprite.flip_x = False
        
        if currentState == "metStella" and stella.map == "inside_hotel":
            stella.direction = -5
            stella.customUpdate = stella.metStellaDownstairs
    
    fade.direction = 1
    timer.createAndStartTimer(6, afterFade)

def meetStella():
    goose.frozen = True
    
    def afterWait():
        stella.sleeping = False
        
        def stellaSpeak():
            def afterSpeak():
                global currentState
                stella.walking = True
                stella.direction = 5
                goose.frozen = False
                currentState = "metStella"
                
                stella.customUpdate = stella.metStellaUpstairs
            
            dialogue.speak("stella", stella.dialogues["meet"], afterSpeak, False)
        
        timer.createAndStartTimer(10, stellaSpeak)

    timer.createAndStartTimer(10, afterWait)

def ending():
    goose.frozen = True
    goose.sprite.flip_x = False

    def afterWait():
        stella.sleeping = False
        stella.sprite.flip_x = False
        
        def afterWait2():
            def afterTalk():
                fade.direction = 1
                
                def afterFade():
                    def afterTalk2():
                        global currentState
                        currentState = "theEnd"

                    global currentMap
                    currentMap = "ending"
                    fade.direction = -1
                    goose.x = 0
                    goose.frozen = True
                    goose.hidden = True
                    
                    dialogue.speak("stella", stella.dialogues["ending2"], afterTalk2, False)
                
                timer.createAndStartTimer(6, afterFade)
                
            dialogue.speak("stella", stella.dialogues["ending"], afterTalk, False)
        
        timer.createAndStartTimer(15, afterWait2)
    
    timer.createAndStartTimer(10, afterWait)

maps = {
    "void" : Map(
        Parallax([]),
        [],
        [],
        0, 90
    ),
    "outside_hotel" : Map(
        Parallax([
            ParallaxFrame("assets/bg_sky.bmp", 0.1, True, 0),
            ParallaxFrame("assets/bg_hill.bmp", 0.2, True, 0),
            ParallaxFrame("assets/trees2.bmp", 0.5, True, 0),
            ParallaxFrame("assets/trees1.bmp", 0.6, True, 0),
            ParallaxFrame("assets/building.bmp", 0.9, False, 0),
            ParallaxFrame("assets/ground.bmp", 1, True, 0),
            ParallaxFrame("assets/pond.bmp", 1, False, -100),
        ]),
        [
            Interactable(110, 40, enterHotel)
        ],
        [],
        -100, 
        100000
    ),
    "outside_hotel_sunset" : Map(
        Parallax([
            ParallaxFrame("assets/bg_sky_sunset.bmp", 0.1, True, 0),
            ParallaxFrame("assets/bg_hill.bmp", 0.2, True, 0),
            ParallaxFrame("assets/trees2.bmp", 0.5, True, 0),
            ParallaxFrame("assets/trees1.bmp", 0.6, True, 0),
            ParallaxFrame("assets/building.bmp", 0.9, False, 0),
            ParallaxFrame("assets/ground.bmp", 1, True, 0),
            ParallaxFrame("assets/pond.bmp", 1, False, -100),
        ]),
        [],
        [
            Trigger(250, True, ending)
        ],
        -100, 
        100000
    ),
    
    "inside_hotel": Map(
        Parallax([
            ParallaxFrame("assets/hotel_floor.bmp", 1, False, 0)
        ]),
        [
            Interactable(-15, 30, exitHotel),
            Interactable(370, 30, upstairsHotel)
        ],
        [],
        -50, 
        400
    ),

    "inside_hotel_floor2": Map(
        Parallax([
            ParallaxFrame("assets/hotel_floor2.bmp", 1, False, 0)
        ]),
        [
            Interactable(400, 50, downstairsHotel),
        ],
        [
            Trigger(10, True, meetStella)
        ],
        -50,
        430
    ),

    "encounter_1": Map(
        Parallax([
            ParallaxFrame("assets/encounter1.bmp", 1, False, 0)
        ]),
        [], [], -100, 100
    ),

    "encounter_2": Map(
        Parallax([
            ParallaxFrame("assets/encounter2.bmp", 1, False, 0)
        ]),
        [], [], -100, 100
    ),

    "ending": Map(
        Parallax([
            ParallaxFrame("assets/ending.bmp", 1, False, 0)
        ]),
        [], [], -100, 100
    )
}

for name, i in maps.items():
    for frame in i.parallax.frames:
        splash.append(frame.sprite)
        splash.append(frame.spriteNext)

greygooseBossfight = GreyGooseBossfight()
splash.append(greygooseBossfight.sprite)
splash.append(greygooseBossfight.healthBar)
splash.append(greygooseBossfight.angerSprite)

mushroomScavenging = MushroomScavenging()
splash.append(mushroomScavenging.sprite)
splash.append(mushroomScavenging.bladeSprite)
splash.append(mushroomScavenging.label)
splash.append(mushroomScavenging.timerLabel)

goose = Goose()
splash.append(goose.sprite)
splash.append(goose.healthBar)
stella = Stella()
splash.append(stella.sprite)
stella.sleeping = True
stella.map = "inside_hotel_floor2"
stella.x = 15

greygoose = GreyGoose()
splash.append(greygoose.sprite)
greygoose.map = "inside_hotel"
greygoose.x = -10000
greygoose.walking = True

buttonIndicator = ButtonIndicator()
splash.append(buttonIndicator.sprite)

splash.append(fade.sprite)

font = bitmap_font.load_font("assets/RobotoMono.bdf")

debugLabel = label.Label(font, text="AwesomeSauce", color=0xFFFFFF)
debugLabel.x = 5
debugLabel.y = 5

#splash.append(debugLabel)

splash.append(dialogue.bgSprite)
splash.append(dialogue.label)

dialogue.loadSpeaker("assets/faces/stella.bmp", "stella")

theEndSheet = displayio.OnDiskBitmap("assets/the_end.bmp")
theEndSprite = displayio.TileGrid(theEndSheet, pixel_shader=theEndSheet.pixel_shader)
theEndSprite.y = -60
splash.append(theEndSprite)

for name, speaker in dialogue.speakers.items():
    splash.append(speaker)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            if currentState == "mushroom_gathering":
                mushroomScavenging.slash()
            else:
                if dialogue.speaking:
                    if not dialogue.autoContinue: dialogue.nextText() 
                else:
                    for interactable in maps[currentMap].interactables:
                        interactable.use(goose.x)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            if currentState == "mushroom_gathering":
                mushroomScavenging.mushroom.skipped = True
    
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_UP]:
        if currentState == "bossfight":
            goose.parrying = True
    elif keys[pygame.K_LEFT]:
        goose.parrying = False
        if goose.x > maps[currentMap].leftBound and not goose.frozen and not goose.parrying:
            goose.walking = True
            goose.x -= goose.SPEED
            goose.sprite.flip_x = False
            
            goose.updateGooseWalk()
    
    elif keys[pygame.K_RIGHT]:
        goose.parrying = False
        if goose.x < maps[currentMap].rightBound and not goose.frozen and not goose.parrying:
            goose.walking = True
            goose.x += goose.SPEED
            goose.sprite.flip_x = True

            goose.updateGooseWalk()       
    else:
        goose.parrying = False
        goose.walking = False

    
    goose.sprite[0] = goose.frame()
    buttonIndicator.update()
    maps[currentMap].parallax.updatePosition(-goose.x)
    debugLabel.text = str(mushroomScavenging.bladeY) + "/" + str(mushroomScavenging.mushroom.sprite.y if mushroomScavenging.mushroom != None else 0)
    
    buttonIndicator.sprite.hidden = True
    
    for interactable in maps[currentMap].interactables:
        if interactable.canUse(goose.x):
            buttonIndicator.sprite.hidden = False
    
    for trigger in maps[currentMap].triggers:
        trigger.update(goose.x)

    if currentState == "bossfight":
        if goose.health <= 0:
            failBossfight()
        elif greygooseBossfight.health <= 0:
            winBossfight()
    
    updateMaps(maps, currentMap)
    
    fade.fade()
    timer.update()
    dialogue.update()
    stella.update(goose.x, currentMap)
    greygoose.update(goose.x, currentMap)
    greygooseBossfight.update(goose)
    goose.update()
    mushroomScavenging.update(dialogue)

    if currentState == "mushroom_gathering":
        if mushroomScavenging.win:
            currentState = "ending"
            finishedGathering()

    if currentState == "theEnd" and theEndSprite.y < 0:
        theEndSprite.y += 3

    if stella.customUpdate != None: stella.customUpdate(goose.x, currentMap)
    
    time.sleep(0.1)
