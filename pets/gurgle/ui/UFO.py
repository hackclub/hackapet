import random
from . import spriteHandler 
import config
import math
from . import animationHandler


class UFO:
   def __init__(self, group, anim: animationHandler.AnimationHandler):
      self.sprite, self.frames = spriteHandler.load_sprite_sheet("./assets/ufo.bmp", 16, 16)
      self.anim = anim

      self.name = f"{random.randint(0, 1000000)}-ufo"
      self.anim.add_animation(self.name, self.sprite, self.frames, 0.1)

      self.sprite.x = -32
      self.sprite.y = 30
      self.speed = random.uniform(3, 7)
      self.wave_amplitude = random.randint(10, 30) 
      self.wave_freq = random.uniform(1.0, 2.0)     
      self.time = 0
      self.group = group
      self.group.append(self.sprite)
      self.isReset = False

   def update(self):
       self.time += 1 / config.LOCK_FPS
       self.sprite.x = int(self.sprite.x + self.speed)
       self.sprite.y = int(30 + math.sin(self.time * self.wave_freq) * self.wave_amplitude) 
       if self.sprite.x > 160:
           self.reset()
           
   def reset(self):
       self.anim.remove_animation(self.name)
       self.group.remove(self.sprite)
       self.isReset = True

