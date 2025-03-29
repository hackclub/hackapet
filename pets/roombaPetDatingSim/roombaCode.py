import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
import pygame
import time
from adafruit_display_text import label
import random

pygame.init()

display = PyGameDisplay(width=128, height=128)
splash = displayio.Group()
display.show(splash)

polkadot_background = displayio.OnDiskBitmap("UROBOT-background.bmp")
bg_sprite = displayio.TileGrid(polkadot_background, pixel_shader=polkadot_background.pixel_shader)
splash.append(bg_sprite)

urobot_banner = displayio.OnDiskBitmap("UROBOT-banner.bmp")
banner_sprite = displayio.TileGrid(urobot_banner, pixel_shader=urobot_banner.pixel_shader)
splash.append(banner_sprite)

player_buttons = displayio.OnDiskBitmap("roomba-LR-buttons.bmp")
buttons_sprite = displayio.TileGrid(
    player_buttons, 
    pixel_shader=player_buttons.pixel_shader,
    x=9, 
    y=103
    )
splash.append(buttons_sprite)

date_start = displayio.OnDiskBitmap("dateStart.bmp")
date_start_sprite = displayio.TileGrid(
    date_start, 
    pixel_shader=date_start.pixel_shader,
    x=31, 
    y=103
    )

player_response = displayio.OnDiskBitmap("player-response.bmp")
player_response_sprite = displayio.TileGrid(
    player_response, 
    pixel_shader=player_response.pixel_shader,
    x=31, 
    y=103
    )
splash.append(player_response_sprite)

roomba_thumbs_down = displayio.OnDiskBitmap("roomba-thumbs-down.bmp")
roomba_thumbs_down_sprite = displayio.TileGrid(
    roomba_thumbs_down, 
    pixel_shader=roomba_thumbs_down.pixel_shader,
    x=58, 
    y=105
    )

roomba_thumbs_up = displayio.OnDiskBitmap("roomba-thumbs-up.bmp")
roomba_thumbs_up_sprite = displayio.TileGrid(
    roomba_thumbs_up, 
    pixel_shader=roomba_thumbs_up.pixel_shader,
    x=58, 
    y=105
    )

upToAdvance = displayio.OnDiskBitmap("upToAdvance.bmp")
upToAdvance_sprite = displayio.TileGrid(
    upToAdvance, 
    pixel_shader=upToAdvance.pixel_shader,
    x=31, 
    y=103
    )

upToReset = displayio.OnDiskBitmap("upToReset.bmp")
upToReset_sprite = displayio.TileGrid(
    upToReset, 
    pixel_shader=upToReset.pixel_shader,
    x=31, 
    y=103
    )

upToResetL = displayio.OnDiskBitmap("upToResetL.bmp")
upToResetL_sprite = displayio.TileGrid(
    upToResetL, 
    pixel_shader=upToResetL.pixel_shader,
    x=31, 
    y=103
    )

title_text = displayio.OnDiskBitmap("roomba-title-text.bmp")
title_text_sprite = displayio.TileGrid(
    title_text, 
    pixel_shader=title_text.pixel_shader,
    x=43, 
    y=105
    )
splash.append(title_text_sprite)

roomba_text_box = displayio.OnDiskBitmap("roomba-textbox.bmp")
roomba_text_box_sprite = displayio.TileGrid(
    roomba_text_box, 
    pixel_shader=roomba_text_box.pixel_shader,
    x=7, 
    y=2
    )

goodPerson_dialoge = displayio.OnDiskBitmap("goodPerson_D.bmp")
goodPerson_D_sprite = displayio.TileGrid(
    goodPerson_dialoge, 
    pixel_shader=goodPerson_dialoge.pixel_shader,
    x=7, 
    y=2
    )

dontLikeIt_D = displayio.OnDiskBitmap("dontLikeIt_D.bmp")
dontLikeIt_D_sprite = displayio.TileGrid(
    dontLikeIt_D, 
    pixel_shader=dontLikeIt_D.pixel_shader,
    x=7, 
    y=2
    )

broom_D = displayio.OnDiskBitmap("broom_D.bmp")
broom_D_sprite = displayio.TileGrid(
    broom_D, 
    pixel_shader=broom_D.pixel_shader,
    x=7, 
    y=2
    )

