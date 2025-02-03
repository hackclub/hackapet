import displayio
import config
# there was a plan to add more content, but i think this is enough for the day :3 - dwifte / rmfosho
class Menu:
    def __init__(self, group, font, save_data):
        self.state = "main"
        self.group = group 
        self.font = font
        self.visible = False
        self.options = {
            "main": ["Stats"] 
        }
        self.save_data = save_data

    def update_save_data(self, new_data):
        self.save_data = new_data

        if self.visible:
            self.update_display()


    def update_display(self):
        self.group.pop() if len(self.group) > 0 else None
        text_group = displayio.Group()

        # Black background
        palette = displayio.Palette(1)
        palette[0] = 0x000000
        bitmap = displayio.Bitmap(128, 128, 1)
        bitmap.fill(0)
        bg_sprite = displayio.TileGrid(bitmap, pixel_shader=palette, x=0, y=0)
        text_group.append(bg_sprite)

        # Show stats
        text_group.append(self.font.write_text(f"Food: {self.save_data['food']}/{config.FOOD_MAX}", 2, 2))
        text_group.append(self.font.write_text(f"mood: {self.save_data['happiness']}/{config.HAPPINESS_MAX}", 2, 14))
        text_group.append(self.font.write_text(f"Food got: {self.save_data['food_have'] or 0}", 2, 26))
        text_group.append(self.font.write_text(f"Special: {self.save_data['special']}", 2, 38))

        self.group.append(text_group)

    def toggle(self):
        self.visible = not self.visible
        if self.visible:
            self.update_display()
        else:
            self.group.pop() if len(self.group) > 0 else None