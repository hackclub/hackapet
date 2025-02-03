import displayio 
from blinka_displayio_pygamedisplay import PyGameDisplay 
import pygame
import time
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font
import random

pygame.init()

scale = 1
display_width = 128
display_height = 128

display = PyGameDisplay(width=display_width * scale, height=display_height * scale)
splash = displayio.Group(scale=scale)

display.show(splash)
# MARK: bg
bg_sheet = displayio.OnDiskBitmap("img/background.bmp")

bg_sprite = displayio.TileGrid(
    bg_sheet,
    pixel_shader=bg_sheet.pixel_shader,
    width=1,
    height=1,
    tile_width=display_width,
    tile_height=display_height,
    default_tile=3 # default bg
)

splash.append(bg_sprite)

# MARK: color buttons
class Button:
  def __init__(self, tile):
    self.tile = tile

color_button_width = 37
color_button_height = 10
color_button_spacing = 3

# cyan
cyan_sheet = displayio.OnDiskBitmap("img/button-cyan.bmp")

button_cyan_sprite = displayio.TileGrid(
    cyan_sheet,
    pixel_shader=cyan_sheet.pixel_shader,
    width=1,
    height=1,
    tile_width=color_button_width,
    tile_height=color_button_height,
    default_tile=3, # selected by default
    x=color_button_spacing,
    y=display_height - color_button_height - color_button_spacing
)

splash.append(button_cyan_sprite)
button_cyan = Button(3)

# magenta
magenta_sheet = displayio.OnDiskBitmap("img/button-magenta.bmp")

button_magenta_sprite = displayio.TileGrid(
    magenta_sheet,
    pixel_shader=cyan_sheet.pixel_shader,
    width=1,
    height=1,
    tile_width=color_button_width,
    tile_height=color_button_height,
    default_tile=0,
    x=(display_width - color_button_width) // 2,
    y=display_height - color_button_height - color_button_spacing    
)

splash.append(button_magenta_sprite)
button_magenta = Button(0)

# yellow
yellow_sheet = displayio.OnDiskBitmap("img/button-yellow.bmp")

button_yellow_sprite = displayio.TileGrid(
    yellow_sheet,
    pixel_shader=cyan_sheet.pixel_shader,
    width=1,
    height=1,
    tile_width=color_button_width,
    tile_height=color_button_height,
    default_tile=0,
    x=display_width - color_button_width - color_button_spacing,
    y=display_height - color_button_height - color_button_spacing    
)

splash.append(button_yellow_sprite)
button_yellow = Button(0)

# MARK: colors
class Color:
    def __init__(self, tile, cyan, magenta, yellow):
        self.tile = tile
        self.cyan = cyan
        self.magenta = magenta
        self.yellow = yellow

colors = [Color(0, 0, 0, 1), # yellow
          Color(0, 0, 0, 2), # yellow
          Color(1, 0, 1, 0), # magenta
          Color(2, 0, 1, 1), # 1m1y (red)
          Color(3, 0, 1, 2), # 1m2y (orange)
          Color(1, 0, 2, 0), # magenta
          Color(4, 0, 2, 1), # 2m1y (scarlet)
          Color(5, 1, 0, 0), # cyan
          Color(6, 1, 0, 1), # 1c1y (green)
          Color(7, 1, 0, 2), # 1c2y (lime)
          Color(8, 1, 1, 0), # 1c1m (blue)
          Color(9, 1, 1, 1), # black
          Color(10, 1, 2, 0), # 1c2m (purple)
          Color(5, 2, 0, 0), # cyan
          Color(11, 2, 0, 1), # 2c1y (turquoise)
          Color(12, 2, 1, 0) # 2c1m (azure)
        ]

# MARK: mixed color
mixed_color_width = 122
mixed_color_height = 6
mixed_color_spacing = 3
mixed_color_y = display_height - color_button_height - color_button_spacing - mixed_color_height - mixed_color_spacing

mixed_color_sheet = displayio.OnDiskBitmap("img/mixed-colors.bmp")

mixed_color_sprite = displayio.TileGrid(
    mixed_color_sheet,
    pixel_shader=mixed_color_sheet.pixel_shader,
    width=1,
    height=1,
    tile_width=mixed_color_width,
    tile_height=mixed_color_height,
    default_tile=13,
    x=(display_width - mixed_color_width) // 2,
    y=mixed_color_y
)

