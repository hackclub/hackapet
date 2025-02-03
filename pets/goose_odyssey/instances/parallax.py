import displayio
import math

class ParallaxFrame:
    def __init__(self, file, speed, doRepeat, xOffset):
        self.speed = speed
        self.sheet = displayio.OnDiskBitmap(file)
        
        self.sprite = displayio.TileGrid(
            self.sheet,
            pixel_shader=self.sheet.pixel_shader,
            x=xOffset
        )
        
        self.spriteNext = displayio.TileGrid(
            self.sheet,
            pixel_shader=self.sheet.pixel_shader,
            x=self.sheet.width+xOffset
        )

        self.spriteNext.hidden = not doRepeat
        
        self.xOffset = xOffset
        self.doRepeat = doRepeat
    
    def getRepeatOffset(self, offset):
        return math.floor((offset * self.speed) / (self.sheet.width)) * self.sheet.width 
     
    def updatePosition(self, offset):
        repeatOffset = self.getRepeatOffset(offset) if self.doRepeat else 0
        
        self.sprite.x = int(offset * self.speed - repeatOffset) + self.xOffset

        if self.doRepeat:
            self.spriteNext.x = int(offset * self.speed - self.sheet.width - repeatOffset) + self.xOffset
        else:
            self.spriteNext.x = -10000
        

class Parallax:
    def __init__(self, frames):
        self.frames = frames

    def appendFrame(self, frame, splash):
        splash.insert(splash.index(self.frames[-1].sprite) + 2, frame.sprite)
        splash.insert(splash.index(self.frames[-1].spriteNext) + 2, frame.spriteNext)
        self.frames.append(frame)
    
    def updatePosition(self, offset):
        for frame in self.frames:
            frame.updatePosition(offset)
