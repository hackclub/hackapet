from ..powerup_class import Powerup
from random import randint

#FUTURE PLAN, NOT FULLY IMPLEMENTED AND NOT USED

class SpeedPowerup(Powerup):
    def __init__(self, anim, sheet, anim_name):
        super().__init__(anim, sheet, anim_name, "Speed Buff")
        self.value = randint(2, 4)

    def start(self):
        self.pet.speed += self.value

    def stop(self):
        self.pet.speed -= self.value
        super().stop()