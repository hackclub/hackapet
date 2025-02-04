from tones import Note, mappings
from clock import Stamp



class Track:

    time_values = {
            "O": 4,
            "o": 2,
            ".": 1,
            "'": -2,
            "*": -4
            }

    def __init__(self, notes, timings, lyrics = None, buttons = None):
        l = len(notes)
        assert(len(timings) == l)
        #assert(len(lyrics) == l)
        self.notes = notes

        self.lyrics = lyrics
        self.buttons = buttons
        self.timings = timings

        self.playing = False

        self.next_sub = 0
        self.next_beat = 0

        self.index = 0
        self.note = None

        self.note_hook = set()

    def parse_notes(self, clk):
        self.note_map = {}
        self.button_map = {}
        gran = clk.granularity

        next = 0

        button_type = None

        for idx, note in enumerate(self.notes):
            print(note)

            if note in "123":
                button_type = int(note) - 1
                continue

            #just a comment
            if note == ".":
                continue

            if button_type is not None:
                self.append_button(button_type, next, note)
                button_type = None

                note = ' '

            self.note_map[next] = note

            symbol = self.timings[idx]
            t = self.time_values[symbol]

            if (t < 0):
                div = abs(t)
                if (clk.granularity % div):
                    raise ValueError(f"Clock granularity can't support division by {div}")
                next += clk.granularity // div
            else:
                next += clk.granularity * t

        self.note_map[next] = " "   #stop playing

    # implement in challenge track
    def append_button(self, button_type, time, note):
        pass

    def add_hook(self, func):
        self.note_hook.add(func)

    def remove_hook(self, func):
        self.note_hook.remove(func)

    def begin(self, clk, boundary = 4):
        next_sub = 0
        next_beat = clk.beat + boundary - (clk.beat % boundary)
        self.index = 0
        self.playing = True

        self.time_zero = Stamp(clk.granularity, next_beat, next_sub)
        self.parse_notes(clk)

    def update(self, clk):
        if self.playing:
            rel = clk.since(self.time_zero)

            sub_beats = rel.get_sub_beats()
            if sub_beats in self.note_map:
                self.stop()
                if self.index >= len(self.timings):
                    self.stop()
                    self.playing = False
                    return
                self.play_note(self.note_map[sub_beats])


                self.index += 1

    def play_note(self, note, maxtime=0):
        if (note == " "):
            self.stop()
            #self.note = None
        elif (note == "~"):
            pass
        else:
            for func in self.note_hook:
                func()
            freq = mappings[note]
            self.note = Note(freq)
            self.note.play(-1, maxtime=maxtime)

    def stop(self):
        if self.note:
            self.note.stop()
        self.note = None


OK = 3

class ChallengeTrack(Track):
    def __init__(self, button_pool, player, text, width, window, early, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.challenge = []
        self.button_pool = button_pool
        self.text = text
        self.player = player

        self.buttons = [
            [],
            [],
            [],
        ]

        self.window = window    # time a note spends on screen
        self.early = early      # percentage of window time a note appears before being on queue
        self.width = width

    def begin(self, clk, boundary = 4):
        super().begin(clk, boundary)
        self.sbeat_window = self.window * clk.granularity

    def append_button(self, button_type, time, note):
        self.buttons[button_type].append((time, note))

    def update(self, clk):
        if self.playing:
            rel = clk.since(self.time_zero)

            sub_beats = rel.get_sub_beats()
            if sub_beats in self.note_map:
                self.stop()
                if self.index >= len(self.timings):
                    self.stop()
                    self.playing = False
                    self.button_pool.clear_all()
                    return
                self.play_note(self.note_map[sub_beats])


                self.index += 1


            start = sub_beats - int(self.sbeat_window * self.early)
            end = sub_beats + int(self.sbeat_window * (1 - self.early))

            if self.player.button is not None:
                buttons = self.buttons[self.player.button]
                for idx, button in enumerate(buttons):
                    time, note = button
                    if (sub_beats - OK) < time < (sub_beats + OK):
                        self.text.tile.text = "good"
                        self.play_note(note)
                        self.buttons[self.player.button][idx] = (-500, note)    #jank alert
                        break

                    else:
                        self.text.tile.text = ":("


                self.text.bounce()
                self.player.button = None


            for track in range(3):
                l = self.buttons[track]
                positions = []
                for button in l:
                    time, note = button
                    if start <= time <= end:
                        relative_progress = (time - start) / self.sbeat_window
                        progress = int((relative_progress) * self.width)
                        positions.append(progress)
                self.button_pool.set_lengths(positions, track)

                    

