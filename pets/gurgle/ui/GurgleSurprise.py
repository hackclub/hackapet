import displayio
import random

from . import spriteHandler

class SpriteScroller:
    def __init__(self):
        self.display_width = 128
        self.display_height = 128
        self.group = displayio.Group()
        
        self.sprites = []
        
    def spawn_single_sprite(self):
        edge = random.randint(0, 3)
        
        if edge == 0:  # top
            x = random.randint(0, self.display_width)
            y = -64
            velocity_y = random.uniform(1, 3)
            velocity_x = random.uniform(-2, 2)
        elif edge == 1:  # r
            x = self.display_width + 64
            y = random.randint(0, self.display_height)
            velocity_x = random.uniform(-3, -1)
            velocity_y = random.uniform(-2, 2)
        elif edge == 2:  # b
            x = random.randint(0, self.display_width)
            y = self.display_height + 64
            velocity_y = random.uniform(-3, -1)
            velocity_x = random.uniform(-2, 2)
        else:  # l
            x = -64
            y = random.randint(0, self.display_height)
            velocity_x = random.uniform(1, 3)
            velocity_y = random.uniform(-2, 2)
            
        sprite_grid, _ = spriteHandler.load_sprite_sheet("./assets/glorb.bmp", 64, 64)
        
        self.sprites.append({
            'x': x,
            'y': y,
            'velocity_x': velocity_x,
            'velocity_y': velocity_y,
            'scale': 1.0,
            'scale_speed': random.uniform(0.005, 0.015),
            'sprite': sprite_grid
        })
        
        self.group.append(sprite_grid)

    def spawn(self, min_count=1, max_count=5):
        count = random.randint(min_count, max_count)
        for _ in range(count):
            self.spawn_single_sprite()
        return count
        
    def update(self):
        for sprite in self.sprites[:]:
            sprite['x'] += sprite['velocity_x']
            sprite['y'] += sprite['velocity_y']
            
            sprite['scale'] *= (1 - sprite['scale_speed'])
            
            sprite['sprite'].x = int(sprite['x'])
            sprite['sprite'].y = int(sprite['y'])
            
            if (sprite['scale'] < 0.1 or 
                sprite['x'] < -100 or sprite['x'] > self.display_width + 100 or 
                sprite['y'] < -100 or sprite['y'] > self.display_height + 100):
                
                if sprite['sprite'] in self.group:
                    self.group.remove(sprite['sprite'])
                self.sprites.remove(sprite)

    def get_sprite_count(self):
        return len(self.sprites)