import displayio
import random
import config
import math

class Star:
   def __init__(self, group):
    bitmap = displayio.OnDiskBitmap("./assets/star.bmp")
    self.sprite = displayio.TileGrid(
        bitmap,
        pixel_shader=bitmap.pixel_shader,
        width=1,
        height=1
    )
    self.sprite.x = random.randint(0, 128)
    self.sprite.y = random.randint(0, 128)
    self.blink_timer = random.uniform(0, 4)
    self.blink_rate = random.uniform(0.5, 1)
    self.group = group
    self.group.append(self.sprite)
       
   def update(self):
       self.blink_timer += 1/config.LOCK_FPS
       self.sprite.hidden = math.sin(self.blink_timer * self.blink_rate) < 0