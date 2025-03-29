import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
import pygame, sys
import time
import random

pygame.init()

scale = 1
display_width = 128 * scale
display_height = 128 * scale
display = PyGameDisplay(width=display_width, height=display_height)
splash = displayio.Group(scale=scale)
display.show(splash)

outback_background = displayio.OnDiskBitmap("outback-background.bmp")

bg_sprite = displayio.TileGrid(
	outback_background,
	pixel_shader=outback_background.pixel_shader
)

tile_width = 32
tile_height = 32

splash.append(bg_sprite)

dragon_sheet_idle = displayio.OnDiskBitmap("jax-idle.bmp")

dragon_sprite_idle = displayio.TileGrid(
	dragon_sheet_idle,
	pixel_shader=dragon_sheet_idle.pixel_shader,
	width=1,
	height=1,
	tile_width = tile_width,
	tile_height = tile_height,
	default_tile=0,
	x=(display.width - tile_width) // 2,
	y=display.height - tile_height - 40
)

splash.append(dragon_sprite_idle)


dragon_sheet_walk = displayio.OnDiskBitmap("jax-walk.bmp")

dragon_sprite_walk = displayio.TileGrid(
	dragon_sheet_walk,
	pixel_shader=dragon_sheet_walk.pixel_shader,
	width=1,
	height=1,
	tile_width = tile_width,
	tile_height = tile_height,
	default_tile=0,
	x=(display.width - tile_width) // 2,
	y=display.height - tile_height - 40
)

splash.append(dragon_sprite_walk)


dragon_sheet_idle_sad = displayio.OnDiskBitmap("jax-idle-sad.bmp")

dragon_sprite_idle_sad = displayio.TileGrid(
	dragon_sheet_idle_sad,
	pixel_shader=dragon_sheet_idle_sad.pixel_shader,
	width=1,
	height=1,
	tile_width = tile_width,
	tile_height = tile_height,
	default_tile=0,
	x=(display.width - tile_width) // 2,
	y=display.height - tile_height - 40
)

splash.append(dragon_sprite_idle_sad)


dragon_sheet_walk_sad = displayio.OnDiskBitmap("jax-walk-sad.bmp")

dragon_sprite_walk_sad = displayio.TileGrid(
	dragon_sheet_idle_sad,
	pixel_shader=dragon_sheet_walk_sad.pixel_shader,
	width=1,
	height=1,
	tile_width = tile_width,
	tile_height = tile_height,
	default_tile=0,
	x=(display.width - tile_width) // 2,
	y=display.height - tile_height - 40
)

splash.append(dragon_sprite_walk_sad)


waterdrop_bitmap = displayio.OnDiskBitmap("water-droplet.bmp")

waterdrops = []

def spawn_waterdrop():
    x_position = random.randint(0, display.width - waterdrop_bitmap.width)
    waterdrop = displayio.TileGrid(
        waterdrop_bitmap,
        pixel_shader=waterdrop_bitmap.pixel_shader,
        width=1,
        height=1,
        tile_width=waterdrop_bitmap.width,
        tile_height=waterdrop_bitmap.height,
        x=x_position,
        y=-32
    )
    waterdrops.append(waterdrop)
    splash.append(waterdrop)

def check_collision(sprite1, sprite2):
    return (
        sprite1.x < sprite2.x + 14 and
        sprite1.x + 32 > sprite2.x and
        sprite1.y < sprite2.y + 14 and
        sprite1.y + 32 > sprite2.y
    )

class HealthBar():
	def __init__(self, x, y, w, h, max_hp):
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.max_hp = max_hp
		self.hp = max_hp

		self.group = displayio.Group()

		self.bg_bitmap = displayio.Bitmap(w, h, 1)
		self.bg_palette = displayio.Palette(1)
		self.bg_palette[0] = 0xFF0000 # Red

		self.bg_tile = displayio.TileGrid(self.bg_bitmap, pixel_shader=self.bg_palette, x=x, y=y)
		self.group.append(self.bg_tile)

		self.fg_bitmap = displayio.Bitmap(w, h, 1)
		self.fg_palette = displayio.Palette(1)
		self.fg_palette[0] = 0x00FF00  # Green

		self.fg_tile = displayio.TileGrid(self.fg_bitmap, pixel_shader=self.fg_palette, x=self.x, y=self.y)
		self.group.append(self.fg_tile)

		self.update(self.hp)

	def update(self, new_hp):
		self.hp = max(0, min(new_hp, self.max_hp))
		ratio = self.hp / self.max_hp
		new_width = max(1, int(self.w * ratio))

		for x in range(self.w):
			for y in range(self.h):
				if x < new_width:
					self.fg_bitmap[x, y] = 0
				else:
					self.fg_bitmap[x, y] = 1


