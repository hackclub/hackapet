import os
import json
import random

#FUTURE PLAN, NOT FULLY IMPLEMENTED AND NOT USED

timings = json.loads(os.environ["TIMINGS"])
screen_width = json.loads(os.environ["SCREEN_WIDTH"])

class Game:
	def __init__(self, pet, game_anim, game_sheet, playing_animation, playing_sheet, ko_anim, ko_sheet):
		self.pet = pet
		self.game_anim = game_anim
		self.game_sheet = game_sheet
		self.ko_anim = ko_anim
		self.ko_sheet = ko_sheet
		self.objects = []
		self.time = 0
		self.frame = 0
		self.ko = False
		pet.set_anim(playing_animation, playing_sheet, "playing")
	
	def run(self, time_dif, left, right):
		base_obj_speed = json.loads(os.environ["BASE_OBJ_SPEED"])
		self.time += time_dif
		self.frame += 1
		self.frame %= self.game_sheet.width // screen_width
		self.game_anim[0] = self.frame
		if left:
			self.pet.move(-self.pet.speed, 0)
		elif right:
			self.pet.move(self.pet.speed, 0)
		for obj in self.objects:
			obj.anim.x -= base_obj_speed * time_dif * self.time / 20
			if not (obj.anim.y + obj.anim.tile_height <= self.pet.anim.y
		   			or obj.anim.y >= self.pet.anim.y + self.pet.anim.tile_height
					or obj.anim.x + obj.main.tile_width <= self.pet.anim.x
					or obj.anim.x >= self.pet.anim.x + self.pet.anim.tile_width):
				obj.on_collide(self.pet, self)
			obj.anim.y -= base_obj_speed * self.time // 20
			obj.run_frame(time_dif)