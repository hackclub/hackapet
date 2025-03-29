from random import randint

import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
import pygame
import time
import adafruit_imageload

pygame.init()

display = PyGameDisplay(width=128, height=128)

# Background init
background = displayio.OnDiskBitmap("./art/background.bmp")
bg_sprite = displayio.TileGrid(
    background,
    pixel_shader=background.pixel_shader)

home_background = displayio.OnDiskBitmap("./art/rabeat.bmp")
home_bg_sprite = displayio.TileGrid(
    home_background,
    pixel_shader=home_background.pixel_shader
)

button_to_start, button_to_start_palette = adafruit_imageload.load(
    "./art/button_to_start.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
button_to_start_palette.make_transparent(0)
button_to_start_sprite = displayio.TileGrid(
    button_to_start,
    pixel_shader=button_to_start_palette
)

# Difficulty screen inits
lightened_bg = displayio.OnDiskBitmap("./art/lightened_background.bmp")
lightened_bg_sprite = displayio.TileGrid(
    lightened_bg,
    pixel_shader=lightened_bg.pixel_shader
)

difficulties, difficulties_palette = adafruit_imageload.load(
    "./art/difficulty/difficulties.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
difficulties_palette.make_transparent(0)
difficulties_sprite = displayio.TileGrid(
    difficulties,
    pixel_shader=difficulties_palette
)

select_difficulty, select_difficulty_palette = adafruit_imageload.load(
    "./art/difficulty/difficulty.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
select_difficulty_palette.make_transparent(0)
select_difficulty_sprite = displayio.TileGrid(
    select_difficulty,
    pixel_shader=select_difficulty_palette
)

easy, easy_palette = adafruit_imageload.load(
    "./art/difficulty/easy.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
easy_palette.make_transparent(0)
easy_sprite = displayio.TileGrid(
    easy,
    pixel_shader=easy_palette
)

normal, normal_palette = adafruit_imageload.load(
    "./art/difficulty/normal.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
normal_palette.make_transparent(0)
normal_sprite = displayio.TileGrid(
    normal,
    pixel_shader=normal_palette
)

hard, hard_palette = adafruit_imageload.load(
    "./art/difficulty/hard.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
hard_palette.make_transparent(0)
hard_sprite = displayio.TileGrid(
    hard,
    pixel_shader=hard_palette
)

# Scoreboard inits
scoreboard, scoreboard_palette = adafruit_imageload.load(
    "./art/in_game_scores/scoreboard.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
scoreboard_palette.make_transparent(0)
scoreboard_sprite = displayio.TileGrid(
    scoreboard,
    pixel_shader=scoreboard_palette
)

in_game_score_sprites = []

in_game_score0, in_game_score0_palette = adafruit_imageload.load(
    "./art/in_game_scores/0.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
in_game_score0_palette.make_transparent(0)
in_game_score0_sprite = displayio.TileGrid(
    in_game_score0,
    pixel_shader=in_game_score0_palette
)
in_game_score_sprites.append(in_game_score0_sprite)

in_game_score1, in_game_score1_palette = adafruit_imageload.load(
    "./art/in_game_scores/1.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
in_game_score1_palette.make_transparent(0)
in_game_score1_sprite = displayio.TileGrid(
    in_game_score1,
    pixel_shader=in_game_score1_palette
)
in_game_score_sprites.append(in_game_score1_sprite)

in_game_score2, in_game_score2_palette = adafruit_imageload.load(
    "./art/in_game_scores/2.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
in_game_score2_palette.make_transparent(0)
in_game_score2_sprite = displayio.TileGrid(
    in_game_score2,
    pixel_shader=in_game_score2_palette
)
in_game_score_sprites.append(in_game_score2_sprite)

in_game_score3, in_game_score3_palette = adafruit_imageload.load(
    "./art/in_game_scores/3.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
in_game_score3_palette.make_transparent(0)
in_game_score3_sprite = displayio.TileGrid(
    in_game_score3,
    pixel_shader=in_game_score3_palette
)
in_game_score_sprites.append(in_game_score3_sprite)

in_game_score4, in_game_score4_palette = adafruit_imageload.load(
    "./art/in_game_scores/4.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
in_game_score4_palette.make_transparent(0)
in_game_score4_sprite = displayio.TileGrid(
    in_game_score4,
    pixel_shader=in_game_score4_palette
)
in_game_score_sprites.append(in_game_score4_sprite)

in_game_score5, in_game_score5_palette = adafruit_imageload.load(
    "./art/in_game_scores/5.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
in_game_score5_palette.make_transparent(0)
in_game_score5_sprite = displayio.TileGrid(
    in_game_score5,
    pixel_shader=in_game_score5_palette
)
in_game_score_sprites.append(in_game_score5_sprite)

in_game_score6, in_game_score6_palette = adafruit_imageload.load(
    "./art/in_game_scores/6.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
in_game_score6_palette.make_transparent(0)
in_game_score6_sprite = displayio.TileGrid(
    in_game_score6,
    pixel_shader=in_game_score6_palette
)
in_game_score_sprites.append(in_game_score6_sprite)

in_game_score7, in_game_score7_palette = adafruit_imageload.load(
    "./art/in_game_scores/7.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
in_game_score7_palette.make_transparent(0)
in_game_score7_sprite = displayio.TileGrid(
    in_game_score7,
    pixel_shader=in_game_score7_palette
)
in_game_score_sprites.append(in_game_score7_sprite)

in_game_score8, in_game_score8_palette = adafruit_imageload.load(
    "./art/in_game_scores/8.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
in_game_score8_palette.make_transparent(0)
in_game_score8_sprite = displayio.TileGrid(
    in_game_score8,
    pixel_shader=in_game_score8_palette
)
in_game_score_sprites.append(in_game_score8_sprite)

in_game_score9, in_game_score9_palette = adafruit_imageload.load(
    "./art/in_game_scores/9.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
in_game_score9_palette.make_transparent(0)
in_game_score9_sprite = displayio.TileGrid(
    in_game_score9,
    pixel_shader=in_game_score9_palette
)
in_game_score_sprites.append(in_game_score9_sprite)

in_game_score10, in_game_score10_palette = adafruit_imageload.load(
    "./art/in_game_scores/10.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
in_game_score10_palette.make_transparent(0)
in_game_score10_sprite = displayio.TileGrid(
    in_game_score10,
    pixel_shader=in_game_score10_palette
)
in_game_score_sprites.append(in_game_score10_sprite)

in_game_score11, in_game_score11_palette = adafruit_imageload.load(
    "./art/in_game_scores/11.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
in_game_score11_palette.make_transparent(0)
in_game_score11_sprite = displayio.TileGrid(
    in_game_score11,
    pixel_shader=in_game_score11_palette
)
in_game_score_sprites.append(in_game_score11_sprite)

in_game_score12, in_game_score12_palette = adafruit_imageload.load(
    "./art/in_game_scores/12.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
in_game_score12_palette.make_transparent(0)
in_game_score12_sprite = displayio.TileGrid(
    in_game_score12,
    pixel_shader=in_game_score12_palette
)
in_game_score_sprites.append(in_game_score12_sprite)

# User rabbit inits
user_rabbits_left = []
user_rabbits_right = []

user_rabbit, user_rabbit_palette = adafruit_imageload.load(
    "./art/user_rabbit/neutral.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
user_rabbit_palette.make_transparent(0)
user_rabbit_sprite = displayio.TileGrid(
    user_rabbit,
    pixel_shader=user_rabbit_palette
)

user_rabbit_bob, user_rabbit_bob_palette = adafruit_imageload.load(
    "./art/user_rabbit/bob.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
user_rabbit_bob_palette.make_transparent(0)
user_rabbit_bob_sprite = displayio.TileGrid(
    user_rabbit_bob,
    pixel_shader=user_rabbit_bob_palette
)

user_rabbit_duck, user_rabbit_duck_palette = adafruit_imageload.load(
    "./art/user_rabbit/duck.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
user_rabbit_duck_palette.make_transparent(0)
user_rabbit_duck_sprite = displayio.TileGrid(
    user_rabbit_duck,
    pixel_shader=user_rabbit_duck_palette
)

user_rabbit_back, user_rabbit_back_palette = adafruit_imageload.load(
    "./art/user_rabbit/back.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
user_rabbit_back_palette.make_transparent(0)
user_rabbit_back_sprite = displayio.TileGrid(
    user_rabbit_back,
    pixel_shader=user_rabbit_back_palette
)

user_rabbit_left1, user_rabbit_left1_palette = adafruit_imageload.load(
    "./art/user_rabbit/left1.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
user_rabbit_left1_palette.make_transparent(0)
user_rabbit_left1_sprite = displayio.TileGrid(
    user_rabbit_left1,
    pixel_shader=user_rabbit_left1_palette
)
user_rabbits_left.append(user_rabbit_left1_sprite)

user_rabbit_left2, user_rabbit_left2_palette = adafruit_imageload.load(
    "./art/user_rabbit/left2.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
user_rabbit_left2_palette.make_transparent(0)
user_rabbit_left2_sprite = displayio.TileGrid(
    user_rabbit_left2,
    pixel_shader=user_rabbit_left2_palette
)
user_rabbits_left.append(user_rabbit_left2_sprite)

user_rabbit_left3, user_rabbit_left3_palette = adafruit_imageload.load(
    "./art/user_rabbit/left3.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
user_rabbit_left3_palette.make_transparent(0)
user_rabbit_left3_sprite = displayio.TileGrid(
    user_rabbit_left3,
    pixel_shader=user_rabbit_left3_palette
)
user_rabbits_left.append(user_rabbit_left3_sprite)

user_rabbit_left4, user_rabbit_left4_palette = adafruit_imageload.load(
    "./art/user_rabbit/left4.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
user_rabbit_left4_palette.make_transparent(0)
user_rabbit_left4_sprite = displayio.TileGrid(
    user_rabbit_left4,
    pixel_shader=user_rabbit_left4_palette
)
user_rabbits_left.append(user_rabbit_left4_sprite)

user_rabbit_right1, user_rabbit_right1_palette = adafruit_imageload.load(
    "./art/user_rabbit/right1.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
user_rabbit_right1_palette.make_transparent(0)
user_rabbit_right1_sprite = displayio.TileGrid(
    user_rabbit_right1,
    pixel_shader=user_rabbit_right1_palette
)
user_rabbits_right.append(user_rabbit_right1_sprite)

user_rabbit_right2, user_rabbit_right2_palette = adafruit_imageload.load(
    "./art/user_rabbit/right2.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
user_rabbit_right2_palette.make_transparent(0)
user_rabbit_right2_sprite = displayio.TileGrid(
    user_rabbit_right2,
    pixel_shader=user_rabbit_right2_palette
)
user_rabbits_right.append(user_rabbit_right2_sprite)

user_rabbit_right3, user_rabbit_right3_palette = adafruit_imageload.load(
    "./art/user_rabbit/right3.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
user_rabbit_right3_palette.make_transparent(0)
user_rabbit_right3_sprite = displayio.TileGrid(
    user_rabbit_right3,
    pixel_shader=user_rabbit_right3_palette
)
user_rabbits_right.append(user_rabbit_right3_sprite)

user_rabbit_right4, user_rabbit_right4_palette = adafruit_imageload.load(
    "./art/user_rabbit/right4.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
user_rabbit_right4_palette.make_transparent(0)
user_rabbit_right4_sprite = displayio.TileGrid(
    user_rabbit_right4,
    pixel_shader=user_rabbit_right4_palette
)
user_rabbits_right.append(user_rabbit_right4_sprite)

# Model rabbit inits
model_rabbits_left = []
model_rabbits_right = []

model_rabbit, model_rabbit_palette = adafruit_imageload.load(
    "./art/model_rabbit/neutral.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
model_rabbit_palette.make_transparent(0)
model_rabbit_sprite = displayio.TileGrid(
    model_rabbit,
    pixel_shader=model_rabbit_palette
)

model_rabbit_bob, model_rabbit_bob_palette = adafruit_imageload.load(
    "./art/model_rabbit/bob.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
model_rabbit_bob_palette.make_transparent(0)
model_rabbit_bob_sprite = displayio.TileGrid(
    model_rabbit_bob,
    pixel_shader=model_rabbit_bob_palette
)

model_rabbit_duck, model_rabbit_duck_palette = adafruit_imageload.load(
    "./art/model_rabbit/duck.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
model_rabbit_duck_palette.make_transparent(0)
model_rabbit_duck_sprite = displayio.TileGrid(
    model_rabbit_duck,
    pixel_shader=model_rabbit_duck_palette
)

model_rabbit_back, model_rabbit_back_palette = adafruit_imageload.load(
    "./art/model_rabbit/back.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
model_rabbit_back_palette.make_transparent(0)
model_rabbit_back_sprite = displayio.TileGrid(
    model_rabbit_back,
    pixel_shader=model_rabbit_back_palette
)

model_rabbit_left1, model_rabbit_left1_palette = adafruit_imageload.load(
    "./art/model_rabbit/left1.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
model_rabbit_left1_palette.make_transparent(0)
model_rabbit_left1_sprite = displayio.TileGrid(
    model_rabbit_left1,
    pixel_shader=model_rabbit_left1_palette
)
model_rabbits_left.append(model_rabbit_left1_sprite)

model_rabbit_left2, model_rabbit_left2_palette = adafruit_imageload.load(
    "./art/model_rabbit/left2.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
model_rabbit_left2_palette.make_transparent(0)
model_rabbit_left2_sprite = displayio.TileGrid(
    model_rabbit_left2,
    pixel_shader=model_rabbit_left2_palette
)
model_rabbits_left.append(model_rabbit_left2_sprite)

model_rabbit_left3, model_rabbit_left3_palette = adafruit_imageload.load(
    "./art/model_rabbit/left3.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
model_rabbit_left3_palette.make_transparent(0)
model_rabbit_left3_sprite = displayio.TileGrid(
    model_rabbit_left3,
    pixel_shader=model_rabbit_left3_palette
)
model_rabbits_left.append(model_rabbit_left3_sprite)

model_rabbit_left4, model_rabbit_left4_palette = adafruit_imageload.load(
    "./art/model_rabbit/left4.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
model_rabbit_left4_palette.make_transparent(0)
model_rabbit_left4_sprite = displayio.TileGrid(
    model_rabbit_left4,
    pixel_shader=model_rabbit_left4_palette
)
model_rabbits_left.append(model_rabbit_left4_sprite)

model_rabbit_right1, model_rabbit_right1_palette = adafruit_imageload.load(
    "./art/model_rabbit/right1.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
model_rabbit_right1_palette.make_transparent(0)
model_rabbit_right1_sprite = displayio.TileGrid(
    model_rabbit_right1,
    pixel_shader=model_rabbit_right1_palette
)
model_rabbits_right.append(model_rabbit_right1_sprite)

model_rabbit_right2, model_rabbit_right2_palette = adafruit_imageload.load(
    "./art/model_rabbit/right2.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
model_rabbit_right2_palette.make_transparent(0)
model_rabbit_right2_sprite = displayio.TileGrid(
    model_rabbit_right2,
    pixel_shader=model_rabbit_right2_palette
)
model_rabbits_right.append(model_rabbit_right2_sprite)

model_rabbit_right3, model_rabbit_right3_palette = adafruit_imageload.load(
    "./art/model_rabbit/right3.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
model_rabbit_right3_palette.make_transparent(0)
model_rabbit_right3_sprite = displayio.TileGrid(
    model_rabbit_right3,
    pixel_shader=model_rabbit_right3_palette
)
model_rabbits_right.append(model_rabbit_right3_sprite)

model_rabbit_right4, model_rabbit_right4_palette = adafruit_imageload.load(
    "./art/model_rabbit/right4.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
model_rabbit_right4_palette.make_transparent(0)
model_rabbit_right4_sprite = displayio.TileGrid(
    model_rabbit_right4,
    pixel_shader=model_rabbit_right4_palette
)
model_rabbits_right.append(model_rabbit_right4_sprite)

beat_signs = []
beat_signs1, beat_signs1_palette = adafruit_imageload.load(
    "./art/beat_signs/1.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
beat_signs1_palette.make_transparent(0)
beat_signs1_sprite = displayio.TileGrid(
    beat_signs1,
    pixel_shader=beat_signs1_palette
)
beat_signs.append(beat_signs1_sprite)

beat_signs2, beat_signs2_palette = adafruit_imageload.load(
    "./art/beat_signs/2.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
beat_signs2_palette.make_transparent(0)
beat_signs2_sprite = displayio.TileGrid(
    beat_signs2,
    pixel_shader=beat_signs2_palette
)
beat_signs.append(beat_signs2_sprite)

beat_signs3, beat_signs3_palette = adafruit_imageload.load(
    "./art/beat_signs/3.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
beat_signs3_palette.make_transparent(0)
beat_signs3_sprite = displayio.TileGrid(
    beat_signs3,
    pixel_shader=beat_signs3_palette
)
beat_signs.append(beat_signs3_sprite)

stage_complete_bg = displayio.OnDiskBitmap("./art/stage_complete.bmp")
stage_complete_bg_sprite = displayio.TileGrid(
    stage_complete_bg,
    pixel_shader=stage_complete_bg.pixel_shader
)

endgame_options, endgame_options_palette = adafruit_imageload.load(
    "./art/menu/endgame/options.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
endgame_options_palette.make_transparent(0)
endgame_options_sprite = displayio.TileGrid(
    endgame_options,
    pixel_shader=endgame_options_palette
)

endgame_quit, endgame_quit_palette = adafruit_imageload.load(
    "./art/menu/endgame/quit.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
endgame_quit_palette.make_transparent(0)
endgame_quit_sprite = displayio.TileGrid(
    endgame_quit,
    pixel_shader=endgame_quit_palette
)

endgame_restart, endgame_restart_palette = adafruit_imageload.load(
    "./art/menu/endgame/restart.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
endgame_restart_palette.make_transparent(0)
endgame_restart_sprite = displayio.TileGrid(
    endgame_restart,
    pixel_shader=endgame_restart_palette
)

end_game_score_sprites = []

end_game_score0, end_game_score0_palette = adafruit_imageload.load(
    "./art/end_game_scores/0.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
end_game_score0_palette.make_transparent(0)
end_game_score0_sprite = displayio.TileGrid(
    end_game_score0,
    pixel_shader=end_game_score0_palette
)
end_game_score_sprites.append(end_game_score0_sprite)

end_game_score1, end_game_score1_palette = adafruit_imageload.load(
    "./art/end_game_scores/1.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
end_game_score1_palette.make_transparent(0)
end_game_score1_sprite = displayio.TileGrid(
    end_game_score1,
    pixel_shader=end_game_score1_palette
)
end_game_score_sprites.append(end_game_score1_sprite)

end_game_score2, end_game_score2_palette = adafruit_imageload.load(
    "./art/end_game_scores/2.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
end_game_score2_palette.make_transparent(0)
end_game_score2_sprite = displayio.TileGrid(
    end_game_score2,
    pixel_shader=end_game_score2_palette
)
end_game_score_sprites.append(end_game_score2_sprite)

end_game_score3, end_game_score3_palette = adafruit_imageload.load(
    "./art/end_game_scores/3.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
end_game_score3_palette.make_transparent(0)
end_game_score3_sprite = displayio.TileGrid(
    end_game_score3,
    pixel_shader=end_game_score3_palette
)
end_game_score_sprites.append(end_game_score3_sprite)

end_game_score4, end_game_score4_palette = adafruit_imageload.load(
    "./art/end_game_scores/4.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
end_game_score4_palette.make_transparent(0)
end_game_score4_sprite = displayio.TileGrid(
    end_game_score4,
    pixel_shader=end_game_score4_palette
)
end_game_score_sprites.append(end_game_score4_sprite)

end_game_score5, end_game_score5_palette = adafruit_imageload.load(
    "./art/end_game_scores/5.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
end_game_score5_palette.make_transparent(0)
end_game_score5_sprite = displayio.TileGrid(
    end_game_score5,
    pixel_shader=end_game_score5_palette
)
end_game_score_sprites.append(end_game_score5_sprite)

end_game_score6, end_game_score6_palette = adafruit_imageload.load(
    "./art/end_game_scores/6.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
end_game_score6_palette.make_transparent(0)
end_game_score6_sprite = displayio.TileGrid(
    end_game_score6,
    pixel_shader=end_game_score6_palette
)
end_game_score_sprites.append(end_game_score6_sprite)

end_game_score7, end_game_score7_palette = adafruit_imageload.load(
    "./art/end_game_scores/7.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
end_game_score7_palette.make_transparent(0)
end_game_score7_sprite = displayio.TileGrid(
    end_game_score7,
    pixel_shader=end_game_score7_palette
)
end_game_score_sprites.append(end_game_score7_sprite)

end_game_score8, end_game_score8_palette = adafruit_imageload.load(
    "./art/end_game_scores/8.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
end_game_score8_palette.make_transparent(0)
end_game_score8_sprite = displayio.TileGrid(
    end_game_score8,
    pixel_shader=end_game_score8_palette
)
end_game_score_sprites.append(end_game_score8_sprite)

end_game_score9, end_game_score9_palette = adafruit_imageload.load(
    "./art/end_game_scores/9.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
end_game_score9_palette.make_transparent(0)
end_game_score9_sprite = displayio.TileGrid(
    end_game_score9,
    pixel_shader=end_game_score9_palette
)
end_game_score_sprites.append(end_game_score9_sprite)

end_game_score10, end_game_score10_palette = adafruit_imageload.load(
    "./art/end_game_scores/10.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
end_game_score10_palette.make_transparent(0)
end_game_score10_sprite = displayio.TileGrid(
    end_game_score10,
    pixel_shader=end_game_score10_palette
)
end_game_score_sprites.append(end_game_score10_sprite)

end_game_score11, end_game_score11_palette = adafruit_imageload.load(
    "./art/end_game_scores/11.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
end_game_score11_palette.make_transparent(0)
end_game_score11_sprite = displayio.TileGrid(
    end_game_score11,
    pixel_shader=end_game_score11_palette
)
end_game_score_sprites.append(end_game_score11_sprite)

end_game_score12, end_game_score12_palette = adafruit_imageload.load(
    "./art/end_game_scores/12.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
end_game_score12_palette.make_transparent(0)
end_game_score12_sprite = displayio.TileGrid(
    end_game_score12,
    pixel_shader=end_game_score12_palette
)
end_game_score_sprites.append(end_game_score12_sprite)

perfect_stage, perfect_stage_palette = adafruit_imageload.load(
    "./art/perfect_stage.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
perfect_stage_palette.make_transparent(0)
perfect_stage_sprite = displayio.TileGrid(
    perfect_stage,
    pixel_shader=perfect_stage_palette
)

confetti = []
confetti1, confetti1_palette = adafruit_imageload.load(
    "./art/confetti/1.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
confetti1_palette.make_transparent(0)
confetti1_sprite = displayio.TileGrid(
    confetti1,
    pixel_shader=confetti1_palette
)
confetti.append(confetti1_sprite)

confetti2, confetti2_palette = adafruit_imageload.load(
    "./art/confetti/2.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
confetti2_palette.make_transparent(0)
confetti2_sprite = displayio.TileGrid(
    confetti2,
    pixel_shader=confetti2_palette
)
confetti.append(confetti2_sprite)

confetti3, confetti3_palette = adafruit_imageload.load(
    "./art/confetti/3.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
confetti3_palette.make_transparent(0)
confetti3_sprite = displayio.TileGrid(
    confetti3,
    pixel_shader=confetti3_palette
)
confetti.append(confetti3_sprite)

confetti4, confetti4_palette = adafruit_imageload.load(
    "./art/confetti/4.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
confetti4_palette.make_transparent(0)
confetti4_sprite = displayio.TileGrid(
    confetti4,
    pixel_shader=confetti4_palette
)
confetti.append(confetti4_sprite)

miss, miss_palette = adafruit_imageload.load(
    "./art/words/miss.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
miss_palette.make_transparent(0)
miss_sprite = displayio.TileGrid(
    miss,
    pixel_shader=miss_palette
)

good, good_palette = adafruit_imageload.load(
    "./art/words/good.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
good_palette.make_transparent(0)
good_sprite = displayio.TileGrid(
    good,
    pixel_shader=good_palette
)

great, great_palette = adafruit_imageload.load(
    "./art/words/great.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
great_palette.make_transparent(0)
great_sprite = displayio.TileGrid(
    great,
    pixel_shader=great_palette
)

perfect, perfect_palette = adafruit_imageload.load(
    "./art/words/perfect.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
perfect_palette.make_transparent(0)
perfect_sprite = displayio.TileGrid(
    perfect,
    pixel_shader=perfect_palette
)

# Menu setup
menu = displayio.OnDiskBitmap("./art/menu/menu.bmp")
menu_sprite = displayio.TileGrid(
    menu,
    pixel_shader=menu.pixel_shader
)

options, options_palette = adafruit_imageload.load(
    "./art/menu/options.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
options_palette.make_transparent(0)
options_sprite = displayio.TileGrid(
    options,
    pixel_shader=options_palette
)

back_to_game, back_to_game_palette = adafruit_imageload.load(
    "./art/menu/back_to_game.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
back_to_game_palette.make_transparent(0)
back_to_game_sprite = displayio.TileGrid(
    back_to_game,
    pixel_shader=back_to_game_palette
)

restart, restart_palette = adafruit_imageload.load(
    "./art/menu/restart.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
restart_palette.make_transparent(0)
restart_sprite = displayio.TileGrid(
    restart,
    pixel_shader=restart_palette
)

how_to_play, how_to_play_palette = adafruit_imageload.load(
    "./art/menu/how_to_play.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
how_to_play_palette.make_transparent(0)
how_to_play_sprite = displayio.TileGrid(
    how_to_play,
    pixel_shader=how_to_play_palette
)

difficulty, difficulty_palette = adafruit_imageload.load(
    "./art/menu/difficulty.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
difficulty_palette.make_transparent(0)
difficulty_sprite = displayio.TileGrid(
    difficulty,
    pixel_shader=difficulty_palette
)

menu_quit, menu_quit_palette = adafruit_imageload.load(
    "./art/menu/quit.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
menu_quit_palette.make_transparent(0)
menu_quit_sprite = displayio.TileGrid(
    menu_quit,
    pixel_shader=menu_quit_palette
)

qr, qr_palette = adafruit_imageload.load(
    "./qr.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette
)
qr_palette.make_transparent(0)
qr_sprite = displayio.TileGrid(
    qr,
    pixel_shader=qr_palette
)

# Screen settings
set_home_screen = True
set_difficulty_screen = False
set_menu_screen = False
set_game_screen = False
set_stage_complete_screen = False
set_how_to_play_screen = False
level = "easy"

# Music settings
music_loaded = False
song_pos = 0
song_bpm = 120
song_pos_offset = 0

# Pose indexes
model_neutral_pose_index = [22, 23]
model_left_pose_index = [14, 15, 16, 17]
model_right_pose_index = [18, 19, 20, 21]
user_neutral_pose_index = [12, 13]
user_left_pose_index = [4, 5, 6, 7]
user_right_pose_index = [8, 9, 10, 11]
random_pose_index = 0
random_pose_index_timer = 0

# Score settings
user_lock = False # To make sure the user doesn't keep holding down a button
rating_on = False
rating_on_timer = 0
num_song_timestamps = 0
current_score = 0
percentage_score = 0
perfects = 0
greats = 0
goods = 0
misses = 0

endgame_option = "restart"
menu_option = "back_to_game"

confetti_timer = 0

# Posing timestamps for songs
model_level_neutral = []
model_level_left = []
model_level_right = []
model_level_random = []

user_level_neutral = []
user_level_left = []
user_level_right = []
user_level_random = []

all_level_timestamps = []

model_easy_take_a_stab_neutral = [12000, 21000, 33000]
model_easy_take_a_stab_left = [4000, 16000, 19000, 25000, 37000]
model_easy_take_a_stab_right = [8000, 27000, 35000]
model_easy_take_a_stab_random = [23000, 29000, 31000]

user_easy_take_a_stab_neutral = [14000, 22000, 34000]
user_easy_take_a_stab_left = [6000, 18000, 20000, 26000, 38000]
user_easy_take_a_stab_right = [10000, 28000, 36000]
user_easy_take_a_stab_random = [24000, 30000, 32000]

model_normal_copycat_curry_neutral = [5500, 13500, 28500, 41500, 47500]
model_normal_copycat_curry_left = [9500, 24500, 40500]
model_normal_copycat_curry_right = [17500, 30500, 37000, 47000]
model_normal_copycat_curry_random = [22500, 26500, 32500, 36500, 41000, 44500, 45500, 46500]

user_normal_copycat_curry_neutral = [7500, 15500, 29500, 43500, 51500]
user_normal_copycat_curry_left = [11500, 25500, 42500]
user_normal_copycat_curry_right = [19500, 31500, 39000, 51000]
user_normal_copycat_curry_random = [23500, 27500, 33500, 38500, 43000, 48500, 49500, 50500]

model_hard_time_to_shine_neutral = [7000, 16800, 31000, 35350, 40500, 42000]
model_hard_time_to_shine_left = [5000, 16400, 23000, 39000]
model_hard_time_to_shine_right = [9000, 15000, 23350, 42500]
model_hard_time_to_shine_random = [8000, 16000, 27000, 27350, 31350, 35000, 40000, 41000]

user_hard_time_to_shine_neutral = [11000, 20800, 33000, 37350, 44500, 46000]
user_hard_time_to_shine_left = [6000, 20400, 25000, 43000]
user_hard_time_to_shine_right = [13000, 19000, 25350, 46500]
user_hard_time_to_shine_random = [12000, 20000, 29000, 29350, 33350, 37000, 44000, 45000]

home_screen = displayio.Group()
home_screen.append(home_bg_sprite)
home_screen.append(user_rabbit_sprite)
home_screen.append(button_to_start_sprite)

difficulty_screen = displayio.Group()
difficulty_screen.append(lightened_bg_sprite)
difficulty_screen.append(difficulties_sprite)
difficulty_screen.append(select_difficulty_sprite)
difficulty_screen.append(easy_sprite)
difficulty_screen[3].hidden = False
difficulty_screen.append(normal_sprite)
difficulty_screen[4].hidden = True
difficulty_screen.append(hard_sprite)
difficulty_screen[5].hidden = True

game_screen = displayio.Group()
game_screen.append(bg_sprite)
game_screen.append(user_rabbit_sprite)
game_screen.append(model_rabbit_sprite)
game_screen.append(scoreboard_sprite)
for rabbit in user_rabbits_left:
    game_screen.append(rabbit)
    game_screen[-1].hidden = True
for rabbit in user_rabbits_right:
    game_screen.append(rabbit)
    game_screen[-1].hidden = True
game_screen.append(user_rabbit_back_sprite)
game_screen[-1].hidden = True
game_screen.append(user_rabbit_duck_sprite)
game_screen[-1].hidden = True
for rabbit in model_rabbits_left:
    game_screen.append(rabbit)
    game_screen[-1].hidden = True
for rabbit in model_rabbits_right:
    game_screen.append(rabbit)
    game_screen[-1].hidden = True
game_screen.append(model_rabbit_back_sprite)
game_screen[-1].hidden = True
game_screen.append(model_rabbit_duck_sprite)
game_screen[-1].hidden = True

game_screen.append(user_rabbit_bob_sprite)
game_screen[-1].hidden = True
game_screen.append(model_rabbit_bob_sprite)
game_screen[-1].hidden = True

game_screen.append(miss_sprite)
game_screen[-1].hidden = True
game_screen.append(good_sprite)
game_screen[-1].hidden = True
game_screen.append(great_sprite)
game_screen[-1].hidden = True
game_screen.append(perfect_sprite)
game_screen[-1].hidden = True

for beat_sign in beat_signs:
    game_screen.append(beat_sign)
    game_screen[-1].hidden = True
for score in in_game_score_sprites:
    game_screen.append(score)
    game_screen[-1].hidden = True
game_screen[-13].hidden = False

stage_complete_screen = displayio.Group()
stage_complete_screen.append(stage_complete_bg_sprite)
stage_complete_screen.append(user_rabbit_sprite)
stage_complete_screen.append(endgame_options_sprite)
stage_complete_screen.append(endgame_restart_sprite)
stage_complete_screen[-1].hidden = False
stage_complete_screen.append(endgame_quit_sprite)
stage_complete_screen[-1].hidden = True
stage_complete_screen.append(perfect_stage_sprite)
stage_complete_screen[-1].hidden = True
for confetti in confetti:
    stage_complete_screen.append(confetti)
    stage_complete_screen[-1].hidden = True

for score in end_game_score_sprites:
    stage_complete_screen.append(score)
    stage_complete_screen[-1].hidden = True

menu_screen = displayio.Group()
menu_screen.append(menu_sprite)
menu_screen.append(options_sprite)
menu_screen.append(back_to_game_sprite)
menu_screen.append(restart_sprite)
menu_screen[-1].hidden = True
menu_screen.append(how_to_play_sprite)
menu_screen[-1].hidden = True
menu_screen.append(difficulty_sprite)
menu_screen[-1].hidden = True
menu_screen.append(menu_quit_sprite)
menu_screen[-1].hidden = True

how_to_play_screen = displayio.Group()
how_to_play_screen.append(lightened_bg_sprite)
how_to_play_screen.append(qr_sprite)

def change_difficulty(level_difficulty):
    if level_difficulty == "easy":
        difficulty_screen[3].hidden = True
        difficulty_screen[4].hidden = False
        level_difficulty = "normal"
    elif level_difficulty == "normal":
        difficulty_screen[4].hidden = True
        difficulty_screen[5].hidden = False
        level_difficulty = "hard"
    elif level_difficulty == "hard":
        difficulty_screen[5].hidden = True
        difficulty_screen[3].hidden = False
        level_difficulty = "easy"
    time.sleep(0.15)
    return level_difficulty

def change_menu_option(option):
    if option == "back_to_game":
        menu_screen[2].hidden = True
        menu_screen[3].hidden = False
        option = "restart"
    elif option == "restart":
        menu_screen[3].hidden = True
        menu_screen[4].hidden = False
        option = "how_to_play"
    elif option == "how_to_play":
        menu_screen[4].hidden = True
        menu_screen[5].hidden = False
        option = "difficulty"
    elif option == "difficulty":
        menu_screen[5].hidden = True
        menu_screen[6].hidden = False
        option = "quit"
    elif option == "quit":
        menu_screen[6].hidden = True
        menu_screen[2].hidden = False
        option = "back_to_game"
    time.sleep(0.15)
    return option

def change_endgame_option(option):
    if option == "restart":
        stage_complete_screen[3].hidden = True
        stage_complete_screen[4].hidden = False
        option = "quit"
    elif option == "quit":
        stage_complete_screen[4].hidden = True
        stage_complete_screen[3].hidden = False
        option = "restart"
    time.sleep(0.15)
    return option

def set_poses(level_difficulty):
    global all_level_timestamps, model_level_left, model_level_right, model_level_neutral, model_level_random, user_level_left, user_level_right, user_level_neutral, user_level_random
    if level_difficulty == "easy":
        model_level_left = model_easy_take_a_stab_left
        model_level_right = model_easy_take_a_stab_right
        model_level_neutral = model_easy_take_a_stab_neutral
        model_level_random = model_easy_take_a_stab_random
        user_level_left = user_easy_take_a_stab_left
        user_level_right = user_easy_take_a_stab_right
        user_level_neutral = user_easy_take_a_stab_neutral
        user_level_random = user_easy_take_a_stab_random
    elif level_difficulty == "normal":
        model_level_left = model_normal_copycat_curry_left
        model_level_right = model_normal_copycat_curry_right
        model_level_neutral = model_normal_copycat_curry_neutral
        model_level_random = model_normal_copycat_curry_random
        user_level_left = user_normal_copycat_curry_left
        user_level_right = user_normal_copycat_curry_right
        user_level_neutral = user_normal_copycat_curry_neutral
        user_level_random = user_normal_copycat_curry_random
    elif level_difficulty == "hard":
        model_level_left = model_hard_time_to_shine_left
        model_level_right = model_hard_time_to_shine_right
        model_level_neutral = model_hard_time_to_shine_neutral
        model_level_random = model_hard_time_to_shine_random
        user_level_left = user_hard_time_to_shine_left
        user_level_right = user_hard_time_to_shine_right
        user_level_neutral = user_hard_time_to_shine_neutral
        user_level_random = user_hard_time_to_shine_random

    all_level_timestamps = model_level_left + model_level_right + model_level_neutral + model_level_random + user_level_left + user_level_right + user_level_neutral + user_level_random


def distribute_randoms():
    index = 0
    for timestamp in model_level_random:
        direction = randint(0, 1)
        if direction == 0:
            model_level_left.append(timestamp)
            user_level_left.append(user_level_random[index])
        elif direction == 1:
            model_level_right.append(timestamp)
            user_level_right.append(user_level_random[index])
        index += 1

def set_timestamp_number():
    global num_song_timestamps
    num_song_timestamps = len(model_level_left) + len(model_level_right) + len(model_level_neutral)

def load_music(level_difficulty, offset):
    if level_difficulty == "easy":
        pygame.mixer.music.load("./music/take_a_stab.mp3")
        offset = 100
    elif level_difficulty == "normal":
        pygame.mixer.music.load("./music/copycat_curry.mp3")
        offset = 100
    elif level_difficulty == "hard":
        pygame.mixer.music.load("./music/time_to_shine.mp3")
        offset = 220
    return True, offset

def change_score(rating):
    global current_score, percentage_score, perfects, greats, goods, misses, rating_on
    rating_on = True
    if rating == "perfect":
        perfects += (1/num_song_timestamps)
        percentage_score += (1/num_song_timestamps)
        game_screen[29].hidden = False
    elif rating == "great":
        greats += (1/num_song_timestamps)
        percentage_score += (0.75/num_song_timestamps)
        game_screen[28].hidden = False
    elif rating == "good":
        goods += (1/num_song_timestamps)
        percentage_score += (0.25/num_song_timestamps)
        game_screen[27].hidden = False
    elif rating == "miss":
        misses += (1/num_song_timestamps)
        game_screen[26].hidden = False

    if percentage_score == 1:
        current_score = 12
    elif percentage_score >= 0.98:
        current_score = 11
    elif percentage_score >= 0.95:
        current_score = 10
    elif percentage_score >= 0.90:
        current_score = 9
    elif percentage_score >= 0.75:
        current_score = 8
    elif percentage_score >= 0.5:
        current_score = 7
    elif percentage_score >= 0.25:
        current_score = 6
    elif percentage_score >= 0.20:
        current_score = 5
    elif percentage_score >= 0.15:
        current_score = 4
    elif percentage_score >= 0.10:
        current_score = 3
    elif percentage_score >= 0.05:
        current_score = 2
    elif percentage_score >= 0.01:
        current_score = 1
    elif percentage_score == 0:
        current_score = 0

def restart():
    global current_score, percentage_score, perfects, greats, goods, misses, music_loaded
    current_score = 0
    percentage_score = 0
    perfects = 0
    greats = 0
    goods = 0
    misses = 0
    music_loaded = False

    i = 0
    while i <= 3:
        game_screen[user_left_pose_index[i]].hidden = True
        game_screen[user_right_pose_index[i]].hidden = True
        game_screen[user_neutral_pose_index[int(i / 2)]].hidden = True
        i += 1
    i = 0
    while i <= 12:
        game_screen[-13 + i].hidden = True
        i += 1
    game_screen[26].hidden = True
    game_screen[27].hidden = True
    game_screen[28].hidden = True
    game_screen[29].hidden = True
    game_screen[32].hidden = True
    game_screen[30].hidden = True
    game_screen[31].hidden = True


# Game loop and controls
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    keys = pygame.key.get_pressed()

    if set_home_screen:
        display.show(home_screen)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                set_difficulty_screen = True
                set_home_screen = False
                time.sleep(0.2)
    elif set_difficulty_screen:
        restart()
        display.show(difficulty_screen)
        time.sleep(0.05)
        if keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_2]:
            level = change_difficulty(level)
        if keys[pygame.K_RETURN] or keys[pygame.K_RIGHT] or keys[pygame.K_3]:
            set_difficulty_screen = False
            set_game_screen = True
            set_poses(level)
            distribute_randoms()
            set_timestamp_number()
            time.sleep(0.5)
    elif set_game_screen:
        display.show(game_screen)
        if current_score == 0:
            game_screen[-13].hidden = False
        if (keys[pygame.K_LEFT] and (keys[pygame.K_RIGHT] or keys[pygame.K_UP])) or (keys[pygame.K_UP] and keys[pygame.K_RIGHT]) or (keys[pygame.K_1] and (keys[pygame.K_2] or keys[pygame.K_3])) or (keys[pygame.K_2] and keys[pygame.K_3]):
            set_menu_screen = True
            set_game_screen = False
            time.sleep(0.2)
        if not music_loaded:
            music_loaded, song_pos_offset = load_music(level, song_pos_offset)
            pygame.mixer.music.play(loops=0)
        song_pos = pygame.mixer.music.get_pos() - song_pos_offset

        # Beat signs for both user and model
        # if any(0 <= abs(timestamp - song_pos) <= 50 for timestamp in all_level_timestamps):
        #     game_screen[32].hidden = True
        #     game_screen[30].hidden = True
        #     game_screen[31].hidden = True
        # elif any(0 <= (timestamp - song_pos) <= 550 for timestamp in all_level_timestamps):
        #     game_screen[32].hidden = True
        #     game_screen[31].hidden = True
        #     game_screen[30].hidden = False
        # elif any(0 <= (timestamp - song_pos) <= 1050 for timestamp in all_level_timestamps):
        #     game_screen[32].hidden = True
        #     game_screen[30].hidden = True
        #     game_screen[31].hidden = False
        # elif any(0 <= (timestamp - song_pos) <= 1550 for timestamp in all_level_timestamps):
        #     game_screen[30].hidden = True
        #     game_screen[31].hidden = True
        #     game_screen[32].hidden = False

        # Beat signs for only user
        if any(0 <= abs(timestamp - song_pos) <= 50 for timestamp in all_level_timestamps):
            game_screen[32].hidden = True
            game_screen[30].hidden = True
            game_screen[31].hidden = True
        elif any(0 <= (timestamp - song_pos) <= 550 for timestamp in (user_level_left + user_level_neutral + user_level_right)):
            game_screen[32].hidden = True
            game_screen[31].hidden = True
            game_screen[30].hidden = False
        elif any(0 <= (timestamp - song_pos) <= 1050 for timestamp in (user_level_left + user_level_neutral + user_level_right)):
            game_screen[32].hidden = True
            game_screen[30].hidden = True
            game_screen[31].hidden = False
        elif any(0 <= (timestamp - song_pos) <= 1550 for timestamp in (user_level_left + user_level_neutral + user_level_right)):
            game_screen[30].hidden = True
            game_screen[31].hidden = True
            game_screen[32].hidden = False

        if any(abs(song_pos - timestamp) <= 20 or (0 <= (song_pos - timestamp) < 200) for timestamp in model_level_left):
            if random_pose_index_timer == 0:
                random_pose_index = randint(0, 3)
                random_pose_index_timer += 1
            game_screen[2].hidden = True
            game_screen[model_left_pose_index[random_pose_index]].hidden = False
            if song_pos % 500 <= 50:
                game_screen[1].hidden = True
                if not rating_on:
                    game_screen[24].hidden = False
        elif any(abs(song_pos - timestamp) <= 20 or (0 <= (song_pos - timestamp) < 200) for timestamp in model_level_right):
            if random_pose_index_timer == 0:
                random_pose_index = randint(0, 3)
                random_pose_index_timer += 1
            game_screen[2].hidden = True
            game_screen[model_right_pose_index[random_pose_index]].hidden = False
            if song_pos % 500 <= 50:
                game_screen[1].hidden = True
                if not rating_on:
                    game_screen[24].hidden = False
        elif any(abs(song_pos - timestamp) <= 20 or (0 <= (song_pos - timestamp) < 200) for timestamp in model_level_neutral):
            if random_pose_index_timer == 0:
                random_pose_index = randint(0, 3)
                random_pose_index_timer += 1
            game_screen[2].hidden = True
            game_screen[model_neutral_pose_index[int(random_pose_index/2)]].hidden = False
            if song_pos % 500 <= 50:
                game_screen[1].hidden = True
                if not rating_on:
                    game_screen[24].hidden = False
        elif song_pos % 500 <= 50:
            game_screen[2].hidden = True
            game_screen[25].hidden = False
            game_screen[1].hidden = True
            if not rating_on:
                game_screen[24].hidden = False
            i = 0
            while i <= 3:
                game_screen[model_left_pose_index[i]].hidden = True
                game_screen[model_right_pose_index[i]].hidden = True
                game_screen[model_neutral_pose_index[int(i / 2)]].hidden = True
                i += 1
        else:
            game_screen[24].hidden = True
            game_screen[25].hidden = True
            if not rating_on:
                game_screen[1].hidden = False
            game_screen[2].hidden = False
            i = 0
            while i <= 3:
                game_screen[model_left_pose_index[i]].hidden = True
                game_screen[model_right_pose_index[i]].hidden = True
                game_screen[model_neutral_pose_index[int(i / 2)]].hidden = True
                i += 1
        if not rating_on and not user_lock:
            if keys[pygame.K_UP] or keys[pygame.K_2]:
                if any(abs(song_pos - timestamp) <= 150 for timestamp in user_level_neutral):
                    change_score("perfect")
                elif any(abs(song_pos - timestamp) <= 200 for timestamp in user_level_neutral):
                    change_score("great")
                elif any(abs(song_pos - timestamp) <= 300 for timestamp in user_level_neutral):
                    change_score("good")
                else:
                    change_score("miss")
                if current_score != 0:
                    game_screen[-13 + current_score - 1].hidden = True
                    game_screen[-13].hidden = True
                    game_screen[-13 + current_score].hidden = False
                elif current_score == 0:
                    game_screen[-13].hidden = False
                game_screen[1].hidden = True
                game_screen[24].hidden = True
                game_screen[user_neutral_pose_index[int(random_pose_index / 2)]].hidden = False
            elif keys[pygame.K_LEFT] or keys[pygame.K_1]:
                if any(abs(song_pos - timestamp) <= 150 for timestamp in user_level_left):
                    change_score("perfect")
                elif any(abs(song_pos - timestamp) <= 200 for timestamp in user_level_left):
                    change_score("great")
                elif any(abs(song_pos - timestamp) <= 300 for timestamp in user_level_left):
                    change_score("good")
                else:
                    change_score("miss")
                if current_score != 0:
                    game_screen[-13 + current_score - 1].hidden = True
                    game_screen[-13].hidden = True
                    game_screen[-13 + current_score].hidden = False
                elif current_score == 0:
                    game_screen[-13].hidden = False
                game_screen[user_left_pose_index[random_pose_index]].hidden = False
                game_screen[1].hidden = True
                game_screen[24].hidden = True
            elif keys[pygame.K_RIGHT] or keys[pygame.K_3]:
                if any(abs(song_pos - timestamp) <= 150 for timestamp in user_level_right):
                    change_score("perfect")
                elif any(abs(song_pos - timestamp) <= 200 for timestamp in user_level_right):
                    change_score("great")
                elif any(abs(song_pos - timestamp) <= 300 for timestamp in user_level_right):
                    change_score("good")
                else:
                    change_score("miss")
                if current_score != 0:
                    game_screen[-13 + current_score - 1].hidden = True
                    game_screen[-13].hidden = True
                    game_screen[-13 + current_score].hidden = False
                elif current_score == 0:
                    game_screen[-13].hidden = False
                game_screen[user_right_pose_index[random_pose_index]].hidden = False
                game_screen[1].hidden = True
                game_screen[24].hidden = True
        if keys[pygame.K_LEFT] or keys[pygame.K_UP] or keys[pygame.K_RIGHT] or keys[pygame.K_1] or keys[pygame.K_2] or keys[pygame.K_3]:
            user_lock = True
        else:
            user_lock = False
        if rating_on:
            rating_on_timer += 1
            if rating_on_timer >= 50:
                rating_on_timer = 0
                rating_on = False
                i = 0
                while i <= 3:
                    game_screen[user_left_pose_index[i]].hidden = True
                    game_screen[user_right_pose_index[i]].hidden = True
                    game_screen[user_neutral_pose_index[int(i / 2)]].hidden = True
                    i += 1

                game_screen[26].hidden = True
                game_screen[27].hidden = True
                game_screen[28].hidden = True
                game_screen[29].hidden = True
        if random_pose_index_timer >= 1:
            random_pose_index_timer += 1
            if random_pose_index_timer >= 150:
                random_pose_index_timer = 0
        time.sleep(0.005)
        if not pygame.mixer.music.get_busy():
            set_stage_complete_screen = True
            set_game_screen = False
            time.sleep(0.2)
    elif set_menu_screen:
        pygame.mixer.music.pause()
        display.show(menu_screen)
        time.sleep(0.05)
        if keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_2]:
            menu_option = change_menu_option(menu_option)
        if keys[pygame.K_RETURN] or keys[pygame.K_RIGHT] or keys[pygame.K_3]:
            if menu_option == "back_to_game":
                set_game_screen = True
                pygame.mixer.music.unpause()
            elif menu_option == "restart":
                restart()
                set_game_screen = True
            elif menu_option == "how_to_play":
                set_how_to_play_screen = True
            elif menu_option == "difficulty":
                set_difficulty_screen = True
            elif menu_option == "quit":
                set_home_screen = True
                restart()
            set_menu_screen = False
            time.sleep(0.2)

    elif set_stage_complete_screen:
        display.show(stage_complete_screen)
        time.sleep(0.05)
        stage_complete_screen[-13 + current_score].hidden = False
        if current_score == 12:
            stage_complete_screen[5].hidden = False
            if confetti_timer > 3:
                confetti_timer = 0
            match confetti_timer:
                case 0:
                    stage_complete_screen[7].hidden = True
                    stage_complete_screen[8].hidden = True
                    stage_complete_screen[9].hidden = True
                    stage_complete_screen[6].hidden = False
                case 1:
                    stage_complete_screen[6].hidden = True
                    stage_complete_screen[8].hidden = True
                    stage_complete_screen[9].hidden = True
                    stage_complete_screen[7].hidden = False
                case 2:
                    stage_complete_screen[6].hidden = True
                    stage_complete_screen[7].hidden = True
                    stage_complete_screen[9].hidden = True
                    stage_complete_screen[8].hidden = False
                case 3:
                    stage_complete_screen[7].hidden = True
                    stage_complete_screen[8].hidden = True
                    stage_complete_screen[6].hidden = True
                    stage_complete_screen[9].hidden = False

            confetti_timer += 0.5

        if keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_2]:
            endgame_option = change_endgame_option(endgame_option)
        if keys[pygame.K_RETURN] or keys[pygame.K_RIGHT] or keys[pygame.K_3]:
            if endgame_option == "restart":
                set_game_screen = True
                set_stage_complete_screen = False
                restart()
            elif endgame_option == "quit":
                set_home_screen = True
                set_stage_complete_screen = False
                restart()
            music_loaded = False
            time.sleep(0.2)
    elif set_how_to_play_screen:
        display.show(how_to_play_screen)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                set_menu_screen = True
                set_how_to_play_screen = False
                time.sleep(0.2)
