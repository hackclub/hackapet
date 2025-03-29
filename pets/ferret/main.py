import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
import pygame
import time
import math
import random
pygame.init()
display = PyGameDisplay(width=128, height=128)
splash = displayio.Group()
display.show(splash)

with open("background.bmp", "rb") as background_file:
    background_sheet = displayio.OnDiskBitmap(background_file)

background = displayio.TileGrid(
    background_sheet,
    pixel_shader=background_sheet.pixel_shader,
    width=1,
    height=1,
    tile_width=128,
    tile_height=128,
    x=0,
    y=0
)
splash.append(background)

with open("ferret-Sheet.bmp", "rb") as ferret_file:
    ferret_sheet = displayio.OnDiskBitmap(ferret_file)

ferret_sprite = displayio.TileGrid(
    ferret_sheet,
    pixel_shader=ferret_sheet.pixel_shader,
    width=1,
    height=1,
    tile_width=64,
    tile_height=64,
    default_tile=0,
    x=(display.width-64) // 2,
    y=display.height-60
)
splash.append(ferret_sprite)

with open("words.bmp", "rb") as words_file:
    words_sheet = displayio.OnDiskBitmap(words_file)

words = displayio.TileGrid(
    words_sheet,
    pixel_shader=words_sheet.pixel_shader,
    width=1,
    height=1,
    tile_width=64,
    tile_height=32,
    default_tile=0,
    x=(display.width-64) // 2,
    y=display.height-110
)
splash.append(words)

confetti = displayio.TileGrid(
    words_sheet,
    pixel_shader=words_sheet.pixel_shader,
    width=1,
    height=1,
    tile_width=64,
    tile_height=32,
    default_tile=0,
    x=(display.width-64) // 2,
    y=display.height-110
)
splash.append(confetti)

with open("mini-Sheet.bmp", "rb") as mini_file:
    mini_sheet = displayio.OnDiskBitmap(mini_file)
minis = []

def spawn_mini():
    mini = displayio.TileGrid(
        mini_sheet,
        pixel_shader=mini_sheet.pixel_shader,
        width=1,
        height=1,
        tile_width=64,
        tile_height=64,
        x=120,
        y=128-60,
    )
    mini.dir = defaultminidir
    if mini.dir == "right":
        mini.x = -90
    mini.dead = False
    mini.deathcount = 50
    minis.append(mini)
    splash.append(mini)

with open("boss-Sheet.bmp", "rb") as boss_file:
    boss_sheet = displayio.OnDiskBitmap(boss_file)
bosses = []

def spawn_boss():
    boss = displayio.TileGrid(
        boss_sheet,
        pixel_shader=boss_sheet.pixel_shader,
        width=1,
        height=1,
        tile_width=64,
        tile_height=64,
        x=128-50,
        y=128-75,
    )
    boss.dir = "left"
    boss.charge = False
    boss.chargecountdown = 50
    boss.chill = True
    boss.ko = False
    boss.lives = 3
    boss.deathcount = 50
    bosses.append(boss)
    splash.append(boss)

def boss_changedir(b):
        if b.dir == "left":
            b.dir = "right"
        else:
            b.dir = "left"

def check_collision(sprite1, sprite2):
    return (
        sprite1.x < sprite2.x + 40 and
        sprite1.x + 40 > sprite2.x and
        sprite1.y < sprite2.y + 40 and
        sprite1.y + 40 > sprite2.y
    )
def on_top_of_mini():
    for i in minis:
        if check_collision(ferret_sprite, i) and not ferret_sprite.y+20 < i.y + 10 and not ferret_sprite.y + 10 < i.y+20:
            return True
    return False

with open("restart-gold.bmp", "rb") as death_file:
    death_sheet = displayio.OnDiskBitmap(death_file)

death_var = []
def display_game_over():
    death_screen = displayio.TileGrid(
        death_sheet,
        pixel_shader=death_sheet.pixel_shader,
        height=1,
        width=1,
        tile_height=32,
        tile_width=64,
        default_tile=0,
        x=(128-64)//2,
        y=(128-32)//2
    )
    death_var.append(death_screen)
    splash.append(death_screen)
    print("game over display added")
    for i in minis:
        splash.remove(i)
    minis.clear()
