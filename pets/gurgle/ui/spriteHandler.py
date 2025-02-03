import displayio

def load_sprite_sheet(filename, tile_width=64, tile_height=64):
    sheet = displayio.OnDiskBitmap(filename)
    
    frame_count = sheet.width // tile_width
    
    sprite = displayio.TileGrid(
        sheet,
        pixel_shader=sheet.pixel_shader,
        tile_width=tile_width,
        tile_height=tile_height,
        default_tile=0,
        width=1,
        height=1
    )
    
    return sprite, frame_count
