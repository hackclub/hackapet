from typing import Self
from sprites.base import FloatVelocitySprite

class PredictedPlayer():
  def __init__(self, player: FloatVelocitySprite, *args, **kwargs):
    super().__init__(*args, **kwargs)

    self._player = player
    self._offset_x = 0
    self._offset_y = 0
    self._offset_timesteps = 0

  @property
  def width(self):
    return self._player.width

  @property
  def height(self):
    return self._player.height

  @property
  def left_extent(self):
    return self._player.left_extent + self._offset_x
  
  @property
  def right_extent(self):
    return self._player.right_extent + self._offset_x

  @property
  def top_extent(self):
    return self._player.top_extent + self._offset_y
  
  @property
  def bottom_extent(self):
    return self._player.bottom_extent + self._offset_y
  
  @property
  def x(self):
    return self._player.x + self._offset_x
  
  @property
  def y(self):
    return self._player.y + self._offset_y
  
  @property
  def center_x(self):
    return self._player.center_x + self._offset_x
  
  @property
  def center_y(self):
    return self._player.center_y + self._offset_y
  
  @property
  def float_x(self):
    return self._player.float_x + self._offset_x
  
  @property
  def float_y(self):
    return self._player.float_y + self._offset_y
  
  @property
  def x_velocity(self):
    return self._player.x_velocity
  
  @property
  def y_velocity(self):
    return self._player.y_velocity

  @property
  def min_x(self):
    return self._player.min_x
  
  @property
  def max_x(self):
    return self._player.max_x
  
  @property
  def min_y(self):
    return self._player.min_y
  
  @property
  def max_y(self):
    return self._player.max_y
  
  @property
  def offset_x(self):
    return self._offset_x
  
  @property
  def offset_y(self):
    return self._offset_y

  @property
  def timesteps(self):
    return self._offset_timesteps

  @timesteps.setter
  def timesteps(self, value):
    self._offset_timesteps = value
    self._offset_x = self._player.x_velocity * self._offset_timesteps
    self._offset_y = self._player.y_velocity * self._offset_timesteps

    self._offset_x = max(self.min_x, min(self.x, self.max_x - self.width)) - self._player.x
    self._offset_y = max(self.min_y, min(self.y, self.max_y - self.height)) - self._player.y

  def step(self, timesteps=1):
    self.timesteps += timesteps
  
  def at(self, timesteps):
    copy = PredictedPlayer(self._player)
    copy.timesteps = timesteps
    return copy

  def copy(self) -> Self:
    return self.at(self.timesteps)