def remove_death_screen():
    for d in death_var:
        d[0] = 1
        #splash.remove(d)

game_over = False
speed = 1
minispeed = 1
wantedminis = 0 # how many minis to spawn at a time, changes throughout
frame = 0
ferretframe = 0
bckgndframe = 0
bobcount = 0
defaultminidir = "left"
direction = "right"
frameoffset = 0
ferretjumping = False
ferretfalling = False
maxjumpheight = 50
gamewasover = False
# stages
minitimeout = random.randint(5, 80)
minitimeoutcounter = 0
counter = 0
stage1done = "False"
stage2done = "False"
stage3done = "False"
stage4done = "False"
stage5done = "False"
stage6done = "False"
chillcountdown = random.randint(45, 50)
chargecountdown = random.randint(200, 250)
kocountdown = 100
bosscountdown = 0
numofdeaths = 0
enemieskilled = 0

breaks = [100, 100, 100, 125, 200]
stages = [500, 800, 1100, 1300]
stagedifficulty = [2, 3, 4, 5]

# stage5 -> final boss spawns

game_done = False


while True:
    if game_over == True:
        display_game_over()
        ferretjumping=False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_over == True:
                for i in minis:
                    splash.remove(i)
                minis.clear()
                for b in bosses:
                    splash.remove(b)
                bosses.clear()
                remove_death_screen()
                print("death screen removed")
                ferret_sprite.x = 10
                ferret_sprite.y=display.height-60
                game_over = False
    
    keys = pygame.key.get_pressed()
    if game_over==False:
        # checking input
        if keys[pygame.K_LEFT]:
            if ferret_sprite.x > -10 and stage5done != "True":
                ferret_sprite.x -= speed
            direction = "left"
            frameoffset = 2
        if keys[pygame.K_RIGHT]:
            if ferret_sprite.x < 128-48 and stage5done != "True":
                ferret_sprite.x += speed
            direction = "right"
            frameoffset = 6
        else:
            if direction == "left":
                frameoffset = 0
            else:
                frameoffset = 4
        if keys[pygame.K_UP] and game_over == False:
            if ferretjumping == False:
                ferretjumping = True
                ferretfalling = False
        elif keys[pygame.K_UP] and game_over == True:
            for i in minis:
                splash.remove(i)
            minis.clear()
            for b in bosses:
                splash.remove(b)
            bosses.clear()
            remove_death_screen()
            print("death screen removed")
            ferret_sprite.y=display.height-60
            game_over = False
        if keys[pygame.K_UP] and game_done == True:
            game_done = False
            print("restarting")
            stage1done = "False"
            stage2done = "False"
            stage3done = "False"
            stage4done = "False"
            stage5done = "False"
            stage6done = "False"
            words[0] = 0
            ferretfalling = False
            ferretjumping = False
            ferret_sprite.y = display.height-60
        
        if ferretjumping == True:
            if on_top_of_mini(): # jumping on top of the boss
                floor = display.height-maxjumpheight
                print("double jump")
            else:
                floor = display.height-60-maxjumpheight
            if ferret_sprite.y <= floor:
                ferretfalling = True
            if ferretfalling == True:
                ferret_sprite.y += 2
            else:
                ferret_sprite.y -= 2
            if ferret_sprite.y == display.height-60:
                ferretjumping = False
        # add more minis
        if stage5done == "False": # making sure minis are spawned when there is no boss
            if len(minis) < wantedminis and minitimeoutcounter == minitimeout:
                spawn_mini()
                print("spawned a mini")
                if defaultminidir == "left":
                    if random.randint(1,2) == 1:
                        defaultminidir = "right"
                else:
                    if random.randint(1,2) == 1:
                        defaultminidir = "left"
                minitimeout = random.randint(70, 225)
                minitimeoutcounter = 0
            elif len(minis) < wantedminis:
                minitimeoutcounter += 1

        # did we hit someone?
        for b in bosses:
            if b.lives > 0 and check_collision(ferret_sprite, b):
                if ferret_sprite.y < b.y + 10 and ferret_sprite.y > b.y - 20:
                    if b.ko == False:
                        game_over = False
                        ferretfalling = False
                        ferretjumping = True
                    elif b.ko == True:
                        game_over=False
                        b.lives -= 1
                        b.ko = False
                if ferret_sprite.y > b.y:
                    game_over = True
                    numofdeaths += 1
        for i in minis:
            if i.dead == False and check_collision(ferret_sprite, i):
                if ferret_sprite.y < i.y+5 and ferret_sprite.y+5 > i.y:
                    i.dead = False
                    game_over=True
                    numofdeaths += 1
                else:
                    game_over=False
                    i.dead = True
                    enemieskilled += 1
    
    # making our people bob
    if frame%10 == 0:
        ferretframe = (ferretframe+1)%2
    if frame % 100 == 0:
        ferret_sprite[0] = ferretframe + 1 + frameoffset
    else:
        ferret_sprite[0] = ferretframe + frameoffset
    
    if frame%10 == 0:
        bckgndframe = (bckgndframe+1)%2
    if stage5done != "True" and stage4done == "True": # background control
        background[0] = 2
    else:
        background[0] = 0
    
    for i in minis: # mini movement
        if i.dead==False:
            if (i.x < -10 and i.dir == "left") or (i.x > 130 and i.dir == "right"): # despawn
                print("a mini has despawned")
                minis.remove(i)
                splash.remove(i)
            else:
                if frame%3 == 1:
                    if i.dir == "left":
                        i.x -= minispeed
                    else:
                        i.x += minispeed
                i[0] = ferretframe
        else: # mini is dead
            i[0] = 2
            i.deathcount -= 1
            if i.deathcount <= 0:
                minis.remove(i)
                splash.remove(i)

    for b in bosses: # boss behaviour
        if b.lives > 0:
            if b.x < 0 or b.x > 128-45: # change direction
                if b.charge == True:
                    b.ko = True
                    b.charge = False
                    bosscountdown = 0
                boss_changedir(b)
                if b.x < 0:
                    b.x = 0
                if b.x > 128-45:
                    b.x = 128-45
            if b.x < ferret_sprite.x - 70 and b.chill == True:
                b.dir = "right"
            elif b.x > ferret_sprite.x + 70 and b.chill == True:
                b.dir = "left"
            if b.charge == True and game_over == False:
                b[0] = 2
                if frame%3 == 1:
                    if b.dir == "left":
                        b.x -= 3
                    else:
                        b.x += 3
            else:
                b[0] = ferretframe # normal bob
            if b.ko == True:
                b[0] = 3
                b.y = display.height - 60

    # stage manager
    if stage1done == "False":
        if counter == breaks[0]:
            stage1done = "Ongoing"
            print("Stage 1 has begun, wantedminis=1")
            minispeed = 1
            spawn_mini()
            counter = 0
            words[0] = 2
        else:
            counter += 1
            wantedminis = 0
    if stage1done == "Ongoing":
        wantedminis = stagedifficulty[0]
        if counter == stages[0]:
            stage1done = "True"
            print("Stage 1 has ended, break has started")
            counter = 0
        else:
            counter += 1
    if stage1done == "True" and stage2done == "False":
        if counter == breaks[1]:
            stage2done = "Ongoing"
            print("Stage 2 has begun, wantedminis=2")
            spawn_mini()
            counter = 0
            words[0] = 3
        else:
            counter += 1
            wantedminis = 0
    if stage2done == "Ongoing":
        wantedminis = stagedifficulty[1]
        if counter == stages[1]:
            stage2done = "True"
            print("Stage 2 has ended, break has started")
            counter = 0
        else:
            counter += 1
    if stage2done == "True" and stage3done == "False":
        if counter == breaks[2]:
            stage3done = "Ongoing"
            print("Stage 3 has begun, wantedminis=2")
            minispeed = 3
            spawn_mini()
            counter = 0
            words[0] = 4
        else:
            counter += 1
            wantedminis = 0
    if stage3done == "Ongoing":
        wantedminis = stagedifficulty[2]
        if counter == stages[2]:
            stage3done = "True"
            print("Stage 3 has ended, break has started")
            counter = 0
        else:
            counter += 1
    if stage3done == "True" and stage4done == "False":
        if counter == breaks[3]:
            stage4done = "Ongoing"
            print("Stage 4 has begun, wantedminis=3")
            spawn_mini()
            counter = 0
            minispeed = 4
            words[0] = 5
        else:
            counter += 1
            wantedminis = 0
    if stage4done == "Ongoing":
        wantedminis = stagedifficulty[3]
        if counter == stages[3]:
            stage4done = "True"
            print("Stage 4 has ended, break has started")
            counter = 0
        else:
            counter += 1
    if stage4done == "True" and stage5done == "False":
        maxjumpheight = 50
        if counter == breaks[4]:
            stage5done = "Ongoing"
            print("Final stage has begun, final boss spawned")
            minispeed = 6
            ferret_sprite.x = 10
            spawn_boss()
            for b in bosses:
                b.chill = True
            counter = 0
            words[0] = 6
        else:
            counter += 1
            wantedminis = 0
    if stage5done == "Ongoing":
        if len(bosses) < 1:
            spawn_boss()
        maxjumpheight = 70
        wantedminis = 0
        for b in bosses:
            defaultminidir = b.dir
            if b.ko == False and b.chill == False and b.charge == False:
                b.chill = True
                bosscountdown = 0
            if b.ko == True:
                b.chill = False
                b.charge = False
                if bosscountdown == kocountdown:
                    b.ko = False
                    b.chill = True
                    bosscountdown = 0
                    b.y = display.height-75
                    kocountdown = random.randint(100, 110)
                else:
                    bosscountdown += 1
            if b.chill == True:
                b.y = display.height-75
                b.charge = False
                b.ko = False
                if bosscountdown == chillcountdown:
                    b.chill = False
                    b.charge = True
                    chillcountdown = random.randint(90, 110)
                    bosscountdown = 0
                else:
                    bosscountdown += 1
                    if random.randint(1, 100) < 5:
                        spawn_mini()
            if b.charge == True:
                b.y = display.height-75
                b.chill = False
                b.ko = False
                if bosscountdown == chargecountdown:
                    b.chill = True
                    b.charge = False
                    chargecountdown = random.randint(200, 250)
                    bosscountdown = 0
                else:
                    bosscountdown += 1
            if b.lives == 0:
                b.x = (display.width//2) - 32
                b.y = (display.height//2) - 32
                enemieskilled += 1
                stage5done = "True"
                for i in minis:
                    splash.remove(i)
                minis.clear()
                print("Stage 5 Complete!")
                confetti.x = ferret_sprite.x
                confetti.y = ferret_sprite.y
                words[0] = 8
                bosscountdown = 300
    if stage5done == "True" and stage6done == "False":
            stage6done = "Ongoing"
            maxjumpheight = 50
    if stage6done == "Ongoing":
        confetti.x = ferret_sprite.x
        confetti.y = ferret_sprite.y
        if bosscountdown == 150:
            for b in bosses:
                splash.remove(b)
            bosses.clear()
            confetti[0] = 9
        if bosscountdown == 100:
            confetti[0] = 10
        if bosscountdown == 50:
            confetti[0] = 11
        if bosscountdown > 0:
            bosscountdown -= 1
        if bosscountdown == 0:
            confetti[0] = 0
            game_done = True
            print("game completed in " + str(numofdeaths) + " deaths")
            print("you killed " + str(enemieskilled) + " enemies")
            print("ready to restart...")
            bosscountdown -= 1
        if bosscountdown < 0:
            if ferretjumping == False:
                ferretjumping = True
                ferretfalling = False

    frame += 1
    time.sleep(0.02)