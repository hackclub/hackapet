import random
import time

import displayio
import pygame
from blinka_displayio_pygamedisplay import PyGameDisplay
import math

pygame.init()

display = PyGameDisplay(width=128, height=128)
splash = displayio.Group()
display.show(splash)
background_bitmap = displayio.OnDiskBitmap("./assets/Background.bmp")
bg_frame = random.randint(0, 2)
bg_sprite = displayio.TileGrid(
    background_bitmap,
    pixel_shader=background_bitmap.pixel_shader,
    width=1,
    height=1,
    tile_width=128,
    tile_height=128,
    default_tile= bg_frame,
    x=0,
    y=0
    )
splash.append(bg_sprite)


bg_time = 15*1000
pygame.time.set_timer(pygame.USEREVENT, bg_time)
def change_bg():
    bg_sprite[0] = bg_frame
    return (bg_frame+1) % (background_bitmap.width // tile_width)

start_bitmap = displayio.OnDiskBitmap("./assets/Start.bmp")
start_sprite = displayio.TileGrid(start_bitmap, pixel_shader=start_bitmap.pixel_shader)
splash.append(start_sprite)

tile_bitmap = displayio.OnDiskBitmap("./assets/Dance Tiles.bmp")
tile_sprite = displayio.TileGrid(tile_bitmap, pixel_shader=tile_bitmap.pixel_shader)
tile_sprite.y = 25


fire_bitmap = displayio.OnDiskBitmap("./assets/Fire.bmp")

hurt_bitmap = displayio.OnDiskBitmap("./assets/Hurt.bmp")
hurt_sprite = displayio.TileGrid(hurt_bitmap, pixel_shader=hurt_bitmap.pixel_shader)


try_again_bitmap = displayio.OnDiskBitmap("./assets/Try Again.bmp")
try_again_sprite = displayio.TileGrid(try_again_bitmap, pixel_shader=try_again_bitmap.pixel_shader)
try_again_sprite.y = 25

duck_sheet = displayio.OnDiskBitmap("./assets/Duck Sprites.bmp")

tile_width = 128
tile_height = 128
duck_frame = 0
duck_sprite = displayio.TileGrid(
    duck_sheet,
    pixel_shader=duck_sheet.pixel_shader,
    width=1,
    height=1,
    tile_width=tile_width,
    tile_height=tile_height,
    default_tile=0,
    x=0,
    y=25
)

arrows = [] #Things that are needed for game setup
hearts = []
fires = []

game_over = False
score = 0


class Heart:
    tile_width = 32
    tile_height = 32
    heart_sheet = displayio.OnDiskBitmap("./assets/Heart.bmp")
    def __init__(self, index):
        self.sprite = displayio.TileGrid(
    Heart.heart_sheet,
    pixel_shader=Heart.heart_sheet.pixel_shader,
    width=1,
    height=1,
    tile_width=Heart.tile_width,
    tile_height=Heart.tile_height,
    default_tile=0,
    x=16+32*index,#To spread out the hearts
    y=-4
    )
        splash.append(self.sprite)
        self.frame = 1
        self.alive = True
    def lose(self):
        self.alive = False
        self.sprite[0] = self.frame
        self.frame =  (self.frame+1) % (Heart.heart_sheet.width // Heart.tile_width)

class Arrow:
    bitmap = displayio.OnDiskBitmap("./assets/Arrow.bmp")
    def __init__(self):

        self.sprite = displayio.TileGrid(
            Arrow.bitmap,
            pixel_shader=Arrow.bitmap.pixel_shader
        )
        self.sprite.y = 26
        splash.append(self.sprite)
        self.frame = 0
        self.orientation = random.randint(1, 3)
        # 1 is left, 2 is top, 3 is right
        if self.orientation ==1:
            self.sprite.x = -64
        elif self.orientation == 2:
            self.sprite.transpose_xy = True
            self.sprite.y = -64
        elif self.orientation == 3:
            self.sprite.flip_x = True
            self.sprite.x = 64

    def move(self):
        speed = 3
        if self.orientation ==1:
            self.sprite.x+=speed
        elif self.orientation ==2:
            self.sprite.y+=speed
        elif self.orientation ==3:
            self.sprite.x-=speed


def changeSprite(duck_frame, new_frame):
    duck_sprite[0] = duck_frame
    return (new_frame)%(duck_sheet.width//tile_width)

def spawn_arrows():
    if random.random() < 0.075:  # spawn rate
        arrows.append(Arrow())


def arrow_collision(arrow_sprite):
    x_offset = 8
    y_offset = 16
    return (
        duck_sprite.x < arrow_sprite.x + x_offset and
        duck_sprite.x + x_offset > arrow_sprite.x and
        duck_sprite.y < arrow_sprite.y + y_offset and
        duck_sprite.y + y_offset > arrow_sprite.y
)

def arrow_dance(arrow_sprite):
    x_offset = 45
    y_offset = 45 #Higher number increases hitbox
    return (
        tile_sprite.x < arrow_sprite.x + x_offset and
        tile_sprite.x + x_offset > arrow_sprite.x and
        tile_sprite.y < arrow_sprite.y + y_offset and
        tile_sprite.y + y_offset > arrow_sprite.y)
        #return (arrow_sprite.x + x_offset-tile_sprite.x, arrow_sprite.y + y_offset-tile_sprite.y)

def display_game_over():
    for f in fires:
        splash.remove(f)
    fires.clear()
    for a in arrows:
        splash.remove(a.sprite)
    arrows.clear()
    for h in hearts:
        splash.remove(h.sprite)
    hearts.clear()

def remove_arrow(a):
    splash.remove(a.sprite)
    arrows.remove(a)

def reach_score(score, interval):
    if score>interval:
        x = random.randint(15, 95)
        y = random.randint(8, 70)
        fire_sprite = displayio.TileGrid(fire_bitmap, pixel_shader=fire_bitmap.pixel_shader)
        fire_sprite.x = x
        fire_sprite.y = y
        fires.append(fire_sprite)
        splash.insert(1, fire_sprite)
        return 0
    return score

def create_hearts():
    for i in range(3):
        hearts.append(Heart(i))

def lose_heart():
    for h in hearts[:-1]:
        if h.alive:
            h.lose()
            return False
    return True

def startGame():
    create_hearts()

start_screen = True
while start_screen: #Displays start screen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            start_screen = False
            break
        elif event.type ==pygame.USEREVENT:
            bg_frame = change_bg()
    time.sleep(0.1)

splash.remove(start_sprite)
splash.append(duck_sprite) #Sets up the game stuff
splash.append(tile_sprite)
startGame()


while True:
    left = False
    mid = False
    right = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                duck_frame = changeSprite(duck_frame, 3)
                left = True
            if keys[pygame.K_UP]or keys[pygame.K_DOWN]:
                duck_frame = changeSprite(duck_frame, 1)
                mid = True
            if keys[pygame.K_RIGHT]:
                duck_frame = changeSprite(duck_frame, 2)
                right = True
        elif event.type == pygame.KEYUP:
            duck_frame = changeSprite(duck_frame, 0)
        elif event.type ==pygame.USEREVENT:
            bg_frame = change_bg()
        elif event.type == pygame.USEREVENT+1:
            splash.remove(hurt_sprite)
            pygame.time.set_timer(pygame.USEREVENT + 1, 0)

    if game_over:
        if left or right or mid:
            game_over = False
            splash.remove(try_again_sprite)
            startGame()
    else:
        spawn_arrows()
        score = reach_score(score, 5)
    for a in arrows:
        a.move()
        if arrow_collision(a.sprite):
            remove_arrow(a)
            splash.append(hurt_sprite)
            pygame.time.set_timer(pygame.USEREVENT+1, 300)
            if lose_heart():
                display_game_over()
                game_over = True
                score = 0
                splash.append(try_again_sprite)
            break
        if left and a.orientation == 1 and arrow_dance(a.sprite):
            remove_arrow(a)
            score+=1
        elif mid and a.orientation == 2 and arrow_dance(a.sprite):
            remove_arrow(a)
            score += 1
        elif right and a.orientation == 3 and arrow_dance(a.sprite):
            remove_arrow(a)
            score += 1

    time.sleep(0.1)