killYourself_D = displayio.OnDiskBitmap("killYourself_D.bmp")
killYourself_D_sprite = displayio.TileGrid(
    killYourself_D, 
    pixel_shader=killYourself_D.pixel_shader,
    x=7, 
    y=2
    )

haveBetterRizz_D = displayio.OnDiskBitmap("haveBetterRizz_D.bmp")
haveBetterRizz_D_sprite = displayio.TileGrid(
    haveBetterRizz_D,
    pixel_shader=haveBetterRizz_D.pixel_shader,
    x=7,
    y=2
    )

imOut_D = displayio.OnDiskBitmap("imOut_D.bmp")
imOut_D_sprite = displayio.TileGrid(
    imOut_D,
    pixel_shader=imOut_D.pixel_shader,
    x=7,
    y=2
    )

wonMeOver_D = displayio.OnDiskBitmap("wonMeOver_D.bmp")
wonMeOver_D_sprite = displayio.TileGrid(
    wonMeOver_D,
    pixel_shader=wonMeOver_D.pixel_shader,
    x=7,
    y=2
    )

comeHome_D = displayio.OnDiskBitmap("comeHome_D.bmp")
comeHome_D_sprite = displayio.TileGrid(
    comeHome_D,
    pixel_shader=comeHome_D.pixel_shader,
    x=7,
    y=2
    )

excitedToSeeYou_D = displayio.OnDiskBitmap("excitedToSeeYou_D.bmp")
excitedToSeeYou_D_sprite = displayio.TileGrid(
    excitedToSeeYou_D,
    pixel_shader=excitedToSeeYou_D.pixel_shader,
    x=7,
    y=2
    )

notAQuestion_D = displayio.OnDiskBitmap("notAQuestion_D.bmp")
notAQuestion_D_sprite = displayio.TileGrid(
    notAQuestion_D,
    pixel_shader=notAQuestion_D.pixel_shader,
    x=7,
    y=2
    )

notHeadsOrTails_D = displayio.OnDiskBitmap("notHeadsOrTails_D.bmp")
notHeadsOrTails_D_sprite = displayio.TileGrid(
    notHeadsOrTails_D,
    pixel_shader=notHeadsOrTails_D.pixel_shader,
    x=7,
    y=2
    )

headsOrTails_D = displayio.OnDiskBitmap("headsOrTails_D.bmp")
headsOrTails_D_sprite = displayio.TileGrid(
    headsOrTails_D,
    pixel_shader=headsOrTails_D.pixel_shader,
    x=7,
    y=2
    )

justLeave_D = displayio.OnDiskBitmap("justLeave_D.bmp")
justLeave_D_sprite = displayio.TileGrid(
    justLeave_D,
    pixel_shader=justLeave_D.pixel_shader,
    x=7,
    y=2
    )

tastesTheSame_D = displayio.OnDiskBitmap("tastesTheSame_D.bmp")
tastesTheSame_D_sprite = displayio.TileGrid(
    tastesTheSame_D,
    pixel_shader=tastesTheSame_D.pixel_shader,
    x=7,
    y=2
    )

pineapple_D = displayio.OnDiskBitmap("pineapple_D.bmp")
pineapple_D_sprite = displayio.TileGrid(
    pineapple_D,
    pixel_shader=pineapple_D.pixel_shader,
    x=7,
    y=2
    )

bald_D = displayio.OnDiskBitmap("bald_D.bmp")
bald_D_sprite = displayio.TileGrid(
    bald_D,
    pixel_shader=bald_D.pixel_shader,
    x=7,
    y=2
    )

noHairButThanks_D = displayio.OnDiskBitmap("noHairButThanks_D.bmp")
noHairButThanks_D_sprite = displayio.TileGrid(
    noHairButThanks_D,
    pixel_shader=noHairButThanks_D.pixel_shader,
    x=7,
    y=2
    )

hairLook_D = displayio.OnDiskBitmap("hairLook_D.bmp")
hairLook_D_sprite = displayio.TileGrid(
    hairLook_D,
    pixel_shader=hairLook_D.pixel_shader,
    x=7,
    y=2
    )

