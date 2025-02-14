# blinka_displayio_pygamedisplay.PyGameDisplay patch by @Gamer153
# fixes: pygame.error: Unable to make EGL context current (call to eglMakeCurrent failed, reporting an error of EGL_BAD_ACCESS)

import time
from PIL import Image
import pygame

def blinka_pygame_display_initalize_patched(self, init_sequence):
    # pylint: disable=unused-argument

    # initialize the pygame module
    pygame.init()  # pylint: disable=no-member
    # load and set the logo

    if self._icon:
        print(f"loading icon: {self._icon}")
        icon = pygame.image.load(self._icon)
        pygame.display.set_icon(icon)

    if self._caption:
        pygame.display.set_caption(self._caption)

    # create the screen; must happen on main thread on macOS
    self._pygame_screen = pygame.display.set_mode(
        size=(self._width, self._height), flags=self._flags
    )

def blinka_pygame_display_pygamerefresh_patched(self):
    time.sleep(1 / self._native_frames_per_second)
    # refresh pygame-display
    if not self._auto_refresh and not self._pygame_display_force_update:
        pygame.display.flip()
        return

    self._pygame_display_force_update = False

    # Go through groups and and add each to buffer
    if self._core._current_group is not None:
        buffer = Image.new("RGBA", (self._core._width, self._core._height))
        # Recursively have everything draw to the image

        self._core._current_group._fill_area(
            buffer
        )  # pylint: disable=protected-access

        # Scale the image if needed
        if self._scale != 1:
            buffer = buffer.resize(
                (buffer.width * self._scale, buffer.height * self._scale),
                resample=Image.NEAREST
            )
            
        # save image to buffer (or probably refresh buffer so we can compare)
        self._buffer.paste(buffer)

    self._subrectangles = self._core.get_refresh_areas()
    for area in self._subrectangles:
        self._refresh_display_area(area)