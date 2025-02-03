import displayio

class Fade:
    def __init__(self):
        self.sheet = displayio.OnDiskBitmap("assets/fade.bmp")
        self.sprite = displayio.TileGrid(
            self.sheet,
            pixel_shader=self.sheet.pixel_shader,
            width=1, height=1,
            tile_width=128, tile_height=128,
            default_tile=0,
            x=0, y=0,
        )
        
        self.direction = 0

    def fade(self):
        if self.direction == 1 and self.sprite[0] < 5:
            self.sprite[0] += 1
        elif self.direction == -1 and self.sprite[0] > 0:
            self.sprite[0] -= 1
        
        self.sprite.hidden = self.sprite[0] == 0

    
    

        