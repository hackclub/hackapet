import time
import displayio

import patch
from blinka_displayio_pygamedisplay import PyGameDisplay
PyGameDisplay._initialize = patch.blinka_pygame_display_initalize_patched
PyGameDisplay.refresh = patch.blinka_pygame_display_pygamerefresh_patched

from sprites.score import Score
from sprites.base import DangerousSprite, AnimatableSprite
from sprites.shelly import Shelly
from runner.base import Runner
from sprites.squid.squid import Squid

GROUND_BITMAP = displayio.OnDiskBitmap("textures/ground.bmp")

def update_dangers(dangers, player, score) -> bool:
    for sprite in dangers:
            if isinstance(sprite, DangerousSprite):
                if sprite.is_dangerous() and sprite.collides_with(player):
                    return True

            if isinstance(sprite, AnimatableSprite):
                sprite.animate()
                if sprite.is_animation_finished():
                    if isinstance(sprite, DangerousSprite):
                        score.increase(sprite.get_score(player))

                    dangers.remove(sprite)
                    continue
    
    return False

def main(runner: Runner):
    ground = displayio.TileGrid(
        GROUND_BITMAP,
        pixel_shader=GROUND_BITMAP.pixel_shader
    )

    player = Shelly()
    dangers = displayio.Group()
    squid = Squid()
    score_text = Score(True)
    peaceful_mode = True
    game_begin_cooldown_frames = 0

    runner.splash.append(ground)
    runner.splash.append(squid)
    runner.splash.append(player)
    runner.splash.append(dangers)
    runner.splash.append(score_text)

    def reset(game_start = False):
        nonlocal peaceful_mode, game_begin_cooldown_frames

        player.center_x = 64
        player.y = -32
        player.x_velocity = 0
        player.y_velocity = 0
        peaceful_mode = True
        score_text.set_high_score_mode(True)
        game_begin_cooldown_frames = 20

        if not game_start:
            squid.reset(score_text.score)
        
        score_text.reset()

        while len(dangers) > 0:
            dangers.pop()

    def start():
        nonlocal peaceful_mode

        score_text.set_high_score_mode(False)
        peaceful_mode = False

    def run_game_loop():
        nonlocal peaceful_mode, game_begin_cooldown_frames

        movement_direction = 0
        if runner.input.left:
            movement_direction -= 1
        
        if runner.input.right:
            movement_direction += 1

        if peaceful_mode:
            if runner.input.left and runner.input.right and \
                game_begin_cooldown_frames == 0:
                start()
            
            game_begin_cooldown_frames = max(0, game_begin_cooldown_frames - 1)

        player_hit = update_dangers(dangers, player, score_text)
        if player_hit:
            reset()
            return

        squid.update(player, dangers, peaceful_mode)

        player.update(movement_direction, runner.input.middle)

    reset(True)

    target_fps = 30
    target_execution_time = 1.0 / target_fps
    while True:
        start_time = time.perf_counter()
        runner.update()

        run_game_loop()

        runner.refresh()
        if runner.check_exit():
            break

        end_time = time.perf_counter()
        process_time = end_time - start_time
        sleep_time = target_execution_time - process_time

        if sleep_time > 0:
            time.sleep(sleep_time)

if __name__ == "__main__":
    from runner.pygame import PygameRunner
    runner = PygameRunner()
    runner.run(main)
