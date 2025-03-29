import displayio


number = displayio.OnDiskBitmap("art/number.bmp")

class Number:
    def __init__(self, splash, position):
        self.value = 10
        self.sprite = displayio.TileGrid(
            number,
            pixel_shader=number.pixel_shader,
            width=1,
            height=1,
            tile_width=number.width // 10,
            tile_height=number.height,
            default_tile=10,
            x=(128 - position * 6) - 8,
            y=10
        )
        self.position = position

        splash.append(self.sprite)
    
    def update(self, score):
        num_str = str(score)
        self.value = self.right(score, self.position)
        self.sprite[0] = self.value
    
    def right(self, number, x):
        num_str = str(number)
        if x > len(num_str):
            return 0
        return int(num_str[-x])
