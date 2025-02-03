import os
import sys
import random
import pygame
import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
import adafruit_imageload
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import label

pygame.init()

def safe_remove(layer, group):
    if layer in group:
        group.remove(layer)

def safe_insert(index, layer, group):
    if layer in group:
        group.remove(layer)
    group.insert(index, layer)

def safe_append(layer, group):
    if layer not in group:
        group.append(layer)

SCREEN_WIDTH = 128
SCREEN_HEIGHT = 128
FPS = 60
WHITE = 0xFFFFFF
COLOR_KEY = 0xF600FF

START = "start"
PLAYING = "playing"
current_state = START

score = 0
high_score = 0
HIGH_SCORE_FILE = "high_score.txt"

bird_speed = 1.0
speed_increase_interval = 10000
last_speed_increase = pygame.time.get_ticks()
speed_increment = 0.1
max_bird_speed = 5.0

background_switch_time = 5000
last_background_switch = pygame.time.get_ticks()
current_background_index = 2

display = PyGameDisplay(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
main_group = displayio.Group()
display.show(main_group)
display.auto_refresh = False

clock = pygame.time.Clock()
start_ticks = 0

def load_high_score():
    if os.path.exists(HIGH_SCORE_FILE):
        with open(HIGH_SCORE_FILE, "r") as f:
            try:
                return int(f.read())
            except:
                return 0
    return 0

def save_high_score(s):
    with open(HIGH_SCORE_FILE, "w") as f:
        f.write(str(s))

high_score = load_high_score()

font = bitmap_font.load_font("fonts/5x8.bdf")

def load_bmp_raw(path):
    bitmap, palette = adafruit_imageload.load(
        path, bitmap=displayio.Bitmap, palette=displayio.Palette
    )
    for i in range(len(palette)):
        if palette[i] == COLOR_KEY:
            palette.make_transparent(i)
    return bitmap, palette

def make_tilegrid(bitmap, palette, x=0, y=0, scale=1):
    tg = displayio.TileGrid(bitmap, pixel_shader=palette, x=x, y=y)
    tg.scale = scale
    return tg


bg_start_bmp,   bg_start_pal   = load_bmp_raw("assets/backgrounds/start_ground.bmp")
bg_no_text_bmp, bg_no_text_pal = load_bmp_raw("assets/backgrounds/start_no_text.bmp")
bg_sky1_bmp,    bg_sky1_pal    = load_bmp_raw("assets/backgrounds/sky1.bmp")
bg_sky2_bmp,    bg_sky2_pal    = load_bmp_raw("assets/backgrounds/sky2.bmp")
bg_sky3_bmp,    bg_sky3_pal    = load_bmp_raw("assets/backgrounds/sky3.bmp")

bg_start   = make_tilegrid(bg_start_bmp,   bg_start_pal)
bg_no_text = make_tilegrid(bg_no_text_bmp, bg_no_text_pal)
bg_sky1    = make_tilegrid(bg_sky1_bmp,    bg_sky1_pal)
bg_sky2    = make_tilegrid(bg_sky2_bmp,    bg_sky2_pal)
bg_sky3    = make_tilegrid(bg_sky3_bmp,    bg_sky3_pal)

backgrounds = [bg_start, bg_no_text, bg_sky1, bg_sky2, bg_sky3]

cat_no_balloons_bmp, cat_no_balloons_pal = load_bmp_raw("assets/cat/cat_no_balloons.bmp")
cat_3_balloons_bmp, cat_3_balloons_pal   = load_bmp_raw("assets/cat/cat_3_balloons.bmp")
cat_3_balloons_pop_bmp, cat_3_balloons_pop_pal = load_bmp_raw("assets/cat/cat_3_balloons_pop.bmp")
cat_2_balloons_bmp, cat_2_balloons_pal   = load_bmp_raw("assets/cat/cat_2_balloons.bmp")
cat_2_balloons_pop_bmp, cat_2_balloons_pop_pal = load_bmp_raw("assets/cat/cat_2_balloons_pop.bmp")
cat_1_balloon_bmp, cat_1_balloon_pal     = load_bmp_raw("assets/cat/cat_1_balloon.bmp")
cat_1_balloon_pop_bmp, cat_1_balloon_pop_pal = load_bmp_raw("assets/cat/cat_1_balloon_pop.bmp")

cat_frames = {
    "no_balloons":      make_tilegrid(cat_no_balloons_bmp, cat_no_balloons_pal),
    "3_balloons":       make_tilegrid(cat_3_balloons_bmp, cat_3_balloons_pal),
    "3_balloons_pop":   make_tilegrid(cat_3_balloons_pop_bmp, cat_3_balloons_pop_pal),
    "2_balloons":       make_tilegrid(cat_2_balloons_bmp, cat_2_balloons_pal),
    "2_balloons_pop":   make_tilegrid(cat_2_balloons_pop_bmp, cat_2_balloons_pop_pal),
    "1_balloon":        make_tilegrid(cat_1_balloon_bmp, cat_1_balloon_pal),
    "1_balloon_pop":    make_tilegrid(cat_1_balloon_pop_bmp, cat_1_balloon_pop_pal),
}

bird1_bmp, bird1_pal = load_bmp_raw("assets/birds/bird1.bmp")
bird2_bmp, bird2_pal = load_bmp_raw("assets/birds/bird2.bmp")
bird_frame_data = [
    (bird1_bmp, bird1_pal),
    (bird2_bmp, bird2_pal)
]
class Cat:
    def __init__(self, x, y):
        self.balloon_count = 3
        self.current_frame_key = "3_balloons"
        self.tilegrid = cat_frames[self.current_frame_key]
        self.x = x
        self.y = y
        self.speed_x = 5
        self.popping = False
        self.pop_duration = 250
        self.pop_start_time = 0

        safe_append(self.tilegrid, main_group)
        self.tilegrid.x = self.x
        self.tilegrid.y = self.y

    def set_frame(self, key):
        if self.current_frame_key == key:
            return
        safe_remove(self.tilegrid, main_group)
        self.current_frame_key = key
        self.tilegrid = cat_frames[key]
        safe_append(self.tilegrid, main_group)
        self.tilegrid.x = self.x
        self.tilegrid.y = self.y

    def lose_balloon(self):
        if self.balloon_count > 0 and not self.popping:
            self.popping = True
            self.pop_start_time = pygame.time.get_ticks()
            self.balloon_count -= 1
            if self.balloon_count == 2:
                self.set_frame("3_balloons_pop")
            elif self.balloon_count == 1:
                self.set_frame("2_balloons_pop")
            else:
                self.set_frame("1_balloon_pop")

    def update(self):
        if self.popping:
            now = pygame.time.get_ticks()
            if now - self.pop_start_time >= self.pop_duration:
                self.popping = False
                if self.balloon_count == 3:
                    self.set_frame("3_balloons")
                elif self.balloon_count == 2:
                    self.set_frame("2_balloons")
                elif self.balloon_count == 1:
                    self.set_frame("1_balloon")
                else:
                    self.set_frame("no_balloons")

    def move_left(self):
        self.x = max(0, self.x - self.speed_x)
        self.tilegrid.x = self.x

    def move_right(self):
        right_edge = SCREEN_WIDTH - 32
        self.x = min(right_edge, self.x + self.speed_x)
        self.tilegrid.x = self.x

    def get_rect(self):
        return pygame.Rect(self.x, self.y, 32, 32)

class Bird:
    def __init__(self, x, y, speed_y):
        self.frames = []
        for (bmp, pal) in bird_frame_data:
            tg = displayio.TileGrid(bmp, pixel_shader=pal, x=int(x), y=int(y))
            self.frames.append(tg)

        self.current_index = 0
        self.x = x
        self.y = y
        self.speed_y = speed_y
        self.animation_time = 300
        self.last_update = pygame.time.get_ticks()

        self.tilegrid = self.frames[self.current_index]
        safe_append(self.tilegrid, main_group)

    def update(self):
        self.y += self.speed_y
        self.tilegrid.y = int(self.y)

        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_time:
            safe_remove(self.tilegrid, main_group)
            self.current_index = (self.current_index + 1) % len(self.frames)
            self.tilegrid = self.frames[self.current_index]
            safe_append(self.tilegrid, main_group)
            self.tilegrid.x = int(self.x)
            self.tilegrid.y = int(self.y)
            self.last_update = now

    def off_screen(self):
        return self.y > SCREEN_HEIGHT

    def remove_from_group(self):
        for f in self.frames:
            safe_remove(f, main_group)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, 18, 18)

