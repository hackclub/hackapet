import displayio #type: ignore
import pygame # type: ignore
import math

ghostty_sheet = displayio.OnDiskBitmap("art/ghostty-Sheet.bmp")
restart = displayio.OnDiskBitmap("art/restart.bmp")

tile_width = 32
tile_height = 32


class Sprite:
    def __init__(self, splash, terminals, controls):
        self.sprite = displayio.TileGrid(
            ghostty_sheet,
            pixel_shader=ghostty_sheet.pixel_shader,
            width=1,
            height=1,
            tile_width=tile_width,
            tile_height=tile_height,
            default_tile=0,
            x=tile_width/4,
            y=128 - tile_height
        )

        self.restart = displayio.TileGrid(
            restart,
            pixel_shader=restart.pixel_shader
        )


        splash.append(self.sprite)
        self.frame = 0
        self.down = False
        self.up = False
        self.jump = False
        self.vel = 0
        self.splash = splash
        self.terminals = terminals
        self.controls = controls
        self.good_prompt_score = int(open("objects/good_prompt_score.txt", "r").read())
    
    def update(self):
        keys = pygame.key.get_pressed()
	
        if keys[pygame.K_LEFT] == False:
            if self.down == True:
                self.frame-=1
                self.sprite[0] = math.floor(self.frame)
                self.frame-=1
                self.down = False
                self.up = True
            elif self.up == True:
                self.sprite[0] = math.floor(self.frame)
                if self.frame > 31:
                    self.frame -= 1
                else:
                    self.up = False
                    self.frame = 0
            else:
                self.sprite[0] = math.floor(self.frame)
                self.frame = (((self.frame + 0.1)) % (30))
        elif keys[pygame.K_LEFT] and self.down == False: 
            '''and ((1 <= (self.frame // 10) <= 6) or (10 <= (self.frame // 10) <= 12) or (26 <= (self.frame // 10) <= 30))'''
            # 1-6, 10-12, 26-30
            self.down = True
            self.frame = 31
        elif self.down == True:
            self.sprite[0] = math.floor(self.frame)
            if self.frame < (ghostty_sheet.width // tile_width)-1:
                self.frame += 0.5
        else:
            self.sprite[0] = math.floor(self.frame)
            self.frame = (((self.frame + 0.1)) % (30))
        if keys[pygame.K_RIGHT] and self.sprite.y > 0 and self.jump == False:
            self.vel = -4
            self.jump = True

        self.vel += 0.2
        setpoint = self.sprite.y + self.vel
        if setpoint > 128 - tile_height:
            self.sprite.y = 128 - tile_height
            self.vel = 0
            self.jump = False
        terminals = self.terminals.terminals.copy()
        for terminal in terminals:
            if self.horizontal_collide(terminal):
                if self.sprite.y + tile_height <= terminal.sprite.y  < setpoint + tile_height:
                    self.sprite.y = terminal.sprite.y - tile_height
                    self.vel = 0
                    self.jump = False
                elif self.vertical_collide(terminal):
                    self.restart_screen()

        bad_prompts = self.terminals.bad_prompts.copy()
        for bad_prompt in bad_prompts:
            if self.horizontal_collide_prompt(bad_prompt) and self.vertical_collide_prompt(bad_prompt):
                self.restart_screen()
        self.sprite.y += math.floor(self.vel)
        good_prompts = self.terminals.good_prompts.copy()
        for good_prompt in good_prompts:
            if self.horizontal_collide_prompt(good_prompt) and self.vertical_collide_prompt(good_prompt):
                self.good_prompt_score += 1
                self.terminals.good_prompts.remove(good_prompt)
                good_prompt.remove()
    
    def horizontal_collide(self, terminal):
        ghostty_left = self.sprite.x + 7
        ghostty_right = self.sprite.x + 25

        terminal_left = terminal.sprite.x
        terminal_right = terminal.sprite.x + 32

        return (ghostty_left < terminal_right and 
                ghostty_right > terminal_left)

    def horizontal_collide_prompt(self, prompt):
        ghostty_left = self.sprite.x + 7
        ghostty_right = self.sprite.x + 25

        terminal_left = prompt.sprite.x + 9
        terminal_right = prompt.sprite.x + 24

        return (ghostty_left < terminal_right and 
                ghostty_right > terminal_left)

    def vertical_collide(self, terminal):
        if self.down:
            ghostty_top = self.sprite.y + 16
            ghostty_bottom = self.sprite.y + 32
        else:
            ghostty_top = self.sprite.y
            ghostty_bottom = self.sprite.y + 26

        terminal_top = terminal.sprite.y
        terminal_bottom = terminal.sprite.y + 32

        return (terminal_top < ghostty_bottom and 
                terminal_bottom > ghostty_top)
    def vertical_collide_prompt(self, prompt):
        if self.down:
            ghostty_top = self.sprite.y + 16
            ghostty_bottom = self.sprite.y + 32
        else:
            ghostty_top = self.sprite.y
            ghostty_bottom = self.sprite.y + 26

        terminal_top = prompt.sprite.y + 11
        terminal_bottom = prompt.sprite.y + 16

        return (terminal_top < ghostty_bottom and 
                terminal_bottom > ghostty_top)
    def restart_screen(self):
        to_wait = True
        self.splash.append(self.restart)
        open("objects/good_prompt_score.txt", "w").write(str(self.good_prompt_score))
        while to_wait:
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if keys[pygame.K_DOWN]:
                    to_wait = False
        self.splash.remove(self.restart)
        self.terminals.empty()
        self.controls.hide()