allToMyself_D = displayio.OnDiskBitmap("allToMyself_D.bmp")
allToMyself_D_sprite = displayio.TileGrid(
    allToMyself_D,
    pixel_shader=allToMyself_D.pixel_shader,
    x=7,
    y=2
    )

betterThanMe_D = displayio.OnDiskBitmap("betterThanMe_D.bmp")
betterThanMe_D_sprite = displayio.TileGrid(
    betterThanMe_D,
    pixel_shader=betterThanMe_D.pixel_shader,
    x=7,
    y=2
    )

aroundPeople_D = displayio.OnDiskBitmap("aroundPeople_D.bmp")
aroundPeople_D_sprite = displayio.TileGrid(
    aroundPeople_D,
    pixel_shader=aroundPeople_D.pixel_shader,
    x=7,
    y=2
    )

youreHere_D = displayio.OnDiskBitmap("youreHere_D.bmp")
youreHere_D_sprite = displayio.TileGrid(
    youreHere_D,
    pixel_shader=youreHere_D.pixel_shader,
    x=7,
    y=2
    )

moreTheMerrier_D = displayio.OnDiskBitmap("moreTheMerrier_D.bmp")
moreTheMerrier_D_sprite = displayio.TileGrid(
    moreTheMerrier_D,
    pixel_shader=moreTheMerrier_D.pixel_shader,
    x=7,
    y=2
    )

ownVacuum_D = displayio.OnDiskBitmap("ownVacuum_D.bmp")
ownVacuum_D_sprite = displayio.TileGrid(
    ownVacuum_D,
    pixel_shader=ownVacuum_D.pixel_shader,
    x=7,
    y=2
    )

everybodyDidThat_D = displayio.OnDiskBitmap("everybodyDidThat_D.bmp")
everybodyDidThat_D_sprite = displayio.TileGrid(
    everybodyDidThat_D,
    pixel_shader=everybodyDidThat_D.pixel_shader,
    x=7,
    y=2
    )

justLikeMeFR_D = displayio.OnDiskBitmap("justLikeMeFR_D.bmp")
justLikeMeFR_D_sprite = displayio.TileGrid(
    justLikeMeFR_D,
    pixel_shader=justLikeMeFR_D.pixel_shader,
    x=7,
    y=2
    )

suckForMoney_D = displayio.OnDiskBitmap("suckForMoney_D.bmp")
suckForMoney_D_sprite = displayio.TileGrid(
    suckForMoney_D,
    pixel_shader=suckForMoney_D.pixel_shader,
    x=7,
    y=2
    )

staySafe_D = displayio.OnDiskBitmap("staySafe_D.bmp")
staySafe_D_sprite = displayio.TileGrid(
    staySafe_D,
    pixel_shader=staySafe_D.pixel_shader,
    x=7,
    y=2
    )

huhHow_D = displayio.OnDiskBitmap("huhHow_D.bmp")
huhHow_D_sprite = displayio.TileGrid(
    huhHow_D,
    pixel_shader=huhHow_D.pixel_shader,
    x=7,
    y=2
    )

drinkElectricity_D = displayio.OnDiskBitmap("drinkElectricity_D.bmp")
drinkElectricity_D_sprite = displayio.TileGrid(
    drinkElectricity_D,
    pixel_shader=drinkElectricity_D.pixel_shader,
    x=7,
    y=2
    )

weak_D = displayio.OnDiskBitmap("weak_D.bmp")
weak_D_sprite = displayio.TileGrid(
    weak_D,
    pixel_shader=weak_D.pixel_shader,
    x=7,
    y=2
    )

humanOfCulture_D = displayio.OnDiskBitmap("humanOfCulture_D.bmp")
humanOfCulture_D_sprite = displayio.TileGrid(
    humanOfCulture_D,
    pixel_shader=humanOfCulture_D.pixel_shader,
    x=7,
    y=2
    )

spicyFood_D = displayio.OnDiskBitmap("spicyFood_D.bmp")
spicyFood_D_sprite = displayio.TileGrid(
    spicyFood_D,
    pixel_shader=spicyFood_D.pixel_shader,
    x=7,
    y=2
    )

