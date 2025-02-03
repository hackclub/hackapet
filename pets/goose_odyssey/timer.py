class Timer:
    def __init__(self, ticks, function):
        self.ticks = ticks
        self.function = function
        self.ticksPassed = 0

    def update(self):
        self.ticksPassed += 1

        if self.ticksPassed >= self.ticks:
            self.function()

        return self.ticksPassed >= self.ticks

timers = []

def update():
    for timer in timers:
        finished = timer.update()
        
        if finished:
            timers.remove(timer)


def createAndStartTimer(ticks, function):
    timers.append(Timer(ticks, function))