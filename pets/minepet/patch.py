import time
from typing import BinaryIO, Union
from PIL import Image
from displayio import _structs, Palette, ColorConverter
import pygame

def bitmap_create_init_patched(self, width: int, height: int, value_count: int):
    """Create a Bitmap object with the given fixed size. Each pixel stores a value that is
    used to index into a corresponding palette. This enables differently colored sprites to
    share the underlying Bitmap. value_count is used to minimize the memory used to store
    the Bitmap.
    """
    self._bmp_width = width
    self._bmp_height = height
    self._read_only = False

    if value_count < 0:
        raise ValueError("value_count must be > 0")

    bits = 1
    while (value_count - 1) >> bits:
        if bits < 8:
            bits = bits << 1
        else:
            bits += 8

    self._bits_per_value = bits

    if (
        self._bits_per_value > 8
        and self._bits_per_value != 16
        and self._bits_per_value != 32
    ):
        raise NotImplementedError("Invalid bits per value")

    self._image = Image.new("RGBA", (width, height), 0)
    self._dirty_area = _structs.RectangleStruct(0, 0, width, height)

def tilegrid_fill_area_patched(self, buffer):
    # pylint: disable=too-many-locals,too-many-branches,too-many-statements
    """Draw onto the image"""
    if self._hidden_tilegrid:
        return

    if self._bitmap.width <= 0 or self._bitmap.height <= 0:
        return

    # Copy class variables to local variables in case something changes
    x = self._x
    y = self._y
    width = self._width
    height = self._height
    tile_width = self._tile_width
    tile_height = self._tile_height
    bitmap_width = self._bitmap.width
    pixel_width = self._pixel_width
    pixel_height = self._pixel_height
    tiles = self._tiles
    absolute_transform = self._absolute_transform
    pixel_shader = self._pixel_shader
    bitmap = self._bitmap
    tiles = self._tiles

    tile_count_x = bitmap_width // tile_width

    image = Image.new(
        "RGBA",
        (width * tile_width, height * tile_height),
        (0, 0, 0, 0),
    )

    for tile_x in range(width):
        for tile_y in range(height):
            tile_index = tiles[tile_y * width + tile_x]
            tile_index_x = tile_index % tile_count_x
            tile_index_y = tile_index // tile_count_x
            tile_image = bitmap._image  # type: Image.Image
            if isinstance(pixel_shader, Palette):
                tile_image_p = Image.new("PA", (tile_image.width, tile_image.height))
                tile_image_p.putdata([x[0] for x in list(tile_image.getdata())])
                tile_image = tile_image_p
                self._apply_palette(tile_image)
                
                alpha = tile_image.copy()
                alpha.putpalette(
                    self._pixel_shader._get_alpha_palette()  # pylint: disable=protected-access
                )
                tile_image.putalpha(alpha.convert("L"))

                tile_image = tile_image.convert("RGBA")
            elif isinstance(pixel_shader, ColorConverter):
                # This will be needed for eInks, grayscale, and monochrome displays
                pass
            image.alpha_composite(
                tile_image,
                dest=(tile_x * tile_width, tile_y * tile_height),
                source=(
                    tile_index_x * tile_width,
                    tile_index_y * tile_height,
                    tile_index_x * tile_width + tile_width,
                    tile_index_y * tile_height + tile_height,
                ),
            )

    if absolute_transform is not None:
        if absolute_transform.scale > 1:
            image = image.resize(
                (
                    int(pixel_width * absolute_transform.scale),
                    int(
                        pixel_height * absolute_transform.scale,
                    ),
                ),
                resample=Image.NEAREST,
            )
        if absolute_transform.mirror_x != self._flip_x:
            image = image.transpose(Image.FLIP_LEFT_RIGHT)
        if absolute_transform.mirror_y != self._flip_y:
            image = image.transpose(Image.FLIP_TOP_BOTTOM)
        if absolute_transform.transpose_xy != self._transpose_xy:
            image = image.transpose(Image.TRANSPOSE)
        x *= absolute_transform.dx
        y *= absolute_transform.dy
        x += absolute_transform.x
        y += absolute_transform.y

    source_x = source_y = 0
    if x < 0:
        source_x = round(0 - x)
        x = 0
    if y < 0:
        source_y = round(0 - y)
        y = 0

    x = round(x)
    y = round(y)

    if (
        x <= buffer.width
        and y <= buffer.height
        and source_x <= image.width
        and source_y <= image.height
    ):
        buffer.alpha_composite(image, (x, y), source=(source_x, source_y))

def palette_make_alpha_palette_patched(self):
    palette = []
    for color in self._colors:
        for _ in range(3):
            palette += [color["rgba"][3] if color["transparent"] else 255]
    return palette


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
        # save image to buffer (or probably refresh buffer so we can compare)
        self._buffer.paste(buffer)

    self._subrectangles = self._core.get_refresh_areas()
    for area in self._subrectangles:
        self._refresh_display_area(area)