stayHumble_D = displayio.OnDiskBitmap("stayHumble_D.bmp")
stayHumble_D_sprite = displayio.TileGrid(
    stayHumble_D,
    pixel_shader=stayHumble_D.pixel_shader,
    x=7,
    y=2
    )

nahIdWin_D = displayio.OnDiskBitmap("nahIdWin_D.bmp")
nahIdWin_D_sprite = displayio.TileGrid(
    nahIdWin_D,
    pixel_shader=nahIdWin_D.pixel_shader,
    x=7,
    y=2
    )

wouldYouLose_D = displayio.OnDiskBitmap("wouldYouLose_D.bmp")
wouldYouLose_D_sprite = displayio.TileGrid(
    wouldYouLose_D,
    pixel_shader=wouldYouLose_D.pixel_shader,
    x=7,
    y=2
    )

riledUp_D = displayio.OnDiskBitmap("riledUp_D.bmp")
riledUp_D_sprite = displayio.TileGrid(
    riledUp_D,
    pixel_shader=riledUp_D.pixel_shader,
    x=7,
    y=2
    )

loveMe_D = displayio.OnDiskBitmap("loveMe_D.bmp")
loveMe_D_sprite = displayio.TileGrid(
    loveMe_D,
    pixel_shader=loveMe_D.pixel_shader,
    x=7,
    y=2
    )

keepGrounded_D = displayio.OnDiskBitmap("keepGrounded_D.bmp")
keepGrounded_D_sprite = displayio.TileGrid(
    keepGrounded_D,
    pixel_shader=keepGrounded_D.pixel_shader,
    x=7,
    y=2
    )

thatsRude_D = displayio.OnDiskBitmap("thatsRude_D.bmp")
thatsRude_D_sprite = displayio.TileGrid(
    thatsRude_D,
    pixel_shader=thatsRude_D.pixel_shader,
    x=7,
    y=2
    )

tooCliche_D = displayio.OnDiskBitmap("tooCliche_D.bmp")
tooCliche_D_sprite = displayio.TileGrid(
    tooCliche_D,
    pixel_shader=tooCliche_D.pixel_shader,
    x=7,
    y=2
    )

niceWeather_D = displayio.OnDiskBitmap("niceWeather_D.bmp")
niceWeather_D_sprite = displayio.TileGrid(
    niceWeather_D,
    pixel_shader=niceWeather_D.pixel_shader,
    x=7,
    y=2
    )

wiseChoice_D = displayio.OnDiskBitmap("wiseChoice_D.bmp")
wiseChoice_D_sprite = displayio.TileGrid(
    wiseChoice_D,
    pixel_shader=wiseChoice_D.pixel_shader,
    x=7,
    y=2
    )

howDoILook_D = displayio.OnDiskBitmap("howDoILook_D.bmp")
howDoILook_D_sprite = displayio.TileGrid(
    howDoILook_D,
    pixel_shader=howDoILook_D.pixel_shader,
    x=7,
    y=2
    )

youHateMe_D = displayio.OnDiskBitmap("youHateMe_D.bmp")
youHateMe_D_sprite = displayio.TileGrid(
    youHateMe_D,
    pixel_shader=youHateMe_D.pixel_shader,
    x=7,
    y=2
    )

choicesMatter_D = displayio.OnDiskBitmap("choicesMatter_D.bmp")
choicesMatter_D_sprite = displayio.TileGrid(
    choicesMatter_D,
    pixel_shader=choicesMatter_D.pixel_shader,
    x=7,
    y=2
    )

filmCritic_D = displayio.OnDiskBitmap("filmCritic_D.bmp")
filmCritic_D_sprite = displayio.TileGrid(
    filmCritic_D,
    pixel_shader=filmCritic_D.pixel_shader,
    x=7,
    y=2
    )

goodMovie_D = displayio.OnDiskBitmap("goodMovie_D.bmp")
goodMovie_D_sprite = displayio.TileGrid(
    goodMovie_D,
    pixel_shader=goodMovie_D.pixel_shader,
    x=7,
    y=2
    )

