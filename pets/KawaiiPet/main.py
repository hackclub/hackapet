from settings import *
from characters import *
from random import randint,uniform
from variables import *
from functions import *

with open("settings.toml", "r") as f:
    config = load(f)

## Initializing pygame and display
pg.init()
screen=pg.display.set_mode(SIZE)
pg.display.set_caption("KawaiiPet")
pg.event.set_allowed([pg.QUIT,pg.KEYDOWN,pg.KEYUP])

clock=pg.time.Clock()

font=pg.freetype.Font("font/PixelatedElegance.ttf",15*SCALE)

############################## Menu variables ####################################################
## Beach Map
ground=pg.image.load("images/Sand.png").convert_alpha()
ground=pg.transform.scale(ground,(WIDTH,15*SCALE))
skyRect=pg.Rect(0,0,WIDTH,HEIGHT)
sun=AnimSprite("images/CuteSun.png",2*SCALE,2*SCALE,30,30,SCALE,5,4)
cloud=Sprite("images/Cloud.png",randint(-30,WIDTH+30),randint(0,3*SCALE),50,32,SCALE)
cloud2=Sprite("images/Cloud.png",randint(-30,WIDTH+30),randint(0,3*SCALE),50,32,SCALE*2/3)
bucket=AnimSprite("images/Bucket.png",-10*SCALE,HEIGHT-15*SCALE-50*SCALE,40,50,SCALE,20,4)
sandhill=Sprite("images/Sandhill.png",WIDTH-25*SCALE,HEIGHT-15*SCALE-33*SCALE,40,50,SCALE*2/3)

bgHome=Sprite("images/bg/bgHome.png",0,0,128,128,SCALE)

## Start Menu
BtnArr=[1,0,0]
inMenu=True
animBG=AnimSprite("images/bg/bg.png",0,0,128,128,SCALE,20,12)

## extra game
garden=Sprite("images/bg/Garden.png",0,0,128,128,SCALE)

highscore=getConf("game","highscore")
bones=[]

boneSound=pg.mixer.Sound("audio/bone.wav")
bonePoints=0
boneFps=0
highScore=getConf("scores","highscore")

SPAWN_EVENT=pg.USEREVENT+1
pg.time.set_timer(SPAWN_EVENT,BONE_INTERVAL)

## Game Pause Menu
pausedBtnsArr=[1,0,0,0]

## SettingsMenu
SettingsBtnArr=[1,0,0,0]
activitiesBtnsArr=[1,0,0,0]

