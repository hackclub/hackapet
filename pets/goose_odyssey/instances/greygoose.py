import displayio

class GreyGoose:
    def __init__(self):
        self.sheet = displayio.OnDiskBitmap("assets/greygoose.bmp")
        self.sprite = displayio.TileGrid(
            self.sheet,
            pixel_shader=self.sheet.pixel_shader,
            width=1, height=1,
            tile_width=32, tile_height=32,
            default_tile=0,
            x=int(64 - 16), y=64
        )
        
        self.x = -10000
        
        self.passingOut = 0
        self.walking = False
        self.walkFrame = 0
        self.map = "inside_hotel"
        self.direction = 0
    
    def update(self, gooseX, currentMap):
        if self.walking:
            self.walkFrame += 1
            
            if self.walkFrame == 6:
                self.walkFrame = 0

        self.sprite[0] = self.frame()

        self.sprite.hidden = self.map != currentMap
        self.x += self.direction
        self.sprite.x = self.x - gooseX

    def frame(self):
        if self.passingOut != 0:
            return 6 + self.passingOut
        elif self.walking:
            return self.walkFrame + 1
        
        return 0