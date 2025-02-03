import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
import pygame
import time

class PetGame:
    def __init__(self):
        self.display = PyGameDisplay(width=128, height=128)
        pygame.display.set_caption("Virtual Pet")
        
        self.main_group = displayio.Group()
        self.display.show(self.main_group)

        self.background_group = displayio.Group()
        self.pet_group = displayio.Group()
        self.ui_group = displayio.Group()
        self.main_group.append(self.background_group)
        self.main_group.append(self.pet_group)
        self.main_group.append(self.ui_group)

        self._create_background()
        self._load_pet_sprites()
        self._create_ui()

        self.stats = {
            "hunger": 100,
            "health": 100,
            "happiness": 100,
            "energy": 100
        }
        self.state = "idle"
        self.is_sleeping = False
        self.last_update = time.monotonic()
        
        pygame.font.init()
        self.font = pygame.font.Font(None, 12)
        self.screen = pygame.display.get_surface()
        self.overlay = pygame.Surface((128, 128), pygame.SRCALPHA)
        self.pre_render_stats()

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
                "idle": displayio.OnDiskBitmap("cathappy.bmp"),
                "happy": displayio.OnDiskBitmap("cathappy.bmp"),
                "hungry": displayio.OnDiskBitmap("cathungry.bmp"),
                "sick": displayio.OnDiskBitmap("catsick.bmp"),
                "sleeping": displayio.OnDiskBitmap("cathappy.bmp"),
                "dead": displayio.OnDiskBitmap("catdead.bmp")
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

    def _create_ui(self):
        try:
            self.ui_icons = {
                "FOOD": displayio.OnDiskBitmap("food_icon.bmp"),
                "MED": displayio.OnDiskBitmap("medicine_icon.bmp"),
                "SLEEP": displayio.OnDiskBitmap("sleep_icon.bmp"),
                "PLAY": displayio.OnDiskBitmap("play_icon.bmp")
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

    def pre_render_stats(self):
        self.overlay.fill((0, 0, 0, 0))
        
        pygame.draw.rect(self.overlay, (0, 0, 0, 150), (0, 0, 80, 65))
        
        stats_y = 5
        for stat, value in self.stats.items():
            text_surface = self.font.render(f"{stat[:4]}: {int(value)}", True, (255, 255, 255))
            self.overlay.blit(text_surface, (5, stats_y))
            stats_y += 15
            
        label_positions = [(100, 10), (100, 36), (100, 62), (100, 88)]
        for pos, label in zip(label_positions, ["FOOD", "MED", "SLEEP", "PLAY"]):
            pygame.draw.rect(self.overlay, (0, 0, 0, 150), (pos[0], pos[1], 30, 15))
            text_surface = self.font.render(label, True, (255, 255, 255))
            self.overlay.blit(text_surface, (pos[0] + 2, pos[1] + 2))

    def update_stats(self):
        current_time = time.monotonic()
        if current_time - self.last_update > 1:
            if not self.is_sleeping:
                self.stats["hunger"] = max(0, self.stats["hunger"] - 1)
                self.stats["happiness"] = max(0, self.stats["happiness"] - 0.5)
                self.stats["energy"] = max(0, self.stats["energy"] - 1)
                
                if self.stats["hunger"] < 30:
                    self.stats["health"] = max(0, self.stats["health"] - 1)
                
                if self.stats["energy"] < 20:
                    self.stats["health"] = max(0, self.stats["health"] - 0.5)
            else:
                self.stats["energy"] = min(100, self.stats["energy"] + 2)
                if self.stats["energy"] >= 100:
                    self.is_sleeping = False
                    
            self.last_update = current_time
            self.pre_render_stats()

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
                if label == "FOOD" and not self.is_sleeping:
                    self.stats["hunger"] = min(100, self.stats["hunger"] + 30)
                elif label == "MED" and not self.is_sleeping:
                    self.stats["health"] = min(100, self.stats["health"] + 20)
                elif label == "PLAY" and not self.is_sleeping:
                    self.stats["happiness"] = min(100, self.stats["happiness"] + 25)
                    self.stats["energy"] = max(0, self.stats["energy"] - 10)
                elif label == "SLEEP":
                    self.is_sleeping = not self.is_sleeping
                self.pre_render_stats()

    def run(self):
        clock = pygame.time.Clock()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_input(event.pos)

            self.update_stats()
            new_state = self.update_state()
            
            if new_state != self.state:
                self.state = new_state
                self.pet_group.pop()
                new_pet = displayio.TileGrid(
                    self.pet_states[self.state],
                    pixel_shader=self.pet_states[self.state].pixel_shader,
                    x=48,
                    y=48
                )
                self.pet_group.append(new_pet)

            self.display.refresh()
            
            self.screen.blit(self.overlay, (0, 0))
            
            pygame.display.flip()
            time.sleep(0.1)

        pygame.quit()

if __name__ == "__main__":
    game = PetGame()
    game.run()
