from world import World

PLAYER_SIZE = 8

P_RIGHT = 1
P_LEFT = 2

PT_NORMAL = 0
PT_UMBRELLA = 1
PT_NOCLIP = 2

FALL_FRAME_INTERVAL = 15
JUMP_HEIGHT = 2
JUMP_FALL_FRAMES = JUMP_HEIGHT * FALL_FRAME_INTERVAL
JUMP_UP_FRAMES = JUMP_HEIGHT * -2
class Player:
    def __init__(self, spawn_y: int, world: World):
        self.x = 0
        self.y = spawn_y
        self.jump_frame = 0
        self.world = world
        self.should_update = False
        self.should_render = False
        self.looking = P_RIGHT
        self.falling_frame = 0
        self.texture_tile = PT_NORMAL
        self.short_fall = False

        self.noclip = False
    
    def change_texture_tile(self, tid: int, ignore_noclip: bool = False):
        if tid != self.texture_tile and (self.texture_tile != PT_NOCLIP or ignore_noclip):
            self.texture_tile = tid
            self.should_render = True

    def jump(self) -> bool:
        if self.jump_frame != 0: return
        up = 0
        while self.world.block_at(self.x, self.y + up + 1) is None and up < JUMP_HEIGHT:
            up += 1
        if up == 0: return False

        self.jump_frame = JUMP_UP_FRAMES
        # self.jump_frame = 60
        # if not self.move(0, up):
        #     self.jump_frame = 0
        #     return False
        return True
    
    def tick(self):
        if self.noclip:
            self.jump_frame = 0
            self.falling_frame = 0
            return

        if self.jump_frame > 0:
            self.jump_frame -= 1
            if self.jump_frame % (JUMP_FALL_FRAMES // JUMP_HEIGHT) == 1:
                if not self.move(0, -1):
                    self.jump_frame = 0
                    self.change_texture_tile(PT_NORMAL)
            elif self.jump_frame == 0:
                self.move(0, 0) # fall to ground
                self.change_texture_tile(PT_NORMAL)
        elif self.jump_frame < 0: # jumping up
            self.jump_frame += 1
            if self.jump_frame % (JUMP_UP_FRAMES // JUMP_HEIGHT) == -1:
                if not self.move(0, 1):
                    self.jump_frame = JUMP_FALL_FRAMES
                    self.change_texture_tile(PT_UMBRELLA)
            elif self.jump_frame == 0:
                self.jump_frame = JUMP_FALL_FRAMES
                self.change_texture_tile(PT_UMBRELLA)
        
        if self.falling_frame > 0:
            if not self.short_fall: self.change_texture_tile(PT_UMBRELLA)
            self.falling_frame -= 1
            if self.falling_frame % FALL_FRAME_INTERVAL == 0:
                if not self.move(0, -1):
                    self.falling_frame = 0
                    self.change_texture_tile(PT_NORMAL)
        

        if self.jump_frame == 0 and self.falling_frame == 0:
            self.change_texture_tile(PT_NORMAL)
    
    def move(self, dx: int, dy: int) -> bool:
        # print("try moving", dx, dy, "- block:", self.world.block_at(self.x + dx, self.y + dy), "at", self.x + dx, self.y + dy)
        l = self.looking
        if dx < 0: l = P_LEFT
        elif dx > 0: l = P_RIGHT
        if l != self.looking:
            self.looking = l
            self.should_render = True

        if self.noclip:
            self.x += dx
            self.y += dy
            self.should_update = True
            return True

        if self.world.block_at(self.x + dx, self.y + dy) is not None and (dx != 0 or dy != 0):
            return False
        else:
            self.x += dx
            self.y += dy
            down = 0
            if self.jump_frame == 0:
                while self.world.block_at(self.x, self.y - down - 1) is None:
                    down += 1
            # self.y -= down
            if self.falling_frame == 0:
                self.falling_frame = (FALL_FRAME_INTERVAL * down) if down > 1 else 5 if down > 0 else 0
                self.short_fall = (down == 1)
            
            self.should_update = True

            if self.world.block_at(self.x, self.y - 1) is not None:
                self.change_texture_tile(PT_NORMAL)
            return True
    
    def toggle_noclip(self):
        self.noclip = not self.noclip
        if self.noclip:
            self.change_texture_tile(PT_NOCLIP, True)
        else:
            self.change_texture_tile(PT_NORMAL, True)