theColorPurple_D = displayio.OnDiskBitmap("theColorPurple_D.bmp")
theColorPurple_D_sprite = displayio.TileGrid(
    theColorPurple_D,
    pixel_shader=theColorPurple_D.pixel_shader,
    x=7,
    y=2
    )

cheesy_D = displayio.OnDiskBitmap("cheesy_D.bmp")
cheesy_D_sprite = displayio.TileGrid(
    cheesy_D,
    pixel_shader=cheesy_D.pixel_shader,
    x=7,
    y=2
    )

howsItGoing_D = displayio.OnDiskBitmap("howsItGoing_D.bmp")
howsItGoing_D_sprite = displayio.TileGrid(
    howsItGoing_D,
    pixel_shader=howsItGoing_D.pixel_shader,
    x=7,
    y=2
    )

meeting_D = displayio.OnDiskBitmap("meeting_D.bmp")
meeting_D_sprite = displayio.TileGrid(
    meeting_D,
    pixel_shader=meeting_D.pixel_shader,
    x=7,
    y=2
    )

hello_D = displayio.OnDiskBitmap("hello_D.bmp")
hello_D_sprite = displayio.TileGrid(
    hello_D,
    pixel_shader=hello_D.pixel_shader,
    x=7,
    y=2
    )

roomba_sheet = displayio.OnDiskBitmap("roomba-pet-happy.bmp")

roomba_emotion = 1
tile_width = 100
tile_height = 45

roomba_sprite = displayio.TileGrid(
    roomba_sheet,
    pixel_shader=roomba_sheet.pixel_shader,
    width=1,
    height=1,
    tile_width=tile_width,
    tile_height=tile_height,
    default_tile=0,
    x=(display.width - tile_width) // 2,  
    y=48     
)

splash.append(roomba_sprite)

fireball_bitmap = displayio.OnDiskBitmap("fireball.bmp")

fireballs = []
screen_state = "home_screen"
thumb_type = "up"
thumb_active = False
question_count = 0
game_over = False
#home_screen = True
#start_screen = False
#game_screen = False
current_question = 0
player_score = 0

def change_roomba_sprite():
    roomba_sprite = displayio.TileGrid(
    roomba_sheet,
    pixel_shader=roomba_sheet.pixel_shader,
    width=1,
    height=1,
    tile_width=tile_width,
    tile_height=tile_height,
    default_tile=0,
    x=(display.width - tile_width) // 2,  
    y=48     
    )
    splash.append(roomba_sprite)

# Function to check for collisions
def check_collision(sprite1, sprite2):
    return (
        sprite1.x < sprite2.x + 32 and
        sprite1.x + 32 > sprite2.x and
        sprite1.y < sprite2.y + 32 and
        sprite1.y + 32 > sprite2.y
    )

death = displayio.OnDiskBitmap("restart.bmp")

def start_game():
    splash.append(bg_sprite)
    splash.append(roomba_sprite)
    splash.append(player_response_sprite)
    splash.append(buttons_sprite)
    splash.append(roomba_sprite)
    splash.append(date_start_sprite)

def display_game_over():
    global death_hi
    death_hi = displayio.TileGrid(
        death,
        pixel_shader=roomba_sheet.pixel_shader,
        width=1,
        height=1,
        tile_width=64,
        tile_height=32,
        default_tile=0,
        x=(display.width - 64) // 2,  
        y=(display.height - 32) // 2  
    )
    splash.append(death_hi)
    for i in fireballs:
        splash.remove(i)
    fireballs.clear()

asked_questions = []

def set_initial_response():
    splash.append(roomba_text_box_sprite)
    splash.append(player_response_sprite)
    splash.append(upToAdvance_sprite)
    random_response = random.randint(1,3)
    if random_response == 1:
        splash.append(hello_D_sprite)
    elif random_response == 2:
        splash.append(meeting_D_sprite)
    elif random_response == 3:
        splash.append(howsItGoing_D_sprite)
    
