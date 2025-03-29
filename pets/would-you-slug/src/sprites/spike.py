import displayio

from sprites.base import HitboxOffsetSprite, DangerousSprite, AnimatableSprite

SPIKE_BITMAP = displayio.OnDiskBitmap("./textures/spike.bmp")
SPIKE_FRAMEDATA = [1, 4, 2, 2, 4, 2, 4, 1, 1, 1, 20]

class Spike(HitboxOffsetSprite, DangerousSprite, AnimatableSprite):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    self._sprite = displayio.TileGrid(
      SPIKE_BITMAP,
      pixel_shader=SPIKE_BITMAP.pixel_shader,
      tile_width=16,
      tile_height=16,
      default_tile=0,
    )
    
    self.append(self._sprite)

    self._current_frame = 0
    self._update_sprite()
  
  @property
  def _left_hitbox_offset(self):
    return -2

  @property
  def _right_hitbox_offset(self):
    return -2
  
  @property
  def _top_hitbox_offset(self):
    if self._current_frame >= 7:
      return -5
    else:
      return -6
  
  @property
  def width(self):
    return self._sprite.tile_width

  @property
  def height(self):
    return self._sprite.tile_height
  
  def _update_sprite(self):
    self._sprite[0] = self._current_frame
    self._frame_counter = 0
  
  def is_animation_finished(self):
    return self._current_frame == 10

  def animate(self):
    if self._frame_counter >= SPIKE_FRAMEDATA[self._current_frame]:
      self._current_frame = (self._current_frame + 1) % 11
      self._update_sprite()

    if not self.is_animation_finished():
      self._frame_counter += 1

  def is_dangerous(self):
    return self._current_frame >= 5
  
  def get_score(self, player):
    return 1
  
  def can_remove(self):
    return self._current_frame >= 8
