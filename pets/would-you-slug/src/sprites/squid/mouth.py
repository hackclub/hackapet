import displayio
from sprites.base import HitboxOffsetSprite


MOUTH_BITMAP = displayio.OnDiskBitmap("./textures/squid_parts/mouth.bmp")

class Mouth(HitboxOffsetSprite):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    self._sprite = displayio.TileGrid(
      MOUTH_BITMAP,
      pixel_shader=MOUTH_BITMAP.pixel_shader
    )

    self.append(self._sprite)

  @property
  def width(self):
    return self._sprite.tile_width

  @property
  def height(self):
    return self._sprite.tile_height