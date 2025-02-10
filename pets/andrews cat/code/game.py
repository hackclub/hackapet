import pygame
import os

# ---------- Pygame Setup ----------
pygame.init()
screen = pygame.display.set_mode((128, 128))
clock = pygame.time.Clock()
pygame.display.set_caption('Andrews Game')
running = True


base_dir = os.path.dirname(__file__)
art_dir = os.path.join(base_dir, "../art")

background = pygame.image.load(os.path.join(art_dir, "background.png")).convert()

# ---------- Functions ----------
def clamp(n, smallest, largest): return max(smallest, min(n, largest))

# ---------- Cat ----------
cat_frames = [pygame.image.load(os.path.join(art_dir, "cat1.png")).convert_alpha(),
                pygame.image.load(os.path.join(art_dir, "cat2.png")).convert_alpha(),
                pygame.image.load(os.path.join(art_dir, "cat3.png")).convert_alpha(),
                pygame.image.load(os.path.join(art_dir, "cat4.png")).convert_alpha(),
                pygame.image.load(os.path.join(art_dir, "cat5.png")).convert_alpha()]

cat_framerate = 10
cat_frame_counter = 0
cat_current_frame = 0

cat_couch_position = (45, 20)
cat_ground_position = (45, 80)

# ---------- Bars ----------
class Bar:
    def __init__(self, position, frames):
        self.position = position
        self.frames = frames

hunger_bar = Bar(
    (5, 5),
    [pygame.image.load(os.path.join(art_dir, "hunger_bar1.png")).convert_alpha(),
    pygame.image.load(os.path.join(art_dir, "hunger_bar2.png")).convert_alpha(),
    pygame.image.load(os.path.join(art_dir, "hunger_bar3.png")).convert_alpha(),
    pygame.image.load(os.path.join(art_dir, "hunger_bar4.png")).convert_alpha(),
    pygame.image.load(os.path.join(art_dir, "hunger_bar5.png")).convert_alpha(),
    pygame.image.load(os.path.join(art_dir, "hunger_bar6.png")).convert_alpha(),
    pygame.image.load(os.path.join(art_dir, "hunger_bar7.png")).convert_alpha(),
    pygame.image.load(os.path.join(art_dir, "hunger_bar8.png")).convert_alpha(),
    pygame.image.load(os.path.join(art_dir, "hunger_bar9.png")).convert_alpha(),
    pygame.image.load(os.path.join(art_dir, "hunger_bar10.png")).convert_alpha()]
)

happy_bar = Bar(
    (20, 5),
    [pygame.image.load(os.path.join(art_dir, "happy_bar1.png")).convert_alpha(),
    pygame.image.load(os.path.join(art_dir, "happy_bar2.png")).convert_alpha(),
    pygame.image.load(os.path.join(art_dir, "happy_bar3.png")).convert_alpha(),
    pygame.image.load(os.path.join(art_dir, "happy_bar4.png")).convert_alpha(),
    pygame.image.load(os.path.join(art_dir, "happy_bar5.png")).convert_alpha(),
    pygame.image.load(os.path.join(art_dir, "happy_bar6.png")).convert_alpha(),
    pygame.image.load(os.path.join(art_dir, "happy_bar7.png")).convert_alpha(),
    pygame.image.load(os.path.join(art_dir, "happy_bar8.png")).convert_alpha(),
    pygame.image.load(os.path.join(art_dir, "happy_bar9.png")).convert_alpha(),
    pygame.image.load(os.path.join(art_dir, "happy_bar10.png")).convert_alpha()]
)

health_bar = Bar(
    (128 - 10 - 5, 5),
    [pygame.image.load(os.path.join(art_dir, "health_bar1.png")).convert_alpha(),
     pygame.image.load(os.path.join(art_dir, "happy_bar2.png")).convert_alpha(),
     pygame.image.load(os.path.join(art_dir, "happy_bar3.png")).convert_alpha(),
     pygame.image.load(os.path.join(art_dir, "happy_bar4.png")).convert_alpha(),
     pygame.image.load(os.path.join(art_dir, "happy_bar5.png")).convert_alpha(),
     pygame.image.load(os.path.join(art_dir, "happy_bar6.png")).convert_alpha(),
     pygame.image.load(os.path.join(art_dir, "happy_bar7.png")).convert_alpha(),
     pygame.image.load(os.path.join(art_dir, "happy_bar8.png")).convert_alpha(),
     pygame.image.load(os.path.join(art_dir, "happy_bar9.png")).convert_alpha(),
     pygame.image.load(os.path.join(art_dir, "happy_bar10.png")).convert_alpha()]
)

hunger = 100
hunger_deplete_rate = 60
hunger_frame_counter = 0
feed_amount = 5

happy = 100
happy_deplete_rate = 90
happy_frame_counter = 0
play_amount = 2.5

health = 0

# ---------- Buttons ----------
button_frames = [pygame.image.load(os.path.join(art_dir, "buttons1.png")).convert_alpha(),
                    pygame.image.load(os.path.join(art_dir, "buttons2.png")).convert_alpha(),
                    pygame.image.load(os.path.join(art_dir, "buttons3.png")).convert_alpha()]

button_center = (128 / 2) - (16 / 2)
a_button_position = (button_center - 25, 105)
b_button_position = (button_center, 110)
c_button_position = (button_center + 25, 105)

# ---------- Game ----------
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # inputs
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                hunger += feed_amount
            if event.key == pygame.K_b:
                happy += play_amount

    screen.fill("white")
    screen.blit(background, (0, 0))

    # cat

    screen.blit(cat_frames[cat_current_frame], cat_couch_position)

    cat_frame_counter += 1
    if cat_frame_counter >= cat_framerate:
        cat_frame_counter = 0
        cat_current_frame += 1
        if cat_current_frame >= len(cat_frames):
            cat_current_frame = 0

    # health
    health_bar_frame = clamp(10 - (round(health / 10)), 0, len(health_bar.frames) - 1)
    screen.blit(health_bar.frames[health_bar_frame], health_bar.position)

    health = (hunger / 2) + (happy / 2)
    if(health <= 0):
        running = False

    # hunger bar
    hunger_bar_frame = clamp(10 - (round(hunger / 10)), 0, len(hunger_bar.frames) - 1)
    screen.blit(hunger_bar.frames[hunger_bar_frame], hunger_bar.position)

    hunger_frame_counter += 1
    if hunger_frame_counter >= hunger_deplete_rate:
        hunger_frame_counter = 0
        hunger -= 1

    hunger = clamp(hunger, 0, 100)
    
    # happy bar
    happy_bar_frame = clamp(10 - (round(happy / 10)), 0, len(happy_bar.frames) - 1)
    screen.blit(happy_bar.frames[happy_bar_frame], happy_bar.position)

    happy_frame_counter += 1
    if happy_frame_counter >= happy_deplete_rate:
        happy_frame_counter = 0
        happy -= 1

    happy = clamp(happy, 0, 100)

    # buttons
    screen.blit(button_frames[0], a_button_position)
    screen.blit(button_frames[1], b_button_position)
    screen.blit(button_frames[2], c_button_position)

    print("Hungry:" + str(hunger) + " Happy:" + str(happy) + " Health:" + str(health))

    # update screen
    pygame.display.flip()
    clock.tick(60)

pygame.quit()