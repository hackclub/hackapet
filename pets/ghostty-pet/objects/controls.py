import displayio

controls = displayio.OnDiskBitmap("art/controls.bmp")

class Controls:
    def __init__(self, splash):
        self.controls = displayio.TileGrid(
                    controls,
                    pixel_shader=controls.pixel_shader,
                    y=128-16
                )
        splash.append(self.controls)
        self.visible = True
        self.splash = splash
        self.frame = 0
    def update(self):
        self.frame += 1
        if self.visible and self.frame > 300:
            self.visible = False
            self.splash.remove(self.controls)
        elif not self.visible and self.frame < 300:
            self.visible = True
            self.splash.append(self.controls)
    def hide(self):
        if self.visible:
            self.splash.remove(self.controls)
            self.visible = False
        self.frame = 0
