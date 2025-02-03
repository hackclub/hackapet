import displayio
import random
import timer
from adafruit_display_shapes.rect import Rect

FEATHER_START_Y = 30
FEATHER_END_Y = 128

def checkCollision(x1, y1, w1, h1, x2, y2, w2, h2):
    return x1 < x2+w2 and x2 < x1+w1 and y1 < y2+h2 and y2 < y1+h1


class Feather:
    def __init__(self, x, target, parryable):
        self.sheet = displayio.OnDiskBitmap("assets/parryable_feather.bmp" if parryable else "assets/feather.bmp")
        self.sprite = displayio.TileGrid(self.sheet, pixel_shader=self.sheet.pixel_shader)
        
        self.start = x
        self.target = target
        self.sprite.x = x
        self.hit = False
        self.progress = 0
        self.duration = 15 if parryable else 10
        self.parryable = parryable
        self.parried = False
    
    def update(self, goose):
        time = (self.progress / self.duration)
        
        self.sprite.x = int((1 - time) * self.start + time * self.target)
        if self.parried:
            self.sprite.y = int((1 - time) * FEATHER_END_Y + time * FEATHER_START_Y)
        else:
            self.sprite.y = int((1 - time) * FEATHER_START_Y + time * FEATHER_END_Y)
        
        if self.parryable and goose.parrying and not self.parried:
            if checkCollision(self.sprite.x, self.sprite.y, 11, 17, goose.sprite.x - 5, goose.sprite.y - 1, 40, 34):
                self.start = self.sprite.x
                self.target = 64
                self.progress = 0
                self.duration = 5

                self.parried = True
                return

        if checkCollision(self.sprite.x + 3, self.sprite.y + 5, 6, 9, goose.sprite.x + 5, goose.sprite.y + 5, 22, 22)  and not self.parried: 
            goose.health -= 1
            goose.damaged = True
            self.hit = True
            self.sprite.hidden = True
            return
        
        self.progress += 1


class GreyGooseBossfight:
    def __init__(self):
        self.sheet = displayio.OnDiskBitmap("assets/greygoose_fight.bmp")
        self.sprite = displayio.TileGrid(
            self.sheet,
            pixel_shader=self.sheet.pixel_shader,
            width=1, height=1,
            tile_width=128, tile_height=128,
            default_tile=0,
        )

        self.angerSheet = displayio.OnDiskBitmap("assets/angry.bmp")
        self.angerSprite = displayio.TileGrid(self.angerSheet, pixel_shader=self.angerSheet.pixel_shader)
        self.angerSprite.x = 65
        self.angerSprite.hidden = True

        self.sprite.hidden = True
        
        self.featherSheet = displayio.OnDiskBitmap("assets/feather.bmp")
        self.leftWing = False
        self.rightWing = False
        self.damaged = True
        self.damageTicks = 0

        self.MAX_HEALTH = 10
        self.health = self.MAX_HEALTH
        self.feathers = []
        
        self.healthBar = Rect(0, 0, 128, 8, fill=0x666666)
        self.healthBar.hidden = True
        self.parryFeatherCount = 0
        self.parryFeatherRequiredCount = 6
    
    def update(self, goose):
        if self.health <= int(self.MAX_HEALTH / 2) and self.health > 0 and not self.sprite.hidden:
            self.angerSprite.hidden = False
        else:
            self.angerSprite.hidden = True
        
        if self.damaged:
            self.damageTicks += 1
            
            if self.damageTicks == 4:
                self.damageTicks = 0
                self.damaged = False
            
            self.sprite[0] = 4
        elif self.leftWing and self.rightWing:
            self.sprite[0] = 3
        elif self.rightWing and not self.leftWing:
            self.sprite[0] = 2
        elif self.leftWing and not self.rightWing:
            self.sprite[0] = 1
        else:
            self.sprite[0] = 0

        self.healthBar.x = int(128 * (self.health / self.MAX_HEALTH)) - 128
        
        for feather in self.feathers:
            feather.update(goose)
            
            if feather.hit:
                self.feathers.remove(feather)
            if feather.progress > feather.duration:
                if feather.parried:
                    self.health -= 1
                    self.damaged = True
                    feather.sprite.hidden = True

                self.feathers.remove(feather)
    
    def attackLeft(self, gooseX, splash):
        self.leftWing = True
        self.parryFeatherCount += 1

        def lowerWing():
            self.leftWing = False

        timer.createAndStartTimer(5, lowerWing)
        
        parryable = self.parryFeatherCount == self.parryFeatherRequiredCount
        if parryable:
            self.parryFeatherCount = 0
            self.parryFeatherRequiredCount = random.randint(7,10)

        feather = Feather(x=random.randint(0,40), target=gooseX + random.randint(-4,4), parryable=parryable)
        splash.append(feather.sprite)
        self.feathers.append(feather)
    
    def attackRight(self, gooseX, splash):
        self.rightWing = True
        self.parryFeatherCount += 1
        def lowerWing():
            self.rightWing = False
        
        timer.createAndStartTimer(5, lowerWing)
        parryable = self.parryFeatherCount == self.parryFeatherRequiredCount

        if parryable:
            self.parryFeatherCount = 0
            self.parryFeatherRequiredCount = random.randint(6,10)

        feather = Feather(x=random.randint(80,120), target=gooseX + random.randint(-4,4), parryable=parryable)
        splash.append(feather.sprite)
        self.feathers.append(feather)
