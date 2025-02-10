class Updateable:
    """ Responsible for bounce effects mostly"""
    def __init__(self, tile):
        self.tile = tile
        self.tx = tile.x
        self.ty = tile.y

        self.accum = 0
        self.bounce_time = 0
        self.bounce_dist = 3
        self.curve = 3
        self.bouncing = False
        self.vibing = False

    def bounce(self, time = 0.3, off = 5, curve = 1):
        if self.bouncing:
            pass
        self.bounce_time = time
        self.bounce_dist = off
        self.curve = curve
        self.accum = 0
        self.bouncing = True

    def update(self, dt):
        if self.bouncing:

            self.accum += dt
            if (self.accum >= self.bounce_time):
                self.bouncing = False
                self.accum = 0
                self.tile.y = self.ty
            else:
                midpoint = self.bounce_time / 2
                if self.accum <= midpoint:
                    p = self.accum
                else:
                    p = self.bounce_time - self.accum
                progress = p / midpoint
                scale = pow(progress, self.curve)
                off = int(scale * self.bounce_dist)
                self.tile.y = self.ty - off


class Animateable(Updateable):
    # Default 
    def __init__(self, group, tiles: list, timings : list):
        self.group = group
        self.tiles = tiles # each tile represents a different spritesheet containing a full animation
        self.timings = timings # milliseconds to play each frame
        self.playing = False
        self.tile_index = 0
        self.animation_index = 0
        self.accum_time = 0
        super().__init__(tiles[0])

    def reset_animation(self):
        self.accum_time = 0
        self.animation_index = 0
        self.playing = False
    
    def set_animation(self, index, playing = False):
        if self.tile is self.tiles[index]:
            pass
        # remove current TileGrid from group
        if self.tile in self.group:
            self.group.remove(self.tile)

        # add new TileGrid
        self.tile = self.tiles[index]
        self.group.append(self.tile)
        self.tile_index = index

        self.reset_animation()
        if playing:
            self.play_animation()

    def play_animation(self, reset = True):
        if reset:
            self.reset_animation()
        self.playing = True

    def update(self, dt):
        super().update(dt)
        if self.playing:
            self.accum_time += dt
            timing = self.timings[self.tile_index]
            if (self.accum_time >= timing[self.animation_index]):
                self.accum_time = 0
                self.animation_index += 1
                # reset to frame zero if we reached the end
                if self.animation_index >= len(timing):
                    self.reset_animation()

        self.tile[0] = self.animation_index

class Professor(Animateable):
    def bounce(self, *args, **kwargs):
        super().bounce(*args, **kwargs)
        self.play_animation()
