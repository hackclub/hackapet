''' for now, use left and right arrow keys to move the player'''
'''A to restart game, B to kick the ball, C to end game'''

import pygame
import time
import random

pygame.init()
W, H = 128, 128
pygame.display.set_caption("Slay or Save")
clk = pygame.time.Clock()

screen = pygame.display.set_mode((W, H))

def load_img(file):
    return pygame.image.load(file)

start_img = load_img("starte.bmp")
screen.blit(start_img, (0, 0))
pygame.display.update()
time.sleep(4)

bg_files = ["bg_1.bmp", "bg_2.bmp", "bg_3.bmp"]
bgs = [load_img(f) for f in bg_files]
bg_idx = 0

p_imgs = [load_img("player_idle.bmp"), load_img("player_kick_1.bmp"), load_img("player_kick_2.bmp")]
gk_imgs = [load_img("goalkeeper_idle.bmp"), load_img("goalkeeper_hands_up.bmp")]
fb_imgs = [load_img("football_1.bmp"), load_img("football_2.bmp")]
gp_img = load_img("goalpost.bmp")

font = pygame.font.Font(None, 16)

def reset_game():
    global p_x, p_y, gk_x, gk_y, gp_x, gp_y, fb_x, fb_y, gk_dir, score, ball_kicked, fb_dx, fb_dy, fb_dir
    p_x, p_y = 10, 80
    gk_x, gk_y = 50, 30
    gp_x, gp_y = 32, 10  
    fb_x, fb_y = 40, 90
    gk_dir = 1
    score = 0
    ball_kicked = False
    fb_dx, fb_dy = 0, 0
    fb_dir = 2

reset_game()

def reset_ball(is_goal):
    global fb_x, fb_y, score, ball_kicked, fb_dx, fb_dy, fb_dir
    if is_goal:
        score += 1  
    else:
        score -= 1  

    fb_x, fb_y = 40, 90  
    ball_kicked = False  
    fb_dx, fb_dy = 0, 0  
    fb_dir = 2  

def animate_kick():
    for img in p_imgs[1:]:
        screen.blit(img, (p_x, p_y))
        pygame.display.update()
        time.sleep(0.1)

run = True
frame, bg_frame, fb_frame = 0, 0, 0

while run:
    screen.blit(bgs[bg_idx], (0, 0))
    screen.blit(gp_img, (gp_x, gp_y))
    screen.blit(p_imgs[0], (p_x, p_y))
    screen.blit(gk_imgs[0], (gk_x, gk_y))
    screen.blit(fb_imgs[0], (fb_x, fb_y))

    for evt in pygame.event.get():
        if evt.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and p_x > 0:
        p_x -= 2
    if keys[pygame.K_RIGHT] and p_x < W - 20:
        p_x += 2

    if keys[pygame.K_b] and not ball_kicked:  
        animate_kick()
        ball_kicked = True
        fb_dx = random.choice([-2, 2])  
        fb_dy = -3  

    if keys[pygame.K_a]:  
        reset_game()

    if keys[pygame.K_c]:  
        run = False  

    if ball_kicked:
        fb_x += fb_dx  
        fb_y += fb_dy  
    else:
        fb_x += fb_dir
        if fb_x <= 0 or fb_x >= W - 16:
            fb_dir *= -1  

    if fb_x <= 0 or fb_x >= W - 16:
        fb_dx *= -1  

    if fb_y <= gp_y:  
        if gp_x < fb_x < gp_x + 32:  
            reset_ball(True)  
        else:
            reset_ball(False)  

    if fb_y < 0:  
        reset_ball(False)  

    gk_x += gk_dir
    if gk_x <= 0 or gk_x >= W - 16:
        gk_dir *= -1

    frame += 1
    bg_frame += 1
    fb_frame += 1

    if frame >= 20:
        frame = 0
        gk_imgs.reverse()

    if bg_frame >= 20:
        bg_frame = 0
        bg_idx = (bg_idx + 1) % len(bgs)

    if fb_frame >= 10:
        fb_frame = 0
        fb_imgs.reverse()

    text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(text, (5, 5))

    pygame.display.update()
    clk.tick(30)

end_img = load_img("ende.bmp")
screen.blit(end_img, (0, 0))
pygame.display.update()

end_text = font.render(f"Final Score: {score}", True, (255, 255, 255))
screen.blit(end_text, (20, 60))
pygame.display.update()
time.sleep(4)

pygame.quit()
