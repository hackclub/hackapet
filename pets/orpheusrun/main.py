import displayio
import pygame
from blinka_displayio_pygamedisplay import PyGameDisplay
import time
import random
import os
from displayio import OnDiskBitmap, TileGrid, Palette

pygame.init()

display = PyGameDisplay(width=128, height=128)

main_group = displayio.Group()
display.show(main_group)

BLACK = 0x000000
WHITE = 0xFFFFFF

GROUND_Y = 100
DINO_X = 20
GRAVITY = 0.8
JUMP_FORCE = -12
OBSTACLE_SPEED = 3
SPRITE_WIDTH = 32
SPRITE_HEIGHT = 32
ANIMATION_FRAMES = 9
FPS = 12

PINEAPPLE_MIN_SCALE = 1.2
PINEAPPLE_MAX_SCALE = 1.5
BACKGROUND_SCROLL_SPEED = 1

FONT = pygame.font.Font(None, 20)

class Dinosaur:
    def __init__(self):
        self.width = SPRITE_WIDTH
        self.height = SPRITE_HEIGHT
        self.x = DINO_X
        self.y = GROUND_Y - self.height
        self.velocity_y = 0
        self.is_jumping = False
        self.jumps_left = 3
        
        sprite_sheet = OnDiskBitmap("sprites/orpheus.png")
        self.palette = sprite_sheet.pixel_shader
        
        self.tile_grid = TileGrid(
            bitmap=sprite_sheet,
            pixel_shader=self.palette,
            width=1,
            height=1,
            tile_width=SPRITE_WIDTH,
            tile_height=SPRITE_HEIGHT
        )
        
        self.tile_grid.x = int(self.x)
        self.tile_grid.y = int(self.y)
        
        self.current_frame = 0
        self.frame_count = 0
        self.frames_per_update = 60 // FPS
    
    def update_animation(self):
        self.frame_count += 1
        if self.frame_count >= self.frames_per_update:
            self.frame_count = 0
            self.current_frame = (self.current_frame + 1) % ANIMATION_FRAMES
            self.tile_grid[0] = self.current_frame
    
    def jump(self):
        if self.jumps_left > 0:
            self.velocity_y = JUMP_FORCE
            self.is_jumping = True
            self.jumps_left -= 1
    
    def update(self):
        self.velocity_y += GRAVITY
        self.y += self.velocity_y
        
        if self.y > GROUND_Y - self.height:
            self.y = GROUND_Y - self.height
            self.velocity_y = 0
            self.is_jumping = False
            self.jumps_left = 3
        
        self.tile_grid.y = int(self.y)
        
        if not self.is_jumping:
            self.update_animation()

class Obstacle:
    def __init__(self):
        base_width = 16
        base_height = 16
        self.width = base_width
        self.height = base_height
        self.x = 128
        self.y = GROUND_Y - self.height
        
        sprite_sheet = OnDiskBitmap("sprites/pumpkin.png")
        self.palette = sprite_sheet.pixel_shader
        
        self.tile_grid = TileGrid(
            bitmap=sprite_sheet,
            pixel_shader=self.palette,
            width=1,
            height=1,
            tile_width=base_width,
            tile_height=base_height
        )
        
        self.tile_grid.x = int(self.x)
        self.tile_grid.y = int(self.y)
    
    def update(self):
        self.x -= OBSTACLE_SPEED
        self.tile_grid.x = int(self.x)
    
    def is_off_screen(self):
        return self.x + self.width < 0