splash.append(mixed_color_sprite)

# MARK: arrow buttons
arrow_button_width = 9
arrow_button_height = 6
arrow_button_spacing_h = 16
arrow_button_spacing_v = 3

button_sheet = displayio.OnDiskBitmap("img/button-arrow.bmp")

button_arrow_0_sprite = displayio.TileGrid(
    button_sheet,
    pixel_shader=button_sheet.pixel_shader,
    width=1,
    height=1,
    tile_width=arrow_button_width,
    tile_height=arrow_button_height,
    default_tile=0,
    x=arrow_button_spacing_h,
    y=display_height - color_button_height - color_button_spacing - mixed_color_height - mixed_color_spacing - arrow_button_height - arrow_button_spacing_v
)

splash.append(button_arrow_0_sprite)

button_arrow_1_sprite = displayio.TileGrid(
    button_sheet,
    pixel_shader=button_sheet.pixel_shader,
    width=1,
    height=1,
    tile_width=arrow_button_width,
    tile_height=arrow_button_height,
    default_tile=0,
    x=(display_width - arrow_button_width) // 2,
    y=display_height - color_button_height - color_button_spacing - mixed_color_height - mixed_color_spacing - arrow_button_height - arrow_button_spacing_v
)

splash.append(button_arrow_1_sprite)

button_arrow_2_sprite = displayio.TileGrid(
    button_sheet,
    pixel_shader=button_sheet.pixel_shader,
    width=1,
    height=1,
    tile_width=arrow_button_width,
    tile_height=arrow_button_height,
    default_tile=0,
    x=display_width - arrow_button_width - arrow_button_spacing_h,
    y=display_height - color_button_height - color_button_spacing - mixed_color_height - mixed_color_spacing - arrow_button_height - arrow_button_spacing_v
)

splash.append(button_arrow_2_sprite)


# MARK: blocks
class Block:
    def __init__(self, color_id, column, block_sprite):
        self.color_id = color_id
        self.column = column # 0, 1, or 2
        self.block_sprite = block_sprite

blocks = [] 

block_width = 37
block_height = 10
block_spacing = 3

block_sheet = displayio.OnDiskBitmap("img/color-blocks.bmp")

# MARK: score label
score = 0
best_score = 0

font = bitmap_font.load_font("font/helvR12.bdf")

score_label = label.Label(
    font, 
    text=str(score), 
    color=0xFFFFFF, 
    x=display_width - 10 - len(str(score)) * 8, 
    y=10)

score_label_shadow = label.Label(
    font, 
    text=str(score), 
    color=0x36393C, 
    x=(display_width - 10 - len(str(score)) * 8) + 1, 
    y=11)

splash.append(score_label_shadow)
splash.append(score_label)

# MARK: Start Screen
start_screen_sheet = displayio.OnDiskBitmap("img/start-screen.bmp")

start_screen_sprite = displayio.TileGrid(
    start_screen_sheet,
    pixel_shader=start_screen_sheet.pixel_shader,
    width=1,
    height=1,
    tile_width=display_width,
    tile_height=display_height,
    default_tile=0
)

splash.append(start_screen_sprite)

# MARK: color selection fcns
def update_color_button_sprites():
    button_cyan_sprite[0] = button_cyan.tile
    button_magenta_sprite[0] = button_magenta.tile
    button_yellow_sprite[0] = button_yellow.tile

def switch_selected_color_button(curr):
    if curr == button_cyan:
        curr = button_magenta
        button_cyan.tile = (button_cyan.tile + 3) % 6
        button_magenta.tile = (button_magenta.tile + 3) % 6
    elif curr == button_magenta: 
        curr = button_yellow
        button_magenta.tile = (button_magenta.tile + 3) % 6
        button_yellow.tile = (button_yellow.tile + 3) % 6
    else:
        curr = button_cyan
        button_yellow.tile = (button_yellow.tile + 3) % 6
        button_cyan.tile = (button_cyan.tile + 3) % 6

    update_color_button_sprites()

    return curr

