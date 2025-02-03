import displayio
import time 
import math
import pygame
import random
from blinka_displayio_pygamedisplay import PyGameDisplay

from ui import bg, animationHandler, font, saveManager, UFO, Star, Menu, TextManager, Gurgle, RemovalManager, GurgleSurprise, Pizza
import config

pygame.init()

removalManager = RemovalManager.RemovalManager()

trackedTime = {
    "last_save": time.monotonic(),
    "frame_track": time.monotonic(),
    "track_second": time.monotonic(),
    "food_track": time.monotonic(),
    "happiness_track": time.monotonic(),
    "float_track": time.monotonic()
}

buttons = {
    "left": pygame.K_LEFT,
    "middle": pygame.K_UP,
    "right": pygame.K_RIGHT
}

display = PyGameDisplay(width=128, height=128)
anim = animationHandler.AnimationHandler()

pizzaTexture = animationHandler

# space mono, 10x15px, 10 font size
spaceMono = font.Font("./assets/space-mono-10.bmp", 10, 15)
spaceMonoManager = TextManager.TextManager(spaceMono)

splash = displayio.Group()

splashText = [
    spaceMono.write_text("gurgle!", 2, 2),
    spaceMono.write_text("a space pet", 2, 20),
    spaceMono.write_text("loading...", 2, 96),
]

for text in splashText:
    splash.append(text)

display.show(splash)

save_data = saveManager.load_save_file() or {
    "food": math.ceil(config.FOOD_MAX / 2),
    "happiness": math.ceil(config.HAPPINESS_MAX / 2),
    "food_have": math.ceil(config.FOOD_MAX / 4),
    "special": 0
}
print("loaded save data", save_data)
time.sleep(2) # for splash screen

print("""
      Hello! Welcome to gurgle! (thats the cats name)\n
      controls:
        left arrow = eat food (makes him not hungry)
        up arrow = menu (see stats!)
        right arrow = use special item! (makes him happy)
      
        menu + left arrow = make gurgle float! (he becomes happier)
        
        enjoy! :3
      """)


star_group = displayio.Group()
text_under_group = displayio.Group()
ufos_group = displayio.Group()
text_over_group = displayio.Group()
menu_group = displayio.Group()
glorp_group = displayio.Group()
pizza_group = displayio.Group()

main_group = displayio.Group()

menu = Menu.Menu(menu_group, spaceMono, save_data)


stars = [Star.Star(star_group) for _ in range(20)]
pizzas = []
ufos = []
gSurprise = GurgleSurprise.SpriteScroller()

hide_text = config.HIDE_TEXT

if not hide_text:
    food_text = spaceMonoManager.create_text('food', f"food: {save_data['food']}/{config.FOOD_MAX}", 2, 2)
    happiness_text = spaceMonoManager.create_text('happiness', f"mood: {save_data['happiness']}/{config.HAPPINESS_MAX}", 2, 12)

    text_under_group.append(food_text)
    text_under_group.append(happiness_text)

# by priority of rendering

main_group.append(bg.Background())
main_group.append(star_group)
main_group.append(ufos_group)
main_group.append(text_under_group)
main_group.append(gSurprise.group)
main_group.append(text_over_group)
main_group.append(menu_group)
main_group.append(glorp_group)
main_group.append(pizza_group)


# sprites
gurgle = Gurgle.Gurgle(glorp_group, 32, 128 - 64)
anim.add_animation('gurgle', gurgle.current_sprite, gurgle.frames, 0.1)

deadFrames = 0

display.root_group = main_group

foodDecayTime = random.uniform(config.FOOD_TIME_DECAY["min"], config.FOOD_TIME_DECAY["max"])

def safe_remove_from_group(group, element):
    try:
        if element in group:
            group.remove(element)
            return True
        return False
    except Exception as e:
        print(f"Error removing element from group: {e}")
        return False