health_bar = HealthBar(0, 120, 128, 5, 100)
HEALTH_DECAY_RATE = 1

splash.append(health_bar.group)


death = displayio.OnDiskBitmap("restart.bmp")

death_hi = displayio.TileGrid(
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


start = displayio.OnDiskBitmap("start.bmp")

start_screen = displayio.TileGrid(
	start,
	pixel_shader=start.pixel_shader,
	width=1,
	height=1,
	tile_width=128,
	tile_height=128,
	default_tile=0,
	x=0,  
	y=0
)

splash.append(start_screen)


frame = 0
speed = 4
game_over = False
game_started = False

while True:


	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()


	if health_bar.hp > 0 and game_started == True:
		if death_hi in splash:
			splash.remove(death_hi)
		health_bar.update(health_bar.hp - HEALTH_DECAY_RATE)
		display.refresh()
		for waterdrop in waterdrops:
			waterdrop.y += 5
			if waterdrop.y > (display.height - 30):
				splash.remove(waterdrop)
				waterdrops.remove(waterdrop)
			elif check_collision(dragon_sprite_idle, waterdrop):
				health_bar.update(health_bar.hp + 20)
				splash.remove(waterdrop)
				waterdrops.remove(waterdrop)
	elif health_bar.hp <= 0:
		for i in waterdrops:
			splash.remove(i)
		waterdrops.clear()
		game_over = True
		if game_over == True:
			splash.append(death_hi)


	keys = pygame.key.get_pressed()

	if game_started == False:
		if keys[pygame.K_RIGHT] and keys[pygame.K_LEFT]:
			game_started = True
			splash.remove(start_screen)
		if keys[pygame.K_SPACE]:
			pygame.quit()
			exit()

	if (game_over == False) and (game_started == True):
		if keys[pygame.K_LEFT]:
			dragon_sprite_idle.x -= speed
			dragon_sprite_walk.x -= speed
			dragon_sprite_idle_sad.x -= speed
			dragon_sprite_walk_sad.x -= speed
			if health_bar.hp > 40:
				dragon_sprite_idle.hidden = True
				dragon_sprite_walk.hidden = False
				dragon_sprite_idle_sad.hidden = True
				dragon_sprite_walk_sad.hidden = True
			if health_bar.hp <= 40:
				dragon_sprite_idle.hidden = True
				dragon_sprite_walk.hidden = True
				dragon_sprite_idle_sad.hidden = True
				dragon_sprite_walk_sad.hidden = False
		if keys[pygame.K_RIGHT]:
			dragon_sprite_idle.x += speed
			dragon_sprite_walk.x += speed
			dragon_sprite_idle_sad.x += speed
			dragon_sprite_walk_sad.x += speed
			if health_bar.hp > 40:
				dragon_sprite_idle.hidden = True
				dragon_sprite_walk.hidden = False
				dragon_sprite_idle_sad.hidden = True
				dragon_sprite_walk_sad.hidden = True
			if health_bar.hp <= 40:
				dragon_sprite_idle.hidden = True
				dragon_sprite_walk.hidden = True
				dragon_sprite_idle_sad.hidden = True
				dragon_sprite_walk_sad.hidden = False
		elif (not keys[pygame.K_LEFT]) and (not keys[pygame.K_RIGHT]):
			if health_bar.hp > 40:
				dragon_sprite_walk.hidden = True
				dragon_sprite_idle.hidden = False
				dragon_sprite_walk_sad.hidden = True
				dragon_sprite_idle_sad.hidden = True
			if health_bar.hp <= 40:
				dragon_sprite_walk.hidden = True
				dragon_sprite_idle.hidden = True
				dragon_sprite_walk_sad.hidden = True
				dragon_sprite_idle_sad.hidden = False
	if (game_over == False) and (game_started == True):
		if random.random() < 0.05:
			spawn_waterdrop()
		if keys[pygame.K_SPACE]:
			pygame.quit()
			exit()
	elif game_over == True:
		if keys[pygame.K_SPACE]:
			pygame.quit()
			exit()
		if keys[pygame.K_RIGHT] and keys[pygame.K_LEFT]:
			health_bar.hp = 100
			game_over = False
			splash.remove(death_hi)


	dragon_sprite_walk_sad[0] = frame
	dragon_sprite_idle_sad[0] = frame
	dragon_sprite_walk[0] = frame
	dragon_sprite_idle[0] = frame
	frame = (frame + 1) % (dragon_sheet_idle.width // tile_width)

	time.sleep(0.15)