class Game:
    def __init__(self):
        self.show_title = True
        self.start_time = None
        self.survival_time = 0
        
        self.title_sprite = OnDiskBitmap("sprites/title.png")
        self.title_palette = self.title_sprite.pixel_shader
        self.title_grid = TileGrid(
            bitmap=self.title_sprite,
            pixel_shader=self.title_palette,
            width=1,
            height=1,
            tile_width=self.title_sprite.width,
            tile_height=self.title_sprite.height
        )
        
        self.title_group = displayio.Group()
        self.title_group.append(self.title_grid)
        
        display.show(self.title_group)
        
        self.bg_sprite = OnDiskBitmap("sprites/background.png")
        self.bg_palette = self.bg_sprite.pixel_shader
        
        self.bg_tiles = displayio.Group()
        self.bg1 = TileGrid(
            bitmap=self.bg_sprite,
            pixel_shader=self.bg_palette,
            width=1,
            height=1,
            tile_width=self.bg_sprite.width,
            tile_height=self.bg_sprite.height
        )
        self.bg2 = TileGrid(
            bitmap=self.bg_sprite,
            pixel_shader=self.bg_palette,
            width=1,
            height=1,
            tile_width=self.bg_sprite.width,
            tile_height=self.bg_sprite.height
        )
        
        self.bg1.x = 0
        self.bg2.x = self.bg_sprite.width
        
        self.bg_tiles.append(self.bg1)
        self.bg_tiles.append(self.bg2)
        
        self.ground_fill = displayio.Bitmap(128, 128 - GROUND_Y, 1)
        self.ground_fill_palette = displayio.Palette(1)
        self.ground_fill_palette[0] = WHITE
        self.ground_fill_grid = displayio.TileGrid(
            self.ground_fill,
            pixel_shader=self.ground_fill_palette,
            x=0,
            y=GROUND_Y
        )
        
        for x in range(128):
            for y in range(128 - GROUND_Y):
                self.ground_fill[x, y] = 0
        
        main_group.append(self.bg_tiles)
        main_group.append(self.ground_fill_grid)
        
        self.dino = Dinosaur()
        self.obstacles = []
        self.game_over = False
        
        self.ground_palette = displayio.Palette(1)
        self.ground_palette[0] = WHITE
        self.ground_bitmap = displayio.Bitmap(128, 1, 1)
        self.ground_grid = displayio.TileGrid(self.ground_bitmap, pixel_shader=self.ground_palette)
        self.ground_grid.y = GROUND_Y
        
        for i in range(128):
            self.ground_bitmap[i, 0] = 0
        
        main_group.append(self.ground_grid)
        main_group.append(self.dino.tile_grid)
        
        
        self.game_over_group = displayio.Group()
        
        
        self.black_bg = displayio.Bitmap(128, 128, 1)
        self.black_palette = displayio.Palette(1)
        self.black_palette[0] = BLACK
        self.black_bg_grid = displayio.TileGrid(
            self.black_bg,
            pixel_shader=self.black_palette
        )
        self.game_over_group.append(self.black_bg_grid)
        
        
        self.pumpkin_sprite = OnDiskBitmap("sprites/pumpkin.png")
        self.pumpkin_palette = self.pumpkin_sprite.pixel_shader
        
        
        self.pumpkins = []
        for i in range(3):
            pumpkin = TileGrid(
                bitmap=self.pumpkin_sprite,
                pixel_shader=self.pumpkin_palette,
                width=1,
                height=1,
                tile_width=16,
                tile_height=16
            )
            pumpkin.x = 40 + (i * 24)  
            pumpkin.y = 56  
            self.pumpkins.append(pumpkin)
    
    def start_game(self):
        self.show_title = False
        self.start_time = time.monotonic()
        display.show(main_group)
    
    def show_game_over(self):
        self.survival_time = time.monotonic() - self.start_time
        
        
        while len(self.game_over_group) > 1:
            self.game_over_group.pop()
            
        
        if self.survival_time >= 30:
            for pumpkin in self.pumpkins:
                self.game_over_group.append(pumpkin)
        elif self.survival_time >= 10:
            for pumpkin in self.pumpkins[:2]:
                self.game_over_group.append(pumpkin)
        else:
            self.game_over_group.append(self.pumpkins[0])
            
        display.show(self.game_over_group)
    
    def update_background(self):
        self.bg1.x -= BACKGROUND_SCROLL_SPEED
        self.bg2.x -= BACKGROUND_SCROLL_SPEED
        
        if self.bg1.x <= -self.bg_sprite.width:
            self.bg1.x = self.bg2.x + self.bg_sprite.width
        if self.bg2.x <= -self.bg_sprite.width:
            self.bg2.x = self.bg1.x + self.bg_sprite.width
    
    def spawn_obstacle(self):
        if len(self.obstacles) == 0 and random.random() < 0.02:
            obstacle = Obstacle()
            self.obstacles.append(obstacle)
            main_group.append(obstacle.tile_grid)
    
    def check_collision(self, obstacle):
        dino_rect = pygame.Rect(self.dino.x, self.dino.y, self.dino.width, self.dino.height)
        obstacle_rect = pygame.Rect(obstacle.x, obstacle.y, obstacle.width, obstacle.height)
        return dino_rect.colliderect(obstacle_rect)
    
    def update(self):
        if not self.show_title:
            if not self.game_over:
                self.update_background()
                self.dino.update()
                
                self.spawn_obstacle()
                for obstacle in self.obstacles[:]:
                    obstacle.update()
                    
                    if self.check_collision(obstacle):
                        self.game_over = True
                        self.show_game_over()
                    
                    if obstacle.is_off_screen():
                        main_group.remove(obstacle.tile_grid)
                        self.obstacles.remove(obstacle)

def main():
    game = Game()
    last_update = time.monotonic()
    update_interval = 1/60  
    
    while True:
        current_time = time.monotonic()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if game.show_title:
                        game.start_game()
                    elif game.game_over:
                        main_group.remove(game.dino.tile_grid)
                        for obstacle in game.obstacles:
                            main_group.remove(obstacle.tile_grid)
                        game = Game()
                    else:
                        game.dino.jump()
        
        
        if current_time - last_update >= update_interval:
            if not game.show_title:
                game.update()
            last_update = current_time
        
        display.refresh()
        time.sleep(max(0, update_interval - (time.monotonic() - current_time)))

if __name__ == "__main__":
    main()
