import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
import pygame
import time

# Initialize the display
pygame.init()
display = PyGameDisplay(width=128, height=128)
splash = displayio.Group()
display.show(splash)

# Score variable
score = 0

# initial cookie image
cookie1_path = r"\cookie\cookie1.bmp"
cookie2_path = r"\cookie\cookie2.bmp"
cookie1 = displayio.OnDiskBitmap(cookie1_path)
bg_sprite = displayio.TileGrid(
    cookie1,
    pixel_shader=cookie1.pixel_shader
)
splash.append(bg_sprite)


pygame_screen = pygame.display.set_mode((128, 128))
font = pygame.font.Font(None, 24) 


def update_cookie_image(image_path):
    new_cookie = displayio.OnDiskBitmap(image_path)
    splash.pop()  # Remove the old sprite
    new_sprite = displayio.TileGrid(new_cookie, pixel_shader=new_cookie.pixel_shader)
    splash.append(new_sprite)

def render_score_text():
    pygame_screen.fill((0, 0, 0))
    text_surface = font.render(f"Score: {score}", True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(64, 110))
    pygame_screen.blit(text_surface, text_rect)
    pygame.display.flip()

# Main loop
running = True
render_score_text()  # Initial score display
while running:
    time.sleep(0.1)
    display.refresh()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                update_cookie_image(cookie2_path)  
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                update_cookie_image(cookie1_path)
                score += 1 
                render_score_text()
