try:
    import board
    import displayio
    display = board.DISPLAY  

    background = displayio.OnDiskBitmap("pets/cemetery crawler !/hp-background.png")
    reaper_img = displayio.OnDiskBitmap("reaper.png")
    soul_img = displayio.OnDiskBitmap("soul.png")
    spirit_img = displayio.OnDiskBitmap("spirit.png")
    gravestone_img = displayio.OnDiskBitmap("gravestone.png")


except (NotImplementedError, NameError):
    import blinka_displayio_pygamedisplay as displayio
    from PIL import Image
    import pygame

    display = displayio.PyGameDisplay(width=300, height=300)  

import time
import random
time.sleep(1)  

pygame.init()
screen = pygame.display.set_mode((128, 128))

background = pygame.image.load("hp-background.png")
background = pygame.transform.scale(background, (128, 128))

reaper_img = pygame.image.load("reaper.png")
reaper_img = pygame.transform.scale(reaper_img, (20, 20))

soul_img = pygame.image.load("soul.png")
soul_img = pygame.transform.scale(soul_img, (20, 20)) 

spirit_img = pygame.image.load("spirit.png")
spirit_img = pygame.transform.scale(spirit_img, (20, 20))

gravestone_img = pygame.image.load("gravestone.png")
gravestone_img = pygame.transform.scale(gravestone_img, (30, 30))


gravity = 0.5
jump_power = -10
speed = 5
bg_x = 0

class Reaper:
    def __init__(self):
        self.sprite = pygame.image.load("reaper.png")
        self.x = 0
        self.y = 0
        self.velocity = 0
        self.on_ground = True
        self.score = 0
        self.stunned = False

    def move(self, direction):
        if direction == "left":
            self.x -= speed
        elif direction == "right":
            self.x += speed
        self.sprite.x = self.x

    def jump(self):
        if self.on_ground and not self.stunned:
            self.velocity = jump_power
            self.on_ground = False

    def attack(self, spirits):
        for spirit in spirits:
            if abs(self.x - spirit.x) < 20:
                spirits.remove(spirit)
                self.score += 2  

    def update(self, screen):  
        screen.blit(self.sprite, (self.x, self.y))

reaper = Reaper()
souls = []
spirits = []
gravestones = []

running = True
while running:
    screen.fill((0, 0, 0))  
    reaper.update(screen) 
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
