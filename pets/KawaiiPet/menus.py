from functions import *
from toml import dump,load
from random import randint,uniform
import pygame  as pg
from characters import *
from variables import *

## Menus/Types
def startMenu(screen):
    animBG.update()
    animBG.render(screen)
    titleTxt,titleRect=font.render(f"KawaiiPet",fgcolor=textColor)
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

def gameMenu(screen):
    animBG.update()
    animBG.render(screen)

    titleTxt,titleRect=font.render(f"KawaiiPet",fgcolor=textColor)
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
    
def startSettings(screen):
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


def gamePauseMenu(screen):
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

def activitiesMenu(screen):
    pg.draw.rect(screen,(17, 17, 27),skyRect)
    titleTxt,titleRect=font.render(f"Paused",fgcolor=textColor)
    activitiesTexts=[f">Bath",f">Feed",f">Pet your pet!",f">Shout at it!"]
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
    screen.blit(menuSelect,(WIDTH//2-menuRect.width//2,9*menuRect.height+10*SCALE))
    screen.blit(Btn1,(WIDTH//2-Btn1Rect.width//2,9*Btn1Rect.height+10*SCALE))
    screen.blit(Btn2,(WIDTH//2-Btn2Rect.width//2,9*Btn2Rect.height+10*SCALE))

def startHelp(screen):
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

def startGame(screen):
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
