# cavebot-fiesta

Automated cavebot for tibia 7.4

Features include: `cavebot 100% AFK`, `auto looter`, `auto attacker`, `rune maker`, `waypoints maker`, `drop food and items on the floor` and `mining`.

This repository also includes [autofishing](https://github.com/emmacyberia/cavebot-fiesta/blob/main/utils/autofishing.py).

>[!NOTE]
>[Mining (darkrest only)](https://darkrest-online.gitbook.io/darkrest.online-wiki/gathering-and-crafting/gathering) is a lucrative gathering profession centered around extracting valuable ores from mineral deposits found scattered across the game world.

![](https://github.com/emmacyberia/cavebot-fiesta/blob/main/docs/images/cavebot-fiesta.gif)

## Usage

### Prerequisites

>[!NOTE]
>Ensure that you have [Conda](https://www.anaconda.com/download/) installed on your system.

```bash
# clone this repository
git clone https://github.com/emmacyberia/cavebot-fiesta.git

cd cavebot-fiesta

# create a conda environment and install dependencies
conda env create -f environment.yml

# activate the environment
conda activate cavebot-fiesta
```

>[!NOTE]
>Before running, ensure that the configuration file is set up properly.
>Edit the [configuration file](https://github.com/emmacyberia/cavebot-fiesta/blob/env/cavebot-fiesta/core/config.py) to match your desired settings.

### Run cavebot-fiesta

```bash
# run the cavebot
python cavebot-fiesta/main.py
```

Before running, set up the [configuration file](https://github.com/emmacyberia/cavebot-fiesta/blob/main/cavebot-fiesta/core/antiga/config.py).

>[!NOTE]
>Execute [locateOnScreen.py](https://github.com/emmacyberia/cavebot-fiesta/blob/main/utils/locateOnScreen.py) to capture coordinates. Hover your mouse over desired locations while the script runs, and save the X,Y coords in the configuration file.
>
>You also have to set the waypoints route in your MINIMAP using [screenshot.py](https://github.com/emmacyberia/cavebot-fiesta/blob/main/utils/screenshot.py).

Then, run the bot and press `PageUp` in-game to start the cavebot.

![](https://github.com/emmacyberia/cavebot-fiesta/blob/main/cavebot-fiesta/assets/darkrest/images/positions.PNG)

## Ingame hotkeys

```
Mana trainer (adori vis // adura vita) = F3
```

## Extra

[actions.py](https://github.com/emmacyberia/cavebot-fiesta/blob/main/cavebot-fiesta/core/actions.py) optimizes performance with multithreading.

The `threadKillMonster` manages the `attack_next_monster` function. This parallel approach optimizes the bot's performance, especially when searching for images or executing actions simultaneously.
