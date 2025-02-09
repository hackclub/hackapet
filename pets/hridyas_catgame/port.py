import time
import board
import displayio
import digitalio
from adafruit_display_text import label
import terminalio

display = board.DISPLAY

main_group = displayio.Group()
display.show(main_group)

class Buttons:
    def __init__(self):
        self.btn_a = digitalio.DigitalInOut(board.BUTTON_A)
        self.btn_a.switch_to_input(pull=digitalio.Pull.DOWN)
        self.btn_b = digitalio.DigitalInOut(board.BUTTON_B)
        self.btn_b.switch_to_input(pull=digitalio.Pull.DOWN)
        self.btn_c = digitalio.DigitalInOut(board.BUTTON_C)
        self.btn_c.switch_to_input(pull=digitalio.Pull.DOWN)
        
        self.last_press = time.monotonic()
        self.debounce = 0.3

    def check_press(self, button):
        if time.monotonic() - self.last_press > self.debounce:
            if button.value:
                self.last_press = time.monotonic()
                return True
        return False

buttons = Buttons()

class VirtualPet:
    def __init__(self):
        self.background_group = displayio.Group()
        self.pet_group = displayio.Group()
        self.ui_group = displayio.Group()
        
        main_group.append(self.background_group)
        main_group.append(self.pet_group)
        main_group.append(self.ui_group)
        
        self._create_background()
        self._load_pet_sprites()
        self._create_status_bar()

        self.stats = {
            "hunger": 100,
            "health": 100,
            "happiness": 100,
            "energy": 100
        }
        self.state = "idle"
        self.is_sleeping = False
        self.last_stats_update = time.monotonic()
        self.stats_update_interval = 5.0
        
        self.c_pressed = False
        self.c_press_start = 0
        self.long_press_duration = 1.0

    def _create_background(self):
        color_bitmap = displayio.Bitmap(display.width, display.height, 1)
        color_palette = displayio.Palette(1)
        color_palette[0] = 0xADAFE5
        bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette)
        self.background_group.append(bg_sprite)
        floor_bitmap = displayio.Bitmap(display.width, 30, 1)
        floor_palette = displayio.Palette(1)
        floor_palette[0] = 0x6B4226
        floor = displayio.TileGrid(floor_bitmap, pixel_shader=floor_palette, y=display.height-30)
        self.background_group.append(floor)

    def _load_pet_sprites(self):
        self.pet_states = {
            "idle": "cathappy.bmp",
            "happy": "cathappy.bmp",
            "hungry": "cathungry.bmp",
            "sick": "catsick.bmp",
            "sleeping": "cathungry.bmp",
            "dead": "catdead.bmp"
        }
        self.current_pet = displayio.OnDiskBitmap(self.pet_states["idle"])
        self.pet_sprite = displayio.TileGrid(
            self.current_pet,
            pixel_shader=self.current_pet.pixel_shader,
            x=display.width//2 - 16,
            y=display.height//2 - 16
        )
        self.pet_group.append(self.pet_sprite)

    def _create_status_bar(self):
        self.status_label = label.Label(
            font=terminalio.FONT,
            text="H:100 Hl:100 Ha:100 E:100",
            color=0xFFFFFF,
            x=4,
            y=display.height - 8
        )
        self.ui_group.append(self.status_label)

    def update_pet_sprite(self, state):
        self.pet_group.remove(self.pet_sprite)
        self.current_pet = displayio.OnDiskBitmap(self.pet_states[state])
        self.pet_sprite = displayio.TileGrid(
            self.current_pet,
            pixel_shader=self.current_pet.pixel_shader,
            x=display.width//2 - 16,
            y=display.height//2 - 16
        )
        self.pet_group.append(self.pet_sprite)

    def update_stats(self):
        current_time = time.monotonic()
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
            self._update_status()

    def _update_status(self):
        self.status_label.text = (
            f"H:{self.stats['hunger']} Hl:{self.stats['health']} "
            f"Ha:{self.stats['happiness']} E:{self.stats['energy']}"
        )

    def check_state(self):
        if self.stats["health"] <= 0:
            return "dead"
        if self.is_sleeping:
            return "sleeping"
        if self.stats["hunger"] < 30:
            return "hungry"
        if self.stats["health"] < 50:
            return "sick"
        if self.stats["happiness"] < 30:
            return "hungry"
        if self.stats["happiness"] > 80:
            return "happy"
        return "idle"

    def handle_input(self):
        if buttons.check_press(buttons.btn_a) and not self.is_sleeping:
            self.stats["hunger"] = min(100, self.stats["hunger"] + 30)
                
        if buttons.check_press(buttons.btn_b) and not self.is_sleeping:
            self.stats["health"] = min(100, self.stats["health"] + 20)
        
        if buttons.btn_c.value:
            if not self.c_pressed:
                self.c_pressed = True
                self.c_press_start = time.monotonic()
            else:
                if (time.monotonic() - self.c_press_start >= 
                    self.long_press_duration):
                    self.is_sleeping = not self.is_sleeping
                    self.c_pressed = False
        else:
            if self.c_pressed:
                if (time.monotonic() - self.c_press_start < 
                    self.long_press_duration):
                    if not self.is_sleeping:
                        self.stats["happiness"] = min(100, self.stats["happiness"] + 25)
                        self.stats["energy"] = max(0, self.stats["energy"] - 10)
                self.c_pressed = False

    def run(self):
        while True:
            self.handle_input()
            self.update_stats()
            
            new_state = self.check_state()
            if new_state != self.state:
                self.state = new_state
                self.update_pet_sprite(self.state)
            
            time.sleep(0.1)

pet_game = VirtualPet()
pet_game.run()
