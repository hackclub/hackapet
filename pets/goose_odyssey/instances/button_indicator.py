import displayio

class ButtonIndicator:
    def __init__(self):
        self.sheet = displayio.OnDiskBitmap("assets/button_arrow.bmp")
        self.sprite = displayio.TileGrid(
            self.sheet,
            pixel_shader=self.sheet.pixel_shader,
            width=1, height=1,
            tile_width=32, tile_height=32,
            default_tile=0,
            x=int(64 - 16), y=95
        )

        self.sprite.hidden = True

    def update(self):
        self.sprite[0] += 1
        
        if self.sprite[0] == 4:
            self.sprite[0] = 0