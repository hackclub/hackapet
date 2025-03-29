import displayio

golden_number = displayio.OnDiskBitmap("art/golden_number.bmp")

class Golden_Numbers:
    def __init__(self, splash):
        self.list = []
        for i in range(1, 5):
            self.list.append(Golden_Number(splash, i))
            splash.append(self.list[-1].sprite)
    def update(self, score):
        for i in self.list:
            i.update(score)

class Golden_Number:
    def __init__(self, splash, position):
        self.value = 10
        self.sprite = displayio.TileGrid(
            golden_number,
            pixel_shader=golden_number.pixel_shader,
            width=1,
            height=1,
            tile_width=golden_number.width // 10,
            tile_height=golden_number.height,
            default_tile=10,
            x=(128 - position * 6) - 8,
            y=20
        )
        self.position = position

        splash.append(self.sprite)
    
    def update(self, score):
        self.value = self.right(score, self.position)
        self.sprite[0] = self.value
    
    def right(self, number, x):
        num_str = str(number)
        if x > len(num_str):
            return 0
        return int(num_str[-x])
