from . import spriteHandler
import config
import math

class Gurgle:
    def __init__(self, group, x, y):
        self.state = None
        self.x = x
        self.y = y
        self.time = 0
        self.float_speed = 2
        self.float_radius = 35
        self.float_x_radius = 40
        self.base_y = y
        self.base_x = x  
        self.animations = {
            "happy": self.load_animation("./assets/goob.bmp"),
            "drool": self.load_animation("./assets/goob_drool.bmp"),
            "sad": self.load_animation("./assets/goob_sad.bmp"),
            "dead": self.load_animation("./assets/goob_dead.bmp"),
            "floating": self.load_animation("./assets/goob_small.bmp")
        }
        self.current_sprite = None
        self.frames = None
        self.group = group
        self.change_state("happy")
        self.isDead = False
        self.is_floating = False
        self.original_x = x
        self.original_y = y
        self.float_center_y = 64

    def toggle_float(self):
        self.is_floating = not self.is_floating
        if self.is_floating:
            self.base_y = self.float_center_y
            self.base_x = self.original_x
            self.change_state("floating")
        else:
            self.base_y = self.original_y
            self.base_x = self.original_x
            self.y = self.original_y
            self.x = self.original_x
            if self.current_sprite:
                self.current_sprite.y = int(self.original_y)
                self.current_sprite.x = int(self.original_x)
            self.state = None 

    def change_state(self, new_state):
        if new_state != self.state:
            print("Changing state to", new_state)
            if self.current_sprite and self.current_sprite in self.group:
                print("Removing sprite", self.current_sprite)
                self.group.remove(self.current_sprite)
            
            self.state = new_state
            self.current_sprite = self.animations[new_state][0]
            self.frames = self.animations[new_state][1]
            self.current_sprite.x = int(self.x)
            self.current_sprite.y = int(self.base_y)
            self.group.append(self.current_sprite)

    def load_animation(self, filename):
        sprite, frames = spriteHandler.load_sprite_sheet(filename, 64, 64)
        return (sprite, frames)

    def update(self, happiness):
        if self.isDead:
            if self.state != "dead":
                self.change_state("dead")
                return True
            else:
                return False
                        
        if self.is_floating:
            self.time += 1 / config.LOCK_FPS
            float_y = self.base_y + math.sin(self.time) * self.float_radius
            float_x = self.base_x + math.cos(self.time * 0.7) * self.float_x_radius 
            
            if self.current_sprite:
                self.current_sprite.x = int(float_x)
                self.current_sprite.y = int(float_y)
            return False
        
        changed = False
        new_state = None
        
        if happiness >= config.STATES["happy"]:
            new_state = "happy"
        elif happiness >= config.STATES["drool"]:
            new_state = "drool"
        else:
            new_state = "sad"
            
        if new_state != self.state:
            print(f"Changing state to {new_state}")
            self.change_state(new_state)
            changed = True
            
        return changed