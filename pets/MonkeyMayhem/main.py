import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
import pygame
from adafruit_display_text import label
import random
import os
import time
import math


pygame.init()


SCREEN_WIDTH = 128
SCREEN_HEIGHT = 128


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Monkey Banana Game")


ASSET_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dependencies")
BACKGROUND_IMAGES = [
    os.path.join(ASSET_PATH, f"background{i}.bmp")
    for i in range(4)
]
MONKEY_IMAGES = {
    "right": os.path.join(ASSET_PATH, "monkey_right.bmp"),
    "left": os.path.join(ASSET_PATH, "monkey_left.bmp"),
    "standing": os.path.join(ASSET_PATH, "monkey_standing.bmp"),
}
BANANA_IMAGES = {
    "normal": os.path.join(ASSET_PATH, "banana_normal.bmp"),
    "rotten": os.path.join(ASSET_PATH, "banana_rotten.bmp"),
    "super": os.path.join(ASSET_PATH, "banana_super.bmp"),
}
UI_IMAGES = {
    "heart": os.path.join(ASSET_PATH, "heart.bmp"),
    "start_screen": os.path.join(ASSET_PATH, "start_screen.bmp"),
    "death_screen": os.path.join(ASSET_PATH, "death_screen.bmp"),
}


backgrounds = [pygame.image.load(img) for img in BACKGROUND_IMAGES]
monkey_right = pygame.image.load(MONKEY_IMAGES["right"])
monkey_left = pygame.image.load(MONKEY_IMAGES["left"])
monkey_standing = pygame.image.load(MONKEY_IMAGES["standing"])
banana_images = {key: pygame.image.load(img) for key, img in BANANA_IMAGES.items()}
ui_images = {key: pygame.image.load(img) for key, img in UI_IMAGES.items()}


monkey_right = pygame.transform.scale(monkey_right, (32, 32))
monkey_left = pygame.transform.scale(monkey_left, (32, 32))
monkey_standing = pygame.transform.scale(monkey_standing, (32, 32))
for key in banana_images:
    banana_images[key] = pygame.transform.scale(banana_images[key], (32, 32))

clock = pygame.time.Clock()


monkey_x = SCREEN_WIDTH // 2 - 16
monkey_y = SCREEN_HEIGHT - 32
monkey_speed = 3
monkey_direction = "right"
hearts = 3
score = 0

banana_list = []
banana_speed = 2
banana_spawn_rate = 30
last_speed_increase = 0  

background_index = 0

game_running = False
game_over_displayed = False

last_background_switch = time.time()


dance_amplitude = 20  
dance_frequency = 4  
dance_x = SCREEN_WIDTH // 2 - 16
dance_base_y = SCREEN_HEIGHT // 2

def spawn_banana():
    banana_type = random.choices(
        ["normal", "rotten", "super"], weights=[60, 25, 15], k=1
    )[0]
    x = random.randint(0, SCREEN_WIDTH - 32)
    y = -32
    return {"type": banana_type, "x": x, "y": y}

def move_bananas():
    global banana_speed
    for banana in banana_list:
        banana["y"] += banana_speed

def check_collisions():
    global hearts, score, banana_speed, last_speed_increase
    for banana in banana_list[:]:
        if (
            banana["x"] < monkey_x + 32
            and banana["x"] + 32 > monkey_x
            and banana["y"] < monkey_y + 32
            and banana["y"] + 32 > monkey_y
        ):
            if banana["type"] == "normal":
                score += 1
            elif banana["type"] == "rotten":
                hearts -= 1
            elif banana["type"] == "super":
                hearts = min(3, hearts + 1)
                score += 3
            banana_list.remove(banana)
            
            
            if score // 10 > last_speed_increase:
                banana_speed = banana_speed * 1.1  
                last_speed_increase = score // 10

def draw_game():
    global background_index, last_background_switch
    current_time = time.time()
    
    if current_time - last_background_switch >= 1.0:  
        background_index = (background_index + 1) % len(backgrounds)
        last_background_switch = current_time
    
    screen.blit(backgrounds[background_index], (0, 0))
    
    if monkey_direction == "right":
        screen.blit(monkey_right, (monkey_x, monkey_y))
    else:
        screen.blit(monkey_left, (monkey_x, monkey_y))
    for banana in banana_list:
        screen.blit(banana_images[banana["type"]], (banana["x"], banana["y"]))
    
    
    heart_img = ui_images["heart"]
    for i in range(hearts):
        screen.blit(heart_img, (5 + i * 15, 5))
    
    font = pygame.font.SysFont(None, 24)
    score_text = font.render(f"Score: {score}", True, (255, 0, 0))
    screen.blit(score_text, (SCREEN_WIDTH - 70, 5))

def reset_game():
    global monkey_x, monkey_y, hearts, score, banana_list, banana_speed, game_running, game_over_displayed, last_speed_increase
    monkey_x = SCREEN_WIDTH // 2 - 16
    monkey_y = SCREEN_HEIGHT - 32
    hearts = 3
    score = 0
    banana_list = []
    banana_speed = 2
    last_speed_increase = 0
    game_running = False
    game_over_displayed = False

running = True
frame_count = 0
while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if not game_running:
        if hearts <= 0:
            screen.blit(ui_images["death_screen"], (0, 0))
            font = pygame.font.SysFont(None, 16)
            score_text = font.render(f"Final Score: {score}", True, (255, 0, 0))
            score_x = SCREEN_WIDTH // 2 - score_text.get_width() // 2
            screen.blit(score_text, (score_x, SCREEN_HEIGHT // 2 + 20))
            
            if keys[pygame.K_SPACE]:
                reset_game()
                game_running = True
        else:
            screen.blit(ui_images["start_screen"], (0, 0))
            
            
            current_time = time.time()
            dance_y = dance_base_y + math.sin(current_time * dance_frequency) * dance_amplitude
            
            
            dance_x_offset = math.sin(current_time * dance_frequency * 0.5) * dance_amplitude
            current_dance_x = dance_x + dance_x_offset
            
            
            screen.blit(monkey_standing, (current_dance_x, dance_y))
            
            if keys[pygame.K_SPACE]:
                game_running = True
    else:
        if keys[pygame.K_LEFT] and monkey_x > 0:
            monkey_x -= monkey_speed
            monkey_direction = "left"
        if keys[pygame.K_RIGHT] and monkey_x < SCREEN_WIDTH - 32:
            monkey_x += monkey_speed
            monkey_direction = "right"
        if frame_count % banana_spawn_rate == 0:
            banana_list.append(spawn_banana())
        move_bananas()
        check_collisions()
        banana_list = [b for b in banana_list if b["y"] < SCREEN_HEIGHT]
        draw_game()
        if hearts <= 0:
            game_running = False

    pygame.display.flip()
    clock.tick(30)
    frame_count += 1

pygame.quit()
