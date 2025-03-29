from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font

from sprites.base import HitboxOffsetSprite

FONT = bitmap_font.load_font("fonts/munro-10.bdf")

class Score(HitboxOffsetSprite):
  def __init__(self, high_score_mode = False, *args, **kwargs):
    super().__init__(*args, **kwargs)

    self._sprite = label.Label(font=FONT, text="", color=0xFFFF00)
    self._sprite.anchor_point = (1, 0)
    self._sprite.anchored_position = (127, 2)

    self.append(self._sprite)

    self._score = 0
    self._high_score = 0
    self._high_score_mode = high_score_mode
    self._update_text()
  
  @property
  def width(self):
    self._sprite.width
  
  @property
  def height(self):
    self._sprite.height

  @property
  def score(self):
    return self._score

  @property
  def high_score(self):
    return self._high_score
  
  def _update_text(self):
    if self._high_score_mode:
      self._sprite.text = "High Score: " + str(self._high_score)
    else:
      self._sprite.text = "Score: " + str(self._score)
  
  def set_high_score_mode(self, high_score_mode: bool):
    self._high_score_mode = high_score_mode
    self._update_text()

  def reset(self):
    self._score = 0
    self._update_text()
  
  def increase(self, value):
    self._score = max(0, self._score + value)
    self._high_score = max(self._high_score, self._score)
    self._update_text()
  
  def decrease(self, value):
    self.increase(-value)
