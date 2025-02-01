import pygame as pg


class AnimSprite():
    def __init__(self,sheet,x,y,width,height,scale,frameChange,totalFrames):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.scale=scale

        ## Player Images/Sprites
        self.spriteSheet=pg.image.load(sheet).convert_alpha()
        self.og_image=pg.Surface((width,height),pg.SRCALPHA).convert_alpha()
        self.rect=pg.Rect(x,y,width*scale,height*scale)

        ## Counters for animations
        self.spriteIndex=0
        self.frameCounter=0
        self.frameChangeRate=frameChange
        self.totalSpriteFrames=totalFrames

    def update(self):
        self.frameCounter+=1
        if self.frameCounter>=self.frameChangeRate:
            self.spriteIndex=(self.spriteIndex+1)%self.totalSpriteFrames
            self.frameCounter=0
            if self.spriteIndex>=self.totalSpriteFrames:
                self.spriteIndex=0
            self.image=self.og_image.fill((0,0,0,0))
            self.og_image.blit(self.spriteSheet,(0,0),(self.spriteIndex*self.width,0,self.width,self.height))
        self.rect.x=self.x
        self.rect.y=self.y

    def render(self,surf):
        self.image=pg.transform.scale(self.og_image,(self.width*self.scale,self.height*self.scale))
        surf.blit(self.image,(self.x,self.y))

class Character(AnimSprite):
    def __init__(self,sheet,x,y,width,height,scale,frameChange,totalFrames):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.scale=scale
        self.angle=0
        self.flippedX=False

        ## Player States
        self.playerState="MOVING"
        self.rotatedTo=2 # 1-> Left, 2->Right, -1->Up, -2->Down

        ## Player stats
        self.happiness=100
        self.energy=100
        
        ## Player Images/Sprites
        self.spriteSheetOg=pg.image.load(sheet).convert_alpha()
        self.spriteSheet=pg.image.load(sheet).convert_alpha()
        self.og_image=pg.Surface((width,height),pg.SRCALPHA).convert_alpha()
        self.rect=pg.Rect(self.x,self.y,width*scale,height*scale)

        ## Counters for animations
        self.spriteIndex=0
        self.frameCounter=0
        self.frameChangeRate=frameChange
        self.totalSpriteFrames=totalFrames

        self.animFrame=0
        self.animFrameLimit=0

    def rotate(self,angle):
        self.angle=angle
    def flip(self,flipBool):
        self.flippedX = flipBool
    def render(self,surf):
        self.image=pg.transform.scale(pg.transform.flip(pg.transform.rotate(self.og_image,self.angle),self.flippedX,False),(self.width*self.scale,self.height*self.scale))
        surf.blit(self.image,(self.x,self.y))
        self.animFrame+=1
        self.rect.x=self.x
        self.rect.y=self.y
        if self.animFrame==self.animFrameLimit:
            self.spriteSheet=self.spriteSheetOg
            self.animFrame=0

    def showAnim(self,spritePath,limit=250):
        self.spriteSheet=pg.image.load(spritePath).convert_alpha()
        self.animFrameLimit=limit
        self.animFrame=0

class Sprite():
    def __init__(self,sheet,x,y,width,height,scale):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.scale=scale
        self.angle=0

        self.rect=pg.Rect(self.x,self.y,width*scale,height*scale)
        ## Player Images/Sprites
        self.og_image=pg.image.load(sheet)

    def update(self,dx,dy):
        self.x+=dx
        self.y+=dy
        self.rect.x=self.x
        self.rect.y=self.y

    def render(self,surf,dtheta=0):
        self.image=pg.transform.scale(pg.transform.rotate(self.og_image,self.angle+dtheta),(self.width*self.scale,self.height*self.scale))
        self.angle+=dtheta
        surf.blit(self.image,(self.x,self.y))

class Block():
    def __init__(self,x,y,width,height,scale):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.scale=scale
        self.angle=0
        self.dim=(self.x,self.y,self.x+width,self.y+height)
        self.rect=pg.Rect(x,y,width*scale,height*scale)

    def render(self,surf):
        pg.draw.rect(surf,(64,128,20),self.rect)


