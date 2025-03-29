import math
import random
import displayio
import pygame
from blinka_displayio_pygamedisplay import PyGameDisplay
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font
pygame.init()

class Animation:
    def __init__(self, start_frame, end_frame, ticks_per_frame, one_shot=False):
        self.start_frame = start_frame
        self.end_frame = end_frame
        self.frame = start_frame
        self.ticks = 0
        self.ticks_per_frame = ticks_per_frame
        self.one_shot = one_shot

    def next_frame(self):
        if self.one_shot and self.frame == self.end_frame:
            return self.frame

        self.ticks += 1

        if self.ticks >= self.ticks_per_frame:
            self.frame += 1
            if self.frame > self.end_frame:
                self.frame = self.start_frame

            self.ticks = 0

        return self.frame

class Player:
    def __init__(self, splash, x, y):
        self.health = 1000
        self.bitmap_sheet = displayio.OnDiskBitmap('res/penguin.png')
        self.sprite = displayio.TileGrid(
            self.bitmap_sheet,
            pixel_shader=self.bitmap_sheet.pixel_shader,
            tile_width=20,
            tile_height=29,
            x=x - 20,
            y=y - 29
        )

        self.walk_animation = Animation(0, 2, 2)
        self.idle_animation = Animation(2, 4, 10)
        self.hurt_animation = Animation(6, 8, 5, one_shot=True)
        self.current_animation = self.idle_animation
        splash.append(self.sprite)

        self.weapon = Bazooka(splash)
        self.weapon.sprite.x = self.sprite.x
        self.weapon.sprite.y = self.sprite.y

        self.firing = False
        self.score = 0

    def reset(self):
        self.health = 1000
        self.current_animation = self.idle_animation
        self.firing = True
        self.score = 0

    def update(self, splash):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.sprite.x -= 2
            self.sprite.flip_x = True
        if keys[pygame.K_RIGHT]:
            self.sprite.x += 2
            self.sprite.flip_x = False
        if keys[pygame.K_UP] and not self.firing:
            self.weapon.fire(splash, int((self.sprite.flip_x - 0.5) * -10), 0)
            self.firing = True

        if not keys[pygame.K_UP]:
            self.firing = False

        if self.current_animation == self.hurt_animation:
            if self.hurt_animation.frame == self.hurt_animation.end_frame:
                self.current_animation = self.idle_animation
                self.hurt_animation.frame = self.hurt_animation.start_frame
        else:
            if not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
                self.current_animation = self.idle_animation
            else:
                self.current_animation = self.walk_animation

        self.sprite[0] = self.current_animation.next_frame()

        self.weapon.sprite.x = int(self.sprite.x - self.weapon.bitmap.width // 2 + self.sprite.tile_width // 2 + (self.sprite.flip_x - 0.5) * 2 * -5)
        self.weapon.sprite.y = self.sprite.y + 10
        self.weapon.sprite.flip_x = self.sprite.flip_x

        self.weapon.update()


class Weapon:
    def __init__(self, splash, damage, bitmap, width, height):
        self.damage = damage
        self.bitmap = bitmap
        self.sprite = displayio.TileGrid(
            self.bitmap,
            pixel_shader=self.bitmap.pixel_shader,
            tile_width=width,
            tile_height=height,
        )

        splash.append(self.sprite)
        self.bullets = []

    def fire(self, splash, vel_x, vel_y):
        pass

class Bullet:
    def __init__(self, splash, x, y, x_vel, y_vel, bitmap, width, height):
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.bitmap = bitmap
        self.detonated = False
        self.sprite = displayio.TileGrid(
            bitmap,
            pixel_shader=bitmap.pixel_shader,
            tile_width=width,
            tile_height=height,
            x=x,
            y=y
        )

        splash.append(self.sprite)

    def update(self):
        pass

class Rocket(Bullet):
    def __init__(self, splash, x, y, x_vel, y_vel):
        super().__init__(splash, x, y, x_vel, y_vel, displayio.OnDiskBitmap('res/rocket.png'), 12, 8)

        self.sprite.flip_x = self.x_vel < 0
        splash.append(self.sprite)

    def update(self):
        self.sprite.x += self.x_vel
        self.sprite.y += self.y_vel


class Bazooka(Weapon):
    def __init__(self, splash):
        super().__init__(splash, 50, displayio.OnDiskBitmap('res/bazooka-lowres.png'), 28, 10)

    def update(self):
        for bullet in self.bullets:
            bullet.update()

        new_bullets = []
        for bullet in self.bullets:
            if not bullet.detonated and -12 < bullet.sprite.x < screen_width:
                new_bullets.append(bullet)
            else:
                splash.remove(bullet.sprite)
                # why is this not removing, whatever
                bullet.sprite.x = -100

        self.bullets = new_bullets

    def fire(self, splash, vel_x, vel_y):
        self.bullets.append(Rocket(splash, self.sprite.x, self.sprite.y, vel_x, vel_y))


class Enemy:
    def __init__(self, health, damage, speed):
        self.health = health
        self.damage = damage
        self.speed = speed
        self.dead = False

    def update(self, splash, player):
        pass

class Zombie(Enemy):
    def __init__(self, splash, x, y, is_elite, speed):
        super().__init__(200 if is_elite else 50, 150 if is_elite else 20, speed)

        self.bitmap_sheet = displayio.OnDiskBitmap('res/elite_zombie.png' if is_elite else 'res/zombie.png')
        self.sprite = displayio.TileGrid(
            self.bitmap_sheet,
            pixel_shader=self.bitmap_sheet.pixel_shader,
            tile_width= 30 if is_elite else 20,
            tile_height= 43 if is_elite else 29,
            x=x - (30 if is_elite else 20),
            y=y - (43 if is_elite else 29)
        )

        self.real_x = self.sprite.x

        splash.append(self.sprite)
        self.attack_ticks = 0
        self.ticks_per_attack = 10 if is_elite else 20

        self.walk_animation = Animation(0, 2, int(2 * self.speed))
        self.death_animation = Animation(3, 7, 3, one_shot=True)
        self.current_animation = self.walk_animation

    def update(self, splash, player):
        self.sprite[0] = self.current_animation.next_frame()

        if self.dead:
            return

        for bullet in player.weapon.bullets:
            if abs(bullet.sprite.x + bullet.bitmap.width // 2 - self.sprite.x - self.sprite.tile_width // 2) < 15:
                self.health -= player.weapon.damage
                player.score += 10
                bullet.detonated = True

        if self.health <= 0:
            self.dead = True
            self.current_animation = self.death_animation

        if abs(self.sprite.x - player.sprite.x) < 18:
            self.attack_ticks += 1
            if self.attack_ticks > self.ticks_per_attack:
                self.attack_ticks = 0
                player.health = max(0, player.health - 10)
                player.current_animation = player.hurt_animation

            return

        self.attack_ticks = 0
        if self.sprite.x - player.sprite.x > 0:
            self.real_x -= self.speed
            self.sprite.flip_x = True
        else:
            self.real_x += self.speed
            self.sprite.flip_x = False

        self.sprite.x = round(self.real_x)

class World:
    def __init__(self, splash):
        self.ground_bitmap = displayio.OnDiskBitmap('res/ground.png')
        self.ground_y = screen_height - 32
        self.ground_sprite = displayio.TileGrid(
            self.ground_bitmap,
            pixel_shader=self.ground_bitmap.pixel_shader,
            tile_width=128,
            tile_height=32,
            x=0,
            y=self.ground_y
        )

        splash.append(self.ground_sprite)

        self.background_bitmap = displayio.OnDiskBitmap('res/background.png')
        self.background_sprite = displayio.TileGrid(
            self.background_bitmap,
            pixel_shader=self.background_bitmap.pixel_shader,
            tile_width=128,
            tile_height=96,
            x=0,
            y=0
        )

        splash.append(self.background_sprite)

        self.player = Player(splash, screen_width // 2, self.ground_y)
        self.player_health_label = label.Label(bitmap_font.load_font('res/pixelade-8px.bdf'), text='Health: ', color=0x0ab2e, x=5, y=10)
        splash.append(self.player_health_label)

        self.enemies = []
        self.spawn_enemy_ticks = 170
        self.ticks_per_spawn_enemy = 200

        self.score_label = label.Label(bitmap_font.load_font('res/pixelade-8px.bdf'), text='Score: ', color=0x0ffc02b, x=50, y=10)
        splash.append(self.score_label)

        self.max_enemy_corpse = 5
        self.spawn_elite_chance = 0.05
        self.enemy_speed = 1

    def add_enemy(self, x, y):
        self.enemies.append(Zombie(splash, x, y, random.random() < self.spawn_elite_chance, self.enemy_speed * (2 if random.random() < 0.05 else 1)))

    def update(self, splash):
        dead_count = 0
        dead = None
        for enemy in self.enemies:
            enemy.update(splash, self.player)
            dead_count += enemy.dead

            if not dead and enemy.dead:
                dead = enemy

        if dead_count > self.max_enemy_corpse:
            self.enemies.remove(dead)
            splash.remove(dead.sprite)

        self.spawn_enemy_ticks += 1
        if self.spawn_enemy_ticks >= self.ticks_per_spawn_enemy:
            self.spawn_enemy_ticks = 0
            self.add_enemy(-30 if random.random() < 0.5 else screen_width + 30, self.ground_y)
            self.ticks_per_spawn_enemy *= 0.90
            self.ticks_per_spawn_enemy = max(30, self.ticks_per_spawn_enemy)

            self.spawn_elite_chance += 0.05
            self.spawn_elite_chance = min(0.4, self.spawn_elite_chance)
            self.enemy_speed += 0.1
            self.enemy_speed = min(3, self.enemy_speed)

        self.player.update(splash)
        self.player_health_label.text = f'HP: {self.player.health}'

        self.score_label.text = f'Score: {math.floor(self.player.score)}'
        self.player.score += 0.01

    def reset(self, splash):
        for enemy in self.enemies:
            splash.remove(enemy.sprite)

        self.enemies = []
        self.spawn_enemy_ticks = 170
        self.ticks_per_spawn_enemy = 200
        self.spawn_elite_chance = 0.05
        self.enemy_speed = 1
        self.player.reset()


screen_width = screen_height = 128
display = PyGameDisplay(width=screen_width, height=screen_height)
splash = displayio.Group()
display.show(splash)

world = World(splash)

restart_panel_target_y = -128
restart_panel_real_y = -128
restart_panel_bitmap = displayio.OnDiskBitmap('res/bb.png')
restart_panel_sprite = displayio.TileGrid(
    restart_panel_bitmap,
    pixel_shader=restart_panel_bitmap.pixel_shader,
    tile_width=128,
    tile_height=128,
    x=0,
    y=-128
)

splash.append(restart_panel_sprite)

restart_panel_score_label = label.Label(bitmap_font.load_font('res/pixelade-8px.bdf'), text='Score: ', color=0x0ffc02b, scale=2, x=64, y=-128, anchor_point=(0.5, 1), anchored_position=(64, 0))
splash.append(restart_panel_score_label)

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    restart_panel_real_y += (restart_panel_target_y - restart_panel_real_y) * 0.05
    restart_panel_sprite.y = int(restart_panel_real_y)
    restart_panel_score_label.y = restart_panel_sprite.y + 50

    if abs(restart_panel_target_y - restart_panel_real_y) < 3:
        restart_panel_real_y = restart_panel_target_y

    if world.player.health <= 0:
        if restart_panel_target_y == -128:
            restart_panel_target_y = 0

        restart_panel_score_label.text = f'Score: {math.floor(world.player.score)}'

        if restart_panel_real_y == restart_panel_target_y and pygame.key.get_pressed()[pygame.K_UP]:
            world.reset(splash)
            restart_panel_target_y = -128
    else:
        world.update(splash)

    clock.tick(30)