import time

class AnimationHandler:
    def __init__(self):
        self.animations = {}
        self.last_update = time.monotonic()
    
    def add_animation(self, name, sprite, frame_count, frame_delay=0.1):
        self.animations[name] = {
            'sprite': sprite,
            'frame_count': frame_count,
            'current_frame': 0,
            'frame_delay': frame_delay,
            'last_update': self.last_update
        }

    def remove_animation(self, name):
        del self.animations[name]
    
    def update(self):
        current_time = time.monotonic()
        
        for anim in self.animations.values():
            if current_time - anim['last_update'] >= anim['frame_delay']:
                anim['current_frame'] = (anim['current_frame'] + 1) % anim['frame_count']
                anim['sprite'][0] = anim['current_frame']
                anim['last_update'] = current_time