from functions import *
from toml import dump,load
from random import randint,uniform
import pygame  as pg
from characters import *
from variables import *

## loading config
with open("settings.toml", "r") as f:
    config = load(f)

def setConf(section,var,value) -> None:
    config[section][var]=value
    with open("settings.toml","w") as f:
        dump(config,f)

def getConf(section, var):
    try:
        return config[section][var]
    except KeyError:
        print(f"Unable to find {var}, in {section} section of the configuration")
        return None

def saveSettings():
    setConf("general","pet",PET_NUM)
    setConf("general","map",MAP_NUM)
    setConf("sounds","bgm",PLAY_BGM)
    setConf("sounds","sfx",PLAY_SFX)

