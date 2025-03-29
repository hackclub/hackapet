import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
import pygame
import time
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font
import random
import math



pygame.init()
pygame.font.init()

display = PyGameDisplay(width=128, height=128)
splash = displayio.Group()
splash2 = displayio.Group()

display.show(splash)

Font = bitmap_font.load_font("PixelifySans-Regular-12px.bdf")

#Sprites

#Dungeon_Background = displayio.OnDiskBitmap("Dungeon_Background.bmp")
#Dungbg_sprite = displayio.TileGrid(Dungeon_Background, pixel_shader=Dungeon_Background.pixel_shader, width=1, height=1, tile_width=128, tile_height=128)

area_sprites = displayio.OnDiskBitmap("Area_Backgrounds.bmp")

area_sprite = displayio.TileGrid(
    area_sprites,
    pixel_shader=area_sprites.pixel_shader,
    width=1,
    height=1,
    tile_width=128,
    tile_height=128,
    default_tile=1
)
area=[1, area_sprites.width/128-1, []]
for i in range(int(area_sprites.width/128)):
    area[2].append([])

splash.append(area_sprite)

Arrow = displayio.OnDiskBitmap("Arrow_Down.bmp")

Arrow_Sprite = displayio.TileGrid(
    Arrow,
    pixel_shader=Arrow.pixel_shader,
    y=16
)




Health_ = 3
HeartsList = []

for Heart_ in range(Health_):
    Hearts = displayio.OnDiskBitmap("Heart.bmp")
    Heart = displayio.TileGrid(Hearts, pixel_shader=Hearts.pixel_shader, tile_width=11, tile_height=9, y=5, x=Heart_*14+6, width=1)
    HeartsList.append(Heart)
    splash.append(Heart)



Slime_Anim_Sheet = displayio.OnDiskBitmap("Slime_Anim_Sheet.bmp")

Slime_Sprite = displayio.TileGrid(
    Slime_Anim_Sheet,
    pixel_shader=Slime_Anim_Sheet.pixel_shader,
    tile_width=18,
    tile_height=11
)


#Sprite declarations
Merchant_All = ["Merchant.bmp", displayio.OnDiskBitmap("Merchant.bmp"), displayio.TileGrid(displayio.OnDiskBitmap("Merchant.bmp"), pixel_shader=displayio.OnDiskBitmap("Merchant.bmp").pixel_shader, tile_height=50, tile_width=38), []]
Witch_Merchant_All = ["Witch_Merchant.bmp", displayio.OnDiskBitmap("Witch_Merchant.bmp"), displayio.TileGrid(displayio.OnDiskBitmap("Witch_Merchant.bmp"), pixel_shader=displayio.OnDiskBitmap("Witch_Merchant.bmp").pixel_shader, tile_height=48, tile_width=38), []]
Snack_All = ["Snacks.bmp", displayio.OnDiskBitmap("Snacks.bmp"), displayio.TileGrid(displayio.OnDiskBitmap("Snacks.bmp"), pixel_shader=(displayio.OnDiskBitmap("Snacks.bmp").pixel_shader)), []]
Potions_All = ["Potions.bmp", displayio.OnDiskBitmap("Potions.bmp"), displayio.TileGrid(displayio.OnDiskBitmap("Potions.bmp"), pixel_shader=(displayio.OnDiskBitmap("Potions.bmp").pixel_shader)), []]

Shield = displayio.TileGrid(displayio.OnDiskBitmap("Shield.bmp"), pixel_shader=(displayio.OnDiskBitmap("Shield.bmp").pixel_shader))

#Variables
#Movement Variables
Float = 0.15
JumpSpeed = 3
speed=2
UpVelocity=0
Default_Jumps = 1
Jumps = 1
#Miscellaneous
alive=True
Arrows = []
Pet = Slime_Sprite
NumPets = Slime_Anim_Sheet.width//108
RandPet = random.randint(0, NumPets-1)
splash.append(Pet)
Pet.x = (display.width - Pet.tile_width) // 2
Pet.y = display.height - 16 - Pet.tile_height
Merchant_Price = 25
Witch_Merchant_Price = 50
#Slime_Anim_Sheet.width // Pet.tile_width
Gold=0
Gold_Speed=1



