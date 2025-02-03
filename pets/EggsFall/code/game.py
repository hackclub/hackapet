import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
import pygame
import time
import random

WIDTH = 128
HEIGHT = 128
EGG_TIME = 15
EGG_SPAWN = 30
DIGIT_SPACE = 16
SPEED_UP_EVERY = 10
SPEED_MULT = 0.9

FARMER_POSES = ["idle", "pos_1", "pos_2", "pos_3", "pos_4", "idle_sad"]

SPLASH_CREDITS = "assets/gui/credits_splash.bmp"
SPLASH_TUTORIAL = "assets/gui/tutorial_splash.bmp"
PRESS_START_BITMAP = "assets/gui/press_start.bmp"
PAUSE_BITMAP = "assets/gui/pause.bmp"
EGGSFALL_BITMAP = "assets/gui/eggsfall.bmp"
BACKGROUND_BITMAP = "assets/bg.bmp"
FARMER_ASSET = "assets/farmer/farmer_{}.bmp"
EGG_ASSET = "assets/egg/{}/egg_pos_{}.bmp"
DIGIT_ASSET = "assets/digits/{}.bmp"


class Sprite:
    def __init__(self, image_path, screen):
        self.screen = screen
        self.image_path = image_path
        self.img = self._load_image(image_path)
        self.screen.append(self.img)

    def _load_image(self, image_path):
        bitmap = displayio.OnDiskBitmap(image_path)
        return displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader)

    def update(self, image_path):
        self.remove()
        self.image_path = image_path
        self.img = self._load_image(image_path)
        self.screen.append(self.img)

    def remove(self):
        if self.img in self.screen:
            self.screen.remove(self.img)


class Farmer(Sprite):
    def __init__(self, screen):
        super().__init__(FARMER_ASSET.format("idle"), screen)
        self.sprite = "idle"

    def change_sprite(self, name):
        super().update(FARMER_ASSET.format(name))
        self.sprite = name

    def get_pos(self):
        if self.sprite == "pos_1":
            return 1
        elif self.sprite == "pos_2":
            return 2
        elif self.sprite == "pos_3":
            return 3
        elif self.sprite == "pos_4":
            return 4
        return None


class Egg(Sprite):
    def __init__(self, pos, screen):
        self.pos = pos
        self.frame = 1
        self.timer = 0
        super().__init__(EGG_ASSET.format(pos, self.frame), screen)

    def update(self, egg_time):
        self.timer += 1
        if self.timer % egg_time == 0:
            self.frame += 1
            if self.frame > 5:
                return False
            super().update(EGG_ASSET.format(self.pos, self.frame))
        return True