def set_question():
    global current_question
    global thumb_active
    global thumb_type
    global roomba_emotion
    global toChangeEmotion
    splash.append(roomba_text_box_sprite)
    splash.append(player_response_sprite)
    splash.append(roomba_thumbs_up_sprite)
    random_response = random.randint(1,15)
    if random_response in asked_questions:
        random_response = random.randint(1,15)
    if random_response == 1:
        splash.append(broom_D_sprite)
    elif random_response == 2:
        splash.append(theColorPurple_D_sprite)
    elif random_response == 3:
        splash.append(choicesMatter_D_sprite)
    elif random_response == 4:
        splash.append(howDoILook_D_sprite)
    elif random_response == 5:
        splash.append(niceWeather_D_sprite)
    elif random_response == 6:
        splash.append(loveMe_D_sprite)
    elif random_response == 7:
        splash.append(wouldYouLose_D_sprite)
    elif random_response == 8:
        splash.append(spicyFood_D_sprite)
    elif random_response == 9:
        splash.append(drinkElectricity_D_sprite)
    elif random_response == 10:
        splash.append(suckForMoney_D_sprite)
    elif random_response == 11:
        splash.append(ownVacuum_D_sprite)
    elif random_response == 12:
        splash.append(aroundPeople_D_sprite)
    elif random_response == 13:
        splash.append(hairLook_D_sprite)
    elif random_response == 14:
        splash.append(pineapple_D_sprite)
    elif random_response == 15:
        splash.append(headsOrTails_D_sprite)
    asked_questions.append(random_response)
    current_question = random_response
    thumb_active = True
    thumb_type = "up"
    roomba_emotion = 1
    toChangeEmotion = True

def results():
    global toChangeEmotion
    global roomba_emotion
    splash.append(player_response_sprite)
    splash.append(roomba_text_box_sprite)
    
    random_response = random.randint(1,3)
    if player_score > 0:
        splash.append(upToReset_sprite)
        if random_response == 1:
            splash.append(excitedToSeeYou_D_sprite)
            roomba_emotion = 5
        elif random_response == 2:
            splash.append(comeHome_D_sprite)
            roomba_emotion = 6
        elif random_response == 3:
            splash.append(wonMeOver_D_sprite)
            roomba_emotion = 5
    elif player_score <= 0:
        splash.append(upToResetL_sprite)
        if random_response == 1:
            splash.append(imOut_D_sprite)
            roomba_emotion = 6
        elif random_response == 2:
            splash.append(haveBetterRizz_D_sprite)
            roomba_emotion = 2
        elif random_response == 3:
            splash.append(killYourself_D_sprite)
            roomba_emotion = 4
    toChangeEmotion = True

def reset():
    global roomba_emotion
    global toChangeEmotion
    global current_question
    global player_score
    global screen_state
    global thumb_type
    global question_count
    global thumb_active
    screen_state = "home_screen"
    thumb_type = "up"
    thumb_active = False
    question_count = 0
    current_question = 0
    player_score = 0
    splash.append(bg_sprite)
    roomba_emotion = 1
    toChangeEmotion = True
    splash.append(roomba_sprite)
    splash.append(banner_sprite)
    splash.append(buttons_sprite)
    splash.append(player_response_sprite)
    splash.append(title_text_sprite)

def spawn_fireball():
    x_position = random.randint(0, display.width - fireball_bitmap.width)
    fireball = displayio.TileGrid(
        fireball_bitmap,
        pixel_shader=fireball_bitmap.pixel_shader,
        width=1,
        height=1,
        tile_width=fireball_bitmap.width,
        tile_height=fireball_bitmap.height,
        x=x_position,
        y=-32
    )
    fireballs.append(fireball)
    splash.append(fireball)

frame = 0
speed = 4 
toChangeEmotion = False