## Pet
pet=Character("images/Pets/KawaiiDog/KawaiiDog.png",(WIDTH//2)-((78*SCALE)//2),HEIGHT-(15*SCALE)-78*SCALE,78,78,SCALE,5,10)

### Variables
# 0-> Start Menu  ,1 -> Game , 2-> settings menu ,  3-> Help menu ,4->Paused Menu ,5->Activities page
menuType=0
running=1
musicStarted=False
currMusic="audio/bgm/menuBgm.mp3"

## Colors
textColor=(205,214,244)
selectedColor=(137, 180, 250)

## SFX
selectChange=pg.mixer.Sound("audio/select.mp3")
pressEnter=pg.mixer.Sound("audio/selectConfirm.mp3")
eat=pg.mixer.Sound("audio/eat.mp3")

######################################## Extra functions ######################################

## Functions
def setConf(section:str,var:str,value:str) -> None:
    config[section][var]=value
    with open("settings.toml","w") as f:
        dump(config,f)

def getConf(section:str, var:str):
    try:
        return config[section][var]
    except KeyError:
        print(f"Unable to find {var}, in {section} section of the configuration")
        return None
def saveSettings() ->  None:
    setConf("general","pet",PET_NUM)
    setConf("general","map",MAP_NUM)
    setConf("sounds","bgm",PLAY_BGM)
    setConf("sounds","sfx",PLAY_SFX)

def selectDown(btnArr:list) -> list:
    newArr=[0]*len(btnArr)
    for ind,i in enumerate(btnArr):
        if i==1:
            if ind==len(btnArr)-1:
                newArr[-1]=1
            else:
                newArr[ind+1]=1
                if PLAY_SFX:
                    selectChange.play()
    # print(newArr)
    return newArr

def selectUp(btnArr:list)->list:
    newArr=[0]*len(btnArr)
    for ind,i in enumerate(btnArr):
        if i==1:
            if ind==0:
                newArr[0]=1
            else:
                newArr[ind-1]=1
                if PLAY_SFX:
                    selectChange.play()
    return newArr

def selectOption()->None:
    global menuType,PLAY_SFX,PLAY_BGM,MAP_NUM,PET_NUM
    if menuType==0:
        if BtnArr[0]==1:
            menuType=1 #Game
            musicStarted=False
        elif BtnArr[1]==1:
            menuType=2 #Settings
        else:
            menuType=3 #Help
    elif menuType==2:
        if SettingsBtnArr[0]==1:
            PET_NUM=0
            # PET_NUM+=1
            # if PET_NUM==2:
            #     PET_NUM=0
        elif SettingsBtnArr[1]==1:
            MAP_NUM+=1
            if MAP_NUM==2:
                MAP_NUM=0

        elif SettingsBtnArr[2]==1:
            PLAY_BGM=not PLAY_BGM
            if PLAY_BGM==False:
                pg.mixer.music.stop()
            else:
                pg.mixer.music.load(currMusic)
                pg.mixer.music.play()
        elif SettingsBtnArr[3]==1:
            PLAY_SFX=not PLAY_SFX
    elif menuType==4:
        if pausedBtnsArr[0]:
            menuType=1
        elif pausedBtnsArr[1]:
            menuType=0
        elif pausedBtnsArr[2]:
            menuType=5
        elif pausedBtnsArr[3]:
            quit()
    elif menuType==5:
        if activitiesBtnsArr[0]:
            menuType=6
        elif activitiesBtnsArr[1]:
            pet.showAnim("images/Pets/KawaiiDog/KawaiiDog-feed.png",75)
            eat.play()
            menuType=1
        elif activitiesBtnsArr[2]:
            pet.showAnim("images/Pets/KawaiiDog/KawaiiDog-petting.png")
            menuType=1
        elif activitiesBtnsArr[3]:
            pet.showAnim("images/Pets/KawaiiDog/KawaiiDog-scold.png",200000)
            menuType=1

    saveSettings()
    if PLAY_SFX:
        pressEnter.play()

############################################### Menu Functions ################################################

def startMenu(screen:pg.surface.Surface) -> None:
    animBG.update()
    animBG.render(screen)
    titleTxt,titleRect=font.render("KawaiiPet",fgcolor=textColor)
    if BtnArr[0]==1:
        Btn1,Btn1Rect=font.render(BtnTexts[0].replace(">","> "),fgcolor=selectedColor,size=10*SCALE)
        Btn2,Btn2Rect=font.render(BtnTexts[1],fgcolor=textColor,size=10*SCALE)
        Btn3,Btn3Rect=font.render(BtnTexts[2],fgcolor=textColor,size=10*SCALE)
    elif BtnArr[1]==1:
        Btn1,Btn1Rect=font.render(BtnTexts[0],fgcolor=textColor,size=10*SCALE)
        Btn2,Btn2Rect=font.render(BtnTexts[1].replace(">","> "),fgcolor=selectedColor,size=10*SCALE)
        Btn3,Btn3Rect=font.render(BtnTexts[2],fgcolor=textColor,size=10*SCALE)
    else:
        Btn1,Btn1Rect=font.render(BtnTexts[0],fgcolor=textColor,size=10*SCALE)
        Btn2,Btn2Rect=font.render(BtnTexts[1],fgcolor=textColor,size=10*SCALE)
        Btn3,Btn3Rect=font.render(BtnTexts[2].replace(">","> "),fgcolor=selectedColor,size=10*SCALE)

    screen.blit(titleTxt,(WIDTH//2-titleRect.width//2,HEIGHT//2-titleRect.height//2-20*SCALE))
    screen.blit(Btn1,(WIDTH//2-Btn1Rect.width//2,HEIGHT//2-Btn1Rect.height//2))
    screen.blit(Btn2,(WIDTH//2-Btn2Rect.width//2,HEIGHT//2-Btn2Rect.height//2+15*SCALE))
    screen.blit(Btn3,(WIDTH//2-Btn3Rect.width//2,HEIGHT//2-Btn3Rect.height//2+30*SCALE))

    
def startSettings(screen:pg.surface.Surface)->None:
    pg.draw.rect(screen,(17, 17, 27),skyRect)
    titleTxt,titleRect=font.render(f"Settings",fgcolor=textColor)
    SettingsTexts=[f">Pet Type: {pets[PET_NUM]}",f">Map: {maps[MAP_NUM]}",f">Background Music: {PLAY_BGM}",f">Sound Effects: {PLAY_SFX}"]
    if SettingsBtnArr[0]==1:
        petSelect,petRect=font.render(SettingsTexts[0].replace(">","> "),fgcolor=selectedColor,size=5*SCALE)
        mapSelect,mapRect=font.render(SettingsTexts[1],fgcolor=textColor,size=5*SCALE)

        Btn1,Btn1Rect=font.render(SettingsTexts[2],fgcolor=textColor,size=5*SCALE)
        Btn2,Btn2Rect=font.render(SettingsTexts[3],fgcolor=textColor,size=5*SCALE)
    elif SettingsBtnArr[1]==1:
        petSelect,petRect=font.render(SettingsTexts[0],fgcolor=textColor,size=5*SCALE)
        mapSelect,mapRect=font.render(SettingsTexts[1].replace(">","> "),fgcolor=selectedColor,size=5*SCALE)

        Btn1,Btn1Rect=font.render(SettingsTexts[2],fgcolor=textColor,size=5*SCALE)
        Btn2,Btn2Rect=font.render(SettingsTexts[3],fgcolor=textColor,size=5*SCALE)
    elif SettingsBtnArr[2]==1:
        petSelect,petRect=font.render(SettingsTexts[0],fgcolor=textColor,size=5*SCALE)
        mapSelect,mapRect=font.render(SettingsTexts[1],fgcolor=textColor,size=5*SCALE)

        Btn1,Btn1Rect=font.render(SettingsTexts[2].replace(">","> "),fgcolor=selectedColor,size=5*SCALE)
        Btn2,Btn2Rect=font.render(SettingsTexts[3],fgcolor=textColor,size=5*SCALE)

    elif SettingsBtnArr[3]==1:
        petSelect,petRect=font.render(SettingsTexts[0],fgcolor=textColor,size=5*SCALE)
        mapSelect,mapRect=font.render(SettingsTexts[1],fgcolor=textColor,size=5*SCALE)

        Btn1,Btn1Rect=font.render(SettingsTexts[2],fgcolor=textColor,size=5*SCALE)
        Btn2,Btn2Rect=font.render(SettingsTexts[3].replace(">","> "),fgcolor=selectedColor,size=5*SCALE)

    screen.blit(titleTxt,(WIDTH//2-titleRect.width//2,10*SCALE))
    screen.blit(petSelect,(WIDTH//2-petRect.width//2,9*petRect.height+10*SCALE))
    screen.blit(mapSelect,(WIDTH//2-mapRect.width//2,9*mapRect.height+10*SCALE*2))
    screen.blit(Btn1,(WIDTH//2-Btn1Rect.width//2,9*Btn1Rect.height+10*SCALE*3))
    screen.blit(Btn2,(WIDTH//2-Btn2Rect.width//2,9*Btn2Rect.height+10*SCALE*4.5))


def gamePauseMenu(screen:pg.surface.Surface)->None:
    pg.draw.rect(screen,(17, 17, 27),skyRect)
    titleTxt,titleRect=font.render(f"Paused",fgcolor=textColor)
    pausedTexts=[f">Resume",f">Back To Main Menu",f">Activities",f">Quit"]
    if pausedBtnsArr[0]==1:
        pausedSelect,pausedRect=font.render(pausedTexts[0].replace(">","> "),fgcolor=selectedColor,size=5*SCALE)
        menuSelect,menuRect=font.render(pausedTexts[1],fgcolor=textColor,size=5*SCALE)

        Btn1,Btn1Rect=font.render(pausedTexts[2],fgcolor=textColor,size=5*SCALE)
        Btn2,Btn2Rect=font.render(pausedTexts[3],fgcolor=textColor,size=5*SCALE)
    elif pausedBtnsArr[1]==1:
        pausedSelect,pausedRect=font.render(pausedTexts[0],fgcolor=textColor,size=5*SCALE)
        menuSelect,menuRect=font.render(pausedTexts[1].replace(">","> "),fgcolor=selectedColor,size=5*SCALE)

        Btn1,Btn1Rect=font.render(pausedTexts[2],fgcolor=textColor,size=5*SCALE)
        Btn2,Btn2Rect=font.render(pausedTexts[3],fgcolor=textColor,size=5*SCALE)
    elif pausedBtnsArr[2]==1:
        pausedSelect,pausedRect=font.render(pausedTexts[0],fgcolor=textColor,size=5*SCALE)
        menuSelect,menuRect=font.render(pausedTexts[1],fgcolor=textColor,size=5*SCALE)

        Btn1,Btn1Rect=font.render(pausedTexts[2].replace(">","> "),fgcolor=selectedColor,size=5*SCALE)
        Btn2,Btn2Rect=font.render(pausedTexts[3],fgcolor=textColor,size=5*SCALE)

    elif pausedBtnsArr[3]==1:
        pausedSelect,pausedRect=font.render(pausedTexts[0],fgcolor=textColor,size=5*SCALE)
        menuSelect,menuRect=font.render(pausedTexts[1],fgcolor=textColor,size=5*SCALE)

        Btn1,Btn1Rect=font.render(pausedTexts[2],fgcolor=textColor,size=5*SCALE)
        Btn2,Btn2Rect=font.render(pausedTexts[3].replace(">","> "),fgcolor=selectedColor,size=5*SCALE)

    screen.blit(titleTxt,(WIDTH//2-titleRect.width//2,10*SCALE))
    screen.blit(pausedSelect,(WIDTH//2-pausedRect.width//2,9*pausedRect.height+10*SCALE))
    screen.blit(menuSelect,(WIDTH//2-menuRect.width//2,9*menuRect.height+10*SCALE*2))
    screen.blit(Btn1,(WIDTH//2-Btn1Rect.width//2,9*Btn1Rect.height+10*SCALE*3))
    screen.blit(Btn2,(WIDTH//2-Btn2Rect.width//2,9*Btn2Rect.height+10*SCALE*4))

def activitiesMenu(screen:pg.surface.Surface)->None:
    pg.draw.rect(screen,(17, 17, 27),skyRect)
    titleTxt,titleRect=font.render(f"Activities",fgcolor=textColor)
    activitiesTexts=[f">Play with it",f">Feed",f">Pet your pet!",f">Shout at it!"]
    if activitiesBtnsArr[0]==1:
        pausedSelect,pausedRect=font.render(activitiesTexts[0].replace(">","> "),fgcolor=selectedColor,size=5*SCALE)
        menuSelect,menuRect=font.render(activitiesTexts[1],fgcolor=textColor,size=5*SCALE)

        Btn1,Btn1Rect=font.render(activitiesTexts[2],fgcolor=textColor,size=5*SCALE)
        Btn2,Btn2Rect=font.render(activitiesTexts[3],fgcolor=textColor,size=5*SCALE)
    elif activitiesBtnsArr[1]==1:
        pausedSelect,pausedRect=font.render(activitiesTexts[0],fgcolor=textColor,size=5*SCALE)
        menuSelect,menuRect=font.render(activitiesTexts[1].replace(">","> "),fgcolor=selectedColor,size=5*SCALE)

        Btn1,Btn1Rect=font.render(activitiesTexts[2],fgcolor=textColor,size=5*SCALE)
        Btn2,Btn2Rect=font.render(activitiesTexts[3],fgcolor=textColor,size=5*SCALE)
    elif activitiesBtnsArr[2]==1:
        pausedSelect,pausedRect=font.render(activitiesTexts[0],fgcolor=textColor,size=5*SCALE)
        menuSelect,menuRect=font.render(activitiesTexts[1],fgcolor=textColor,size=5*SCALE)

        Btn1,Btn1Rect=font.render(activitiesTexts[2].replace(">","> "),fgcolor=selectedColor,size=5*SCALE)
        Btn2,Btn2Rect=font.render(activitiesTexts[3],fgcolor=textColor,size=5*SCALE)

    elif activitiesBtnsArr[3]==1:
        pausedSelect,pausedRect=font.render(activitiesTexts[0],fgcolor=textColor,size=5*SCALE)
        menuSelect,menuRect=font.render(activitiesTexts[1],fgcolor=textColor,size=5*SCALE)

        Btn1,Btn1Rect=font.render(activitiesTexts[2],fgcolor=textColor,size=5*SCALE)
        Btn2,Btn2Rect=font.render(activitiesTexts[3].replace(">","> "),fgcolor=selectedColor,size=5*SCALE)

    screen.blit(titleTxt,(WIDTH//2-titleRect.width//2,10*SCALE))
    screen.blit(pausedSelect,(WIDTH//2-pausedRect.width//2,9*pausedRect.height+10*SCALE))
    screen.blit(menuSelect,(WIDTH//2-menuRect.width//2,9*menuRect.height+10*SCALE*2))
    screen.blit(Btn1,(WIDTH//2-Btn1Rect.width//2,9*Btn1Rect.height+10*SCALE*2.5))
    screen.blit(Btn2,(WIDTH//2-Btn2Rect.width//2,9*Btn2Rect.height+10*SCALE*4))

def startHelp(screen:pg.surface.Surface)->None:
    pg.draw.rect(screen,(17, 17, 27),skyRect)
    titleTxt,titleRect=font.render("Help",fgcolor=textColor)
    w=helpMessage.split(";")
    w2=helpKeybindings.split(";")
    screen.blit(titleTxt,(WIDTH//2-titleRect.width//2,10*SCALE))
    helpHeight=0

    for ind,line in enumerate(w):
        helpTxt,helpRect=font.render(line,fgcolor=textColor,size=4*SCALE)
        helpHeight=9*helpRect.height+10*SCALE*ind
        screen.blit(helpTxt,(WIDTH//2-helpRect.width//2,helpHeight))

    for ind,line in enumerate(w2):
        helpTxt,helpRect=font.render(line,fgcolor=selectedColor,size=4*SCALE)
        screen.blit(helpTxt,(WIDTH//2-helpRect.width//2,helpHeight+15*SCALE+10*SCALE*ind))

def petGame(screen:pg.surface.Surface)->None:
    global BONE_SPEED,boneFps,bonePoints,highscore

    if boneFps%100==0 and BONE_SPEED<=BONE_SPEED_MAX:
        BONE_SPEED+=1
    boneFps+=1
    garden.update(0,0)
    garden.render(screen)

    cloud.update(uniform(-1,-0.5),0)
    cloud.render(screen)

    pet.update()
    pet.render(screen)

    for b in bones:
        b.update(0,BONE_SPEED)
        b.render(screen,BONE_SPEED)
        if b.y > (HEIGHT-32-30):
            bones.remove(b)
            bonePoints-=20

        if pet.rect.colliderect(b.rect):
            boneSound.play()
            bonePoints+=10
            if bonePoints>highscore:
                highscore=bonePoints
                setConf("game","highscore",highscore)
            bones.remove(b)

    scoreTxt,scoreRect=font.render(f"Score: {bonePoints}",fgcolor="#11111b",size=10*SCALE)
    highscoreTxt,highscoreRect=font.render(f"H.S: {highscore}",fgcolor="#11111b",size=10*SCALE)
    screen.blit(ground, (0,HEIGHT-15*SCALE))
    screen.blit(scoreTxt, (10,10))
    screen.blit(highscoreTxt, (10,15*SCALE))

    if cloud.x<= -cloud.width*SCALE:
        cloud.x=WIDTH+30
        cloud.y=randint(0,3*SCALE)


def startGame(screen:pg.surface.Surface)->None:
    global map,bgHome
    if not map:
        pg.draw.rect(screen,(68,142,228),skyRect)

        cloud.update(uniform(-1,-0.5),0)
        cloud.render(screen)

        bucket.update()
        bucket.render(screen)
        
        sandhill.update(0,0)
        sandhill.render(screen)

        cloud2.update(uniform(-1,-0.5),0)
        cloud2.render(screen)

        sun.update()
        sun.render(screen)

        bucket.update()
        bucket.render(screen)

        pet.update()
        pet.render(screen)

        screen.blit(ground, (0,HEIGHT-15*SCALE))

        if cloud.x<= -cloud.width*SCALE:
            cloud.x=WIDTH+30
            cloud.y=randint(0,3*SCALE)

        if cloud2.x<= -cloud2.width*SCALE*2/3:
            cloud2.x=WIDTH+30
            cloud2.y=randint(0,3*SCALE)
    else:
        bgHome.update(0,0)
        bgHome.render(screen)

        pet.update()
        pet.render(screen)


def petGameScale(toscale=True):
    if toscale:
        pet.scale=SCALE*0.5
        pet.y=128*SCALE-15*SCALE-SCALE*pet.height*0.5
        pet.x=128*SCALE//2-pet.width*0.5*SCALE
        pet.rect=pg.Rect(pet.x,pet.y,pet.width*pet.scale*0.5,pet.height*pet.scale*0.5)
    else:
        pet.scale=SCALE
        pet.y=128*SCALE-15*SCALE-SCALE*pet.height
        pet.x=128*SCALE//2-pet.width*SCALE//2
        pet.rect=pg.Rect(pet.x,pet.y,pet.width*pet.scale,pet.height*pet.scale)



########################### Reading settings ###############################################
PLAY_BGM=getConf("sounds","bgm")
PLAY_SFX=getConf("sounds","sfx")

PET_NUM=getConf("general","pet")
MAP_NUM=getConf("general","map")

petScaled=False
moveLeft=False
moveRight=False


########################## Main Game Logic ####################################################

while running:

    #=====================| Key Events |=======================================================
    for event in pg.event.get():
        ## Quit Event
        if event.type==pg.QUIT:
            running=0
        elif event.type==SPAWN_EVENT:
            bone=Sprite("images/Collectibles/Bone.png",randint(0,128*SCALE-32*SCALE),0,32,32,SCALE)
            bones.append(bone)

        elif event.type==pg.KEYDOWN:
            ## Down Event
            if event.key in [pg.K_DOWN,pg.K_j]:
                if menuType==0:
                    BtnArr=selectDown(BtnArr)
                elif menuType==2:
                    SettingsBtnArr=selectDown(SettingsBtnArr)
                elif menuType==4:
                    pausedBtnsArr=selectDown(pausedBtnsArr)
                elif menuType==5:
                    activitiesBtnsArr=selectDown(activitiesBtnsArr)

            ## Up Event
            elif event.key in [pg.K_k,pg.K_UP]:
                if menuType==0:
                    BtnArr=selectUp(BtnArr)
                elif menuType==2:
                    SettingsBtnArr=selectUp(SettingsBtnArr)
                elif menuType==4:
                    pausedBtnsArr=selectUp(pausedBtnsArr)
                elif menuType==5:
                    activitiesBtnsArr=selectUp(activitiesBtnsArr)

            elif event.key in [pg.K_LEFT,pg.K_h]:

                if menuType==6:
                    if pet.x-PLAYER_SPEED>-pet.width*SCALE:
                        pet.x-=PLAYER_SPEED
                    else:
                        if not map:
                            map=True
                            pet.x=128*SCALE-pet.width*SCALE
                elif menuType==1:
                    if pet.x-PLAYER_SPEED>-pet.width*SCALE:
                        pet.x-=PLAYER_SPEED*PLAYER_SPEED_MULTIPLIER
                    else:
                        if not map:
                            map=True
                            pet.x=128*SCALE-pet.width*SCALE
            elif event.key in [pg.K_RIGHT,pg.K_l]:
                if menuType==6:
                    if pet.x+PLAYER_SPEED<128*SCALE:
                        pet.x+=PLAYER_SPEED
                    else:
                        if map:
                            map=False
                            pet.x=0
                elif menuType==1:
                    if pet.x+PLAYER_SPEED<128*SCALE:
                        pet.x+=PLAYER_SPEED*PLAYER_SPEED_MULTIPLIER
                    else:
                        if map:
                            map=False
                            pet.x=0


            ## Quit Event (2)
            elif event.key==pg.K_q:
                running=0

            ## Select Event
            elif event.key==pg.K_RETURN: 
                selectOption()

            ## Escape Event
            elif event.key==pg.K_ESCAPE:
                if menuType!=1:
                    menuType=0
                else:
                    menuType=4
        elif event.type==pg.KEYUP:
            if event.key in [pg.K_LEFT,pg.K_h]:
                if menuType==6 or menuType==1:
                    moveLeft=False

            elif event.key in [pg.K_RIGHT,pg.K_l]:
                if menuType==6 or menuType==1:
                    moveRight=False

        ## Scolling events
        elif event.type==pg.MOUSEWHEEL:
            if menuType==0:
                if event.y==1:
                    BtnArr=selectUp(BtnArr)
                elif event.y==-1:
                    BtnArr=selectDown(BtnArr)
            elif menuType==2:
                if event.y==1:
                    SettingsBtnArr=selectUp(SettingsBtnArr)
                elif event.y==-1:
                    SettingsBtnArr=selectDown(SettingsBtnArr)
            elif menuType==4:
                if event.y==1:
                    pausedBtnsArr=selectUp(pausedBtnsArr)
                elif event.y==-1:
                    pausedBtnsArr=selectDown(pausedBtnsArr)
            elif menuType==5:
                if event.y==1:
                    activitiesBtnsArr=selectUp(activitiesBtnsArr)
                elif event.y==-1:
                    activitiesBtnsArr=selectDown(activitiesBtnsArr)

        ## Left Click logic
        elif event.type==pg.MOUSEBUTTONDOWN:
            if event.button==1:
                selectOption()


    #==============| Displaying Menus/Game |============================
    if menuType==0:
        startMenu(screen)
        if PLAY_BGM and not musicStarted:
            currMusic="audio/bgm/menuBgm.mp3"
            pg.mixer.music.stop()
            pg.mixer.music.load(currMusic)
            pg.mixer.music.play(loops=-1)
            musicStarted=True
    elif menuType==1:
        if petScaled:
            petGameScale(False)
            petScaled=False
        startGame(screen)
        if PLAY_BGM and musicStarted:
            if not map:
                currMusic="audio/bgm/oceanWaves.mp3"
                pg.mixer.music.stop()
                pg.mixer.music.load(currMusic)
                pg.mixer.music.play(loops=-1)
                musicStarted=False
            else:
                currMusic="audio/bgm/menuBgm.mp3"
                pg.mixer.music.stop()
                pg.mixer.music.load(currMusic)
                pg.mixer.music.play(loops=-1)
                musicStarted=False


        if moveLeft:
            pet.x-=PLAYER_SPEED
        elif moveRight:
            pet.x+=PLAYER_SPEED
    elif menuType==2:
        startSettings(screen)
    elif menuType==3:
        startHelp(screen)
    elif menuType==4:
        gamePauseMenu(screen)
    elif menuType==5:
        activitiesMenu(screen)
    elif menuType==6:
        if not petScaled:
            petGameScale()
            bones=[]
            petScaled=True
        petGame(screen)
        if moveLeft:
            if pet.x-PLAYER_SPEED>0:
                pet.x-=PLAYER_SPEED
        elif moveRight:
            if pet.x-PLAYER_SPEED<128*SCALE-pet.width*SCALE*0.5:
                pet.x+=PLAYER_SPEED

    pg.display.flip()
    clock.tick(FPS)
pg.quit()
