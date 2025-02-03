import displayio
import math
import random
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import label

class Mushroom():
    def __init__(self, x, y, poison):
        self.sheetPoision = displayio.OnDiskBitmap("assets/mushroom_poison.bmp")
        self.sheet = displayio.OnDiskBitmap("assets/mushroom.bmp")
        self.sprite = displayio.TileGrid(
            self.sheet, 
            pixel_shader=self.sheet.pixel_shader, 
            width=1, height=1,
            tile_width=36, tile_height=41,
            default_tile=0)
        
        self.spritePoision = displayio.TileGrid(
            self.sheetPoision, 
            pixel_shader=self.sheet.pixel_shader, 
            width=1, height=1,
            tile_width=36, tile_height=41,
            default_tile=0
        )
        
        self.sprite.hidden = poison
        self.spritePoision.hidden = not poison
        
        self.sprite.x = x
        self.sprite.y = y
        self.spritePoision.x = x
        self.spritePoision.y = y
        self.skipped = False
        self.poison = poison

class MushroomScavenging:
    def __init__(self):
        self.sheet = displayio.OnDiskBitmap("assets/tree_stump.bmp")
        self.sprite = displayio.TileGrid(self.sheet, pixel_shader=self.sheet.pixel_shader)
        
        self.bladeSheet = displayio.OnDiskBitmap("assets/blade_wing.bmp")
        self.bladeSprite = displayio.TileGrid(self.bladeSheet, pixel_shader=self.bladeSheet.pixel_shader, x=60)
        
        self.bladeY = 0
        self.ySin = 0
        self.xSin = 0
        
        self.score = 0
        self.slashing = False
        self.sprite.hidden = True
        self.bladeSprite.hidden = True

        self.mushroom = None

        self.font = bitmap_font.load_font("assets/PressStart2P.bdf")

        self.label = label.Label(self.font, text="", color=0xFFFFFF)
        self.label.line_spacing = 1
        self.label.x = 2
        self.label.y = 10
        self.label.hidden = True
        
        self.timerLabel = label.Label(self.font, text="", color=0xFFFFFF)
        self.timerLabel.line_spacing = 1
        self.timerLabel.x = 2
        self.timerLabel.y = 28
        self.timerLabel.hidden = True

        self.started = False
        self.win = False

        self.timer = 600
    
    def slash(self):
        if self.slashing: return
        self.xSin = 0.0
        self.slashing = True
    
    def resetMushroom(self):
        self.mushroom.sprite.y = random.randint(0,85)
        self.mushroom.spritePoision.y = self.mushroom.sprite.y
        self.mushroom.poison = random.randint(1,3) == 2
        self.mushroom.skipped = False
        self.mushroom.sprite[0] = 0
        self.mushroom.spritePoision[0] = 0
        self.mushroom.sprite.hidden = self.mushroom.poison
        self.mushroom.spritePoision.hidden = not self.mushroom.poison 
        # There is no time for good code folks... sorrgy

    def onGameEnd(self, dialogue):
        def reset():
            self.score = 0
            self.timer = 600
            self.started = True
        
        def win():
            self.win = True
        
        if self.score < 15:
            dialogue.speak(None, [f"You only got \n{self.score} points...\nTry again..."], reset, True)
        else:
            dialogue.speak(None, [f"You got\n{self.score} points!\nNice!"], win, True)
    
    def update(self, dialogue):
        if not self.started: return

        if self.mushroom != None:
            if self.mushroom.skipped:
                self.mushroom.sprite.y += 8
                self.mushroom.spritePoision.y += 8
                
                if self.mushroom.spritePoision.y > 128 or self.mushroom.sprite.y > 128:
                    if self.mushroom.poison: 
                        self.score += 1
                    else:
                        self.score -= 2
                    self.resetMushroom()

        if not self.slashing:
            self.ySin += 0.2
            self.bladeY = int(math.sin(self.ySin) * 50 + 58)
            self.bladeSprite.y = self.bladeY
        else:
            self.xSin += 0.2
            self.bladeSprite.x = int(math.sin(self.xSin) * -40 + 60)
            
            if self.bladeY >= self.mushroom.sprite.y - 4 and self.bladeY <= self.mushroom.sprite.y + 16 and self.mushroom.sprite[0] == 0 and self.mushroom.spritePoision[0] == 0:
                if self.mushroom.poison:
                    self.mushroom.spritePoision[0] = 1
                    self.score -= 2
                else:
                    self.mushroom.sprite[0] = 1
                    self.score += 1
            
            if self.xSin > 3.0:
                self.bladeSprite.x = 60
                self.slashing = False
                
                if self.mushroom.sprite[0] == 1 or self.mushroom.spritePoision[0] == 1: self.resetMushroom()

        self.label.text = str(self.score)
        self.timer -= 1
        
        if self.timer >= 590:
            self.timerLabel.text = "1:00"
        elif self.timer <= 90:
            self.timerLabel.text = "0:0" + str(math.ceil(self.timer/10))
        else:
            self.timerLabel.text = "0:" + str(math.ceil(self.timer/10))
        
        if self.timer == 0:
            self.onGameEnd(dialogue)
            self.started = False
        
    
    def spawnMushroom(self, splash):
        self.mushroom = Mushroom(25, random.randint(0,85), random.randint(1,3) == 2)
        splash.insert(splash.index(self.bladeSprite) + 1, self.mushroom.sprite)
        splash.insert(splash.index(self.bladeSprite) + 1, self.mushroom.spritePoision)