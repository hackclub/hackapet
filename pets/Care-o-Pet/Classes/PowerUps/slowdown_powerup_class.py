from random import randint
import os
import json
from ..powerup_class import Powerup

#FUTURE PLAN, NOT FULLY IMPLEMENTED AND NOT USED

class SlowdownPowerup(Powerup):
    def __init__(self, anim, sheet, anim_name):
        super().__init__(self, anim, sheet, anim_name)
        self.value = randint(5, 8) / 10

    def start(self):
        os.environ["BASE_OBJ_SPEED"] = json.dumps(json.loads(os.environ["BASE_OBJ_SPEED"]) + self.value)

    def stop(self):
        os.environ["BASE_OBJ_SPEED"] = json.dumps(json.loads(os.environ["BASE_OBJ_SPEED"]) - self.value)
        super().stop()