# returns updated total num_color_portions
def select_color_button(curr, num_color_portions):
    # 3 -> 4 -> 5 -> 3 (0 portions -> 1 -> 2 -> 0)
    # max 3 color portions selected at a time
    if curr.tile == 5:
        curr.tile = 3
        num_color_portions -= 2
    elif num_color_portions < 3:
        curr.tile += 1
        num_color_portions += 1
    else:
        if curr.tile == 4:
            num_color_portions -= 1
        elif curr.tile == 5: 
            num_color_portions -= 2
        curr.tile = 3

    update_color_button_sprites()
    return num_color_portions

def disable_color_button_highlight(curr_selected):
    curr_selected.tile = curr_selected.tile - 3

    update_color_button_sprites()

def get_color_concentration(curr):
    # 0 for none, 1 for one portion, 2 for two portions
    return curr.tile % 3

# returns mixed color id (sprite #)
def mix_colors():
    cyan = get_color_concentration(button_cyan)
    magenta = get_color_concentration(button_magenta)
    yellow = get_color_concentration(button_yellow)

    color_id = next((c.tile for c in colors if c.cyan == cyan and c.magenta == magenta and c.yellow == yellow), 13)
    mixed_color_sprite[0] = color_id
    
    return color_id

def reset_color_buttons():
    # cyan selected by default
    button_cyan.tile = 3
    button_cyan_sprite[0] = 3

    button_magenta.tile = 0
    button_magenta_sprite[0] = 0

    button_yellow.tile = 0
    button_yellow_sprite[0] = 0
    

# MARK: row selection fcns
def switch_selected_arrow_button(curr):
    curr[0] = 0

    if curr == button_arrow_0_sprite:
        button_arrow_1_sprite[0] = 1
        bg_sprite[0] = 1
        curr = button_arrow_1_sprite
    elif curr == button_arrow_1_sprite:
        button_arrow_2_sprite[0] = 1
        bg_sprite[0] = 2
        curr = button_arrow_2_sprite
    else:
        button_arrow_0_sprite[0] = 1
        bg_sprite[0] = 0
        curr = button_arrow_0_sprite
    return curr

def disable_arrow_button_highlight():
    button_arrow_0_sprite[0] = button_arrow_1_sprite[0] = button_arrow_2_sprite[0] = 0
    bg_sprite[0] = 3

# returns num. of blocks shot
def shoot(color_id, arrow):
    if curr_selected_arrow == button_arrow_0_sprite:
        column = 0
    elif curr_selected_arrow == button_arrow_1_sprite:
        column = 1
    else:
        column = 2
    
    num_shot = 0

    for block in blocks:
        if block.column == column and block.color_id == color_id:
            num_shot += 1
            splash.remove(block.block_sprite)
            blocks.remove(block)
    return num_shot

# MARK: block fcns
def spawn_block():
    column = random.randint(0, 2)

    if column == 0:
        x_pos = block_spacing
    elif column == 1:
        x_pos = (display_width - block_width) // 2
    else:
        x_pos = display_width - block_width - block_spacing
    
    color_id = random.randint(0, 12)

    block_sprite = displayio.TileGrid(
        block_sheet,
        pixel_shader=block_sheet.pixel_shader,
        width=1,
        height=1,
        tile_width=block_width,
        tile_height=block_height,
        default_tile=color_id,
        x=x_pos,
        y=-block_height
    )

    blocks.append(Block(color_id, column, block_sprite))
    splash.insert(2, block_sprite) # insert 2 layers up (above bg & score)

# checks whether block has collided with bottom (mixed color bar)
def is_block_collided(block):
    if block.block_sprite.y > mixed_color_y - mixed_color_height * 2:
        return block.block_sprite.y > mixed_color_y - mixed_color_height * 2
    
# MARK: score label fcn
def update_score_label(score):
    score_label.text = str(score)
    score_label_shadow.text = str(score)

# MARK: game over

# displays game over sprite, final score, and high score
def display_game_over():
    game_over_popup = displayio.OnDiskBitmap("img/game-over.bmp")

    game_over_popup_width = 108
    game_over_popup_height = 53

    global game_over_popup_sprite
    game_over_popup_sprite = displayio.TileGrid(
        game_over_popup,
        pixel_shader=game_over_popup.pixel_shader,
        width=1,
        height=1,
        tile_width=game_over_popup_width,
        tile_height=game_over_popup_height,
        default_tile=0,
        x=(display_width - game_over_popup_width) // 2,  
        y=(display_height - game_over_popup_height) // 2 
    )

    splash.append(game_over_popup_sprite)
    display_game_over_text()

