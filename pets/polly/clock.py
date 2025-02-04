import time

class Stamp():
    def __init__(self, granularity, beat = 0, sub_beat = 0):
        self.beat = beat
        self.sub_beat = sub_beat
        self.granularity = granularity

    def get_sub_beats(self):
        return (self.beat * self.granularity) + self.sub_beat

    def __sub__(self, other):
        assert(self.granularity == other.granularity)
        assert(self.sub_beat < self.granularity)
        assert(other.sub_beat < self.granularity)

        beat_diff = self.beat - other.beat
        if (self.sub_beat < other.sub_beat):
            beat_diff -= 1
            sub_beat_diff = self.sub_beat + self.granularity - other.sub_beat
        else:
            sub_beat_diff = self.sub_beat  - other.sub_beat

        #negative time can be used for queing

        return Stamp(self.granularity, beat_diff, sub_beat_diff)
            



class Clock:
    """ Track time elapsed """
    def __init__(self, bpm, granularity):
        self.bpm = bpm                  # beats / minute
        self.granularity = granularity            # a beat is dividable into `granularity` sub-beats

        self.beat = 0
        self.sub_beat = 0

        self.spb = 60 / bpm             # seconds elapsed per beat
        self.spt = self.spb / granularity    # smallest unit of time elapsed per update

        self.sleep = min(self.spt / 2.0, 0.05)          # sleep this much per loop to reduce cpu load

        self.dt = 0                     # time passed between frames
        self.accum = 0                  # time passed before next tick

        self.start = time.monotonic()

        self.beat_listeners = []
        self.sub_beat_listeners = []

    def now(self):
        return Stamp(self.granularity, self.beat, self.sub_beat)

    def since(self, stamp):
        return self.now() - stamp


    def tick(self):
        self.start = time.monotonic()

        while (self.accum >= self.spt):
            self.accum -= self.spt

            for listener in self.sub_beat_listeners:
                listener(self)

            self.sub_beat += 1

            if (self.sub_beat >= self.granularity):
                self.sub_beat -= self.granularity
                for listener in self.beat_listeners:
                    listener(self)
                self.beat += 1



    def tock(self, stall = True):
        if stall:
            time.sleep(self.sleep)
        self.dt = time.monotonic() - self.start
        self.accum += self.dt

