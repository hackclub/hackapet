import pygame
import math
import random
import numpy as np
from collections import defaultdict
import asyncio
import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay

pygame.init()

COLORS = {"BLUE": (12, 18, 226), "RED": (255, 0, 0), "GREEN": (0, 255, 0), "YELLOW": (255, 255, 0), "ORANGE": (255, 165, 0), "PURPLE": (128, 0, 128), "PINK": (255, 192, 203), "CYAN": (0, 255, 255), "WHITE": (255, 255, 255), "BLACK": (0, 0, 0), "GRAY": (128, 128, 128), "BROWN": (165, 42, 42)}
BG_COLOR = (255, 255, 255)
VISION_COLOR = COLORS["GRAY"]
SHOW_VISION = False
BOID_SIZE = 3
WIDTH = 128
HEIGHT = 128
BOID_TYPE = "triangle"
VISION_RADIUS = 7
BOIDS_COUNT = 100
TRANSPARENCY_VALUE = 5
VISION_TYPE = "circle"
BOID_COLOR = COLORS["RED"]
DISPLAY_START_SCREEN = True

class Grid:
    def __init__(self, cell_size):
        self.cell_size = cell_size
        self.grid = defaultdict(list)
        self.max_flock = int(BOIDS_COUNT * 0.3)
    
    def get_cell_coords(self, pos):
        return (int(pos['x'] // self.cell_size), int(pos['y'] // self.cell_size))
    
    def update_boid(self, boid):
        cell = self.get_cell_coords(boid.pos)
        self.grid[cell].append(boid)
    
    def neighbors(self, boid):
        cell = self.get_cell_coords(boid.pos)
        neighbors = []
        neighbor_cells = [(cell[0] + dx, cell[1] + dy) for dx in [-1, 0, 1] for dy in [-1, 0, 1]]
        neighbors = [boid for neighbor_cell in neighbor_cells for boid in self.grid.get(neighbor_cell, [])]
        flock = [n for n in neighbors if n != boid]
        if len(flock) > self.max_flock:
            return []
        return flock

    def clear(self):
        self.grid.clear()

class Boid:
    def __init__(self, posX=random.randint(1, WIDTH), posY=random.randint(0, HEIGHT)):
        self.pos = {'x': posX, 'y': posY}
        angle = math.radians(random.uniform(0, 360))
        self.velocity = {'x': math.cos(angle) * 2, 'y': math.sin(angle) * 2}
        self.size = BOID_SIZE
        self.angle = math.atan2(self.velocity['y'], self.velocity['x'])
        self.cached_neighbors = []
        self.color = BOID_COLOR
        self.points = self.generate_points()

    def generate_points(self):
        return []

    def limit_speed(self, max_speed):
        speed = math.sqrt(self.velocity['x']**2 + self.velocity['y']**2)
        if speed > max_speed:
            self.velocity['x'] = (self.velocity['x'] / speed) * max_speed
            self.velocity['y'] = (self.velocity['y'] / speed) * max_speed

    def point_in_triangle(self, p, a, b, c):
        def sign(p1, p2, p3):
            return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

        d1 = sign(p, a, b)
        d2 = sign(p, b, c)
        d3 = sign(p, c, a)

        has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
        has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)

        return not (has_neg and has_pos)

    def draw(self, display_group):
        if SHOW_VISION:
            if VISION_TYPE == "circle":
                diameter = VISION_RADIUS * 2
                shape = displayio.Shape(diameter, diameter)
                
                center_x = VISION_RADIUS
                center_y = VISION_RADIUS

                for y in range(diameter):
                    for x in range(diameter):
                        distance_sq = (x - center_x) ** 2 + (y - center_y) ** 2
                        if VISION_RADIUS**2 - 2 * VISION_RADIUS <= distance_sq <= VISION_RADIUS**2:
                            shape[x, y] = 1

                pixel_shader = displayio.Palette(2)
                pixel_shader.make_transparent(0)
                pixel_shader[1] = VISION_COLOR

                circle_tilegrid = displayio.TileGrid(shape, pixel_shader=pixel_shader)
                circle_tilegrid.x = int(self.pos['x']) - VISION_RADIUS
                circle_tilegrid.y = int(self.pos['y']) - VISION_RADIUS
                display_group.append(circle_tilegrid)

        points = [
            (self.pos['x'] + self.size * math.cos(self.angle),
            self.pos['y'] + self.size * math.sin(self.angle)),
            (self.pos['x'] + self.size * math.cos(self.angle + 2.5),
            self.pos['y'] + self.size * math.sin(self.angle + 2.5)),
            (self.pos['x'] + self.size * math.cos(self.angle - 2.5),
            self.pos['y'] + self.size * math.sin(self.angle - 2.5))
        ]
        min_x = int(min(p[0] for p in points))
        max_x = int(max(p[0] for p in points))
        min_y = int(min(p[1] for p in points))
        max_y = int(max(p[1] for p in points))
        width = max(1, max_x - min_x + 1)
        height = max(1, max_y - min_y + 1)

        if BOID_TYPE == "triangle":
            shape = displayio.Shape(width, height)
            for y in range(height):
                for x in range(width):
                    px, py = x + min_x, y + min_y
                    if self.point_in_triangle((px, py), points[0], points[1], points[2]):
                        shape[x, y] = 1

            pixel_shader = displayio.Palette(2)
            pixel_shader.make_transparent(0)
            pixel_shader[1] = self.color
            triangle = displayio.TileGrid(shape, pixel_shader=pixel_shader)
            triangle.x = max(0, min_x)
            triangle.y = max(0, min_y)
            display_group.append(triangle)
            
        elif BOID_TYPE == "square":
            shape = displayio.Shape(width, height)
            for y in range(height):
                for x in range(width):
                    shape[x, y] = 1

            pixel_shader = displayio.Palette(2)
            pixel_shader.make_transparent(0)
            pixel_shader[1] = self.color
            square = displayio.TileGrid(shape, pixel_shader=pixel_shader)
            square.x = max(0, min_x)
            square.y = max(0, min_y)
            display_group.append(square)
            
        elif BOID_TYPE == "circle":
            shape = displayio.Shape(width, height)
            for y in range(height):
                for x in range(width):
                    if (x - width // 2)**2 + (y - height // 2)**2 <= (width // 2)**2:
                        shape[x, y] = 1

            pixel_shader = displayio.Palette(2)
            pixel_shader.make_transparent(0)
            pixel_shader[1] = self.color
            circle = displayio.TileGrid(shape, pixel_shader=pixel_shader)
            circle.x = max(0, min_x)
            circle.y = max(0, min_y)
            display_group.append(circle)
            
        elif BOID_TYPE == "gradient":
            flock_size = len(self.cached_neighbors)
            intensity = min(255, 50 + flock_size * 5)
            color1, color2, color3 = self.color
            flock_color = (
            min(255, color1 + intensity),
            min(255, color2 + intensity),
            min(255, color3 + intensity)
            )
            
            shape = displayio.Shape(width, height)
            for y in range(height):
                for x in range(width):
                    px, py = x + min_x, y + min_y
                    if self.point_in_triangle((px, py), points[0], points[1], points[2]):
                        shape[x, y] = 1

            pixel_shader = displayio.Palette(2)
            pixel_shader.make_transparent(0)
            pixel_shader[1] = flock_color
            triangle = displayio.TileGrid(shape, pixel_shader=pixel_shader)
            triangle.x = max(0, min_x)
            triangle.y = max(0, min_y)
            display_group.append(triangle)

    def separation(self, boids):
        steer = {'x': 0, 'y': 0}
        my_pos = np.array([self.pos['x'], self.pos['y']], dtype=np.float64)
        positions = np.array([[b.pos['x'], b.pos['y']] for b in boids], dtype=np.float64)
        if len(positions) > 0:
            differences = positions - my_pos
            distances = np.linalg.norm(differences, axis=1)
            mask = distances < VISION_RADIUS
            if np.any(mask):
                differences = differences[mask]
                distances = distances[mask].reshape(-1, 1)
                steer_forces = np.divide(differences, distances, where=distances != 0)
                steer['x'], steer['y'] = -np.sum(steer_forces, axis=0)

        return steer

    def alignment(self, boids):
        avg_velocity = {'x': 0, 'y': 0}
        count = 0
        for other in boids:
            if other != self:
                dx = self.pos['x'] - other.pos['x']
                dy = self.pos['y'] - other.pos['y']
                distance = math.sqrt(dx**2 + dy**2)
                if distance < VISION_RADIUS:
                    avg_velocity['x'] += other.velocity['x']
                    avg_velocity['y'] += other.velocity['y']
                    count += 1
        if count > 0:
            avg_velocity['x'] /= count
            avg_velocity['y'] /= count
            return avg_velocity
        return {'x': 0, 'y': 0}

    def cohesion(self, boids):
        center = {'x': 0, 'y': 0}
        count = 0
        for other in boids:
            if other != self:
                dx = self.pos['x'] - other.pos['x']
                dy = self.pos['y'] - other.pos['y']
                distance = math.sqrt(dx**2 + dy**2)
                if distance < VISION_RADIUS:
                    center['x'] += other.pos['x']
                    center['y'] += other.pos['y']
                    count += 1
        if count > 0:
            center['x'] /= count
            center['y'] /= count
            return {'x': center['x'] - self.pos['x'], 'y': center['y'] - self.pos['y']}
        return {'x': 0, 'y': 0}
    
    def update(self, boids):
        sep = self.separation(boids)
        align = self.alignment(boids)
        coh = self.cohesion(boids)
        separation_weight = 5.0
        alignment_weight = 1.0
        cohesion_weight = 2.0
        jitter = {'x': (random.random() - 0.5) * 1.0, 'y': (random.random() - 0.5) * 1.0}
        self.velocity['x'] += (separation_weight * sep['x'] + alignment_weight * align['x'] + cohesion_weight * coh['x'] + jitter['x'])
        self.velocity['y'] += (separation_weight * sep['y'] + alignment_weight * align['y'] + cohesion_weight * coh['y'] + jitter['y'])
        self.limit_speed(2)
        self.pos['x'] += self.velocity['x']
        self.pos['y'] += self.velocity['y']
        self.angle = math.atan2(self.velocity['y'], self.velocity['x'])

        if BOID_TYPE == "exp" and random.randint(1, 100) == 1:
            self.points = self.generate_points()

        if self.pos['x'] < -self.size:
            self.pos['x'] = WIDTH + self.size
        elif self.pos['x'] > WIDTH + self.size:
            self.pos['x'] = -self.size
        if self.pos['y'] < -self.size:
            self.pos['y'] = HEIGHT + self.size
        elif self.pos['y'] > HEIGHT + self.size:
            self.pos['y'] = -self.size

async def main():
    global BOID_TYPE, BOID_COLOR, SHOW_VISION, DISPLAY_START_SCREEN
    running = True
    DISPLAY_START_SCREEN = True

    boids = []
    
    for boid in range(BOIDS_COUNT):
        boids.append(Boid(random.randint(1, WIDTH), random.randint(1, HEIGHT)))

    display = PyGameDisplay(width=WIDTH, height=HEIGHT)
    display_group = displayio.Group()
    display.show(display_group)
    running = True
    grid = Grid(VISION_RADIUS)
    bg = displayio.OnDiskBitmap("startScreenBG.bmp")
    bg_sprite = displayio.TileGrid(
        bg, 
        pixel_shader=bg.pixel_shader
    )

    def update_boids():
        if running:
            grid.clear()
            for boid in boids:
                grid.update_boid(boid)
            for boid in boids:
                boid.cached_neighbors = grid.neighbors(boid)
                boid.update(boid.cached_neighbors)

    def draw_boids():
        if running:
            if DISPLAY_START_SCREEN:
                display_group.append(bg_sprite)
            else:
                if bg_sprite in display_group:
                    display_group.remove(bg_sprite)
                if len(display_group) > 0:
                    display_group.pop()
                new_group = displayio.Group()
                for boid in boids:
                    boid.draw(new_group)
                display_group.append(new_group)
                display.refresh()



    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                boids.append(Boid(x, y))
            elif event.type == pygame.KEYDOWN:
                if DISPLAY_START_SCREEN:
                    DISPLAY_START_SCREEN = False
                    new_bg = displayio.OnDiskBitmap("BG.bmp")
                    new_bg_sprite = displayio.TileGrid(new_bg, pixel_shader=new_bg.pixel_shader)
                    if bg_sprite in display_group:
                        display_group.remove(bg_sprite)
                    display_group.pop()
                    display_group.append(new_bg_sprite)
                else:
                    if event.key == pygame.K_v:
                        SHOW_VISION = not SHOW_VISION
                    elif event.key == pygame.K_c:
                        BOID_COLOR = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                        for boid in boids: boid.color = BOID_COLOR
                    elif event.key == pygame.K_r:
                        if hasattr(event, 'last_click_time') and pygame.time.get_ticks() - event.last_click_time < 500:
                            for _ in range(random.randint(1, 20)):
                                if boids:
                                    boids.pop()
                        else:
                            for _ in range(random.randint(1, 10)):
                                boids.append(Boid(random.randint(1, WIDTH), random.randint(1, HEIGHT)))
                        event.last_click_time = pygame.time.get_ticks()
                    elif event.key == pygame.K_b:
                        if BOID_TYPE == "triangle":
                            BOID_TYPE = "square"
                        elif BOID_TYPE == "square":
                            BOID_TYPE = "circle"
                        elif BOID_TYPE == "circle":
                            BOID_TYPE = "gradient"
                        else:
                            BOID_TYPE = "triangle"
                    elif event.key == pygame.K_MINUS:
                        for _ in range(random.randint(1, 100)):
                            if boids:
                                boids.pop()
        draw_boids()

        update_boids()
        
        pygame.time.wait(25)

    pygame.quit()

if __name__ == "__main__":
    asyncio.run(main())
