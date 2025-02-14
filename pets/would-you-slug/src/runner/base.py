from abc import ABCMeta, abstractmethod
import displayio

class Input():
  class ButtonState:
    _value = False
    _last_value = False

    def __bool__(self):
      return self.down
    
    def update(self):
      self._last_value = self._value

    def set(self, value):
      if not isinstance(value, bool):
        raise ValueError("Expecting a boolean or integer value")
      self._last_value = self._value
      self._value = value

    @property
    def down(self):
      return self._value
    
    @property
    def pressed(self):
      return self._value and (not self._last_value)
    
    @property
    def released(self):
      return (not self._value) and self._last_value
    
    @property
    def held(self):
      return self._value and self._last_value

  _left = ButtonState()
  _middle = ButtonState()
  _right = ButtonState()

  def update(self):
    self._left.update()
    self._middle.update()
    self._right.update()

  @property
  def left(self) -> ButtonState:
    return self._left
  
  @left.setter
  def left(self, value):
    self._left.set(value)

  @property
  def middle(self) -> ButtonState:
    return self._middle
  
  @middle.setter
  def middle(self, value):
    self._middle.set(value)
  
  @property
  def right(self) -> ButtonState:
    return self._right
  
  @right.setter
  def right(self, value):
    self._right.set(value)

class Runner(metaclass=ABCMeta):
  input: Input
  splash: displayio.Group
  display: displayio.Display

  def __init__(self):
    self.input = Input()
    self.splash = displayio.Group()

    self.display = self._init_display()
    self.display.show(self.splash)
  
  @abstractmethod
  def _init_display(self):
    return None

  @abstractmethod
  def _update(self):
    pass

  def update(self):
    self.input.update()
    self._update()

  @abstractmethod
  def refresh(self):
    pass

  @abstractmethod
  def check_exit(self) -> bool:
    return False

  def run(self, main_function):
    main_function(self)
