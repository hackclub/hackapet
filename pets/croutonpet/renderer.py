import displayio, pygame, time, random, math, os
from blinka_displayio_pygamedisplay import PyGameDisplay
from adafruit_display_text import label


###make sprites draw top down and not overdraw stuff

class Renderer:
    def __init__(self, palette_path):
        pygame.init()
        self.display = PyGameDisplay(width=128, height=128)
        self.splash = displayio.Group(scale=1)
        self.display.show(self.splash)

        self.load_palette(palette_path)

        self.bg_bmp = displayio.Bitmap(128, 128, len(self.palette_list))
        self.bg_grid = displayio.TileGrid(self.bg_bmp, pixel_shader=self.palette, width=1, 
                            height=1, tile_height=128, tile_width=128, default_tile=0)
        self.splash.append(self.bg_grid)

        self.screen_bmp = displayio.Bitmap(128, 128, len(self.palette_list))

        self.screen_grid = displayio.TileGrid(self.screen_bmp, pixel_shader=self.palette, width=1, 
                            height=1, tile_height=128, tile_width=128, default_tile=0)
        
        self.splash.append(self.screen_grid)

        self.key_callbacks = {}

        self.written_pixels = set()

        self.key_left_down = False
        self.key_right_down = False
        self.key_up_down = False

        self.key_left_debounce = False
        self.key_right_debounce = False
        self.key_up_debounce = False

        print(self.clamp(10, 4, 8))

    def set_key_callback(self, key, function):
        self.key_callbacks[key] = function

    def set_background(self, bmp):
        self.bg_bmp = bmp
        self.bg_grid = displayio.TileGrid(self.bg_bmp, pixel_shader=bmp.pixel_shader, width=1, height=1,
                                          tile_height=128, tile_width=128, default_tile=0, x=0)
        width = self.bg_bmp.width//128
        height = self.bg_bmp.height//128
        self.splash[0] = self.bg_grid

        return (width, height)

    def set_background_square(self, x, y):
        num_h_tiles = self.bg_bmp.width/128
        #print(x+(y*num_h_tiles))
        self.bg_grid[0] = x+(y*num_h_tiles)

    def load_menu_atlas(self, path, clear_tile=0):
        self.menu_bmp = displayio.OnDiskBitmap(path)
        self.menu_grid = displayio.TileGrid(self.menu_bmp, pixel_shader=self.menu_bmp.pixel_shader,
                                            width=4, height=4, tile_width=32, tile_height=32, default_tile=clear_tile)
        self.splash.append(self.menu_grid)
        
    def set_menu_visibility(self, visible):
        self.menu_grid.hidden = not visible

    def set_menu_tile(self, menu_tile, source_tile):
        tiles_in_source_row = self.menu_bmp.width/32
        #menu_tile_i = menu_tile[0]+(menu_tile[1]*8)
        source_tile_i = source_tile[0]+(source_tile[1]*tiles_in_source_row)
        self.menu_grid[menu_tile] = source_tile_i
        
    def load_sprite(self, path):
        return displayio.OnDiskBitmap(path)

    def load_palette(self, path):
        with open(path, 'r') as f:
            hex_colours = f.read().splitlines()
            self.palette = displayio.Palette(len(hex_colours))

        self.palette_list = []
        for i, colour in enumerate(hex_colours):
            a, r, g, b = [int(a, 16) for a in [colour[:2], colour[2:4], colour[4:6], colour[6:]]]
            self.palette_list.append((r, g, b))
            self.palette[i] = (r, g, b)
        
        #first colour in palette always transparent colour
        self.palette.make_transparent(0)

    def load_stacked_sprite(self, path, num_slices):
        bmp = displayio.OnDiskBitmap(path)
        return {'bmp': displayio.OnDiskBitmap(path),
                'num_slices': num_slices,
                'slice_width': bmp.width//num_slices}

    def clear_screen(self, col):
        self.written_pixels = set()
        for x in range(128):
            for y in range(128):
                self.draw_pixel(x, y, col, mark_written=False, overwrite=True)

    def find_best_colour_index(self, target_col):
        #print(target_col)
        if type(target_col) == int: return target_col
        #first check if has alpha channel and is transparent
        if len(target_col)==4 and target_col[3] == 0:
            #if so return first colour in palette -> always transparent
            return 0
        
        #else find the colour in the palette and return the indexs
        if target_col[:3] in self.palette_list:
            return self.palette_list.index(target_col[:3])

        raise ValueError(f'Colour {target_col} does not exist in palette')
    
    def draw_pixel(self, x, y, colour, overwrite=False, mark_written=True):
        if x>127 or y>127: return
        if x<0 or y<0: return
        col = self.find_best_colour_index(colour)
        if col != 0 or (col == 0 and overwrite):
            self.screen_bmp[x, y] = col
            if mark_written: self.written_pixels.add((x,y))

    def get_pixel(self, x, y):
        if x>127 or y>127: return None
        if x<0 or y<0: return None
        return self.screen_bmp[x, y]
    
    def get_pixel_written(self, x, y):
        if x>127 or y>127: return True
        if x<0 or y<0: return True
        return (x,y) in self.written_pixels

    def draw_img(self, bmp, ox, oy):
        for x in range(bmp.width):
            for y in range(bmp.height):
                self.draw_pixel(x+ox, y+oy, bmp[x, y])

    def rotate_coords(self, coords, rotation):
        ux = (math.cos(rotation), math.sin(rotation))
        uy = (math.cos(rotation+math.pi/2), math.sin(rotation+math.pi/2))

        #print('x',ux)
        #print('y',uy)

        vx = coords[0]*ux[0] + coords[1]*uy[0]
        vy = coords[0]*ux[1] + coords[1]*uy[1]
        return (round(vx), round(vy))

    # def draw_img_ex(self, bmp, ox, oy, scale=(1,1), rotation=0):
    #     scale_x, scale_y = scale
    #     for x in range(0, bmp.width):
    #         for y in range(0, bmp.height):
    #             for sx in range(scale_x):
    #                 for sy in range(scale_y):
    #                     scaled_coords = (x*scale_x+sx, y*scale_y+sy)
    #                     rotated_coords = self.rotate_coords(scaled_coords, rotation)
    #                     self.draw_pixel(rotated_coords[0]+ox, rotated_coords[1]+oy, bmp[x, y])

    def clamp(self, v, mn, mx):
        return min(max(v, mn), mx)

##    def draw_img_ex(self, bmp, ox, oy, px, py, width, height, scale=(1,1), rotation=0, overlay=True):
##        if width is None: width = bmp.width
##        if height is None: height = bmp.height
##        max_img_size = math.ceil(math.sqrt(width**2 + height**2))
##        hw, hh = max_img_size//2, max_img_size//2
##        bhw, bhh = width//2, height//2
##        #out_img = [[0 for i in range(max_img_size)] for j in range(max_img_size)]
##        scale_x, scale_y = scale
##        for x in range(0, max_img_size):
##            for y in range(0, max_img_size):
##                rx, ry = self.rotate_coords((x-hw, y-hh), -rotation)
##                qx, qy = rx+bhw+px, ry+bhh+py
##                #print(px, py, width, height, qx, qy)
##                col = bmp[self.clamp(qx, px, px+width), qy]
##                if qy < 0: continue
##                for sx in range(scale_x):
##                    for sy in range(scale_y):
##                        dx = ox+sx-hw+x*scale_x
##                        dy = oy+sy-hh+y*scale_y
##                        if not overlay and self.get_pixel_written(dx, dy):
##                            continue
##                        self.draw_pixel(dx, dy, col)

    def apply_shears(self, x, y, alpha, beta):
        x = x + alpha*y
        y = y + beta*x
        x = x + alpha*y
        return x, y

    def draw_img_ex(self, bmp, screen_x_offset, screen_y_offset, frame_x, frame_y, frame_width, frame_height, scale=(1,1), rotation=0, overlay=True):
        alpha = -math.tan(rotation/2)
        beta = math.sin(rotation)
        top_left_shear = self.apply_shears(0, 0, alpha, beta)
        bottom_right_shear = self.apply_shears(frame_width, frame_height, alpha, beta)
        sheared_width = bottom_right_shear[0]-top_left_shear[0]
        shear_x_offset = (sheared_width/2)-top_left_shear[0]
        sheared_height = bottom_right_shear[1]-top_left_shear[1]
        shear_y_offset = (sheared_height/2)-top_left_shear[1]
        for src_x in range(frame_width):
            for src_y in range(frame_height):
                src_col = bmp[src_x+frame_x, src_y+frame_y]
                shear_x, shear_y = self.apply_shears(src_x, src_y, alpha, beta)
                screen_x = int(shear_x+screen_x_offset-shear_x_offset)
                screen_y = int(shear_y+screen_y_offset-shear_y_offset)
                self.draw_pixel(screen_x, screen_y, src_col, overwrite=False)

    def draw_stacked_sprite(self, sprite, ox, oy, scale=1, rotation=0):
        bmp = sprite['bmp']
        top_y = oy-sprite['num_slices']*scale
        for n_slice in reversed(range(0, sprite['num_slices']+1)):
            self.draw_img_ex(bmp, ox, top_y+n_slice*scale, bmp.width-(n_slice*sprite['slice_width']), 0, sprite['slice_width'], bmp.height, scale=(scale, scale), rotation=rotation, overlay=False)

    # def draw_stacked_sprite(self, name, ox, oy, scale=1, rotation=0, offset=1):
    #     self.sprite_tiles = []
    #     for i, bmp in enumerate(self.stacked_sprites[name]):
    #         self.sprite_tiles.append(displayio.TileGrid(bmp, pixel_shader=self.palette,
    #                                                     x=ox, y=oy-i))
    #         self.splash.append(self.sprite_tiles[-1])

    def mainevents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

        keys = pygame.key.get_pressed()
        self.key_left_debounce = self.key_left_down
        self.key_left_down = keys[pygame.K_LEFT]
        
        self.key_right_debounce = self.key_right_down
        self.key_right_down = keys[pygame.K_RIGHT]

        self.key_up_debounce = self.key_up_down
        self.key_up_down = keys[pygame.K_UP]
        self.key_down = self.key_left_down or self.key_right_down or self.key_up_down

#renderer = Renderer('miyazaki-16.txt')
#renderer.clear_screen((255, 255, 255))

#car_bmp = displayio.OnDiskBitmap('RedCarpal.bmp')

#tama = renderer.load_stacked_sprite('tamashort')
#tama_rot = 0





#renderer.draw_stacked_sprite('YellowCar', 64, 64)

# renderer.draw_img(renderer.stacked_sprites['YellowCar'][5], 20, 20)
# renderer.draw_img_ex(renderer.stacked_sprites['YellowCar'][5], 64, 64, scale=(1,1), rotation=0)


#renderer.draw_stacked_sprite(tama, 64, 64, scale=2, rotation=0)
#while True:
    #renderer.mainevents()
    #renderer.clear_screen((255, 255, 255))
    #renderer.draw_stacked_sprite(tama, 64, 64, scale=2, rotation=0)
