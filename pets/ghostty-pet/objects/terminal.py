import displayio
import math

terminal_bitmap = displayio.OnDiskBitmap("art/terminal.bmp")

class Terminal:
    def __init__(self, splash, height):
        self.sprite = displayio.TileGrid(
            terminal_bitmap,
            pixel_shader=terminal_bitmap.pixel_shader,
            width=1,
            height=1,
            tile_width=terminal_bitmap.width,
            tile_height=terminal_bitmap.height,
            x=128,
            y=128-(32*height)
        )
        splash.append(self.sprite)
        self.splash = splash
        self.height = height
        self.x = 128
        self.is_removed = False
        self.speed = 0.8
    def update(self):
        self.x -= self.speed
        if self.x < -32 and not self.is_removed:
            self.splash.remove(self.sprite)
            self.is_removed = True
        self.sprite.x = math.floor(self.x)
    def remove(self):
        self.splash.remove(self.sprite)
        self.is_removed = True
            