while True:
    current_time = time.monotonic()

    # this makes inputs bad?
    #if display.check_quit():
    #    break
    
    events = pygame.event.get()  
    
    for event in events:
        if event.type == pygame.KEYDOWN:
            if gurgle.isDead:
                continue
            if event.key == buttons["middle"]:
                menu.toggle()
            elif event.key == buttons["left"]:

                if menu.visible:
                    gurgle.toggle_float()
                else:
                    if save_data["food"] > 0 and not gurgle.isDead:
                        if (save_data["food_have"] >= 3 and save_data["food"] <= config.FOOD_MAX):

                            oldFood = save_data["food"]
                            save_data["food"] = min(save_data["food"] + 3, config.FOOD_MAX)
                            save_data["food_have"] -= save_data["food"] - oldFood

                            if not hide_text:
                                new_food_text = spaceMonoManager.update_text('food', f"food: {save_data['food']}/{config.FOOD_MAX}")
                                text_under_group.remove(food_text)
                                text_under_group.append(new_food_text)
                                food_text = new_food_text

                            pizza = Pizza.Pizza(pizza_group, anim, 32, 128 - 40)
                            pizzas.append(pizza)

                            menu.update_save_data(save_data)

            elif event.key == buttons["right"]:
                if menu.visible:
                    hide_text = not hide_text

                    if hide_text:
                        try:
                            text_food = spaceMonoManager.get_current_group('food')
                            text_happiness = spaceMonoManager.get_current_group('happiness')
                            text_under_group.remove(text_food)
                            text_under_group.remove(text_happiness)

                            text_food = None
                            text_happiness = None
                        except Exception as e:
                            print("Error in removing text", e)
                    else:
                        try:
                            text_food = spaceMonoManager.get_current_group('food')
                            text_happiness = spaceMonoManager.get_current_group('happiness')
                            text_under_group.remove(text_food)
                            text_under_group.remove(text_happiness)

                            text_food = None
                            text_happiness = None
                        except Exception as e:
                            print("Error in removing text", e)

                        
                        food_text = spaceMonoManager.create_text('food', f"food: {save_data['food']}/{config.FOOD_MAX}", 2, 2)
                        happiness_text = spaceMonoManager.create_text('happiness', f"mood: {save_data['happiness']}/{config.HAPPINESS_MAX}", 2, 12)
                        text_under_group.append(food_text)
                        text_under_group.append(happiness_text)
                else:
                    if save_data["special"] >= 1:
                        save_data["special"] -= 1
                        save_data["happiness"] = min(save_data["happiness"] + 3, config.HAPPINESS_MAX)

                        if not hide_text:
                            current_happiness_text = spaceMonoManager.get_current_group('happiness')
                            new_happiness_text = spaceMonoManager.update_text('happiness', f"mood: {save_data['happiness']}/{config.HAPPINESS_MAX}")
                            
                            if current_happiness_text:
                                text_under_group.remove(current_happiness_text)
                            text_under_group.append(new_happiness_text)
                            happiness_text = new_happiness_text


                        gSurprise.spawn(10, 15)
                        menu.update_save_data(save_data)


    if time.monotonic() - trackedTime["food_track"] >= foodDecayTime and not gurgle.isDead:
        save_data["food_have"] += random.randint(config.FOOD_DECAY["min"] + 2, config.FOOD_DECAY["max"] + 2) # make it easy for user to get food
        foodMin = config.FOOD_DECAY["min"]
        foodMax = config.FOOD_DECAY["max"]

        if gurgle.is_floating:
            foodMin = math.ceil(foodMin * 1.5)
            foodMax = math.ceil(foodMax * 1.5)

        save_data["food"] = max(0, save_data["food"] - random.randint(foodMin, foodMax))
      
        if not hide_text:
            new_food_text = spaceMonoManager.update_text('food', f"food: {save_data['food']}/{config.FOOD_MAX}")
            try:
                text_under_group.remove(food_text)
            except Exception as e:
                print("Error in removing text", e)
            text_under_group.append(new_food_text)
            food_text = new_food_text


        foodDecayTime = random.uniform(config.FOOD_TIME_DECAY["min"], config.FOOD_TIME_DECAY["max"])
        trackedTime["food_track"] = time.monotonic()

    if time.monotonic() - trackedTime["happiness_track"] >= random.uniform(config.HAPPINESS_TIME_DECAY["min"], config.HAPPINESS_TIME_DECAY["max"]) and not gurgle.isDead:
        save_data["happiness"] = max(0, save_data["happiness"] - random.randint(config.HAPPINESS_DECAY["min"], config.HAPPINESS_DECAY["max"]))
        
        if not hide_text:
            current_happiness_text = spaceMonoManager.get_current_group('happiness')
            new_happiness_text = spaceMonoManager.update_text('happiness', f"mood: {save_data['happiness']}/{config.HAPPINESS_MAX}")
            
            try:
                if current_happiness_text:
                    text_under_group.remove(current_happiness_text)
                text_under_group.append(new_happiness_text)
                happiness_text = new_happiness_text
            except Exception as e:
                print("Error in removing text", e)

        trackedTime["happiness_track"] = time.monotonic()

    if current_time - trackedTime["frame_track"] >= 1/config.LOCK_FPS:

        for pizza in pizzas[:]: 
            if pizza.update():
                try:
                    safe_remove_from_group(pizza_group, pizza.sprite)
                    pizzas.remove(pizza)
                except Exception as e:
                    print("Error in removing pizza", e)

        gSurprise.update()
        changed = gurgle.update(save_data["happiness"])
        

        if changed:
            if gurgle.state == "happy":
                gurglText = spaceMono.write_text("happy!", 8, 30)
                text_over_group.append(gurglText)
                removalManager.add_item(text_over_group, gurglText, 3, current_time)
            elif gurgle.state == "drool":
                gurglText = spaceMono.write_text("i drool!", 8, 40)
                text_over_group.append(gurglText)
                removalManager.add_item(text_over_group, gurglText, 3, current_time)
            else:
                gurglText = spaceMono.write_text(":(", 8, 40)
                text_over_group.append(gurglText)
                removalManager.add_item(text_over_group, gurglText, 3, current_time)
            anim.add_animation('gurgle', gurgle.current_sprite, gurgle.frames, 0.1)


        if save_data["food"] <= 0:
            # he dies! woop woop :(
            if gurgle.is_floating:
                gurgle.toggle_float()
            gurgle.isDead = True
            changed = gurgle.update(0)
            if changed:
                anim.add_animation('gurgle', gurgle.current_sprite, gurgle.frames, 0.1)
            deadFrames += 1
            

            if deadFrames >= config.LOCK_FPS * 5:
                save_data = {
                    "food": math.ceil(config.FOOD_MAX / 2),
                    "happiness": math.ceil(config.HAPPINESS_MAX / 2),
                    "food_have": math.ceil(config.FOOD_MAX / 4),
                    "special": 0
                }

                print("new save data", save_data)


                if not hide_text:
                    current_food_text = spaceMonoManager.get_current_group('food')
                    current_happiness_text = spaceMonoManager.get_current_group('happiness')

                    new_food_text = spaceMonoManager.update_text('food', f"food: {save_data['food']}/{config.FOOD_MAX}")
                    new_happiness_text = spaceMonoManager.update_text('happiness', f"mood: {save_data['happiness']}/{config.HAPPINESS_MAX}")

                    try:
                        if current_food_text:
                            text_under_group.remove(current_food_text)
                        if current_happiness_text:
                            text_under_group.remove(current_happiness_text)

                        text_under_group.append(new_happiness_text)
                        text_under_group.append(new_food_text)
                        
                        food_text = new_food_text
                        happiness_text = new_happiness_text
                    except Exception as e:
                        print("Error in resetting text", e)

                menu.update_save_data(save_data)
                gurgle.isDead = False
                deadFrames = 0
                continue
            
        anim.update()
        
        if not gurgle.isDead:
            for ufo in ufos:
            
                if ufo.isReset:
                    ufos.remove(ufo)
                else:
                    ufo.update()
        
        for star in stars:
            star.update()
            
        trackedTime["frame_track"] = current_time

    if time.monotonic() - trackedTime["float_track"] >= 1 and gurgle.is_floating:
        trackedTime["float_track"] = time.monotonic()
        save_data["happiness"] = min(save_data["happiness"] + 1, config.HAPPINESS_MAX)

        if not hide_text:
            current_happiness_text = spaceMonoManager.get_current_group('happiness')
            new_happiness_text = spaceMonoManager.update_text('happiness', f"mood: {save_data['happiness']}/{config.HAPPINESS_MAX}")
            
            if current_happiness_text:
                text_under_group.remove(current_happiness_text)
            text_under_group.append(new_happiness_text)
            happiness_text = new_happiness_text

        menu.update_save_data(save_data)

    if time.monotonic() - trackedTime["last_save"] >= config.SAVE_DELAY and not gurgle.isDead:

        hello = spaceMono.write_text("saving...", 8, 50)
        text_over_group.append(hello)
        saveManager.save_data(save_data)
        trackedTime["last_save"] = time.monotonic()
        time.sleep(0.2)
        text_over_group.remove(hello)


    if current_time - trackedTime["track_second"] >= 1 and not gurgle.isDead:
        trackedTime["track_second"] = current_time
        if random.uniform(0.0, 1.0) > 1 - config.SPECIAL_ITEM_CHANCE:
            save_data["special"] += 1
            
            ufo = UFO.UFO(ufos_group, anim)
            ufos.append(ufo)
            specialItemText = spaceMono.write_text("woah! ufo!", 8, 70)
            text_over_group.append(specialItemText)

            removalManager.add_item(text_over_group, specialItemText, 1, current_time)

            menu.update_save_data(save_data)

    removalManager.update(current_time)

