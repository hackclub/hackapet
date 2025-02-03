from instances.parallax import Parallax, ParallaxFrame

class Interactable:
    def __init__(self, x, width, function):
        self.x = x
        self.width = width
        self.function = function
    
    def canUse(self, x):
        return x >= self.x and x <= self.x + self.width
    
    def use(self, x):
        if self.canUse(x):
            self.function()

class Trigger:
    def __init__(self, x, oneshot, function):
        self.x = x
        self.oneshot = oneshot # This is a reference to the 2016 hit indie game OneShot
        self.function = function
        
        self.triggered = False
    
    def update(self, x):
        if x == self.x:
            if self.oneshot and self.triggered: return
            
            self.triggered = True
            self.function()

class Map:
    def __init__(self, parallax, interactables, triggers, leftBound, rightBound):
        self.parallax = parallax
        self.interactables = interactables
        self.triggers = triggers
        self.leftBound = leftBound
        self.rightBound = rightBound

def updateMaps(maps, currentMap):
    for name, map in maps.items():
        if currentMap != name:
            for frame in map.parallax.frames:
                frame.spriteNext.hidden = True
                frame.sprite.hidden = True
        else:
            for frame in map.parallax.frames:
                frame.spriteNext.hidden = False
                frame.sprite.hidden = False

            