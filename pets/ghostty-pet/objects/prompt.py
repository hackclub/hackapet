import math
import displayio
from objects.terminal import Terminal

good_prompt = displayio.OnDiskBitmap("art/good_prompt.bmp")
bad_prompt = displayio.OnDiskBitmap("art/bad_prompt.bmp")

class Good_Prompt:
    def __init__(self, splash, height):
        self.sprite = displayio.TileGrid(
            good_prompt,
            pixel_shader=good_prompt.pixel_shader,
            width=1,
            height=1,
            tile_width=32,
            tile_height=good_prompt.height,
            default_tile=0,
            x=128,
            y=128-(32*height)
        )
        splash.append(self.sprite)
        self.splash = splash
        self.height = height
        self.x = 128
        self.is_removed = False
        self.speed = 0.8
        self.frame = 0

    def update(self):
        self.sprite[0] = math.floor(self.frame)
        self.x -= self.speed
        if self.x < -32 and not self.is_removed:
            self.splash.remove(self.sprite)
            self.is_removed = True
        self.sprite.x = math.floor(self.x)

    def remove(self):
        self.splash.remove(self.sprite)
        self.is_removed = True

class Bad_Prompt:
    def __init__(self, splash, height):
        self.sprite = displayio.TileGrid(
            bad_prompt,
            pixel_shader=bad_prompt.pixel_shader,
            width=1,
            height=1,
            tile_width=32,
            tile_height=bad_prompt.height,
            default_tile=0,
            x=128,
            y=128-(32*height)
        )
        splash.append(self.sprite)
        self.splash = splash
        self.height = height
        self.x = 128
        self.is_removed = False
        self.speed = 0.8
        self.frame = 0

    def update(self):
        self.sprite[0] = math.floor(self.frame)
        self.x -= self.speed
        if self.x < -32 and not self.is_removed:
            self.splash.remove(self.sprite)
            self.is_removed = True
        self.sprite.x = math.floor(self.x)

    def remove(self):
        self.splash.remove(self.sprite)
        self.is_removed = True