while True:
    #1 = Happy, 2 = Sad, 3 = Excited, 4 = Annoyed, 5 = Love, 6 = OWO, 7 = Confused, 8 = Broken
    if roomba_emotion == 1:
        roomba_sheet = displayio.OnDiskBitmap("roomba-pet-happy.bmp")
    elif roomba_emotion == 2:
        roomba_sheet = displayio.OnDiskBitmap("roomba-pet-sad.bmp")
    elif roomba_emotion == 3:
        roomba_sheet = displayio.OnDiskBitmap("roomba-pet-excited.bmp")
    elif roomba_emotion == 4:
        roomba_sheet = displayio.OnDiskBitmap("roomba-pet-annoyed.bmp")
    elif roomba_emotion == 5:
        roomba_sheet = displayio.OnDiskBitmap("roomba-pet-love.bmp")
    elif roomba_emotion == 6:
        roomba_sheet = displayio.OnDiskBitmap("roomba-pet-owo.bmp")
    elif roomba_emotion == 7:
        roomba_sheet = displayio.OnDiskBitmap("roomba-pet-confused.bmp")
    elif roomba_emotion == 8:
        roomba_sheet = displayio.OnDiskBitmap("roomba-pet-broken.bmp")

    if toChangeEmotion == True:
        change_roomba_sprite()
        toChangeEmotion = False
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_over == True:
                for i in fireballs:
                    splash.remove(i)
                fireballs.clear()
                splash.remove(death_hi)
                game_over = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT] or keys[pygame.K_LEFT]:
        if thumb_active == True:
            splash.append(player_response_sprite)
            if thumb_type == "up":
                thumb_type = "down"
                splash.append(roomba_thumbs_down_sprite)
            elif thumb_type == "down":
                thumb_type = "up"
                splash.append(roomba_thumbs_up_sprite)

    if keys[pygame.K_UP]:
        if screen_state == "home_screen":
            start_game()
            screen_state = "start_screen"

        elif screen_state == "start_screen":
            set_initial_response()
            screen_state = "base_screen"

        elif screen_state == "base_screen":
            if question_count <= 3:
                set_question()
                screen_state = "answer_screen"
            elif question_count > 3:
                screen_state = "finish_screen"

        elif screen_state == "finish_screen":
            results()
            screen_state = "reset_screen"

        elif screen_state == "reset_screen":
            reset()
            screen_state = "home_screen"

        elif screen_state == "answer_screen":
            splash.append(roomba_text_box_sprite)
            if current_question == 1:
                if thumb_type == "up":
                    splash.append(dontLikeIt_D_sprite)
                    roomba_emotion = 7
                    player_score = player_score - 1 
                elif thumb_type == "down":
                    splash.append(cheesy_D_sprite)
                    roomba_emotion = 3
                    player_score = player_score + 1 
            if current_question == 2:
                if thumb_type == "up":
                    splash.append(goodMovie_D_sprite)
                    roomba_emotion = 5
                    player_score = player_score + 1 
                elif thumb_type == "down":
                    splash.append(filmCritic_D_sprite)
                    roomba_emotion = 4
                    player_score = player_score - 1 
            if current_question == 3:
                if thumb_type == "up":
                    splash.append(goodPerson_D_sprite)
                    roomba_emotion = 3
                    player_score = player_score + 1 
                elif thumb_type == "down":
                    splash.append(youHateMe_D_sprite)
                    roomba_emotion = 2
                    player_score = player_score - 1 
            if current_question == 4:
                if thumb_type == "up":
                    splash.append(wiseChoice_D_sprite)
                    roomba_emotion = 1
                    player_score = player_score + 1 
                elif thumb_type == "down":
                    splash.append(thatsRude_D_sprite)
                    roomba_emotion = 2
                    player_score = player_score - 1 
            if current_question == 5:
                if thumb_type == "up":
                    splash.append(tooCliche_D_sprite)
                    roomba_emotion = 4
                    player_score = player_score - 1 
                elif thumb_type == "down":
                    splash.append(keepGrounded_D_sprite)
                    roomba_emotion = 5
                    player_score = player_score + 1 
            if current_question == 6:
                if thumb_type == "up":
                    splash.append(riledUp_D_sprite)
                    roomba_emotion = 6
                    player_score = player_score + 1 
                elif thumb_type == "down":
                    splash.append(riledUp_D_sprite)
                    roomba_emotion = 4
                    player_score = player_score - 1 
            if current_question == 7:
                if thumb_type == "up":
                    splash.append(stayHumble_D_sprite)
                    roomba_emotion = 1
                    player_score = player_score + 1 
                elif thumb_type == "down":
                    splash.append(nahIdWin_D_sprite)
                    roomba_emotion = 4
                    player_score = player_score - 1 
            if current_question == 8:
                if thumb_type == "up":
                    splash.append(humanOfCulture_D_sprite)
                    roomba_emotion = 1
                    player_score = player_score + 1 
                elif thumb_type == "down":
                    splash.append(weak_D_sprite)
                    roomba_emotion = 2
                    player_score = player_score - 1 
            if current_question == 9:
                if thumb_type == "up":
                    splash.append(huhHow_D_sprite)
                    roomba_emotion = 7
                    player_score = player_score - 1 
                elif thumb_type == "down":
                    splash.append(staySafe_D_sprite)
                    roomba_emotion = 5
                    player_score = player_score + 1 
            if current_question == 10:
                if thumb_type == "up":
                    splash.append(justLikeMeFR_D_sprite)
                    roomba_emotion = 3
                    player_score = player_score + 1 
                elif thumb_type == "down":
                    splash.append(everybodyDidThat_D_sprite)
                    roomba_emotion = 7
                    player_score = player_score - 1 
            if current_question == 11:
                if thumb_type == "up":
                    splash.append(moreTheMerrier_D_sprite)
                    roomba_emotion = 3
                    player_score = player_score + 1 
                elif thumb_type == "down":
                    splash.append(youreHere_D_sprite)
                    roomba_emotion = 4
                    player_score = player_score - 1 
            if current_question == 12:
                if thumb_type == "up":
                    splash.append(betterThanMe_D_sprite)
                    roomba_emotion = 2
                    player_score = player_score - 1 
                elif thumb_type == "down":
                    splash.append(allToMyself_D_sprite)
                    roomba_emotion = 6
                    player_score = player_score + 1 
            if current_question == 13:
                if thumb_type == "up":
                    splash.append(noHairButThanks_D_sprite)
                    roomba_emotion = 1
                    player_score = player_score + 1 
                elif thumb_type == "down":
                    splash.append(bald_D_sprite)
                    roomba_emotion = 2
                    player_score = player_score - 1 
            if current_question == 14:
                if thumb_type == "up":
                    splash.append(tastesTheSame_D_sprite)
                    roomba_emotion = 3
                    player_score = player_score + 1 
                elif thumb_type == "down":
                    splash.append(justLeave_D_sprite)
                    roomba_emotion = 4
                    player_score = player_score - 1 
            if current_question == 15:
                if thumb_type == "up":
                    splash.append(notHeadsOrTails_D_sprite)
                    roomba_emotion = 7
                    player_score = player_score - 1 
                elif thumb_type == "down":
                    splash.append(notAQuestion_D_sprite)
                    roomba_emotion = 1
                    player_score = player_score + 1 
            thumb_active = False
            toChangeEmotion = True
            screen_state = "base_screen"
            question_count = question_count + 1
            splash.append(player_response_sprite)
            splash.append(upToAdvance_sprite)
        
    if game_over == False:
        if keys[pygame.K_1]:
            roomba_emotion = 1
            toChangeEmotion = True
        if keys[pygame.K_2]:
            roomba_emotion = 2
            toChangeEmotion = True
        if keys[pygame.K_3]:
            roomba_emotion = 3
            toChangeEmotion = True
        if keys[pygame.K_4]:
            roomba_emotion = 4
            toChangeEmotion = True
        if keys[pygame.K_5]:
            roomba_emotion = 5
            toChangeEmotion = True
        if keys[pygame.K_6]:
            roomba_emotion = 6
            toChangeEmotion = True
        if keys[pygame.K_7]:
            roomba_emotion = 7
            toChangeEmotion = True
        if keys[pygame.K_8]:
            roomba_emotion = 8
            toChangeEmotion = True
      #  if random.random() < 0.05:  # spawn rate
           # spawn_fireball()

    for fireball in fireballs:
        fireball.y += 5 
        if fireball.y > display.height:
            splash.remove(fireball)
            fireballs.remove(fireball)
        elif check_collision(roomba_sprite, fireball):
            game_over = True
            display_game_over()
            
            
    roomba_sprite[0] = frame
    frame = (frame + 1) % (roomba_sheet.width // tile_width)

    time.sleep(0.1)