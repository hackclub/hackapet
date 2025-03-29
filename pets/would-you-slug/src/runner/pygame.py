import pygame.locals
import patch
from blinka_displayio_pygamedisplay import PyGameDisplay
PyGameDisplay._initialize = patch.blinka_pygame_display_initalize_patched
PyGameDisplay.refresh = patch.blinka_pygame_display_pygamerefresh_patched
import pygame

from runner.base import Runner

class PygameRunner(Runner):
  _should_exit = False

  def _init_display(self):
    return PyGameDisplay(width=128, height=128)
  
  def _update_inputs(self, key, pressed):
    if key == pygame.K_a:
      self.input.left = pressed
    elif key == pygame.K_w:
      self.input.middle = pressed
    elif key == pygame.K_d:
      self.input.right = pressed

  def _update(self):
    for event in pygame.event.get():
      if event.type == pygame.locals.QUIT:
        self._should_exit = True
      if event.type == pygame.KEYDOWN:
        self._update_inputs(event.key, True)
      if event.type == pygame.KEYUP:
        self._update_inputs(event.key, False)
    
    return False
  
  def refresh(self):
    self.display.refresh()

  def check_exit(self):
    return self._should_exit
