import random
from objects.prompt import Bad_Prompt, Good_Prompt
from objects.terminal import Terminal
from objects.number import Number


class Terminals:
    def __init__(self, splash):
        self.terminals = set()
        self.numbers = []
        self.frame = 0
        self.splash = splash
        self.just_emptied = False
        self.speed = 0.8
        self.previous_terminal = None
        self.score = 0
        self.high_score = int(open("objects/high_score.txt", "r").read())
        self.bad_prompts = set()
        self.good_prompts = set()
        self.previous_good_prompt = None
        self.previous_bad_prompt = None
        self.previous_previous_terminal = None
        self.percentage = 0
        self.num_bars = 0
        for i in range(1, 5):
            self.numbers.append(Number(splash, i))

    def update(self):
        to_remove = set()
        
        for terminal in self.terminals.copy():
            terminal.update()
            terminal.speed = self.speed
            if round(terminal.x) == (-32+8):
                self.score+=1
            if terminal.is_removed:
                to_remove.add(terminal)
        self.terminals -= to_remove

        if (self.score > self.high_score):
            self.high_score = self.score

        to_remove = set()
        
        for bad_prompt in self.bad_prompts.copy():
            bad_prompt.update()
            bad_prompt.speed = self.speed
            if bad_prompt.is_removed:
                to_remove.add(bad_prompt)
        self.bad_prompts -= to_remove

        for good_prompt in self.good_prompts.copy():
            good_prompt.update()
            good_prompt.speed = self.speed
            if good_prompt.is_removed:
                to_remove.add(good_prompt)
        self.good_prompts -= to_remove
        
        for number in self.numbers:
            number.update(self.score)

        if (self.frame % (32/self.speed)) == 0 and not self.just_emptied:
            if self.previous_terminal != None:
                if random.randint(1, 2) == 1:
                    if round(self.previous_terminal.x) == 96:
                        if self.previous_terminal.height == 1:
                            self.previous_previous_terminal = self.previous_terminal
                            self.previous_terminal = Terminal(self.splash, random.randint(1, 2))
                            self.terminals.add(self.previous_terminal)
                        else:
                            if self.previous_good_prompt != None and self.previous_previous_terminal != None:
                                if round(self.previous_good_prompt.x) == 96 and self.previous_good_prompt.height == 3 and self.previous_previous_terminal.height == 3:
                                    self.previous_previous_terminal = self.previous_terminal
                                    self.previous_terminal = Terminal(self.splash, random.randint(1, 2))
                                    self.terminals.add(self.previous_terminal)
                                else:
                                    self.previous_previous_terminal = self.previous_terminal
                                    self.previous_terminal = Terminal(self.splash, random.randint(2, 3))
                                    self.terminals.add(self.previous_terminal)
                            else:
                                self.previous_previous_terminal = self.previous_terminal
                                self.previous_terminal = Terminal(self.splash, random.randint(2, 3))
                                self.terminals.add(self.previous_terminal)
                    elif round(self.previous_terminal.x) < 64:
                        if self.previous_bad_prompt != None:
                            if round(self.previous_bad_prompt.x) != 96:
                                self.previous_terminal = Terminal(self.splash, 1)
                                self.terminals.add(self.previous_terminal)
                        else:
                            self.previous_terminal = Terminal(self.splash, 1)
                            self.terminals.add(self.previous_terminal)

                    if random.randint(1, 10) == 1:
                        if round(self.previous_terminal.x) < 64:
                            self.previous_good_prompt = Good_Prompt(self.splash, 1)
                            self.good_prompts.add(self.previous_good_prompt)
                        else:
                            self.previous_good_prompt = Good_Prompt(self.splash, self.previous_terminal.height + 1)
                            self.good_prompts.add(self.previous_good_prompt)
                elif round(self.previous_terminal.x) < 64 and random.randint(1, 4) == 1:
                    self.previous_bad_prompt = Bad_Prompt(self.splash, 1)
                    self.bad_prompts.add(self.previous_bad_prompt)
            else:
                self.previous_terminal = Terminal(self.splash, 1)
                self.terminals.add(self.previous_terminal)
        self.frame+=1

        if self.just_emptied and self.frame % 64 == 0:
            self.just_emptied = False
            self.frame = 0
        self.percentage = round((self.score/self.high_score)*100)
        if self.num_bars < 20:
            self.num_bars = self.percentage // 5
    def empty(self):
        for terminal in self.terminals.copy():
            terminal.remove()
        
        for bad_prompt in self.bad_prompts.copy():
            bad_prompt.remove()

        for good_prompt in self.good_prompts.copy():
            good_prompt.remove()

        self.just_emptied = True
        self.frame = 0
        self.previous_terminal = None
        self.terminals = set()
        self.bad_prompts = set()
        self.good_prompts = set()
        if self.score > self.high_score:
            self.high_score = self.score
            f = open("objects/high_score.txt", "w")
            f.write(str(self.high_score))
        self.score = 0
        self.percentage = 0
        self.num_bars = 0
