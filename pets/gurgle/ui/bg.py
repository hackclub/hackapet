import displayio

def Background():
    bg = displayio.OnDiskBitmap("./assets/space_scene.bmp")

    tile_grid = displayio.TileGrid(bg, pixel_shader=bg.pixel_shader)

    return tile_grid
