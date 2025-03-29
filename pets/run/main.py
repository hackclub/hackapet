import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
import time
import pygame
import random
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font

# Initialize display
display = PyGameDisplay(width=128, height=128)
splash = displayio.Group()
display.show(splash)

# Game states
MENU = 0
PLAYING = 1
GAME_OVER = 2
current_state = MENU

# Load sprites
bg_sprite = displayio.OnDiskBitmap("bg.bmp")
player_sprite = displayio.OnDiskBitmap("player_run_sheet.bmp")
enemy_sprite = displayio.OnDiskBitmap("enemy_run_sheet.bmp")

font10 = bitmap_font.load_font("QuinqueFive-10-rb.bdf")
font6 = bitmap_font.load_font("QuinqueFive-6-rb.bdf")
font4 = bitmap_font.load_font("QuinqueFive-4-r.bdf")

# Background setup
bg1 = displayio.TileGrid(bg_sprite, pixel_shader=bg_sprite.pixel_shader, x=0, y=0)
bg2 = displayio.TileGrid(bg_sprite, pixel_shader=bg_sprite.pixel_shader, x=0, y=-(display.height))

game_over_text = label.Label(font=font6, text="GAME OVER!", x=10, y=50)
restart_text = label.Label(font=font4, text="SPACE TO RESTART", x=15, y=65)

game_title_text = label.Label(font=font10, text="RUN", x=37, y=50)
start_text = label.Label(font=font4, text="SPACE TO START", x=20, y=70)

score_text = label.Label(font=font6, text="0", x=10, y=10)

# Player setup
player = displayio.TileGrid(
    player_sprite,
    pixel_shader=player_sprite.pixel_shader,
    width=1,
    height=1,
    tile_width=20,
    tile_height=39,
    x=54,
    y=80
)

# Groups
main_group = displayio.Group()
game_group = displayio.Group()
enemy_group = displayio.Group()
game_over_group = displayio.Group()
main_menu_group = displayio.Group()

main_menu_group.append(game_title_text)
main_menu_group.append(start_text)

game_over_group.append(game_over_text)
game_over_group.append(restart_text)

main_group.append(bg1)
main_group.append(bg2)
game_group.append(player)
game_group.append(enemy_group)
main_group.append(main_menu_group)
main_group.append(score_text)
main_group.append(game_group)
main_group.append(game_over_group)

display.show(main_group)

# Game variables
bg_scroll_speed = 1
player_frame = 0
player_frame_count = 10
enemy_frame = 0
enemy_frame_count = 12
player_lane = 2
enemy_speed = 5
enemy_spawn_interval = 1.4
last_enemy_spawn_time = time.time() + 1
score = 0
start_time = time.time()

# Helper functions
def get_enemy_lanes():
    first = random.choice([1, 2, 3])
    choices = [num for num in [1, 2, 3] if num != first]
    second = random.choice(choices)
    return first, second

def get_enemy_x_by_lane(lane: int):
    if lane == 1:
        return 7
    elif lane == 2:
        return 50
    else:
        return 90

def get_player_x_by_lane():
    if player_lane == 1:
        return 9
    elif player_lane == 2:
        return 54
    else:
        return 100

def reset_game():
    global start_time, score, player_lane, enemy_group, last_enemy_spawn_time, enemy_spawn_interval
    player_lane = 2
    player.x = get_player_x_by_lane()
    game_group.remove(enemy_group)
    enemy_group = displayio.Group()
    game_group.append(enemy_group)
    last_enemy_spawn_time = time.time() + 1
    enemy_spawn_interval = 1.4
    score = 0
    start_time = time.time()

# Main game loop
while True:
    score_text.text = str(int(score))
    # Scroll background
    bg1.y += bg_scroll_speed
    bg2.y += bg_scroll_speed
    if bg1.y == display.height:
        bg1.y = -(display.height)
    if bg2.y == display.height:
        bg2.y = -(display.height)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break

        if current_state == MENU:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    current_state = PLAYING
                    reset_game()

        elif current_state == PLAYING:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if player_lane - 1 >= 1:
                        player_lane -= 1
                    player.x = get_player_x_by_lane()
                elif event.key == pygame.K_RIGHT:
                    if player_lane + 1 <= 3:
                        player_lane += 1
                    player.x = get_player_x_by_lane()

        elif current_state == GAME_OVER:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    current_state = PLAYING
                    reset_game()
                elif event.key == pygame.K_ESCAPE:
                    current_state = MENU

    if current_state == PLAYING:
        score = time.time() - start_time

        score_text.hidden = False
        game_over_group.hidden = True
        main_menu_group.hidden = True
        game_group.hidden = False

        # Spawn enemies
        if time.time() >= last_enemy_spawn_time + enemy_spawn_interval:
            a, b = get_enemy_lanes()
            enemy1 = displayio.TileGrid(enemy_sprite, pixel_shader=enemy_sprite.pixel_shader, width=1, height=1, tile_width=24, tile_height=35, x=get_enemy_x_by_lane(a), y=-35)
            enemy2 = displayio.TileGrid(enemy_sprite, pixel_shader=enemy_sprite.pixel_shader, width=1, height=1, tile_width=24, tile_height=35, x=get_enemy_x_by_lane(b), y=-35)
            enemy_group.append(enemy1)
            enemy_group.append(enemy2)
            last_enemy_spawn_time = time.time()
            if enemy_spawn_interval > 1:
                enemy_spawn_interval -= 0.001

        # Update enemies
        for enemy in enemy_group:
            enemy.y += enemy_speed
            enemy[0] = enemy_frame

            # Check for collision
            if (player.x < enemy.x + enemy.tile_width and player.x + player.tile_width > enemy.x and player.y < enemy.y + enemy.tile_height - 10 and player.y + player.tile_height > enemy.y + 10):
                current_state = GAME_OVER

            # Remove off-screen enemies
            if enemy.y >= display.height:
                enemy_group.remove(enemy)

        # Update player animation
        player[0] = player_frame
        player_frame = (player_frame + 1) % player_frame_count

        # Update enemy animation
        enemy_frame = (enemy_frame + 1) % enemy_frame_count

    elif current_state == MENU:
        score_text.hidden = True
        game_over_group.hidden = True
        main_menu_group.hidden = False
        game_group.hidden = True

    elif current_state == GAME_OVER:
        score_text.hidden = False
        game_over_group.hidden = False
        main_menu_group.hidden = True
        game_group.hidden = True

    time.sleep(0.05)