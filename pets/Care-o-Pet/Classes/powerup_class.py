from obj_class import Obj
from random import randint


class Powerup(Obj):
    def __init__(self, anim, sheet, anim_name, name):
        super().__init__(anim, sheet, anim_name, "Powerup")
        self.name = name
        self.pet = None
        self.duration = randint(15, 20)

    def on_collide(self, pet, game):
        pet.add_powerup(self)
        self.pet = pet
        super().on_collide(pet, game)

    def start(self):
        pass

    def stop(self):
        del self

    def run(self, time_dif):
        self.duration -= time_dif
        if self.duration <= 0:
            self.pet.rem_powerup(self)