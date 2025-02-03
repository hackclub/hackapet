import displayio
from adafruit_display_shapes.rect import Rect
class Goose:
    def __init__(self):
        self.sheet = displayio.OnDiskBitmap("assets/goose.bmp")

        self.sprite = displayio.TileGrid(
            self.sheet,
            pixel_shader=self.sheet.pixel_shader,
            width=1, height=1,
            tile_width=32, tile_height=32,
            default_tile=0,
            x=int(64 - 16), y=64
        )
        
        self.x = -100
        self.sprite.flip_x = True
        
        self.passingOut = 0
        self.walking = False
        self.walkFrame = 0
        
        self.frozen = False
        self.cameraFollow = True
        
        self.SPEED = 5
        self.MAX_HEALTH = 20
        self.health = self.MAX_HEALTH
        self.damaged = False
        self.hidden = False
        self.showHealth = False
        
        self.healthBar = Rect(0, 128-5, 128, 5, fill=0xFF0000)
        self.parrying = False

        self.afterGatherX = 0
    
    def updateGooseWalk(self):
        self.walkFrame += 1

        if self.walkFrame == 6:
            self.walkFrame = 0

    def frame(self):
        if self.passingOut != 0:
            return 8 + self.passingOut
        elif self.damaged:
            self.damaged = False
            return 7
        elif self.parrying:
            return 8
        if self.walking:   
            return self.walkFrame + 1
    
        
        return 0
    
    def update(self):
        self.sprite.hidden = self.hidden

        if self.cameraFollow:
            self.sprite.x = 48
        else:
            self.sprite.x = self.x
        
        self.healthBar.hidden = not self.showHealth
        self.healthBar.x = int(128 * (self.health / self.MAX_HEALTH)) - 128
    