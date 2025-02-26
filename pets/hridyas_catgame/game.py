import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
import pygame
import time
import random

class PetGame:
    def __init__(self):
        pygame.init()
        self.display = PyGameDisplay(width=128, height=128)
        pygame.display.set_caption("Virtual Pet")
        
        self.screen = pygame.display.get_surface()
        
        self.main_group = displayio.Group()
        self.display.show(self.main_group)

        self.background_group = displayio.Group()
        self.pet_group = displayio.Group()
        self.candy_group = displayio.Group()
        self.ui_group = displayio.Group()
        self.status_bars_group = displayio.Group()
        
        self.main_group.append(self.background_group)
        self.main_group.append(self.pet_group)
        self.main_group.append(self.candy_group)
        self.main_group.append(self.status_bars_group)
        self.main_group.append(self.ui_group)

        self.stats = {
            "hunger": 100,
            "health": 100,
            "happiness": 100,
            "energy": 100
        }
        self.candy_count = 5
        self.state = "idle"
        self.is_sleeping = False
        self.last_stats_update = time.monotonic()
        self.stats_update_interval = 5.0
        self.candy_display_time = 2.0
        self.candies_visible = False
        self.candy_timestamp = 0

        self._create_background()
        self._load_pet_sprites()
        self._load_candy_sprites()
        self._create_ui()
        self._create_status_bars()
    
    def _create_background(self):
        bg_bitmap = displayio.Bitmap(128, 128, 1)
        bg_palette = displayio.Palette(1)
        bg_palette[0] = 0xADAFE5
        background = displayio.TileGrid(bg_bitmap, pixel_shader=bg_palette)
        self.background_group.append(background)
        floor_bitmap = displayio.Bitmap(128, 38, 1)
        floor_palette = displayio.Palette(1)
        floor_palette[0] = 0x6B4226
        floor = displayio.TileGrid(floor_bitmap, pixel_shader=floor_palette, y=90)
        self.background_group.append(floor)

    def _load_pet_sprites(self):
        try:
            self.pet_states = {
                "idle": displayio.OnDiskBitmap("cathappy.png"),
                "happy": displayio.OnDiskBitmap("cathappy.png"),
                "hungry": displayio.OnDiskBitmap("cathungry.png"),
                "sick": displayio.OnDiskBitmap("catsick.png"),
                "sleeping": displayio.OnDiskBitmap("cathappy.png"),
                "dead": displayio.OnDiskBitmap("catdead.png")
            }
            self.pet_sprite = displayio.TileGrid(
                self.pet_states["idle"],
                pixel_shader=self.pet_states["idle"].pixel_shader,
                x=48,
                y=48
            )
            self.pet_group.append(self.pet_sprite)
        except Exception as e:
            print(f"Error loading pet sprites: {e}")
            raise

    def _load_candy_sprites(self):
        try:
            self.candy_bitmap = displayio.OnDiskBitmap("candy.png")
        except Exception as e:
            print(f"Error loading candy sprites: {e}")
            raise

    def _create_status_bars(self):
        hunger_bg = displayio.Bitmap(50, 10, 1)
        hunger_bg_palette = displayio.Palette(1)
        hunger_bg_palette[0] = 0x666666
        self.hunger_bg = displayio.TileGrid(hunger_bg, pixel_shader=hunger_bg_palette, x=5, y=5)
        
        self.hunger_bar_bitmap = displayio.Bitmap(48, 8, 1)
        hunger_palette = displayio.Palette(1)
        hunger_palette[0] = 0x00FF00
        self.hunger_bar = displayio.TileGrid(self.hunger_bar_bitmap, 
                                        pixel_shader=hunger_palette, 
                                        x=6, y=6)
        
        self.status_bars_group.append(self.hunger_bg)
        self.status_bars_group.append(self.hunger_bar)
        
        self.update_status_bars()

    def _create_ui(self):
        try:
            self.ui_icons = {
                "FOOD": displayio.OnDiskBitmap("food_icon.png"),
                "MED": displayio.OnDiskBitmap("medicine_icon.png"),
                "SLEEP": displayio.OnDiskBitmap("sleep_icon.png"),
                "PLAY": displayio.OnDiskBitmap("play_icon.png")
            }
            
            self.buttons = {}
            positions = [(100, 10), (100, 36), (100, 62), (100, 88)]
            
            for pos, (label, icon) in zip(positions, self.ui_icons.items()):
                button = displayio.TileGrid(
                    icon,
                    pixel_shader=icon.pixel_shader,
                    x=pos[0],
                    y=pos[1]
                )
                self.ui_group.append(button)
                self.buttons[label] = pygame.Rect(pos[0], pos[1], 16, 16)
                
        except Exception as e:
            print(f"Error creating UI: {e}")
            raise

    def update_status_bars(self):
        bar_width = int((48 * self.stats["hunger"]) / 100)
        for x in range(48):
            for y in range(8):
                if x < bar_width:
                    self.hunger_bar_bitmap[x, y] = 0
                else:
                    self.hunger_bar_bitmap[x, y] = 1

    def show_candies(self):
        if not self.candies_visible and self.candy_count > 0:
            while len(self.candy_group) > 0:
                self.candy_group.pop()
            
            candy_positions = [
                (60, 40),
                (36, 62),
                (84, 62),
                (60, 84)
            ]
            
            for base_pos in candy_positions:
                offset_x = random.randint(-5, 5)
                offset_y = random.randint(-5, 5)
                candy = displayio.TileGrid(
                    self.candy_bitmap,
                    pixel_shader=self.candy_bitmap.pixel_shader,
                    x=base_pos[0] + offset_x,
                    y=base_pos[1] + offset_y
                )
                self.candy_group.append(candy)
            
            self.candies_visible = True
            self.candy_timestamp = time.monotonic()
            self.candy_count -= 1
            self.update_status_bars()

    def hide_candies(self):
        while len(self.candy_group) > 0:
            self.candy_group.pop()
        self.candies_visible = False

    def update_stats(self):
        current_time = time.monotonic()
        stats_updated = False
        
        if current_time - self.last_stats_update > self.stats_update_interval:
            if not self.is_sleeping:
                self.stats["hunger"] = max(0, self.stats["hunger"] - 2)
                self.stats["happiness"] = max(0, self.stats["happiness"] - 1)
                self.stats["energy"] = max(0, self.stats["energy"] - 2)
                
                if self.stats["hunger"] < 30:
                    self.stats["health"] = max(0, self.stats["health"] - 2)
                
                if self.stats["energy"] < 20:
                    self.stats["health"] = max(0, self.stats["health"] - 1)
            else:
                self.stats["energy"] = min(100, self.stats["energy"] + 4)
                if self.stats["energy"] >= 100:
                    self.is_sleeping = False
                    
            self.last_stats_update = current_time
            stats_updated = True

        if self.candies_visible and current_time - self.candy_timestamp > self.candy_display_time:
            self.hide_candies()
            
        if stats_updated:
            self.update_status_bars()

    def update_state(self):
        if self.stats["health"] <= 0:
            return "dead"
        elif self.is_sleeping:
            return "sleeping"
        elif self.stats["hunger"] < 30:
            return "hungry"
        elif self.stats["health"] < 50:
            return "sick"
        elif self.stats["happiness"] < 30:
            return "hungry"
        elif self.stats["happiness"] > 80:
            return "happy"
        return "idle"

    def handle_input(self, pos):
        if self.state == "dead":
            return
            
        x, y = pos
        for label, rect in self.buttons.items():
            if rect.collidepoint(x, y):
                self.activate_button(label)

    def activate_button(self, label):
        if self.state == "dead":
            return
        if label == "FOOD" and not self.is_sleeping and self.candy_count > 0:
            self.stats["hunger"] = min(100, self.stats["hunger"] + 30)
            self.show_candies()
            self.update_status_bars()
        elif label == "MED" and not self.is_sleeping:
            self.stats["health"] = min(100, self.stats["health"] + 20)
        elif label == "PLAY" and not self.is_sleeping:
            self.stats["happiness"] = min(100, self.stats["happiness"] + 25)
            self.stats["energy"] = max(0, self.stats["energy"] - 10)
        elif label == "SLEEP":
            self.is_sleeping = not self.is_sleeping

    def run(self):
        clock = pygame.time.Clock()
        running = True
        self.display.refresh()
        pygame.display.flip()
        
        while running:
            time.sleep(0.1)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_input(event.pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.activate_button("FOOD")
                    elif event.key == pygame.K_2:
                        self.activate_button("MED")
                    elif event.key == pygame.K_3:
                        self.activate_button("SLEEP")
                    elif event.key == pygame.K_4:
                        self.activate_button("PLAY")

            self.update_stats()
            new_state = self.update_state()
            
            if new_state != self.state:
                self.state = new_state
                self.pet_group.pop()
                new_pet = displayio.TileGrid(
                    self.pet_states[self.state],
                    pixel_shader=self.pet_states[self.state].pixel_shader,
                    x=48,
                    y=62
                )
                self.pet_group.append(new_pet)
            
            self.display.refresh()
            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    game = PetGame()
    game.run()