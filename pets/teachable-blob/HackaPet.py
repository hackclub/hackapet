import pygame
import os

pygame.init()

# Set up display
screen_width = 128
screen_height = 128
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Hackapet")


# Load image


def load_image(file_path, scale, pos_x, pos_y, w, h, idx):
    image_path = os.path.join(os.path.dirname(__file__), "art",file_path)
    image = pygame.image.load(image_path).convert_alpha()
    img_w, img_h = image.get_size()
    width = scale*w
    height = scale*h
    image = pygame.transform.scale(image, (scale*img_w, scale*img_h))
    cropped_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    cropped_surface.blit(image, (0, 0), (idx*width, 0, width, height))
    screen.blit(cropped_surface, (pos_x, pos_y))


def setup_background(bg_name):
    background = os.path.join(os.path.dirname(__file__), "art", bg_name)
    image = pygame.image.load(background)
    image = pygame.transform.scale(image, (128, 128))
    screen.blit(image, (0, 0))


def check_keys():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_1]:
        button_colors[0] = BLACK
    if keys[pygame.K_2]:
        button_colors[1] = BLACK
    if keys[pygame.K_3]:
        button_colors[2] = BLACK




class Pet():
    def __init__(self, stage, animation):
        self.stage = stage
        self.animation = animation
        self.hunger = 2
        self.progress = 0
        self.eating = False
        self.frame = 0
        self.skill = 0
        self.teaching = False
        self.bullet_dist = 1
        self.bullet_dir = True
        self.plant = ["berry_red.bmp", 0, 2, 8, 15]

    def button_pressed(self, id):
        if self.stage == 0:
            self.stage = 1
            self.animation = ["egg_hatch.bmp", 2, 11, 10, False]
            return
        elif id == 0:
            if icon.name < 1: # change this number every time an icon is added
                icon.name += 1
            else:
                icon.name = 0
        elif id == 1:
            if not self.teaching or self.eating:
                icon.select()
            elif self.teaching and self.progress == 0:
                self.progress = 1
                if self.bullet_dir:
                    self.bullet_dist -= 1
                else:
                    self.bullet_dist += 1
                inaccuracy = self.bullet_dist - 4
                self.plant = ["berry.bmp", 0, 0, 7, 13]
                if abs(inaccuracy) - self.skill < 1:
                    self.skill += 0.2
                    self.plant[3:5] = [8, 15]
                    if inaccuracy == 0:
                        self.plant[0] = "berry_red.bmp"
                        self.plant[2] = 2
                        self.plant[3] = 9
                    elif inaccuracy < 0:
                        self.plant[0] = "berry_green.bmp"
                        self.plant[2] = 3
                    elif inaccuracy > 0:
                        self.plant[0] = "berry_pink.bmp"
                        self.plant[2] = 3
                        self.plant[3] = 10
                self.animation = ["baby_left.bmp", 0, 7, 5, False]
                self.bullet_dir = False
                self.bullet_dist = 64

        elif id == 2:
            self.eating = False
            self.teaching = False
            self.progress = 0
            self.animation = ["baby_idle.bmp", 1, 10, 6, True]


    def next_animation(self):
        if self.eating:
            if self.progress < 2:
                self.progress += 1
                self.animation = ["baby_idle.bmp", 1, 10, 6, False]
                return
            elif self.progress < 4:
                self.progress += 1
                self.animation = ["baby_eat.bmp", 1, 7, 7, False]
                return
            self.animation = ["baby_idle.bmp", 1, 10, 6, True]
            self.progress = 0
            self.eating = False
        elif self.teaching:
            self.animation = ["baby_left.bmp", 0, 7, 5, False]
            if self.bullet_dist > 15: # change this to go a bit farther or less
                self.bullet_dist -= 5 # far based on "inaccuracy"
                return
            self.plant[1] += 1
            self.bullet_dist += 5
            self.bullet_dir = True
            if self.plant[1] > self.plant[2]:
                self.teaching = False
                self.progress = 0
        elif self.stage == 1:
            self.animation = ["baby_idle.bmp", 1, 10, 6, True]

    def teach(self):
        self.animation = ["baby_left.bmp", 0, 7, 6, True]
        self.teaching = True
        self.progress = 0
        self.bullet_dist = 1

    def eat(self):
        # self.frame = 0
        self.eating = True
        # determine stage
        self.animation = ["baby_idle.bmp", 1, 10, 6, False]
        load_image("wood_chips.bmp", 2, 10, 100, 14, 10, 3)
        self.progress = 0
        self.hunger -= 1

    def sad_screen(self):
        self.animation = ["sad_screen" + str(int(self.progress / 8)+1)
                              + ".bmp", 0, 32, 32, False]

