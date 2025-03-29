from ..powerup_class import Powerup

#FUTURE PLAN, NOT FULLY IMPLEMENTED AND NOT USED

class HealthPowerup(Powerup):
    def __init__(self, anim, sheet, anim_name):
        super().__init__(anim, sheet, anim_name, "Health Buff")

    def start(self):
        self.pet.health += 1