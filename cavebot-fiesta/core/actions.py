from pyautogui import locateOnScreen, moveTo, click, locateAllOnScreen, center, dragTo
from keyboard import add_hotkey, press_and_release
import core.nostalther.config
import threading
from collections import defaultdict
from time import sleep, strftime, localtime
import os

def start_loop():
    global loop_status
    loop_status = True
    log("STARTED!")

def pause_loop():
    global loop_status
    loop_status = False
    log("PAUSED!")
    log("PRESS PAGE UP TO RESUME")

def stop_loop():
    log("EXITING...")
    os._exit(0)

# register keys to turn on/off the cavebot
add_hotkey(START_KEY, start_loop)
add_hotkey(PAUSE_KEY, pause_loop)
add_hotkey(STOP_KEY, stop_loop)

def log(message):
    """Prints a log message with a timestamp."""
    timestamp = strftime("%H:%M:%S", localtime())
    print(f"{timestamp}: {message}")

def use_uh():
    """Uses an Ultimate Healing Rune if health is below HEAL_BELOW_HP."""
    health_percentage = get_bar_percentage(REGION_HEALTH)
    if health_percentage > HEAL_BELOW_HP:
        return

    log(f"Health: {health_percentage:1f}% - Using one Ultimate Healing Rune...")
    moveTo(REGION_UH)
    click(REGION_UH, button='right')
    moveTo(PLAYER_SQM)
    click(PLAYER_SQM, button='left')
    sleep(1)

def cast_spell(spell_name):
    """Casts a spell if mana is above CAST_SPELL_ABOVE_MANA."""
    mana_percentage = get_bar_percentage(REGION_MANA)
    if mana_percentage < CAST_SPELL_ABOVE_MANA:
        return

    eat_food()
    spell_key = SPELLS.get(spell_name)
    log(f"Mana: {mana_percentage:.1f}% - Casting {spell_name}...")
    press_and_release(spell_key)
    sleep(1)

def eat_food():
    """Eat food."""
    moveTo(REGION_FOOD)
    for _ in range(2):
        click(REGION_FOOD, button='right')

def attack_next_monster():
    """Search for a monster and attack if found in the REGION_BATTLE. If the battle is clean and a monster was attacked, it will open the dead corpses.
    """
    monster_attacked = False
    while True:
        monster_on_battle = False
        for target in target_list:
            targeting = locateOnScreen(IMG_DIR + "targeting_" + target + ".PNG", confidence=0.99, region=REGION_BATTLE)
            monster_on_battle = locateOnScreen(IMG_DIR + target + ".PNG", confidence=0.9, region=REGION_BATTLE)
            if monster_on_battle and not targeting:
                sleep(1)
                moveTo(MONSTER_IN_BATTLE)
                sleep(0.5)
                click(button="left")
                monster_attacked = True  # set to True when a monster is attacked
                break
        # exit the while loop if no monster is found
        if not monster_on_battle:
            break

    # check if a monster was attacked
    if monster_attacked:
        open_corpse()

def open_corpse():
    """Open the dead corpses in a 8x8 sqm area around REGION_PLAYER (8x8 sqm). It moves the mouse to pre-defined positions and right-clicks to open corpses.
    """
    for pos in POS_LIST:
        moveTo(pos[0], pos[1])
        click(button="right")

'''
# TODO: The corpses of some creatures are not being found. Find a effective method to locate them in the function below.
def open_corpse(target_monster):
    # find and open dead corpse in REGION_PLAYER (8x8 sqm)
  count = len(target_monster)
  for monster in range(0,(count)):
      dead_monster = locateAllOnScreen(IMG_DIR + target_monster[monster] + ".PNG", confidence=0.96, region=REGION_PLAYER)
    sleep(0.5)
    for corpse in dead_monster:
        center_x, center_y = center(corpse)
      moveTo(center_x, center_y)
      click(button="right")
      sleep(0.8)
'''

def eat_food_from_corpse(fooditems):
    """Eat food from the corpse by right-clicking on identified food items in the REGION_LOOT.

    Parameters:
        fooditems (list): List of food item image names to locate and eat."""
    count = len(fooditems)
    for item in range(count):
        food = locateAllOnScreen(IMG_DIR + fooditems[item] + ".PNG", confidence=0.9, region=REGION_LOOT)
        for item in food:
            center_x, center_y = center(item)
            moveTo(center_x, center_y)
            sleep(0.5)
            click(button="right") 

def loot_corpse(lootitems):
    """Loot items from a corpse by dragging them to the backpack.

    Parameters:
        lootitems (list): List of loot item image names to locate and loot."""
    backpack = locateOnScreen(bpname)
    count = len(lootitems)
    for item in range(count):
        gold = locateAllOnScreen(IMG_DIR + lootitems[item] + ".PNG", confidence=0.9, region=REGION_LOOT)
        for item in gold:
            center_x, center_y = center(item)
            moveTo(center_x, center_y)
            sleep(0.5)
            dragTo(backpack.left, backpack.top + 20, duration=0.2)
            sleep(0.5)
            press_and_release('enter')
            sleep(1)

