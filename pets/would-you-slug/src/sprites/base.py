from abc import ABCMeta, abstractmethod
from typing import Self, Protocol, runtime_checkable

import displayio

class Sprite(displayio.Group, metaclass=ABCMeta):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

  @property
  @abstractmethod
  def width(self) -> int:
    pass

  @property
  @abstractmethod
  def height(self) -> int:
    pass
  
  @property
  def center_x(self) -> int:
    return self.x + self.width // 2

  @center_x.setter
  def center_x(self, value):
    self.x = value - self.width // 2

  @property
  def center_y(self) -> int:
    return self.y + self.height // 2

  @center_y.setter
  def center_y(self, value):
    self.y = value - self.height // 2

  @property
  @abstractmethod
  def left_extent(self) -> int:
    pass

  @property
  @abstractmethod
  def right_extent(self) -> int:
    pass
  
  @property
  @abstractmethod
  def top_extent(self) -> int:
    pass

  @property
  @abstractmethod
  def bottom_extent(self) -> int:
    pass

  @property
  def hitbox_width(self):
    return self.right_extent - self.left_extent
  
  @property
  def hitbox_height(self):
    return self.bottom_extent - self.top_extent

  def collides_with(self, other: Self) -> bool:
    return \
    self.left_extent < other.right_extent and \
    self.right_extent > other.left_extent and \
    self.top_extent < other.bottom_extent and \
    self.bottom_extent > other.top_extent

class HitboxOffsetSprite(Sprite, metaclass=ABCMeta):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

  @property
  def _left_hitbox_offset(self) -> int:
    return 0

  @property
  def _right_hitbox_offset(self) -> int:
    return 0

  @property
  def _top_hitbox_offset(self) -> int:
    return 0

  @property
  def _bottom_hitbox_offset(self) -> int:
    return 0

  @property
  def left_extent(self) -> int:
    return self.x - self._left_hitbox_offset

  @property
  def right_extent(self) -> int:
    return self.x + self.width + self._right_hitbox_offset
  
  @property
  def top_extent(self) -> int:
    return self.y - self._top_hitbox_offset

  @property
  def bottom_extent(self) -> int:
    return self.y + self.height + self._bottom_hitbox_offset

class FloatVelocitySprite(Sprite):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    self.min_x = 0
    self.max_x = 128
    self.min_y = -5
    self.max_y = 112

    self._float_x = 0
    self._float_y = 0
    self.x_velocity = 0
    self.y_velocity = 0
  
  @property
  def float_x(self) -> float:
    return self._float_x
  
  @float_x.setter
  def float_x(self, value):
    super(FloatVelocitySprite, type(self)).x.__set__(self, int(value))
    self._float_x = value

  @property
  def x(self) -> int:
    return int(self.float_x)
  
  @x.setter
  def x(self, value):
    self.float_x = value  

  @property
  def float_y(self) -> float:
    return self._float_y
  
  @float_y.setter
  def float_y(self, value):
    super(FloatVelocitySprite, type(self)).y.__set__(self, int(value))
    self._float_y = value
  
  @property
  def y(self) -> int:
    return int(self.float_y)
  
  @y.setter
  def y(self, value: float):
    self.float_y = value

  def clamp_x_velocity(self, limit):
    self.x_velocity = max(-limit, min(self.x_velocity, limit))

  def clamp_y_velocity(self, limit):
    self.y_velocity = max(-limit, min(self.y_velocity, limit))

  def keep_in_bounds(self):
    if self.float_x < self.min_x:
      self.x = self.min_x
      self.x_velocity = 0

    max_x = self.max_x - self.width
    if self.float_x > max_x:
      self.x = max_x
      self.x_velocity = 0

    if self.float_y < self.min_y:
      self.y = self.min_y
      self.y_velocity = 0

    max_y = self.max_y - self.height
    if self.float_y > max_y:
      self.y = max_y
      self.y_velocity = 0

@runtime_checkable
class DangerousSprite(Protocol):
  @abstractmethod
  def is_dangerous(self) -> bool:
    return False

  @abstractmethod
  def get_score(self, player) -> int:
    return 0

@runtime_checkable
class AnimatableSprite(Protocol):
  @abstractmethod
  def animate(self):
    pass

  @abstractmethod
  def is_animation_finished() -> bool:
    return False
