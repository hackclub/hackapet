import displayio

from sprites.base import HitboxOffsetSprite, FloatVelocitySprite

SHELLY_BITMAP = displayio.OnDiskBitmap("./textures/shelly.bmp")

class Shelly(HitboxOffsetSprite, FloatVelocitySprite):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    self._sprite = displayio.TileGrid(
      SHELLY_BITMAP,
      pixel_shader=SHELLY_BITMAP.pixel_shader
    )

    self.min_y = -32

    self._sprite.flip_x = True
    self.append(self._sprite)

    self.grounded = False

    self.max_air_jumps = 1
    self.remaining_air_jumps = self.max_air_jumps
    self.jump_held = False
  
  @property
  def _left_hitbox_offset(self):
    return -1

  @property
  def _right_hitbox_offset(self):
    return -1
  
  @property
  def _top_hitbox_offset(self):
    return -6
  
  @property
  def width(self):
    return self._sprite.tile_width

  @property
  def height(self):
    return self._sprite.tile_height

  def check_grounded(self):
    self.grounded = self.float_y >= self.max_y - self._sprite._pixel_height
    
    if self.grounded:
      self.remaining_air_jumps = self.max_air_jumps

  def jump(self):
    if self.jump_held:
      return

    if self.grounded:
      self.y_velocity = min(-8.1, self.y_velocity)
    elif self.remaining_air_jumps > 0:
      self.remaining_air_jumps -= 1
      self.y_velocity = min(-6.9, self.y_velocity)
    else:
      return
    
    self.jump_held = True
    
  def update(self, movement_direction, jump):
    if (not (jump and self.jump_held)) and self.y_velocity < 0:
      self.y_velocity += 1.4
    else:
      self.y_velocity += 1
    
    self.check_grounded()
    if jump:
      self.jump()
    else:
      self.jump_held = False

    self.clamp_y_velocity(10)
    self.float_y += self.y_velocity

    self.x_velocity = self.x_velocity + movement_direction * 1.5
    if movement_direction > 0:
      self._sprite.flip_x = True
    elif movement_direction < 0:
      self._sprite.flip_x = False
    else:
      self.x_velocity *= 0.80
    
    self.clamp_x_velocity(3)
    self.float_x += self.x_velocity

    self.keep_in_bounds()