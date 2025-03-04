# software version
VERSION = "v1.0"

# define status and core variables 
loop_status = False
START_KEY = "PAGE UP"
PAUSE_KEY = "PAGE DOWN"
STOP_KEY = "END"
REGION_HEALTH =
REGION_MANA = 
REGION_UH = 
REGION_FOOD = 

# bar percentages
HEAL_BELOW_HP = 60
CAST_SPELL_ABOVE_MANA = 80

# global variables - referencing x and y axis coords
WAYPOINT_RANGE = range(1,33)                            # waypoint (icons) range
REGION_BATTLE = (1746, 362, 170, 165)                   # battle region (below equipment set and skill bar)
REGION_MINIMAP = (1755, 35, 108, 105)                   # northeast minimap
#REGION_MANA = (1840, 161, 24, 18)                       # region when mana is ~95% full
REGION_ARROW = (1841, 289)                              # arrow region
MONSTER_IN_BATTLE = (1754, 383)                         # first monster on battle
REGION_PLAYER = (1193, 193, 126, 129)                   # region 8x8 sqm near player (to loot dead copses)
POS_LIST = [(1223, 206), (1263, 208),                   # region 8x8 sqm to right-clicks to open corpses
            (1301, 213), (1305, 252), 
            (1302, 289), (1265, 285), 
            (1226, 287), (1220, 251)] 
PLAYER_SQM = (1230, 216)                                # sqm under player foot (to drop items from lootbag)
REGION_LOOT = (1748, 677, 169, 360)                     # region to find items from corpse (below battle)

# directory to images (change this to play other ots) 
IMG_DIR =  "cavebot-fiesta/assets/nostalther/images/"
ICONS_DIR = "cavebot-fiesta/assets/nostalther/icons/"

# items to collect from corpse
items = []                                              # loot this items
coins = ["goldcoin1", "goldcoin2"]                      # gold coins from loot (1-4 and 5-100 stacks)
food = ["ham", "meat"]                                  # food to eat from dead corpse
drop_items = ["mace", "sword", "ham"]                   # items to drop on the floor
bpname = img_dir + "golden_backpack" + ".PNG"           # backpack to store gold
bags = ["bagloot"]                                      # bagloot from monster

# hunting monsters (change this for other hunts)
target_list = ["rotworm"]
dead_monster = ["dead_rotworm"]
