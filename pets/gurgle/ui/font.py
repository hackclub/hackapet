import displayio

# website used to convert ttf -> bitmap images = https://stmn.itch.io/font2bitmap
class Font:
    def __init__(self, filename, char_width=10, char_height=10, chars=" abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMOPQRSTUVWXYZ1234567890!.,?^_:;<>/"):
        self.sheet = displayio.OnDiskBitmap(filename)
        self.chars = chars
        self.char_width = char_width
        self.char_height = char_height
        
    def get_char_sprite(self, char):
        if char not in self.chars:
            return None
            
        index = self.chars.index(char)
        sprite = displayio.TileGrid(
            self.sheet,
            pixel_shader=self.sheet.pixel_shader,
            tile_width=self.char_width,
            tile_height=self.char_height,
            default_tile=index,
            width=1,
            height=1
        )
        return sprite
        
    def write_text(self, text, x, y):
        group = displayio.Group()
        offset = 0
        
        for char in text:
            if char == ' ':
                offset += self.char_width
                continue
                
            sprite = self.get_char_sprite(char)
            if sprite:
                sprite.x = x + offset
                sprite.y = y
                group.append(sprite)
                offset += self.char_width
                
        return group