cat_sprite = None
birds = []
def spawn_bird():
    if len(birds) < 10:
        x = random.randint(0, SCREEN_WIDTH - 18)
        y = -random.randint(40, 100)
        b = Bird(x, y, bird_speed)
        birds.append(b)
def init_start_screen():
    global info_label, hs_label
    info_label = label.Label(font, text="Press SPACE to Start", color=WHITE, x=20, y=100)
    hs_label   = label.Label(font, text=f"High Score: {high_score}", color=WHITE, x=20, y=115)
    
    safe_insert(0, backgrounds[0], main_group)
    safe_append(info_label, main_group)
    safe_append(hs_label, main_group)

def cleanup_start_screen():
    global info_label, hs_label
    safe_remove(backgrounds[0], main_group)
    safe_remove(info_label, main_group)
    safe_remove(hs_label, main_group)
    info_label = None
    hs_label   = None
def init_playing_state():
    global cat_sprite, score, start_ticks, last_background_switch
    global current_background_index, score_label

    score = 0
    start_ticks = pygame.time.get_ticks()
    last_background_switch = pygame.time.get_ticks()
    current_background_index = 4  

    for b in birds:
        b.remove_from_group()
    birds.clear()

    safe_remove(backgrounds[current_background_index], main_group)
    safe_insert(0, backgrounds[current_background_index], main_group)

    cat_x = SCREEN_WIDTH // 2 - 16
    cat_y = SCREEN_HEIGHT - 40
    cat_sprite = Cat(cat_x, cat_y)

    for _ in range(3):
        spawn_bird()

    score_label = label.Label(font, text="", color=WHITE, x=5, y=5)
    safe_append(score_label, main_group)

