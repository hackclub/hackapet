import time
import pygame
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((128, 128))
pygame.display.set_caption("Pee on Trees!")
clock = pygame.time.Clock()

bg1 = pygame.image.load("./Anims/Bg/bg-1.png")
bg2 = pygame.image.load("./Anims/Bg/bg-2.png")
bg3 = pygame.image.load("./Anims/Bg/bg-3.png")
bg4 = pygame.image.load("./Anims/Bg/bg-4.png")
backgrounds = [bg1, bg2, bg3, bg4]

def load_image_with_transparency(filename):
    image = pygame.image.load(filename)
    return image

idle_animation = [load_image_with_transparency(f"./Anims/Idle/idle-{i}.png") for i in range(1, 7)]
walk_animation = [load_image_with_transparency(f"./Anims/Walking/walking-{i}.png") for i in range(1, 7)]

font = pygame.font.SysFont("Arial", 16)

def restart_game():
    return {
        "character_x": 64,
        "character_y": 96,
        "tree_positions": [(10, 96), (108 - 10, 96)],
        "tree_states": [True, True],
        "current_tree": 0,
        "xp": 0,
        "bg_index": 0,
        "start_time": time.time(),
        "current_frame": 0,
        "animation_timer": 0,
        "moving": False,
        "feedback_timer": 0,
    }

game_state = restart_game()
is_game_over = False

running = True
while running:
    screen.fill((0, 0, 0)) 
    current_time = time.time()

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if is_game_over:
                if event.key == K_SPACE:
                    game_state = restart_game()
                    is_game_over = False
            else:
                if event.key == K_LEFT:
                    game_state["character_x"] = max(0, game_state["character_x"] - 10)
                    game_state["moving"] = True
                elif event.key == K_RIGHT:
                    game_state["character_x"] = min(118, game_state["character_x"] + 10)
                    game_state["moving"] = True
                elif event.key == K_SPACE:
                    target_tree_x, target_tree_y = game_state["tree_positions"][game_state["current_tree"]]
                    if (
                        abs(game_state["character_x"] - target_tree_x) < 10
                        and abs(game_state["character_y"] - target_tree_y) < 10
                        and game_state["tree_states"][game_state["current_tree"]]
                    ):
                        game_state["xp"] += 1
                        game_state["tree_states"][game_state["current_tree"]] = False
                        game_state["current_tree"] = 1 - game_state["current_tree"]
                        game_state["feedback_timer"] = 30
                        game_state["tree_states"][game_state["current_tree"]] = True

    if not is_game_over:
        if current_time - game_state["start_time"] > 30:  # 30 sec / scene
            game_state["bg_index"] += 1
            if game_state["bg_index"] >= len(backgrounds):
                is_game_over = True
            else:
                game_state["start_time"] = current_time
                game_state["tree_states"] = [True, True]

        if not is_game_over:
            screen.blit(backgrounds[game_state["bg_index"]], (0, 0))

        game_state["animation_timer"] += clock.get_time()
        if game_state["animation_timer"] > 200:  
            game_state["current_frame"] = (game_state["current_frame"] + 1) % (
                len(walk_animation) if game_state["moving"] else len(idle_animation)
            )
            game_state["animation_timer"] = 0

        current_animation = walk_animation if game_state["moving"] else idle_animation
        screen.blit(current_animation[game_state["current_frame"]], (game_state["character_x"], game_state["character_y"]))
        game_state["moving"] = False  

        if game_state["feedback_timer"] > 0:
            feedback_text = font.render("XP +1!", True, (255, 255, 0))
            screen.blit(feedback_text, (game_state["character_x"], game_state["character_y"] - 20))
            game_state["feedback_timer"] -= 1
    else:
        end_text = font.render(f"Game Over! Total XP: {game_state['xp']}", True, (255, 0, 0))
        restart_text = font.render("Press SPACE to play again!", True, (255, 255, 255))
        screen.blit(end_text, (10, 50))
        screen.blit(restart_text, (10, 70))

    pygame.display.flip()
    clock.tick(30) 

pygame.quit()
