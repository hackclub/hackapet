import math
import random
import displayio

from sprites.base import FloatVelocitySprite, Sprite

from sprites.spike import Spike
from sprites.squid.dialogue import Dialouge, choose_dialogue
from sprites.squid.eye import Eye
from sprites.squid.mouth import Mouth
from sprites.squid.predicted_player import PredictedPlayer

# 30 fps
HANDICAP_LOWER_FRAMES = [(5 * 30) + (i * 5 * 30) for i in range(10)]


class Squid(Sprite):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    self._left_eye = Eye()
    self._left_eye.center_x = 39
    self._left_eye.center_y = 25

    self._right_eye = Eye()
    self._right_eye.center_x = 128 - 39
    self._right_eye.center_y = 25

    self._mouth = Mouth()
    self._mouth.center_x = 64
    self._mouth.center_y = 57

    self._dialouge = Dialouge()
    self._dialouge.set_text("Hello human. Welcome to my simulation! Press Left+Right to start the \"fun\"")
    self._dialouge.position = (64, 72)
    self._dialouge.anchor = (0.5, 0.5)

    self.append(self._left_eye)
    self.append(self._right_eye)
    self.append(self._mouth)
    self.append(self._dialouge)

    self.reset()

  @property
  def width(self):
    return self.hitbox_width

  @property
  def height(self):
    return self.hitbox_height
  
  @property
  def left_extent(self):
    return min(self._left_eye.left_extent, self._right_eye.left_extent, self._mouth.left_extent)

  @property
  def right_extent(self):
    return max(self._left_eye.right_extent, self._right_eye.right_extent, self._mouth.right_extent)
  
  @property
  def top_extent(self):
    return min(self._left_eye.top_extent, self._right_eye.top_extent, self._mouth.top_extent)

  @property
  def bottom_extent(self):
    return max(self._left_eye.bottom_extent, self._right_eye.bottom_extent, self._mouth.bottom_extent)

  def reset(self, score_achieved: int = -1):
    if score_achieved > -1:
      self._dialouge.set_text(choose_dialogue(score_achieved))

    self._time_since_last_danger = -5
    self._danger_spawn_handicap = 10
    self._current_game_frames = 0
    self._handicap_lower_thresholds = HANDICAP_LOWER_FRAMES.copy()

  def reset_danger_time(self, additional_handicap=0):
    # negative numbers means it has to go back t 0 first, increasing the delay
    self._time_since_last_danger = 0 - additional_handicap - self._danger_spawn_handicap

  def track_player(self, player: Sprite):
    x_dist = (player.center_x - (self._left_eye.center_x +  self._right_eye.center_x) // 2)
    y_dist = (player.center_y - (self._left_eye.center_y +  self._right_eye.center_y) // 2)

    eye_x = x_dist // 10
    eye_y = y_dist // 15

    self._left_eye.eye_x = eye_x
    self._left_eye.eye_y = eye_y

    self._right_eye.eye_x = eye_x
    self._right_eye.eye_y = eye_y

  def spawn_spike(self, prediction: PredictedPlayer, dangers) -> bool:
    if self._time_since_last_danger < 10:
      return False
    
    spike_lookahead_frames = random.randint(6, 7)
    in_air = False

    # find the first moment before the player lands
    while prediction.bottom_extent == prediction.max_y:
      prediction.step(-1)

      if prediction.timesteps == 0:
        # We started on the ground, use the correct number for spikes
        prediction.timesteps = spike_lookahead_frames
        break
    else:
      # in air, step to landing
      in_air = True
      prediction.step()

    if prediction.timesteps > spike_lookahead_frames:
        return False

    offset_x = prediction.offset_x
    if in_air:
      current_height = prediction.max_y - prediction.at(0).bottom_extent
      scale_factor = current_height * prediction.x_velocity * 100

      if scale_factor > 1:
        pass#offset_x /= scale_factor

    spike_x = int(prediction.center_x + offset_x)
    spike_x = max(8, min(spike_x, 120))

    spike = Spike()
    spike.center_x = spike_x
    spike.y = 96

    dangers.append(spike)
    return True

  def spawn_danger(self, player: FloatVelocitySprite, dangers: displayio.Group):
    lookahead_time = random.randint(5, 10)

    prediction = PredictedPlayer(player)
    prediction.step(lookahead_time)

    if self.spawn_spike(prediction.copy(), dangers):
      self.reset_danger_time()

  def update(self, player: FloatVelocitySprite, spikes: displayio.Group, peaceful_mode = False):
    self.track_player(player)
    self._dialouge.update()
    
    if peaceful_mode:
      return

    self._dialouge.clear()
    self.spawn_danger(player, spikes)

    if len(self._handicap_lower_thresholds) > 0 and \
      self._current_game_frames > self._handicap_lower_thresholds[0]:
      self._handicap_lower_thresholds.pop(0)
      self._danger_spawn_handicap -= 1
    
    self._current_game_frames += 1
    self._time_since_last_danger += 1