frame = 0
tick=0
Shield_Stat = False



#All Functions

def areachange(Integer):
    for i in area[2][area[0]]:
        splash.remove(i)
    for i in area[2][Integer]:
        splash.append(i)
    area[0]=Integer
    splash.remove(Pet)
    splash.append(Pet)

for i in area[2][area[0]]:
    splash.append(i)


def createobject(Object, x, y, AreaNum, StartNum, width):
    Object[1] = displayio.OnDiskBitmap(Object[0])
    Object[2] = displayio.TileGrid(Object[1], pixel_shader=Object[1].pixel_shader, x=x, y=y, tile_width=width, tile_height=Object[1].height)
    Object[2][0]+=StartNum
    if AreaNum == area[0]:
        splash.append(Object[2])
    area[2][AreaNum].append(Object[2])
    Object[3].append(Object[2])
    splash.remove(Pet)
    splash.append(Pet)

def spawnarrow():
    Arrow = displayio.OnDiskBitmap("Arrow_Down.bmp")

    Arrow_Sprite = displayio.TileGrid(
        Arrow,
        pixel_shader=Arrow.pixel_shader,
        y=-11,
        x=random.randint(1, display.width-6)
    )
    Arrows.append(Arrow_Sprite)
    splash.append(Arrow_Sprite)
    
def check_collision(sprite1, sprite2):
    return (
        sprite1.x < sprite2.x + sprite2.tile_width and
        sprite1.x + sprite1.tile_width > sprite2.x and
        sprite1.y < sprite2.y + sprite2.tile_height and
        sprite1.y + sprite1.tile_height > sprite2.y
    )

createobject(Merchant_All, 45, 62, 1, 0, Merchant_All[1].width)
createobject(Witch_Merchant_All, 45, 64, 3, 0, Witch_Merchant_All[1].width)

Gold_Label = label.Label(Font, text=str(Gold), x=10, y=20)
splash.append(Gold_Label)