def display_game_over_text():
    text = f"{score}  (BEST: {best_score})"

    temp_label = label.Label(font, text=text)
    text_width = temp_label.bounding_box[2]

    global game_over_scores
    game_over_scores = label.Label(
        font, 
        text=text, 
        color=0x36393C, 
        x=(display_width - text_width) // 2, 
        y=display_height // 2 - (display_height // 10))

    global game_over_scores_shadow
    game_over_scores_shadow = label.Label(
        font, 
        text=text, 
        color=0xD2C0BB, 
        x=(display_width - text_width) // 2 + 1, 
        y=display_height // 2 - (display_height // 10) + 1)

    splash.append(game_over_scores_shadow)
    splash.append(game_over_scores)

def hide_game_over_popup():
    splash.remove(game_over_popup_sprite)
    splash.remove(game_over_scores)
    splash.remove(game_over_scores_shadow)

# MARK: gameplay
frame = 0
anim_delay = 5
has_started = False
is_game_over = False
curr_selected_color_button = button_cyan
num_color_portions = 0
mixed_color_id = 13 # none
is_color_selected = False
curr_selected_arrow = None
block_spawn_rate = 0.05
block_speed = 1
cooldown = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if has_started == False: 
                start_screen_sprite[0] = frame
                if event.key:
                    has_started = True
                    splash.remove(start_screen_sprite)
            # MARK: color selection
            elif is_game_over == False:
                if is_color_selected == False:
                    # move to next color button
                    if event.key == pygame.K_RIGHT:
                        curr_selected_color_button = switch_selected_color_button(curr_selected_color_button)
                    # select color
                    elif event.key == pygame.K_SPACE: 
                        num_color_portions = select_color_button(curr_selected_color_button, num_color_portions)
                        mixed_color_id = mix_colors()
                    # finished mixing colors
                    elif event.key == pygame.K_RETURN and mixed_color_id != 13:
                        is_color_selected = True
                        disable_color_button_highlight(curr_selected_color_button)
                        curr_selected_color_button = None
                        curr_selected_arrow = button_arrow_0_sprite
                        curr_selected_arrow[0] = 1
                        bg_sprite[0] = 0
                # MARK: arrow selection
                else: 
                    # move to next arrow button
                    if event.key == pygame.K_RIGHT:
                        curr_selected_arrow = switch_selected_arrow_button(curr_selected_arrow)
                    # shoot, return to color selection
                    elif event.key == pygame.K_RETURN:
                        score += shoot(mixed_color_id, curr_selected_arrow)
                        update_score_label(score)
                        mixed_color_id = 13
                        num_color_portions = 0
                        is_color_selected = False
                        disable_arrow_button_highlight()
                        curr_selected_arrow = None
                        curr_selected_color_button = button_cyan
                        reset_color_buttons()
                        mix_colors()
            else: # game_over == True
                # press K_RETURN or K_SPACE to restart
                # clear all blocks & restore state upon restart
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    is_game_over = False
                    curr_selected_color_button = button_cyan
                    num_color_portions = 0
                    mixed_color_id = 13 # none
                    is_color_selected = False
                    curr_selected_arrow = None
                    score = 0
                    reset_color_buttons()
                    disable_arrow_button_highlight()
                    update_score_label(score)
                    hide_game_over_popup()

                    for block in blocks:
                        splash.remove(block.block_sprite)
                    blocks.clear()

    # update start screen animation only on delay cycles
    if has_started == False and frame % anim_delay == 0: 
        start_screen_sprite[0] = (frame // anim_delay) % (start_screen_sheet.width // start_screen_sprite.tile_width)
    
    frame += 1

    if is_game_over == False and has_started == True:
        if random.random() < block_spawn_rate and cooldown == 0:
            spawn_block()
            cooldown = 20
        elif cooldown > 0:
            cooldown -= 1

        for block in blocks:
            block.block_sprite.y += block_speed
            if block.block_sprite.y > display_height:
                splash.remove(block.block_sprite)
                blocks.remove(block)
            
            # stop game once block collides
            elif is_block_collided(block):
                is_game_over = True
                if (score > best_score):
                    best_score = score
                display_game_over()

    time.sleep(0.1)
