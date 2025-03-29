import renderer, math

class MenuItem:
    def __init__(self, x, y, func):
        self.x = x
        self.y = y
        self.func = func
    
    def __call__(self):
        self.func()

class Game:
    def __init__(self):
        self.screen = renderer.Renderer('miyazaki-16.txt')
        self.tama_sprite = self.screen.load_stacked_sprite('tamashort.png', 19)
        self.tama_sprite_jump = self.screen.load_stacked_sprite('tamajump.png', 18)
        self.tama_sleep_sprite = self.screen.load_stacked_sprite('tamasleep.png', 14)
        self.tama_dead_sprite = self.screen.load_stacked_sprite('grave.png', 20)
        self.current_sprite = self.tama_sprite
        self.tama_rot = 0
        self.tama_pos_x = 64
        self.tama_pos_y = 64
        self.tama_speed = 4
        self.tama_rot_speed = math.pi/20

        self.bg_bmp = self.screen.load_sprite('background.bmp')
        self.world_size = self.screen.set_background(self.bg_bmp)

        self.current_world_tile = [0,0]

        self.screen.set_background_square(*self.current_world_tile)

        self.in_main_menu = False
        self.menu_debounce = False

        self.zoomed_in = False
        self.current_border_size = 128

        self.screen.load_menu_atlas('menu_atlas.bmp', 5)
        self.screen.set_menu_visibility(False)

        self.blank_tile = (5, 0)

        self.screen.set_menu_tile((0,2),(0,0))
        self.screen.set_menu_tile((0,3),(0,1))

        self.screen.set_menu_tile((3,2),(1,0))
        self.screen.set_menu_tile((3,3),(1,1))

        self.menu_items = [MenuItem(2, 0, self.tama_jump),
                           MenuItem(0, 2, self.toggle_sleep),
                           MenuItem(2, 2, self.drink_water)]
        self.set_menu_item(0)

        self.frames_in_jump = None
        self.sleeping = False

        self.inspecting = False
        self.dead = False

        self.sleep_meter = 0
        self.sleep_alerted = False
        self.exercise_meter = 0
        self.exercise_alerted = False
        self.water_meter = 0
        self.water_alerted = False
        self.flower_meter = 0
        self.flower_alerted = False
        #self.reflection_meter = 0

        # self.screen.set_menu_tile((1,2),(2,0))
        # self.screen.set_menu_tile((1,3),(2,1))
        # self.screen.set_menu_tile((2,2),(3,0))
        # self.screen.set_menu_tile((2,3),(3,1))

    def set_menu_item(self, i):
        self.current_item_index = i
        item = self.menu_items[i]
        x, y = item.x, item.y

        self.screen.set_menu_tile((1,2),(x,y))
        self.screen.set_menu_tile((1,3),(x,y+1))
        self.screen.set_menu_tile((2,2),(x+1,y))
        self.screen.set_menu_tile((2,3),(x+1,y+1))

    def move_menu_item(self, di):
        i = (self.current_item_index+di) % len(self.menu_items)
        self.set_menu_item(i)

    def rotate_tama(self, i):
        #print(self.tama_rot)
        self.tama_rot = self.tama_rot+i

    def toggle_zoom(self):
        self.zoomed_in = not self.zoomed_in
        if self.zoomed_in:
            self.screen.splash.scale = 2
            #self.tama_pos_x /= 2
            #self.tama_pos_y /= 2

    def toggle_menu(self):
        self.in_main_menu = not self.in_main_menu
        self.screen.set_menu_visibility(self.in_main_menu)

    def open_menu(self):
        self.in_main_menu = True
        self.screen.set_menu_visibility(True)

    def close_menu(self):
        self.in_main_menu = False
        self.screen.set_menu_visibility(False)

    def toggle_sleep(self):
        self.sleeping = not self.sleeping
        if self.sleeping:
            self.current_sprite = self.tama_sleep_sprite
            if self.get_floor_colour() == (252, 239, 141, 255):
                self.flower_meter -= 100
            #if self.get_floor_colour()
        else:
            self.current_sprite = self.tama_sprite

    def move_world_tile(self, dx, dy):
        if dx:
            if dx==1: self.tama_pos_x = 0
            elif dx==-1: self.tama_pos_x = self.current_border_size
        if dy:
            if dy==1: self.tama_pos_y = 0
            elif dy==-1: self.tama_pos_y = self.current_border_size

        if dx or dy: 
            self.current_world_tile[0] += dx
            self.current_world_tile[1] += dy
            self.set_world_tile(*self.current_world_tile)

    def set_world_tile(self, x, y):
        self.screen.set_background_square(x, y)

    def tama_jump(self):
        self.frames_in_jump = 0
        self.exercise_meter -= 50
        if not self.sleeping: self.current_sprite = self.tama_sprite_jump
        if self.get_floor_colour() == (217, 189, 200, 255):
            self.inspecting = True
    
    def drink_water(self):
        if self.get_floor_colour() == (109, 128, 250, 255):
            self.water_meter -= 100

    def get_floor_colour(self):
        bmp_x = self.tama_pos_x + (128*self.current_world_tile[0])
        bmp_y = self.tama_pos_y + (128*self.current_world_tile[1])
        #print(bmp_x, bmp_y)
        return self.bg_bmp[bmp_x, bmp_y]

    def try_move_tama(self, dx, dy):
        nx = self.tama_pos_x+dx
        ny = self.tama_pos_y+dy
        if 0<ny<128 and 0<nx<128: 
            self.tama_pos_x = nx
            self.tama_pos_y = ny
        else:
            if not(nx < 0 and self.current_world_tile[0]==0) and not(nx>128 and self.current_world_tile[0]==self.world_size[0]-1):
                self.tama_pos_x = nx
            if not(ny < 0 and self.current_world_tile[1]==0) and not(ny>128 and self.current_world_tile[1]==self.world_size[1]-1):
                self.tama_pos_y = ny

    def explode(self):
        if self.dead == False: self.need_redraw = True
        self.dead = True
        self.current_sprite = self.tama_dead_sprite

    def mainloop(self):
        self.screen.draw_stacked_sprite(self.tama_sprite, int(self.tama_pos_x), int(self.tama_pos_y), scale=1, rotation=self.tama_rot)
        #self.screen.draw_stacked_sprite(self.tama_sprite, int(self.tama_pos_x-30), int(self.tama_pos_y), scale=1, rotation=self.tama_rot)
        while True:
            self.screen.mainevents()
            self.need_redraw = False

            self.water_meter += 0.00005
            if not self.sleeping:
                self.sleep_meter += 0.000015
            else:
                self.sleep_meter -= 0.00002
            #self.reflection_meter += 0.2
            self.exercise_meter += 0.000025
            self.flower_meter += 0.00005

            if not self.exercise_alerted and self.exercise_meter > 100:
                self.exercise_alerted = True
                self.screen.set_menu_tile((1,0), (4,3))
            if self.exercise_alerted and self.exercise_meter < 100:
                self.screen.set_menu_tile((1, 0), self.blank_tile)
                self.exercise_alerted = False

            if not self.water_alerted and self.water_meter > 100:
                self.water_alerted = True
                self.screen.set_menu_tile((0,0), (4,0))
            if self.water_alerted and self.water_meter < 100:
                self.screen.set_menu_tile((0, 0), self.blank_tile)
                self.water_alerted = False

            if not self.flower_alerted and self.flower_meter > 100:
                self.flower_alerted = True
                self.screen.set_menu_tile((2,0), (4,2))
            if self.flower_alerted and self.flower_meter < 100:
                self.screen.set_menu_tile((2, 0), self.blank_tile)
                self.flower_alerted = False

            if not self.sleep_alerted and self.sleep_meter > 100:
                self.sleep_alerted = True
                self.screen.set_menu_tile((3,0), (4,1))
            if self.sleep_alerted and self.sleep_meter < 100:
                self.screen.set_menu_tile((3, 0), self.blank_tile)
                self.sleep_alerted = False

            if self.sleep_alerted and self.flower_alerted and self.water_alerted and self.exercise_alerted:
                self.explode()

            dx = -1*(self.tama_pos_x<0)+(self.tama_pos_x>self.current_border_size)
            dy = -1*(self.tama_pos_y<0)+(self.tama_pos_y>self.current_border_size)
            #print(dx, dy)
            if dx or dy: 
                self.move_world_tile(dx, dy)
                self.need_redraw = True
            
            #self.check_water()

            if self.screen.key_up_down:
                #print(self.tama_rot)
                if not self.in_main_menu and not self.sleeping and not self.inspecting and not self.dead:
                    self.try_move_tama(math.sin(self.tama_rot)*self.tama_speed, -math.cos(self.tama_rot)*self.tama_speed)
                    self.need_redraw = True
                elif self.in_main_menu:
                    self.menu_items[self.current_item_index]()
                    self.close_menu()
                    self.need_redraw = True
            elif self.screen.key_left_down and self.screen.key_right_down:
                if self.inspecting:
                    self.inspecting = False
                elif not (self.screen.key_left_debounce and self.screen.key_right_debounce):
                    self.toggle_menu()
                    self.menu_debounce = True
                #self.toggle_zoom()
                
            if self.screen.key_left_down:
                if not self.in_main_menu:
                    self.rotate_tama(-self.tama_rot_speed)
                    self.need_redraw = True
                else:
                    if not self.screen.key_left_debounce: self.move_menu_item(1)
            elif self.screen.key_right_down:
                if not self.in_main_menu:
                    self.rotate_tama(self.tama_rot_speed)
                    self.need_redraw = True
                else:
                    if not self.screen.key_right_debounce: self.move_menu_item(-1)

            if self.frames_in_jump is not None:
                self.tama_pos_y += (3*self.frames_in_jump-12)
                self.frames_in_jump += 1
                self.need_redraw = True
                if self.frames_in_jump == 9:
                    if not self.sleeping: self.current_sprite = self.tama_sprite
                    self.frames_in_jump = None

            if self.need_redraw:
                if self.inspecting: 
                    self.screen.clear_screen(4)
                    self.screen.draw_stacked_sprite(self.current_sprite, 12, 50, scale=4, rotation=self.tama_rot)
                else:
                    self.screen.clear_screen(0)
                    self.screen.draw_stacked_sprite(self.current_sprite, int(self.tama_pos_x), int(self.tama_pos_y), scale=1, rotation=self.tama_rot)
                        #self.screen.draw_stacked_sprite(self.tama_sprite, int(self.tama_pos_x), int(self.tama_pos_y), scale=1, rotation=self.tama_rot)


game = Game()
game.mainloop()
