import displayio
from sprites.base import HitboxOffsetSprite

BRACKET_BITMAP = displayio.OnDiskBitmap("./textures/squid_parts/bracket.bmp")
EYE_BITMAP = displayio.OnDiskBitmap("./textures/squid_parts/eye.bmp")

class Eye(HitboxOffsetSprite):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    self._top_bracket = displayio.TileGrid(
      BRACKET_BITMAP,
      pixel_shader=BRACKET_BITMAP.pixel_shader,
    )

    self._eye = displayio.TileGrid(
      EYE_BITMAP,
      pixel_shader=EYE_BITMAP.pixel_shader,
    )

    self._bottom_bracket = displayio.TileGrid(
      BRACKET_BITMAP,
      pixel_shader=BRACKET_BITMAP.pixel_shader,
    )
    
    self._bottom_bracket.flip_y = True

    self.height = 30
    self.eye_x = 0
    self.eye_y = 0
    
    self.append(self._top_bracket)
    self.append(self._eye)
    self.append(self._bottom_bracket)
  
  @property
  def width(self):
    return self._top_bracket.tile_width

  @property
  def height(self):
    return self._bottom_bracket.y + self._bottom_bracket.tile_height

  @height.setter
  def height(self, value):
    self._bottom_bracket.y = value - self._bottom_bracket.tile_height
  
  @property
  def eye_x(self):
    return self._eye.x - self.width // 2 + self._eye.tile_width // 2
  
  @eye_x.setter
  def eye_x(self, value):
    self._eye.x = value + self.width // 2 - self._eye.tile_width // 2
  
  @property
  def eye_y(self):
    return self._eye.y - self.height // 2 + self._eye.tile_height // 2
  
  @eye_y.setter
  def eye_y(self, value):
    self._eye.y = value + self.width // 2 - self._eye.tile_height // 2
