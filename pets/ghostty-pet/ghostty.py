import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
from objects.number import Number
import pygame
import time
from objects.golden_numbers import Golden_Numbers
from objects.terminals import Terminals
from objects.sprite import Sprite
from objects.controls import Controls


pygame.init()
display = PyGameDisplay(width=128, height=128)
splash = displayio.Group()
display.show(splash)

background = displayio.OnDiskBitmap("art/hackapet_background.bmp")
bg_sprite = displayio.TileGrid(
	background, 
	pixel_shader=background.pixel_shader,
	default_tile=0,
	tile_width=128,
	tile_height=128
)

splash.append(bg_sprite)

controls = Controls(splash)
terminals = Terminals(splash)
ghostty = Sprite(splash, terminals, controls)
golden_numbers = Golden_Numbers(splash)
percentage = []
high_score = []
for i in range(1, 5):
	percentage.append(Number(splash, i))
	percentage[i-1].sprite.y += 19
	high_score.append(Number(splash, i))
	high_score[i-1].sprite.y += 35
	high_score[i-1].sprite.x -= 48

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			open("objects/good_prompt_score.txt", "w").write(str(ghostty.good_prompt_score))
			open("objects/high_score.txt", "w").write(str(terminals.high_score))
			pygame.quit()
			exit()
	ghostty.update()
	terminals.update()
	controls.update()
	golden_numbers.update(ghostty.good_prompt_score)
	bg_sprite[0] = terminals.num_bars + 2
	for i in percentage:
		i.update(terminals.percentage)
	
	for i in high_score:
		i.update(terminals.high_score)

	time.sleep(0.01)
