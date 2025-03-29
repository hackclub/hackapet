###############PLEASE READ THIS###############
#My email is Pinguthong911@gmail.com, my Discord is @Emptip303#9017
#For some reason, my invitation link to the stack is expired and I can't email or message anyone about this
#If you read this, please reach out and contact me please
#Thank you


import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
import pygame
import time
import random

pygame.init()
screen = PyGameDisplay(width=128, height=128)
splash = displayio.Group()
screen	.show(splash)
#######################IMPORT IMAGE##############
background = displayio.OnDiskBitmap("graphics/background.bmp")
bg_sprite = displayio.TileGrid(background, pixel_shader = background.pixel_shader, x = 0, y = 0)

dif_button = displayio.OnDiskBitmap("graphics/dif button.bmp")
dif_sprite = displayio.TileGrid(dif_button, pixel_shader = dif_button.pixel_shader, width = 1, height = 1, tile_width = 40, tile_height = 20, x = 128//2 - 40//2, y = 128//2 - 55)

main_cat = displayio.OnDiskBitmap("graphics/main cat.bmp")
mc_sprite = displayio.TileGrid(main_cat, pixel_shader = main_cat.pixel_shader, x = 10, y = 80)
oppo_cat = displayio.OnDiskBitmap("graphics/oppo cat.bmp")
opc_sprite = displayio.TileGrid(oppo_cat, pixel_shader = oppo_cat.pixel_shader, width = 1, height = 1, tile_width = 32, tile_height = 32, x = 128//2 - 32//2, y = 128//2 - 32)

arrow_button = displayio.OnDiskBitmap("graphics/left arrow.bmp")
left_sprite = displayio.TileGrid(arrow_button, pixel_shader = arrow_button.pixel_shader, x = 20, y = 128//2-20)
right_sprite = displayio.TileGrid(arrow_button, pixel_shader = arrow_button.pixel_shader, x = 128-20, y = 128//2-20)
right_sprite.flip_x = True
play_button = displayio.OnDiskBitmap("graphics/play button.bmp")
pb_sprite = displayio.TileGrid(play_button, pixel_shader = play_button.pixel_shader, x = 128//2-20, y = 128-50)
help_button = displayio.OnDiskBitmap("graphics/help button.bmp")
hb_sprite = displayio.TileGrid(help_button, pixel_shader = help_button.pixel_shader, x = 128//2-20, y = 128-25)
choose_button = displayio.OnDiskBitmap("graphics/choose button.bmp")
cb_sprite = displayio.TileGrid(choose_button, pixel_shader = choose_button.pixel_shader, x = 128//2-20, y = 128-50)
move_bar = displayio.OnDiskBitmap("graphics/move bar.bmp")
move_bar_sprite = displayio.TileGrid(move_bar, pixel_shader = move_bar.pixel_shader, width = 1, height = 1, tile_width = 128, tile_height = 16, x = 0, y = 128-16)

heart = displayio.OnDiskBitmap("graphics/heart.bmp")
player_heart_sprite = displayio.TileGrid(heart, pixel_shader = heart.pixel_shader, width = 1, height = 1, tile_width = 128, tile_height = 128)
oppo_heart_sprite = displayio.TileGrid(heart, pixel_shader = heart.pixel_shader, width = 1, height = 1, tile_width = 128, tile_height = 128)
oppo_heart_sprite.flip_x = True
bullet = displayio.OnDiskBitmap("graphics/bullet.bmp")
player_bullet_sprite = displayio.TileGrid(bullet, pixel_shader = bullet.pixel_shader, width = 1, height = 1, tile_width = 16, tile_height = 16, x = 0, y = 30)
oppo_bullet_sprite = displayio.TileGrid(bullet, pixel_shader = bullet.pixel_shader, width = 1, height = 1, tile_width = 16, tile_height = 16, x = 112, y = 30)
restrict_text = displayio.OnDiskBitmap("graphics/restrict text.bmp")
restrict_sprite = displayio.TileGrid(restrict_text, pixel_shader = restrict_text.pixel_shader, width = 1, height = 1, tile_width = 46, tile_height = 5, x = (128//2 - 46//2), y = 128-16-11)

reload_effect = displayio.OnDiskBitmap("graphics/reload.bmp")
player_reload_sprite = displayio.TileGrid(reload_effect, pixel_shader = reload_effect.pixel_shader, x = 40, y = 83 )
oppo_reload_sprite = displayio.TileGrid(reload_effect, pixel_shader = reload_effect.pixel_shader, x = 80, y = 83 )
shield_effect = displayio.OnDiskBitmap("graphics/shield.bmp")
player_shield_sprite = displayio.TileGrid(shield_effect, pixel_shader = shield_effect.pixel_shader, x = 10, y = 80)
oppo_shield_sprite = displayio.TileGrid(shield_effect, pixel_shader = shield_effect.pixel_shader, x = 83, y = 80)
gun = displayio.OnDiskBitmap("graphics/gun.bmp")
player_gun_sprite = displayio.TileGrid(gun, pixel_shader = gun.pixel_shader, width = 1, height = 1, tile_width = 16, tile_height = 16, x = 30, y = 90)
oppo_gun_sprite = displayio.TileGrid(gun,pixel_shader = gun.pixel_shader, width = 1, height = 1, tile_width = 16, tile_height = 16, x = 85, y = 90)
oppo_gun_sprite.flip_x = True
shot_effect = displayio.OnDiskBitmap("graphics/shot.bmp")
player_shot_sprite = displayio.TileGrid(shot_effect, pixel_shader = shot_effect.pixel_shader, x = 10, y = 80)
oppo_shot_sprite = displayio.TileGrid(shot_effect, pixel_shader = shot_effect.pixel_shader, x = 86, y = 80)
oppo_shot_sprite.flip_x = True
shootvshield_effect = displayio.OnDiskBitmap("graphics/shootvshield.bmp")
shootvshield_sprite = displayio.TileGrid(shootvshield_effect, pixel_shader = shootvshield_effect.pixel_shader, x = 128//2-32//2, y = 128-16-11-15-4)
shootvshoot_effect = displayio.OnDiskBitmap("graphics/shootvshoot.bmp")
shootvshoot_sprite = displayio.TileGrid(shootvshoot_effect, pixel_shader = shootvshoot_effect.pixel_shader, x = 128//2-32//2, y = 128-16-11-15-4)

help_screen = displayio.OnDiskBitmap("graphics/help screen.bmp")
help_screen_sprite = displayio.TileGrid(help_screen,pixel_shader = help_screen.pixel_shader, width = 1, height = 1, tile_width = 128, tile_height = 128, x = 0, y = 0)

end_screen = displayio.OnDiskBitmap("graphics/end screen.bmp")
end_screen_sprite = displayio.TileGrid(end_screen,pixel_shader = end_screen.pixel_shader, width = 1, height = 1, tile_width = 128, tile_height = 128, x = 0, y = 0)
#######################
splash.append(bg_sprite)
splash.append(pb_sprite)
splash.append(hb_sprite)
splash.append(cb_sprite)
splash.append(left_sprite)
splash.append(right_sprite)
splash.append(opc_sprite)
splash.append(dif_sprite)
splash.append(player_heart_sprite)
splash.append(oppo_heart_sprite)
splash.append(mc_sprite)
splash.append(move_bar_sprite)
splash.append(player_gun_sprite)
splash.append(oppo_gun_sprite)
splash.append(player_bullet_sprite)
splash.append(oppo_bullet_sprite)
splash.append(restrict_sprite)
splash.append(player_reload_sprite)
splash.append(oppo_reload_sprite)
splash.append(player_shield_sprite)
splash.append(oppo_shield_sprite)
splash.append(player_shot_sprite)
splash.append(oppo_shot_sprite)
splash.append(shootvshoot_sprite)
splash.append(shootvshield_sprite)
splash.append(end_screen_sprite)
splash.append(help_screen_sprite)
left_sprite.hidden = True
right_sprite.hidden = True
opc_sprite.hidden = True
dif_sprite.hidden = True
player_heart_sprite.hidden = True
oppo_heart_sprite.hidden = True
mc_sprite.hidden = True
move_bar_sprite.hidden = True
player_gun_sprite.hidden = True
oppo_gun_sprite.hidden = True
player_bullet_sprite.hidden = True
oppo_bullet_sprite.hidden = True
restrict_sprite.hidden = True
player_reload_sprite.hidden = True
oppo_reload_sprite.hidden = True
player_shield_sprite.hidden = True
oppo_shield_sprite.hidden = True
player_shot_sprite.hidden = True
oppo_shot_sprite.hidden = True
shootvshoot_sprite.hidden = True
shootvshield_sprite.hidden = True
end_screen_sprite.hidden = True
help_screen_sprite.hidden = True

keepRunning = True
while keepRunning:
	menuLoop = True
	player_choose_at_menu = 0
	cb_sprite.y = (128-50 if player_choose_at_menu == 0 else 128-25)
	pb_sprite.hidden = False
	hb_sprite.hidden = False
	cb_sprite.hidden = False
	while keepRunning and menuLoop:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				keepRunning = False
				menuLoop = False
			if event.type == pygame.KEYDOWN:
				keypress = pygame.key.name(event.key)
				if keypress == "escape":
					keepRunning = False
					menuLoop = False
				if keypress == "left" or keypress == "right":
					player_choose_at_menu = (0 if player_choose_at_menu == 1 else 1)
					cb_sprite.y = (128-50 if player_choose_at_menu == 0 else 128-25)
				if keypress == "up":
					menuLoop = False
	pb_sprite.hidden = True
	hb_sprite.hidden = True
	cb_sprite.hidden = True
	if player_choose_at_menu == 0: #Play
		while bg_sprite.y > -60 and keepRunning:
			bg_sprite.y -= 1
			time.sleep(0.01)
		difficultyLoop = True
		opc_sprite.x = 128//2 - 32//2
		opc_sprite.y = 128//2 - 32
		player_choose_at_dif = 0
		left_sprite.hidden = False
		right_sprite.hidden = False
		opc_sprite.hidden = False
		opc_sprite[0] = player_choose_at_dif
		dif_sprite.hidden = False
		dif_sprite[0] = player_choose_at_dif
		while difficultyLoop and keepRunning:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					keepRunning = False
					difficultyLoop = False
				if event.type == pygame.KEYDOWN:
					keypress = pygame.key.name(event.key)
					if keypress == "escape":
						keepRunning = False
						difficultyLoop = False
					if keypress == "left":
						player_choose_at_dif = (2 if player_choose_at_dif == 0 else (player_choose_at_dif - 1))
						opc_sprite[0] = player_choose_at_dif
						dif_sprite[0] = player_choose_at_dif
					if keypress == "right":
						player_choose_at_dif = (0 if player_choose_at_dif == 2 else (player_choose_at_dif + 1))
						opc_sprite[0] = player_choose_at_dif
						dif_sprite[0] = player_choose_at_dif
					if keypress == "up":
						difficultyLoop = False
		opc_sprite.x = 86 ###
		opc_sprite.y = 80
		opc_sprite.hidden = True
		dif_sprite.hidden = True
		left_sprite.hidden = True
		right_sprite.hidden	= True
		gameLoop = True
		while bg_sprite.y > -72 and keepRunning:
			bg_sprite.y -= 1
			time.sleep(0.025)
		player_heart_sprite.hidden = False
		oppo_heart_sprite.hidden = False
		mc_sprite.hidden = False
		opc_sprite.hidden = False
		opc_sprite[0] = player_choose_at_dif
		opc_sprite.flip_x = True
		move_bar_sprite.hidden = False
		player_gun_sprite.hidden = False
		oppo_gun_sprite.hidden = False
		player_bullet_sprite.hidden = False
		oppo_bullet_sprite.hidden = False
		player_heart_sprite[0] = 0
		oppo_heart_sprite[0] = 0
		player_bullet_sprite[0] = 0
		oppo_bullet_sprite[0] = 0
		restrict_sprite[0] = 0
		player_gun_sprite[0] = 0
		oppo_gun_sprite[0] = 0
		player_time_shield_consecutively = 0
		oppo_time_shield_consecutively = 0
		move_log = []
		while gameLoop and keepRunning and player_heart_sprite[0] < 3 and oppo_heart_sprite[0] < 3:
			player_choose_move = False
			move_bar_sprite[0] = 0
			while not bool(player_choose_move) and keepRunning and gameLoop: ##################################Player play
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						keepRunning = False
						gameLoop = False
						playerLoop = False
					if event.type == pygame.KEYDOWN:
						keypress = pygame.key.name(event.key)
						if keypress == "escape":
							keepRunning = False
							gameLoop = False
							playerLoop = False
						if keypress == "left": #reload
							if move_bar_sprite[0] == 1:
								if player_bullet_sprite[0] < 6:
									player_choose_move = "Reload"
								else:
									restrict_sprite[0] = 0
									restrict_sprite.hidden = False
									time_buffer	= 2
							else:
								move_bar_sprite[0] = 1
						elif keypress == "up": #shield
							if move_bar_sprite[0] == 2:
								if player_time_shield_consecutively < 3:
									player_choose_move = "Shield"
								else:
									restrict_sprite[0] = 1
									restrict_sprite.hidden = False
									time_buffer	= 2
							else:
								move_bar_sprite[0] = 2
						elif keypress == "right": #shoot
							if move_bar_sprite[0] == 3:
								if player_bullet_sprite[0] > 0:
									player_choose_move = "Shoot"
								else:
									restrict_sprite[0] = 2
									restrict_sprite.hidden = False
									time_buffer = 2
							else:
								move_bar_sprite[0] = 3
				if (restrict_sprite.hidden == False) and not bool(player_choose_move):
					time_buffer -= 0.01
					if time_buffer <= 0:
						restrict_sprite.hidden = True
				time.sleep(0.01)
			restrict_sprite.hidden = True
			move = ["Reload", "Shield", "Shoot"] #################################################################Oppo play
			if player_choose_at_dif == 0: ##Easy
				if (oppo_bullet_sprite[0] < 6) and (oppo_time_shield_consecutively < 3) and (oppo_bullet_sprite[0] != 0):
					oppo_choose_move = move[random.randint(0,2)]
				elif (oppo_bullet_sprite[0] < 6) and (oppo_time_shield_consecutively < 3):
					oppo_choose_move = move[random.randint(0,1)]
				elif (oppo_time_shield_consecutively < 3) and (oppo_bullet_sprite[0] != 0):
					oppo_choose_move = move[random.randint(1,2)]
				elif (oppo_bullet_sprite[0] < 6) and (oppo_bullet_sprite[0] != 0):
					oppo_choose_move = move[[0,2][random.randint(0,1)]]
				else:
					if (oppo_bullet_sprite[0] < 6):
						oppo_choose_move = move[0]
					elif (oppo_time_shield_consecutively < 3):
						oppo_choose_move = move[1]
					else:
						oppo_choose_move = move[2]
			elif player_choose_at_dif == 1: #Normal
				##Reload -> Shoot else (Reload)
				##Shield -> Reload
				##Shoot -> Shield
				move_log.append((0 if player_choose_move == "Reload" else (1 if player_choose_move == "Shield" else 2)))
				choose_log = [item for item in move_log]
				if len(choose_log) == 1:
					oppo_choose_move = "Reload"
				else:
					if not (oppo_bullet_sprite[0] < 6): #Full ammo
						while True:
							try:
								choose_log.remove(1)
							except:
								break
					if not (oppo_bullet_sprite[0] != 0): #No ammo
						while True:
							try:
								choose_log.remove(0)
							except:
								break
						choose_log.append(1) #To push ai to reload if there is no ammo
					if not (oppo_time_shield_consecutively < 3): #No shield
						while True:
							try:
								choose_log.remove(2)
							except:
								break
					if len(choose_log) == 0:
						oppo_choose_move = move[random.randint(0,1)]
					else:
						a = choose_log[random.randint(0, len(choose_log) - 1)]
						oppo_choose_move = move[(a-1) if a > 0 else 2]
			elif player_choose_at_dif == 2: #Hard
				move_log.append((0 if player_choose_move == "Reload" else (1 if player_choose_move == "Shield" else 2)))
				if len(move_log) == 1:
					oppo_choose_move = "Reload"
				else:
					if player_choose_move == "Reload": #Either reload or shoot
						if (oppo_bullet_sprite[0] < 6) and (oppo_bullet_sprite[0] != 0):
							a = random.randint(1,3)
							oppo_choose_move = move[0 if a == 1 else 2]
						elif (oppo_bullet_sprite[0] < 6):
							oppo_choose_move = move[0]
						else:
							oppo_choose_move = move[2]
					if player_choose_move == "Shield": #Either reload or shield
						if (oppo_time_shield_consecutively < 3) and (oppo_bullet_sprite[0] < 6):
							a = random.randint(1,3)
							oppo_choose_move = move[1 if a == 1 else 0]
						elif (oppo_bullet_sprite[0] < 6):
							oppo_choose_move = move[0]
						elif oppo_time_shield_consecutively < 3:
							oppo_choose_move = move[1]
						else:
							oppo_choose_move = move[2]
					if player_choose_move == "Shoot": #Either shield or shoot
						if (oppo_time_shield_consecutively < 3) and (oppo_bullet_sprite[0] != 0):
							a = random.randint(1,3)
							oppo_choose_move = move[2 if a == 1 else 1]
						elif (oppo_time_shield_consecutively < 3):
							oppo_choose_move = move[1]
						elif (oppo_bullet_sprite[0] != 0):
							oppo_choose_move = move[2]
						else:
							oppo_choose_move = move[0]
			###########Match decision
			if player_choose_move == "Reload":
				player_bullet_sprite[0] += 1
				player_time_shield_consecutively = 0
				player_reload_sprite.hidden = False
			elif player_choose_move == "Shield":
				player_time_shield_consecutively += 1
				player_shield_sprite.hidden = False
			else:
				player_bullet_sprite[0] -= 1
				player_time_shield_consecutively = 0
				player_gun_sprite[0] = 1

			if oppo_choose_move == "Reload":
				oppo_bullet_sprite[0] += 1
				oppo_time_shield_consecutively = 0
				oppo_reload_sprite.hidden = False
			elif oppo_choose_move == "Shield":
				oppo_time_shield_consecutively += 1
				oppo_shield_sprite.hidden = False
			else:
				oppo_bullet_sprite[0] -= 1
				oppo_time_shield_consecutively = 0
				oppo_gun_sprite[0] = 1

			if player_choose_move == "Reload" and oppo_choose_move == "Shoot":
				player_heart_sprite[0] += 1
				player_shot_sprite.hidden = False
			elif player_choose_move == "Shoot" and oppo_choose_move == "Reload":
				oppo_heart_sprite[0] += 1
				oppo_shot_sprite.hidden = False
			elif player_choose_move == "Shoot" and oppo_choose_move == "Shoot":
				shootvshoot_sprite.hidden = False
			elif player_choose_move == "Shoot" and oppo_choose_move == "Shield":
				shootvshield_sprite.flip_x = False
				shootvshield_sprite.hidden = False
			elif player_choose_move == "Shield" and oppo_choose_move == "Shoot":
				shootvshield_sprite.flip_x = True
				shootvshield_sprite.hidden = False
			time.sleep(1)
			player_reload_sprite.hidden = True
			player_shield_sprite.hidden = True
			player_gun_sprite[0] = 0
			oppo_reload_sprite.hidden = True
			oppo_shield_sprite.hidden = True
			oppo_gun_sprite[0] = 0
			player_shot_sprite.hidden = True
			oppo_shot_sprite.hidden = True
			shootvshoot_sprite.hidden = True
			shootvshield_sprite.hidden = True

		if player_heart_sprite[0] != 3:
			end_screen_sprite[0] = 0
			end_screen_sprite.hidden = False
		else:
			end_screen_sprite[0] = 1
			end_screen_sprite.hidden = False
		press_to_continue = True
		while press_to_continue and keepRunning:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					keepRunning = False
					press_to_continue = False
				if event.type == pygame.KEYDOWN:
					keypress = pygame.key.name(event.key)
					if keypress == "escape":
						keepRunning = False
						press_to_continue = False
					if keypress:
						press_to_continue = False

		player_heart_sprite.hidden = True
		oppo_heart_sprite.hidden = True
		mc_sprite.hidden = True
		opc_sprite.hidden = True
		move_bar_sprite.hidden = True
		player_gun_sprite.hidden = True
		oppo_gun_sprite.hidden = True
		player_bullet_sprite.hidden = True
		oppo_bullet_sprite.hidden = True
		end_screen_sprite.hidden = True
		while bg_sprite.y < 0 and keepRunning:
			bg_sprite.y += 1
			time.sleep(0.01)
	if player_choose_at_menu == 1: #Help
		helpLoop = True
		help_screen_sprite[0] = 0
		help_screen_sprite.hidden = False
		while helpLoop and keepRunning:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					keepRunning = False
					helpLoop = False
				if event.type == pygame.KEYDOWN:
					keypress = pygame.key.name(event.key)
					if keypress == "escape":
						keepRunning = False
						helpLoop = False
					if keypress == "left" and help_screen_sprite[0] > 0:
						help_screen_sprite[0] -= 1
					if keypress == "right" and help_screen_sprite[0] < 3:
						help_screen_sprite[0] += 1
					if keypress == "up":
						helpLoop = False
		help_screen_sprite.hidden = True
			
pygame.quit()
exit()
