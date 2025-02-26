import time
import pygame
import displayio

from blinka_displayio_pygamedisplay import PyGameDisplay
from adafruit_display_text import label 

pygame.init()

display = PyGameDisplay(width=128, height=128)
splash = displayio.Group()
display.show(splash)

backgrnd = displayio.OnDiskBitmap("background.bmp")
bg_sprite1 = displayio.TileGrid(backgrnd, pixel_shader=backgrnd.pixel_shader)
bg_sprite2 = displayio.TileGrid(backgrnd, pixel_shader=backgrnd.pixel_shader)
bg_sprite2.x = 128

splash.append(bg_sprite1)
splash.append(bg_sprite2)

backgrndsun = displayio.OnDiskBitmap("sun.bmp")
sun_sprite1 = displayio.TileGrid(backgrndsun, pixel_shader=backgrndsun.pixel_shader)

splash.append(sun_sprite1)

catcus = displayio.OnDiskBitmap("obstacle_sprite.bmp")
cactus_sprite1 = displayio.TileGrid(catcus, pixel_shader=catcus.pixel_shader)
cactus_sprite1.x = 160
cactus_sprite1.y = 80

splash.append(cactus_sprite1)

dino = displayio.OnDiskBitmap("player_spritedino.bmp")
dino_sprite = displayio.TileGrid(dino, pixel_shader=dino.pixel_shader, tile_width=32, tile_height=32, default_tile=0)
dino_sprite.x = 5
dino_sprite.y = 80

splash.append(dino_sprite)

speed = 5
jumpspeed = 0

isgameover = False

death = displayio.OnDiskBitmap("game_over.bmp")

def display_game_over():
    global deathrip
    global isgameover 
    isgameover = True
    deathrip = displayio.TileGrid(
        death,
        pixel_shader=death.pixel_shader,
        width=1,
        height=1,
        tile_width=128,
        tile_height=128,
        default_tile=0,
        x=0,  
        y=0
    )
    splash.append(deathrip)

while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      exit()
  jumppreessed = False
  keys = pygame.key.get_pressed()
  if keys[pygame.K_SPACE]:
    jumppreessed = True

  if isgameover:
    if jumppreessed:
      isgameover = False
      splash.remove(deathrip)
    continue
  
  bg_sprite1.x -= speed
  bg_sprite2.x -= speed
  cactus_sprite1.x -= speed

  if bg_sprite1.x <= -128:
    bg_sprite1.x += 256
  
  if bg_sprite2.x <= -128:
    bg_sprite2.x += 256

  if cactus_sprite1.x <= -35:
    cactus_sprite1.x += 256
  

  if not dino_sprite.y < 80:
    if jumppreessed:
        jumpspeed = 10
    dino_sprite[0] = (dino_sprite[0] + 1) %3

  if cactus_sprite1.x < 20 and cactus_sprite1.x + cactus_sprite1.tile_width > 10 and dino_sprite.y > 55:
    display_game_over()

  dino_sprite.y -= jumpspeed
  jumpspeed -= 1
  
  # dont fall through the ground pls
  if dino_sprite.y > 80:
    dino_sprite.y = 80
    jumpspeed = 0
  
  display.refresh()
  time.sleep(0.05)