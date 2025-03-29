class growthStage:
    def __init__(self, image, length):
        self.image = image
        self.length = length

class Potato:
    def __init__(self, maxWater, maxFood, maxBugs, maxHealth, growthStages):
        self.maxWater = maxWater
        self.maxFood = maxFood
        self.maxBugs = maxBugs
        self.maxHealth = maxHealth

        self.water = self.maxWater//4
        self.food = self.maxFood//4
        self.bugs = 0
        self.health = maxHealth

        self.growthStages = growthStages
        self.curentStage = 0
        self.stageProg = 0

        self.alive = True


