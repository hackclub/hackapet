import time
from . import animationHandler, spriteHandler
import config
import random

class Pizza:
    def __init__(self, group, anim: animationHandler.AnimationHandler, x, y):
        self.sprite, self.frames = spriteHandler.load_sprite_sheet("./assets/pizza.bmp", 64, 64)
        self.group = group
        self.anim = anim
        self.sprite.x = x
        self.sprite.y = y
        self.group.append(self.sprite)
        self.name = random.randint(0, 1000000)
        self.anim.add_animation(self.name, self.sprite, self.frames, 0.1)
        self.start_time = time.monotonic()
        self.duration = self.frames * (1 / config.LOCK_FPS)

    def update(self):
        current_time = time.monotonic()
        if current_time - self.start_time >= self.duration:
            self.anim.remove_animation(self.name)
            self.group.remove(self.sprite)
            return True 
        return False