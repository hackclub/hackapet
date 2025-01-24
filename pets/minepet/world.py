from math import sin
import displayio

import random

B_GRASS = 0
B_DIRT = 1
B_LOG = 2
B_LEAVES = 3
B_STONE = 4
B_PLANKS = 5
B_SAND = 6
B_BRICKS = 7
B_GLASS = 8
B_STAIRSL = 9
B_STAIRSR = 10
B_FLOWER = 11

NO_COLLISION_BLOCKS = [B_FLOWER]

HILLYNESS = 10
class Random:
    def __init__(self, seed: int):
        self.seed = seed

    def random_at(self, x, y):
        random.seed(f"{self.seed}-{x}-{y}")
        return random.random()

    def height_at(self, x: int):
        x *= .1
        ses = (self.seed % 1024) / 1024
        ses += 1 if ses == 0 else 0
        return round((sin(x * ses) + sin(x*.2*1/ses) + sin(x * 3 * ses) + 3) / 6 * HILLYNESS)

class World:
    changed_blocks: dict[(int, int), int|None]

    def __init__(self, seed: int = 0):
        self.changed_blocks = dict()
        self.random = Random(seed)

    TREE_BOX_SIZE = 6

    def block_at(self, x, y, ignore_collision: bool = False):
        if (x, y) in self.changed_blocks:
            return self.changed_blocks[(x, y)] if (ignore_collision or self.changed_blocks[(x, y)] not in NO_COLLISION_BLOCKS) else None
        if y < -3: return B_STONE
        if y < -2: return B_DIRT if self.random.random_at(x, y) < .25 else B_STONE
        if y < 0: return B_DIRT if self.random.random_at(x, y) <= .5 else B_STONE
        if y >= 0:
            n = self.random.height_at(x)
            sand_possible = self.random.random_at(x // 4, 0) <= .3
            if (y == n or (y == n - 1 and x % 4 in [1, 2])) and sand_possible and y <= n: return B_SAND
            if y < n: return B_DIRT
            if y == n: return B_GRASS if ((x, y + 1) in self.changed_blocks and self.changed_blocks[(x, y + 1)] is None) or not (int(self.random.random_at(x // World.TREE_BOX_SIZE, (y - n) // World.TREE_BOX_SIZE) * 3) == 1 and x % World.TREE_BOX_SIZE == 2) else B_DIRT

            if y == n + 1 and not sand_possible and (x, y - 1) not in self.changed_blocks and self.random.random_at(x, n) < .1 and self.block_at(x, y - 1) in [B_DIRT, B_GRASS]: return B_FLOWER if ignore_collision else None
            elif y > n: # only generate tree if not flower
                tx = x // World.TREE_BOX_SIZE
                base_x = (tx * World.TREE_BOX_SIZE + World.TREE_BOX_SIZE // 2 - 1)
                nb = self.random.height_at(base_x)
                ty = (y - 1 - nb) // World.TREE_BOX_SIZE
                tyr = (y - 1 - nb) % World.TREE_BOX_SIZE
                txr = x % World.TREE_BOX_SIZE
                if ty == 0 and \
                    int(self.random.random_at(tx, ty) * 3) == 1 and \
                    not self.random.random_at(base_x // 4, 0) <= .3 and \
                    not self.random.random_at(base_x, nb) < .1: # if block is on ground, and base is a tree, and base is not sand, and base is not flower
                    if tyr in range(3) and txr == 2: return B_LOG
                    if tyr == 3 and txr in range(1, 4): return B_LEAVES
                    if tyr > 0 and tyr < 3 and (txr in range(0, 2) or txr in range(3, 5)): return B_LEAVES
        # if x < -2: return B_GLASS
    
    def break_block(self, x, y):
        self.changed_blocks[(x, y)] = None
        if (x, y - 1) in self.changed_blocks and self.block_at(x, y - 1) == B_DIRT and (self.block_at(x - 1, y - 1) == B_GRASS or self.block_at(x + 1, y - 1) == B_GRASS):
            self.changed_blocks[(x, y - 1)] = B_GRASS

    def place_block(self, x, y, bid):
        self.changed_blocks[(x, y)] = bid
        if bid != B_FLOWER and self.block_at(x, y - 1) == B_GRASS:
            self.changed_blocks[(x, y - 1)] = B_DIRT
            