def find_coin_positions(coin_image, region):
    """Find gold coin positions (clusters) on the screen within a specified region.

    Parameters:
        coin_image (str): The image file name of the coin.
    region (tuple): The region of the screen to search for coins.

    Returns:
        dict: A dictionary of coin positions grouped by their proximity."""
    coin_positions = defaultdict(list)
    find_objects = locateAllOnScreen(coin_image, confidence=0.9, region=region)

    for coin_pos in find_objects:
        added_to_group = False
        for group, positions in coin_positions.items():
            for pos in positions:
                if abs(coin_pos.left - pos[0]) < 20 and abs(coin_pos.top - pos[1]) < 20:
                    coin_positions[group].append((coin_pos.left, coin_pos.top, coin_pos.width, coin_pos.height))
                    added_to_group = True
                    break
            if added_to_group:
                break

        if not added_to_group:
            coin_positions[len(coin_positions) + 1].append((coin_pos.left, coin_pos.top, coin_pos.width, coin_pos.height))

    return coin_positions

def loot_goldcoin(coins):
    """Loot gold coins from a corpse by dragging them to the backpack.

    Parameters:
        coins (list): List of coin image names to locate and loot."""
    backpack = locateOnScreen(bpname)
    if not backpack:
        print("Backpack not found")
        return

    for coin in coins:
        while True:
            coin_positions = find_coin_positions(IMG_DIR + coin + ".PNG", REGION_LOOT)
            if not coin_positions:
                break  # exit if no more coins are found

            # flag to check if any coin was looted in this iteration
            looted = False

            for group, positions in coin_positions.items():
                if positions:
                    position = positions[0]  # get the first coin position in the group
                    center_x = position[0] + position[2] // 2
                    center_y = position[1] + position[3] // 2
                    moveTo(center_x, center_y)
                    sleep(0.5)
                    dragTo(backpack.left, backpack.top + 20, duration=0.3)
                    sleep(0.1)
                    press_and_release('enter')
                    sleep(0.3) 
                    looted = True
                    break  # break after looting the first coin in the group

            if not looted:
                break  # exit if no coin was looted in this iteration

def drop_loot_on_floor(dropitems, bags):
    """Drop loot on the floor by dragging items from bags to the player's location.

    Parameters:
        dropitems (list): List of items to drop.
    bags (list): List of bag image names to locate and open."""
    for bag in bags:
        bag_positions = list(locateAllOnScreen(IMG_DIR + bag + ".PNG", confidence=0.99, region=REGION_LOOT))
        for position in bag_positions:
            center_x, center_y = center(position)
            moveTo(center_x, center_y)
            sleep(0.5)
            click(button="right")
            sleep(0.2)

    for dropitem in dropitems:
        item_positions = list(locateAllOnScreen(IMG_DIR + dropitem + ".PNG", confidence=0.9, region=REGION_LOOT))
        for position in item_positions:
            center_x, center_y = center(position)
            moveTo(center_x, center_y)
            sleep(0.5)
            dragTo(PLAYER_SQM, duration=0.8)
            sleep(0.5)

def move(location):
    """
    Move the mouse to the center of the specified location.

    Parameters:
        location (tuple): The location to move the mouse to.
    """
    x, y = center(location)
    moveTo(x, y)

def move_and_click(location):
    """
    Move the mouse to the center of the specified location and click.

    Parameters:
        location (tuple): The location to move the mouse to and click.
    """
    move(location)
    click()
    sleep(0.5)

def thread_attack_monster():
    """
    Open a thread to continuously attack monsters while loop_status is True.
    """
    while True:  # infinite loop to continuos attack monsters
        if loop_status:
            attack_next_monster()

# creates an attack thread outside principal loop
threadKillMonster = threading.Thread(target=thread_attack_monster)
threadKillMonster.daemon = True  # defining thread as daemon to stop it when the principal program ends
#threadKillMonster.start()

def main():
    """Main function."""
    log("-------------------")
    log(f"CAVEBOT-FIESTA {VERSION}")
    log("-------------------")
    log(f"{START_KEY}   → Start")
    log(f"{PAUSE_KEY} → Pause")
    log(f"{STOP_KEY}        → Exit")
    log("-------------------")
    while True:
        if loop_status:
            for waypoint in WAYPOINT_RANGE: 
                position_in_map = locateOnScreen(ICONS_DIR + "icon_{}.png".format(waypoint), confidence=0.9, region=REGION_MINIMAP)
            if position_in_map:
                move_and_click(position_in_map)
                log(f"Going to waypoint: {waypoint}")
                conjure_rune()
                #eat_food()
                sleep(10) # sleep while walking to next waypoint 
                check_position = locateOnScreen(ICONS_DIR + "icon_{}.png".format(waypoint), confidence=0.9, region=REGION_MINIMAP)
                if not check_position:
                    log(f"Already on waypoint {waypoint}")
                    conjure_rune()
                    attack_next_monster()

                    while True:
                        conjure_rune()
                        battle = locateOnScreen(IMG_DIR + "battle.PNG", confidence=0.9, region=REGION_BATTLE)
                        if battle:
                            log("Clean battle")
                        #open_corpse(dead_monster)      # locate dead monster corpse
                        #open_corpse()                         # 8x8 right-clicks to open corpse
                        eat_food_from_corpse(food)
                        #loot_corpse(items)
                        loot_goldcoin(coins)
                        drop_loot_on_floor(drop_items, bags)
                        print('---')
                        break