class Icon():
    def __init__(self):
        self.name = 0
        self.namelist = ["eat", "learn"]

    def select(self):
        if self.name == 0:
            blob.eat()
        else:
            blob.teach()


icon = Icon()


class Event_handler():
    def __init__(self, running):
        self.running = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    blob.button_pressed(0)
                elif event.key == pygame.K_2:
                    blob.button_pressed(1)
                elif event.key == pygame.K_3:
                    blob.button_pressed(2)
            elif event.type == pygame.KEYUP:
                if event.key in [pygame.K_1, pygame.K_2, pygame.K_3]:
                    return


# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Button setup
button_width = 30
button_height = 20
button_margin = 10
buttons = [
    pygame.Rect(10, screen_height - 30, button_width, button_height),
    pygame.Rect(50, screen_height - 30, button_width, button_height),
    pygame.Rect(90, screen_height - 30, button_width, button_height)
]
button_colors = [WHITE, WHITE, WHITE]

# LED setup
led_radius = 5
led_positions = [
    (20, 10), (60, 10), (100, 10)
]
led_states = [False, False, False]

# Main game loop
blob = Pet(0, ["egg_wait.bmp", 1, 10, 8, True])
handler = Event_handler(True)
clock = pygame.time.Clock()

while handler.running:
    handler.handle_events()
    check_keys()
    if blob.teaching:
        setup_background("training_bg.bmp")
    elif blob.eating:
        setup_background("eating_bg.bmp")
    else:
        setup_background("background.bmp")

    # handle blob animations


    if blob.animation[0] != "":
        if blob.frame > blob.animation[1]:
            blob.frame = 0
            if not blob.animation[4]:
                blob.next_animation()
    if int(blob.hunger) >= 4:
        blob.sad_screen()
        blob.progress += 1
        if blob.progress > 15:
            handler.running = False
    if blob.hunger > 4:
        load_image(blob.animation[0], 4, 0, 0, blob.animation[2],
                   blob.animation[3], blob.frame)
    else:
        load_image(blob.animation[0], 4, 45, 95, blob.animation[2],
                   blob.animation[3], blob.frame)
    blob.frame += 1

    # handle blob activities

    if blob.eating:
        load_image("wood_chips.bmp", 2, 10, 100, 14, 10, blob.progress)
    if blob.teaching:
        if blob.progress == 0:
            load_image("distance_bar.bmp", 8, 28, 10, 10, 1, 0)
            load_image("goo_bullet" + str(blob.bullet_dir)
                       + ".bmp", 2, blob.bullet_dist*8+28, 5, 6, 3, 0)
            if blob.bullet_dist > 7 or blob.bullet_dist < 1:
                blob.bullet_dir = not blob.bullet_dir
            if blob.bullet_dir:
                blob.bullet_dist += 1
            else:
                blob.bullet_dist -= 1
        else:
            load_image(blob.plant[0], 3, 10, 63, blob.plant[3],
                       blob.plant[4], blob.plant[1])
            load_image("goo_bullet" + str(blob.bullet_dir)
                       + ".bmp", 2, blob.bullet_dist, 80, 6, 3, 0)
    blob.hunger += 0.01


    # show selected icon & stats
    load_image(icon.namelist[icon.name] + "_icon.bmp", 2, 5, 5, 8, 8, 0)
    if not blob.teaching or blob.eating:
        load_image(icon.namelist[icon.name] + ".bmp", 2, 83, 5, 8, 8, 0)
        if icon.name == 0:
            load_image("level.bmp", 4, 100, 5, 6, 4, int(blob.hunger))
        else:
            load_image("level.bmp", 4, 100, 5, 6, 4, 3 - int(blob.skill))

    if blob.hunger >= 3:
        load_image("hunger_warn.bmp", 4, 0, 96, 32, 8, 0)

    # Draw buttons
    # for button, color in zip(buttons, button_colors):
    #     pygame.draw.rect(screen, color, button)
    # Draw LEDs
    # for pos, state in zip(led_positions, led_states):
    #     color = RED if state else BLACK
    #     pygame.draw.circle(screen, color, pos, led_radius)
    # Update display
    pygame.display.flip()
    # Control the frame rate
    clock.tick(4)

pygame.quit()
