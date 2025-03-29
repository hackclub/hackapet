import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
import pygame
import time
import random

scale = 2
display_width = 128 * scale
display_height = 128 * scale
display = PyGameDisplay(width=display_width, height=display_height)
splash = displayio.Group(scale=scale)
display.show(splash)

backgrounds = [
    displayio.OnDiskBitmap("background1.bmp"),
    displayio.OnDiskBitmap("background2.bmp")
]
current_bg = 0

bird_frames = [
    displayio.OnDiskBitmap("fly1.bmp"),
    displayio.OnDiskBitmap("fly2.bmp")
]
dead_bird = displayio.OnDiskBitmap("dead.bmp")

columns = {
    "short": displayio.OnDiskBitmap("short-column.bmp"),
    "medium": displayio.OnDiskBitmap("medium-column.bmp")
}

food = displayio.OnDiskBitmap("Food.bmp")
start_screen_bmp = displayio.OnDiskBitmap("StartScreen.bmp")
game_over_bmp = displayio.OnDiskBitmap("GameOver.bmp")
numbers_bmp = displayio.OnDiskBitmap("numbers.bmp")
game_started = False
game_over = False
score = 0

bg_sprite = displayio.TileGrid(backgrounds[current_bg], pixel_shader=backgrounds[current_bg].pixel_shader)
splash.append(bg_sprite)
game_group = displayio.Group()
splash.append(game_group)

score_group = displayio.Group(x=100, y=8)
food_small = displayio.TileGrid(food, pixel_shader=food.pixel_shader, x=0, y=0)
score_group.append(food_small)
splash.append(score_group)

start_screen = displayio.TileGrid(
    start_screen_bmp,
    pixel_shader=start_screen_bmp.pixel_shader,
    x=0,
    y=0
)
splash.append(start_screen)

bird = displayio.TileGrid(
    bird_frames[0],
    pixel_shader=bird_frames[0].pixel_shader,
    x=16,
    y=56
)
splash.append(bird)

active_columns = []
active_collectibles = []
bird_velocity = 0
gravity = 0.5
jump_strength = -8
last_bg_switch = time.monotonic()
last_frame = time.monotonic()
last_spawn = time.monotonic()
game_over_elements = None

def update_score_display():
    while len(score_group) > 1:
        score_group.pop(-1)
    x_offset = 20
    for digit in str(score):
        index = int(digit)
        number_tile = displayio.TileGrid(
            numbers_bmp,
            pixel_shader=numbers_bmp.pixel_shader,
            tile_width=8,
            tile_height=8,
            default_tile=index
        )
        number_tile.x = x_offset
        score_group.append(number_tile)
        x_offset += 8

def reset_game():
    global game_over, bird_velocity, score, current_bg, last_bg_switch, bird, game_started
    
    game_over = False
    bird_velocity = 0
    score = 0
    update_score_display()
    
    if bird in game_group:
        game_group.remove(bird)
    
    bird = displayio.TileGrid(
        bird_frames[0],
        pixel_shader=bird_frames[0].pixel_shader,
        x=16,
        y=56
    )
    game_group.append(bird)
    
    for column in active_columns[:]:
        if column in game_group:
            game_group.remove(column)
    active_columns.clear()
    
    for collectible in active_collectibles[:]:
        if collectible in game_group:
            game_group.remove(collectible)
    active_collectibles.clear()
    
    current_bg = 0
    bg_sprite.bitmap = backgrounds[current_bg]
    last_bg_switch = time.monotonic()
    game_started = True

def switch_background():
    global current_bg
    current_bg = (current_bg + 1) % len(backgrounds)
    bg_sprite.bitmap = backgrounds[current_bg]

def spawn_column():
    column_type = random.choice(["short", "medium"])
    y_position = 0 if column_type == "short" else 128 - 32
    column = displayio.TileGrid(
        columns[column_type],
        pixel_shader=columns[column_type].pixel_shader,
        x=128,
        y=y_position
    )
    active_columns.append(column)
    game_group.append(column)

def spawn_food():
    collectible = displayio.TileGrid(
        food,
        pixel_shader=food.pixel_shader,
        x=128,
        y=random.randint(16, 112)
    )
    active_collectibles.append(collectible)
    game_group.append(collectible)

def check_collision(obj1, obj2):
    return (
        obj1.x < obj2.x + obj2.tile_width and
        obj1.x + obj1.tile_width > obj2.x and
        obj1.y < obj2.y + obj2.tile_height and
        obj1.y + obj1.tile_height > obj2.y
    )

def show_game_over():
    global game_over_elements
    
    if game_over_elements is not None:
        return
    
    if bird in game_group:
        game_group.remove(bird)
    
    dead_bird_grid = displayio.TileGrid(
        dead_bird,
        pixel_shader=dead_bird.pixel_shader,
        x=bird.x,
        y=bird.y
    )
    game_group.append(dead_bird_grid)
    
    game_over_image = displayio.TileGrid(
        game_over_bmp,
        pixel_shader=game_over_bmp.pixel_shader,
        x=(128 - game_over_bmp.width) // 2,
        y=(128 - game_over_bmp.height) // 2
    )
    splash.append(game_over_image)
    
    game_over_elements = (dead_bird_grid, game_over_image)

while True:
    current_time = time.monotonic()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if game_over:
                if game_over_elements:
                    dead_bird_element, game_over_element = game_over_elements
                    if dead_bird_element in game_group:
                        game_group.remove(dead_bird_element)
                    if game_over_element in splash:
                        splash.remove(game_over_element)
                    game_over_elements = None
                reset_game()
            elif not game_started:
                splash.remove(start_screen)
                if bird in splash:
                    splash.remove(bird)
                game_started = True
            else:
                bird_velocity = jump_strength
        elif event.type == pygame.MOUSEBUTTONDOWN and game_started and not game_over:
            bird_velocity = jump_strength

    if game_started and not game_over:
        if current_time - last_frame > 0.15:
            bird.bitmap = bird_frames[int((current_time % 0.3) > 0.15)]
            last_frame = current_time

        bird_velocity += gravity
        bird.y += int(bird_velocity)
        bird.y = max(16, min(112, bird.y))

        if current_time - last_bg_switch > 10:
            switch_background()
            last_bg_switch = current_time

        if current_time - last_spawn > 2:
            spawn_column()
            if random.random() < 0.3:
                spawn_food()
            last_spawn = current_time

        for column in active_columns[:]:
            column.x -= 2
            if check_collision(bird, column):
                game_over = True
                show_game_over()
                break

        for food_item in active_collectibles[:]:
            food_item.x -= 2
            if check_collision(bird, food_item):
                score += 1
                update_score_display()
                if food_item in game_group:
                    game_group.remove(food_item)
                active_collectibles.remove(food_item)

        for c in active_columns[:]:
            if c.x <= -32:
                if c in game_group:
                    game_group.remove(c)
                active_columns.remove(c)
        for f in active_collectibles[:]:
            if f.x <= -16:
                if f in game_group:
                    game_group.remove(f)
                active_collectibles.remove(f)

    time.sleep(0.016)