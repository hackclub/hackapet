import displayio

# this function isn't really useful anymore so I'm putting it in utils
def vibe(clk, sprite, norm_y, length, boost : int, reverse : int = 0, curve : int = 3):
    max_g = length * clk.granularity

    cur_g = ((clk.beat % length) * clk.granularity) + clk.sub_beat

    direction = ((clk.beat // length) + reverse) % 2
    if (direction):
        cur_g = max_g - cur_g
    portion = cur_g / max_g
    scale = pow(portion, curve)

    off = int(boost * scale)
    sprite.y = norm_y - off


POOL_COUNT = 10
class ButtonPool:
    def __init__(self, root_group, red, purple, blue):
        self.root = root_group
        self.red = red
        self.purple = purple
        self.blue = blue
        self.hidden_distance = 300  #this entire code is super hacky and bad
        self.init_pool()

    def init_pool(self):
        bitmaps = (self.red, self.purple, self.blue)
        self.groups = [displayio.Group(y = x * 5) for x in range(3)]
        for i in range(3):
            button = bitmaps[i]
            for j in range(POOL_COUNT):
                sprite = displayio.TileGrid(button, pixel_shader = button.pixel_shader, x = self.hidden_distance)
                self.groups[i].append(sprite)
            self.root.append(self.groups[i])

    def set_lengths(self, lengths : list, track : int):

        target = len(lengths)
        count = 0

        for tile in self.groups[track]:
            if count < target:
                tile.x = lengths[count]
                count += 1
            else:
                tile.x = self.hidden_distance
    def clear(self, track):
        for tile in self.groups[track]:
            tile.x = self.hidden_distance

    def clear_all(self):
        for i in range(3):
            self.clear(i)