class Game:
    def __init__(self):
        pygame.init()
        self.display = PyGameDisplay(width=WIDTH, height=HEIGHT)
        self.screen = displayio.Group()
        self.display.show(self.screen)
        self._load_background()
        self.farmer = Farmer(self.screen)
        self.eggs = []
        self.digits = []
        self.egg_count = 0
        self.egg_timer = 0
        self.egg_time = EGG_TIME
        self.egg_spawn = EGG_SPAWN
        self.last_count = -1
        self.game_over = False
        self.paused = False
        self.pause_sprite = None

    def _load_background(self):
        bg_bitmap = displayio.OnDiskBitmap(BACKGROUND_BITMAP)
        bg_img = displayio.TileGrid(bg_bitmap, pixel_shader=bg_bitmap.pixel_shader)
        self.screen.append(bg_img)

    def show_splash(self, image_path, duration=2):
        splash = Sprite(image_path, self.screen)
        time.sleep(duration)
        splash.remove()

    def show_main_menu(self):
        logo = Sprite(EGGSFALL_BITMAP, self.screen)
        prompt = Sprite(PRESS_START_BITMAP, self.screen)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                    logo.remove()
                    prompt.remove()
                    return

    def spawn_egg(self):
        pos = random.randint(1, 4)
        for egg in self.eggs:
            if egg.pos == pos:
                return
        self.eggs.append(Egg(pos, self.screen))

    def update_eggs(self):
        for egg in self.eggs[:]:
            if not egg.update(self.egg_time):
                egg.remove()
                self.eggs.remove(egg)
                if self.farmer.get_pos() == egg.pos:
                    self.egg_count += 1
                    self.speed_up()
                else:
                    self.trigger_game_over()
                    return

    def speed_up(self):
        if self.egg_count % SPEED_UP_EVERY == 0:
            self.egg_time = max(5, int(self.egg_time * SPEED_MULT))
            self.egg_spawn = max(5, int(self.egg_spawn * SPEED_MULT))

    def show_number(self, num, x, y):
        if num == self.last_count:
            return
        self.clear_sprites(self.digits)
        num_str = f"{num:04d}"
        for i, char in enumerate(num_str):
            bitmap = displayio.OnDiskBitmap(DIGIT_ASSET.format(char))
            digit = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader)
            digit.x = x + i * DIGIT_SPACE
            digit.y = y
            self.digits.append(digit)
            self.screen.append(digit)
        self.last_count = num

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s and not self.game_over:
                    self.paused = not self.paused
                    if self.paused:
                        self.pause_sprite = Sprite(PAUSE_BITMAP, self.screen)
                    else:
                        if self.pause_sprite is not None:
                            self.pause_sprite.remove()
                            self.pause_sprite = None
                elif not self.paused and not self.game_over:
                    if event.key == pygame.K_a:
                        self.move_farmer("a")
                    elif event.key == pygame.K_d:
                        self.move_farmer("d")

    def move_farmer(self, direction):
        if direction == "a":
            if self.farmer.sprite == "idle":
                self.farmer.change_sprite("pos_1")
            elif self.farmer.sprite == "pos_1":
                self.farmer.change_sprite("pos_2")
            else:
                self.farmer.change_sprite("idle")
        elif direction == "d":
            if self.farmer.sprite == "idle":
                self.farmer.change_sprite("pos_3")
            elif self.farmer.sprite == "pos_3":
                self.farmer.change_sprite("pos_4")
            else:
                self.farmer.change_sprite("idle")

    def clear_sprites(self, sprite_list):
        for sprite in sprite_list:
            if hasattr(sprite, "remove"):
                sprite.remove()
            else:
                if sprite in self.screen:
                    self.screen.remove(sprite)
        sprite_list.clear()

    def reset_game(self):
        self.egg_count = 0
        self.egg_time = EGG_TIME
        self.egg_spawn = EGG_SPAWN
        self.egg_timer = 0
        self.game_over = False
        self.paused = False

        self.clear_sprites(self.eggs)
        self.clear_sprites(self.digits)
        self.last_count = -1

        if self.pause_sprite is not None:
            self.pause_sprite.remove()
            self.pause_sprite = None

        self.farmer.change_sprite("idle")
        self.show_number(self.egg_count, 5, 5)

    def trigger_game_over(self):
        self.game_over = True
        self.clear_sprites(self.eggs)
        self.clear_sprites(self.digits)
        if self.pause_sprite is not None:
            self.pause_sprite.remove()
            self.pause_sprite = None
        self.farmer.change_sprite("idle_sad")

    def run(self):
        self.show_splash(SPLASH_CREDITS, 2)
        self.show_splash(SPLASH_TUTORIAL, 3)
        while True:
            self.show_main_menu()
            self.reset_game()
            while not self.game_over:
                self.handle_input()
                if not self.paused:
                    self.egg_timer += 1
                    if self.egg_timer % self.egg_spawn == 0:
                        self.spawn_egg()
                    self.update_eggs()
                    self.show_number(self.egg_count, 5, 5)
                time.sleep(0.1)


if __name__ == "__main__":
    Game().run()