Merchant_Label = label.Label(Font, text=str(Merchant_Price), x=display.width//2-10, y=display.height//2-12)

splash.append(Merchant_Label)

Witch_Merchant_Label = label.Label(Font, text=str(Witch_Merchant_Price), x=display.width//2-10, y=display.height//2-12)

splash.append(Witch_Merchant_Label)

Witch_Merchant_Label.hidden=True

while True:
    if area[0]!=1:
        Merchant_Label.hidden=True
    if area[0]==1:
        Merchant_Label.hidden=False
    if area[0]!=3:
        Witch_Merchant_Label.hidden=True
    if area[0]==3:
        Witch_Merchant_Label.hidden=False
    if Shield_Stat==True:
        Shield.x=Pet.x
        Shield.y=Pet.y-10
        splash.remove(Shield)
        splash.append(Shield)
    splash.remove(Gold_Label)
    Gold_Label = label.Label(Font, text=str(Gold), x=10, y=20)
    splash.append(Gold_Label)
    keys = pygame.key.get_pressed()
    Left = keys[pygame.K_LEFT]
    Right = keys[pygame.K_RIGHT]
    Up = keys[pygame.K_UP]
    if check_collision(Slime_Sprite, Merchant_All[2]) and Up and Pet.y==display.height - 16 - Pet.tile_height and area[0]==1:
        if Gold>=Merchant_Price:
            Gold-=Merchant_Price
            createobject(Snack_All, random.randint(10, 100), -15, 1, random.randint(0, (Snack_All[1].width//9)-1), 9)
    if check_collision(Slime_Sprite, Witch_Merchant_All[2]) and Up and Pet.y==display.height - 16 - Pet.tile_height and area[0]==3:
        if Gold>=Witch_Merchant_Price:
            Gold-=Witch_Merchant_Price
            createobject(Potions_All, random.randint(10, 100), -15, 3, random.randint(0, (Potions_All[1].width//9)-1), 9)
    if area[0]==1:
        for i in Snack_All[3]:
            if i.y<101:
                i.y+=1
            if check_collision(Pet, i):
                if Health_<len(HeartsList):
                    Health_+=1
                splash.remove(i)
                area[2][1].remove(i)
                Snack_All[3].remove(i)
    if area[0]==3:
        for i in Potions_All[3]:
            if i.y<101:
                i.y+=1
            if check_collision(Pet, i):
                Num = i[0]
                if Num == 0:
                    speed=4
                if Num == 1:
                    JumpSpeed=5
                if Num == 2:
                    if Shield_Stat==False:
                        Shield_Stat = True
                        splash.append(Shield)
                        Shield.x=Pet.x
                        Shield.y=Pet.y-10
                if Num == 3:
                    Gold_Speed+=1
                splash.remove(i)
                area[2][3].remove(i)
                Potions_All[3].remove(i)
    if Left and Pet.x>0:
        Pet.x-=speed
    elif Pet.x<=0 and Left and area[0]>0:
        areachange(area[0]-1)
        Pet.x=display.width
    
    if Right and Pet.x<display.width-Pet.tile_width:
        Pet.x+=speed
    elif Pet.x>=display.width-Pet.tile_width and Right and area[0]<area[1]:
        areachange(area[0]+1)
        Pet.x=-Pet.tile_width
    
    if Up and Jumps>0:
        Jumps-=1
        UpVelocity=JumpSpeed
    if Pet.y==display.height-27:
        Jumps = Default_Jumps
    if Pet.y<display.height-27:
        UpVelocity-=Float
    if Pet.y>display.height-27:
        UpVelocity=0
        Pet.y=display.height-27
    Pet.y-=round(UpVelocity)
    if Pet.y>display.height-27:
        UpVelocity=0
        Pet.y=display.height-27
    
    tick+=1
    if tick==360:
        tick=0

    if tick%20==0 and area[0]==0:
        spawnarrow()
        Gold+=Gold_Speed
    if area[0]==0:
        for Arrow in Arrows:
            Arrow.y+=1
            if Arrow.y>display.height:
                Arrows.remove(Arrow)
                splash.remove(Arrow)
            if check_collision(Pet, Arrow) and Shield_Stat==False:
                if Health_>1:
                    UpVelocity=2
                Health_-=1
                Arrows.remove(Arrow)
                splash.remove(Arrow)
                if Health_<1:
                    RandPet = random.randint(0, NumPets-1)
                    Health_=len(HeartsList)
                    Float = 0.15
                    JumpSpeed = 3
                    speed=2
                    UpVelocity=0
                    Default_Jumps = 1
                    Jumps = 1
                    Gold=0
                    Gold_Speed=1
                    if Gold<0:
                        Gold=0
                    areachange(1)
                    Pet.x=(display.width//2)-9
            if (check_collision(Shield, Arrow) or check_collision(Pet, Arrow)) and Shield_Stat==True:
                Shield_Stat=False
                splash.remove(Shield)
                splash.remove(Arrow)
                Arrows.remove(Arrow)
                Shield = displayio.TileGrid(displayio.OnDiskBitmap("Shield.bmp"), pixel_shader=(displayio.OnDiskBitmap("Shield.bmp").pixel_shader))

    if area[0]!=0:
        for Arrow in Arrows:
            splash.remove(Arrow)
        Arrows.clear()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    for x in range(len(HeartsList)):
        if x+1>Health_:
            if HeartsList[x][0]==0:
                HeartsList[x][0]+=1
        elif x+1<=Health_:
            HeartsList[x][0]=0
    
    area_sprite[0] = area[0]
    Pet[0] = frame + RandPet*6
    if tick%20==0:
        frame = (frame + 1) % (Slime_Anim_Sheet.width // Pet.tile_width // 6)
    
    time.sleep(0.0125)
    
