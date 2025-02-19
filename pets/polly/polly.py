import time
import random
import displayio

from blinka_displayio_pygamedisplay import PyGameDisplay
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import label

import pygame
from pygame.mixer import pre_init

from music import Track, ChallengeTrack
from tones import Note, mappings
from clock import Clock
from utils import ButtonPool

from updateables import *

pre_init(44100, -16, 1, 1024)
pygame.init()

SCALE = 3
BPM = 120
GRANULARITY = 12

POLLYX = 15
POLLYY = 30

PROFFRAMES = 7
PLAYERFRAMES = 6

PROFX = 90
PROFY = 60

BAR_WIDTH = 128
WARNING = 1 - 0.875

PLAYERX = 16

PLAYERY = 80

class Player:
    def __init__(self, bar : Animateable):
        self.bar = bar
        self.button = None

    def update(self, dt):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_z:
                    self.button = 0
                    self.bar.set_animation(index = 0, playing = True)

                if event.key == pygame.K_x:
                    self.button = 1
                    self.bar.set_animation(index = 1, playing = True)

                if event.key == pygame.K_c:
                    self.button = 2
                    self.bar.set_animation(index = 2, playing = True)

font = bitmap_font.load_font("assets/fonts/5x7.bdf")

display = PyGameDisplay(width=128 * SCALE, height=128 * SCALE)

root = displayio.Group(scale = SCALE)

note_group = displayio.Group(y = PLAYERY)

display.show(root)

background_image = displayio.OnDiskBitmap("assets/background.png")
background_sprite = displayio.TileGrid(background_image,
                                  pixel_shader = background_image.pixel_shader)

polly_image = displayio.OnDiskBitmap("assets/polly_front.bmp")
polly_sprite = displayio.TileGrid(polly_image,
                                  pixel_shader = polly_image.pixel_shader,
                                  x = POLLYX,
                                  y = POLLYY)

professor_image = displayio.OnDiskBitmap("assets/boy_spritesheet.png")
professor_sprite = displayio.TileGrid(professor_image,
                                      pixel_shader = professor_image.pixel_shader,
                                      tile_width = 32,
                                      tile_height = 64,
                                      width = 1,
                                      height = 1,
                                      x = PROFX,
                                      y = PROFY)

red_button = displayio.OnDiskBitmap("assets/red_button.png")
blue_button = displayio.OnDiskBitmap("assets/blue_button.png")
purple_button = displayio.OnDiskBitmap("assets/purple_button.png")
buttons = ButtonPool(root_group = note_group, red = red_button,
                     purple = purple_button,
                     blue = blue_button)



def get_bar(path):
    image = displayio.OnDiskBitmap(path)
    sprite = displayio.TileGrid(image,
                                pixel_shader = image.pixel_shader,
                                tile_width = 6,
                                tile_height = 28,
                                width = 1,
                                height = 11,
                                x = PLAYERX,
                                y = 0)
    return sprite
red = get_bar("assets/red.png")
purple = get_bar("assets/purple.png")
blue = get_bar("assets/blue.png")


root.append(background_sprite)
root.append(professor_sprite)
root.append(polly_sprite)

text = label.Label(font, text = ">")
text.x = 15
text.y = 20

root.append(text)

root.append(note_group)

note_group.append(red)
note_group.append(purple)
note_group.append(blue)

polly = Updateable(polly_sprite)
#prof = Updateable(professor_sprite)
prof = Professor(root, [professor_sprite], [[0.01, 0.01, 0.02, 0.02, 0.03, 0.03, 0.03]])
bar = Animateable(note_group, [red, purple, blue], [[0.01 for _ in range(PLAYERFRAMES)] for _ in range(3)])
t = Updateable(text)

player = Player(bar)

def test(clk):
    t.bounce()
    #bar.play_animation()
    
clock = Clock(BPM, GRANULARITY)
#track = Track(notes = "ee eeeec", timings = "''''''''")
#track = Track(notes = "edcdeeedddegg", timings = "......o..o...")

#track = Track(notes   = "e3eeddbbd 3edbded" * 1, 
#              timings = ". ''...... ''''''" * 1)

track = ChallengeTrack(button_pool = buttons,
                       player = player,
                       text = t,
                        width = BAR_WIDTH,
                        window = 8,
                        early = WARNING,
                        notes   = "edcdeeedddegg3e2d1c2d3e3e3e2d2d2d3e2g1g " * 1, 
                        timings = "......o..o... . . . . . . o . . o . . o." * 1)

track.add_hook(prof.bounce)
track.begin(clock)

clock.sub_beat_listeners.append(track.update)



while True:

    clock.tick()

    polly.update(dt = clock.dt)
    prof.update(dt = clock.dt)
    t.update(dt = clock.dt)
    bar.update(dt = clock.dt)
    player.update(dt = clock.dt)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()


    clock.tock() #this could be merged with tick actually

