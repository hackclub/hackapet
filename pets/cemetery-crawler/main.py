import pygame
import random

pygame.init()

WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("cemetery crawler")

background = pygame.image.load("hp-background.png")
reaper_img = pygame.image.load("reaper.png")
soul_img = pygame.image.load("soul.png")
spirit_img = pygame.image.load("spirit.png")
gravestone_img = pygame.image.load("gravestone.png")

gravity = 0.5
jump_power = -10
speed = 5
bg_x = 0

WHITE = (255, 255, 255)

class Reaper:
    def __init__(self):
        self.image = reaper_img
        self.rect = self.image.get_rect(midbottom=(100, HEIGHT - 50))
        self.velocity = 0
        self.on_ground = True
        self.score = 0
        self.stunned = False

    def move(self, keys):
        if keys[pygame.K_a]:
            self.rect.x -= speed
        if keys[pygame.K_d]:
            self.rect.x += speed

    def jump(self):
        if self.on_ground and not self.stunned:
            self.velocity = jump_power
            self.on_ground = False

    def attack(self, spirits):
        for spirit in spirits:
            if self.rect.colliderect(spirit.rect):
                spirits.remove(spirit)
                self.score += 2  

    def update(self):
        if not self.on_ground:
            self.velocity += gravity
        self.rect.y += self.velocity
        if self.rect.bottom >= HEIGHT - 50:
            self.rect.bottom = HEIGHT - 50
            self.on_ground = True
            self.velocity = 0

    def draw(self, screen):
        screen.blit(self.image, self.rect)

def draw_background():
    global bg_x
    bg_x -= speed // 2
    if bg_x <= -WIDTH:
        bg_x = 0
    screen.blit(background, (bg_x, 0))
    screen.blit(background, (bg_x + WIDTH, 0))

class Soul:
    def __init__(self):
        self.image = soul_img
        self.rect = self.image.get_rect(midtop=(random.randint(WIDTH, WIDTH + 100), random.randint(50, 150)))

    def update(self):
        self.rect.x -= speed
        return self.rect.x > -50

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Spirit:
    def __init__(self):
        self.image = spirit_img
        self.rect = self.image.get_rect(midtop=(random.randint(WIDTH, WIDTH + 100), random.randint(50, 150)))

    def update(self):
        self.rect.x -= speed
        return self.rect.x > -50

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Gravestone:
    def __init__(self):
        self.image = gravestone_img
        self.rect = self.image.get_rect(midbottom=(random.randint(WIDTH, WIDTH + 200), HEIGHT - 50))

    def update(self):
        self.rect.x -= speed
        return self.rect.x > -50

    def draw(self, screen):
        screen.blit(self.image, self.rect)

clock = pygame.time.Clock()
reaper = Reaper()
souls = []
spirits = []
gravestones = []
running = True

while running:
    screen.fill(WHITE)
    draw_background()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                reaper.jump()
            if event.key == pygame.K_f:
                reaper.attack(spirits)

    keys = pygame.key.get_pressed()
    reaper.move(keys)
    reaper.update()
    reaper.draw(screen)
    
    if random.randint(1, 80) == 1:
        souls.append(Soul())
    if random.randint(1, 120) == 1:
        spirits.append(Spirit())
    if random.randint(1, 150) == 1:
        gravestones.append(Gravestone())

    for soul in souls[:]:
        if not soul.update():
            souls.remove(soul)
        soul.draw(screen)
        if reaper.rect.colliderect(soul.rect):
            souls.remove(soul)
            reaper.score += 1

    for spirit in spirits[:]:
        if not spirit.update():
            spirits.remove(spirit)
        spirit.draw(screen)
        if reaper.rect.colliderect(spirit.rect):
            reaper.stunned = True
            pygame.time.delay(5000)  
            reaper.stunned = False

    for gravestone in gravestones[:]:
        if not gravestone.update():
            gravestones.remove(gravestone)
        gravestone.draw(screen)
        if reaper.rect.colliderect(gravestone.rect):
            reaper.jump()

    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Skulls: {reaper.score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.update()
    clock.tick(30)

pygame.quit()