def cleanup_playing_state():
    global cat_sprite
    for bg in backgrounds[2:]:
        safe_remove(bg, main_group)

    if cat_sprite and cat_sprite.tilegrid in main_group:
        safe_remove(cat_sprite.tilegrid, main_group)
    cat_sprite = None

    for b in birds:
        b.remove_from_group()
    birds.clear()

    safe_remove(score_label, main_group)
def switch_background_if_needed():
    global current_background_index, last_background_switch
    now = pygame.time.get_ticks()
    if now - last_background_switch > background_switch_time:
        safe_remove(backgrounds[current_background_index], main_group)
        current_background_index = 4 if current_background_index == 2 else current_background_index - 1
        safe_insert(0, backgrounds[current_background_index], main_group)
        last_background_switch = now

init_start_screen()
current_state = START
running = True

while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if current_state == START:
                    cleanup_start_screen()
                    current_state = PLAYING
                    init_playing_state()
                elif current_state == PLAYING:
                    pass

    keys = pygame.key.get_pressed()
    now = pygame.time.get_ticks()

    if current_state == PLAYING and cat_sprite is not None:
        if keys[pygame.K_a]:
            cat_sprite.move_left()
        if keys[pygame.K_d]:
            cat_sprite.move_right()

        if now - last_speed_increase > speed_increase_interval:
            if bird_speed < max_bird_speed:
                bird_speed += speed_increment
            last_speed_increase = now

        if random.randint(1, 100) <= 2:
            spawn_bird()

        cat_sprite.update()

        for b in birds[:]:
            b.update()
            if b.off_screen():
                b.remove_from_group()
                birds.remove(b)

        cat_rect = cat_sprite.get_rect()
        for b in birds[:]:
            if cat_rect.colliderect(b.get_rect()):
                if not cat_sprite.popping:
                    cat_sprite.lose_balloon()
                b.remove_from_group()
                birds.remove(b)

        if cat_sprite.balloon_count == 0 and not cat_sprite.popping:
            if score > high_score:
                high_score = score
                save_high_score(high_score)

            cleanup_playing_state()
            cleanup_start_screen()
            current_state = START
            init_start_screen()

        switch_background_if_needed()

        score = (now - start_ticks) // 1000
        score_label.text = f"Score: {score}"

    display.refresh(minimum_frames_per_second=0)

pygame.quit()

