import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
import pygame
import time

pygame.init()

display = PyGameDisplay(width=128, height=128)
splash = displayio.Group()
display.show(splash)

background = displayio.OnDiskBitmap("resources/background.bmp")
bg_sprite = displayio.TileGrid(background, pixel_shader=background.pixel_shader)
splash.append(bg_sprite)

class Select:
    def __init__(self, sprtB, sprtW):
        self.x = 7
        self.y = 7
        self.sprite_b = sprtB
        self.sprite_w = sprtW
        self.update_turn(True)
        self.sprite.x = self.x * 16; self.sprite.y = self.y * 16

    def update_turn(self, is_white):
        if is_white:
            self.sprite_b.x = -16
            self.sprite_b.y = -16
            self.x = 7
            self.y = 7
            self.sprite_w.x = self.x * 16
            self.sprite_w.y = self.y * 16
            self.sprite = self.sprite_w
        else:
            self.sprite_w.x = -16
            self.sprite_w.y = -16
            self.x = 0
            self.y = 0
            self.sprite_b.x = self.x * 16
            self.sprite_b.y = self.y * 16
            self.sprite = self.sprite_b

    def move(self, x):
        self.x += x
        if self.x < 0:
            if self.y < 7:
                self.x = 7
                self.y += 1
            else:
                self.x = 0
        if self.x > 7:
            if self.y > 0:
                self.x = 0
                self.y -= 1
            else:
                self.x = 7
        
        self.sprite.x = self.x * 16
        self.sprite.y = self.y * 16

select_b_raw = displayio.OnDiskBitmap("resources/select_b.bmp")
select_w_raw = displayio.OnDiskBitmap("resources/select_w.bmp")
select_b_sprite = displayio.TileGrid(select_b_raw, pixel_shader=select_b_raw.pixel_shader)
select_w_sprite = displayio.TileGrid(select_w_raw, pixel_shader=select_w_raw.pixel_shader)
select = Select(select_b_sprite, select_w_sprite)
splash.append(select_b_sprite); splash.append(select_w_sprite)

class Piece:
    def __init__(self, x, y, type):
        self.x, self.y = x, y
        self.type = type
        
        sprt = displayio.OnDiskBitmap(f"resources/{type}.bmp")
        self.sprite = displayio.TileGrid(sprt, pixel_shader=sprt.pixel_shader)
        splash.append(self.sprite)

        self.sprite.x = x * 16
        self.sprite.y = y * 16

    def move_piece(self, x, y):
        self.x, self.y = x, y
        self.sprite.x = x * 16
        self.sprite.y = y * 16

whites = ["pp", "rr", "nn", "bb", "qq", "kk"]
blacks = ["p", "r", "n", "b", "q", "k"]

class Manager:
    def __init__(self):
        self.pieces = [
            Piece(0, 7, "rr"), Piece(1, 7, "nn"), Piece(2, 7, "bb"), Piece(3, 7, "qq"), Piece(4, 7, "kk"), Piece(5, 7, "bb"), Piece(6, 7, "nn"), Piece(7, 7, "rr"),
            Piece(0, 6, "pp"), Piece(1, 6, "pp"), Piece(2, 6, "pp"), Piece(3, 6, "pp"), Piece(4, 6, "pp"), Piece(5, 6, "pp"), Piece(6, 6, "pp"), Piece(7, 6, "pp"),
            Piece(0, 1, "p"), Piece(1, 1, "p"), Piece(2, 1, "p"), Piece(3, 1, "p"), Piece(4, 1, "p"), Piece(5, 1, "p"), Piece(6, 1, "p"), Piece(7, 1, "p"),
            Piece(0, 0, "r"), Piece(1, 0, "n"), Piece(2, 0, "b"), Piece(3, 0, "q"), Piece(4, 0, "k"), Piece(5, 0, "b"), Piece(6, 0, "n"), Piece(7, 0, "r"),
        ]

        self.selected = None

        selected_raw = displayio.OnDiskBitmap("resources/selected.bmp")
        self.selected_sprite = displayio.TileGrid(selected_raw, pixel_shader=selected_raw.pixel_shader)
        splash.append(self.selected_sprite); self.selected_sprite.x = -16; self.selected_sprite.y = -16

        self.moves = []

        self.white_turn = True

    def record_move(self, src, dst, last):
        self.moves.append((src, dst, last.type if last is not None else None))
        self.white_turn = not self.white_turn
        select.update_turn(self.white_turn)

    def undo_move(self):
        if len(self.moves) == 0:
            return

        src, dst, last = self.moves.pop()
        
        for piece in self.pieces:
            if piece.x == dst[0] and piece.y == dst[1]:
                piece.move_piece(src[0], src[1])
                break

        if last is not None:
            self.pieces.append(Piece(dst[0], dst[1], last))

        self.white_turn = not self.white_turn
        select.update_turn(self.white_turn)

    def select_slot(self, x, y):
        if self.selected is not None:
            self.try_move(self.selected, x, y)
            self.selected = None
            self.selected_sprite.x = -16
            self.selected_sprite.y = -16
            return

        for piece in self.pieces:
            if piece.x == x and piece.y == y:
                if (not self.white_turn and piece.type in whites) or (self.white_turn and piece.type in blacks):
                    return

                self.selected = piece

                self.selected_sprite.x = self.selected.x * 16
                self.selected_sprite.y = self.selected.y * 16
                return

    def try_move(self, piece, x, y):
        if piece is None:
            return
        if piece.x == x and piece.y == y:
            return

        last_piece = None
        for other in self.pieces:
            if other.x == x and other.y == y:
                last_piece = other

        if last_piece is not None:
            splash.remove(last_piece.sprite)
            self.pieces.remove(last_piece)

        self.record_move((piece.x, piece.y), (x, y), last_piece if last_piece is not None else None)
        
        piece.move_piece(x, y)
        

manager = Manager()

selected_frame_count = -1
deltaTime = 0.08
dont_select = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                if dont_select:
                    dont_select = False
                else:
                    manager.select_slot(select.x, select.y)
                    dont_select = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        select.move(-1)
    if keys[pygame.K_RIGHT]:
        select.move(1)

    if keys[pygame.K_UP]:
        selected_frame_count += 1
    else:
        selected_frame_count = -1

    if selected_frame_count > 10:
        selected_frame_count = -1
        manager.undo_move()
        dont_select = True

    time.sleep(deltaTime)