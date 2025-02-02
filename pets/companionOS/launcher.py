import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
import pygame
import time
import os

# Display
pygame.init()
display = PyGameDisplay(width=128, height=128)
splash = displayio.Group()
display.show(splash)

# UI file paths
ui_files = [
    r"\ui\ui1.bmp",
    r"\ui\ui2.bmp",
    r"\ui\ui3.bmp",
    r"\ui\ui4.bmp",
    r"\ui\ui5.bmp",
]

# Load Launcher
current_index = 0
ui_bmp = displayio.OnDiskBitmap(ui_files[current_index])
bg_sprite = displayio.TileGrid(
    ui_bmp,
    pixel_shader=ui_bmp.pixel_shader
)
splash.append(bg_sprite)
pygame_screen = pygame.display.set_mode((128, 128))
font = pygame.font.Font(None, 24)

# Update UI
def update_ui(index):
    global bg_sprite
    splash.pop()
    new_ui = displayio.OnDiskBitmap(ui_files[index])
    bg_sprite = displayio.TileGrid(new_ui, pixel_shader=new_ui.pixel_shader)
    splash.append(bg_sprite)

# Show message
def show_message(message, duration=2):
    pygame_screen.fill((0, 0, 0)) 
    text_surface = font.render(message, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(64, 64))
    pygame_screen.blit(text_surface, text_rect)
    pygame.display.flip() 
    time.sleep(duration)
    pygame_screen.fill((0, 0, 0))
    pygame.display.flip()

# Main loop
running = True
while running:
    time.sleep(0.1)
    display.refresh()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:  # Down arrow key
                current_index += 1
                if current_index >= len(ui_files):
                    current_index = 1
                update_ui(current_index)
            elif event.key == pygame.K_UP:
                if current_index == 1:  # UI2 launches dice.py
                    os.system("python dice.py")
                elif current_index == 3:  # UI3 launches cookie.py
                    os.system("python cookie.py")
                elif current_index == 2:  # UI4 launches coin.py
                    os.system("python coin.py")
                else:
                    show_message("Coming Soon")
