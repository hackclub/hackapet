import os
import json

#FUTURE PLAN, NOT FULLY IMPLEMENTED AND NOT USED

timings = json.loads(os.environ["TIMINGS"])

class Obj:
	def __init__(self, anim, sheet, anim_name, type):
		self.anim = anim
		self.sheet = sheet
		self.anim_name = anim_name
		self.type = type
		self.time = 0
		self.frame = 0
	
	def reset_anim(self):
		self.anim[0] = 0
        
	def run_frame(self, time_dif):
		self.time += time_dif
		if self.time >= timings:
			frame = (self.frame + 1) % (self.sheet.width // self.anim.tile_width)
			self.time = 0
			self.anim[0] = frame
	
	def move(self, x, y):
		self.anim.x += x
		self.anim.y += y
	
	def move_to(self, x, y):
		self.anim.x = x
		self.anim.y = y
	
	def on_collide(self, pet, game):
		game.splash.remove(self.anim)
		game.objects.remove(self)

	def update_speed(self, value):
		self.speed = value