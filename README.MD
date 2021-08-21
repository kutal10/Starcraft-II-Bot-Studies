<h1 align="center">
  Starcraft II Bot Studies
</h1>

<h4 align="center">Using both scripted and reinforcement learning in Starcraft II</h4>

<p align="center">
  <a href="#Folder Contents">Folder Contents</a> •
  <a href="#how-to-use">How To Use</a> •
  <a href="#Scripted Bot">Scripted Bot</a> •
  <a href="#Reinforcement Learning Bot">Reinforcement Learning Bot</a> •
  <a href="#Credits">Credits</a> •
  <a href="#Further reading on Starcraft II">Further reading on Starcraft II</a>
</p>

<p align="center">
  <img src="https://pbs.twimg.com/media/CZGtC82UkAAej8Z.jpg" width =600/>
</p>  
  
## Game Basics

### The base mechanics of Starcraft 2

Players are required to strategically and quickly manage their Economy, Technology and Army in order to defeat their opponent. The basis of playing is, on the one hand, to harvest resources and on the other hand using said resources to purchase buildings, upgrades and units.

https://user-images.githubusercontent.com/36085864/130316865-3fa4fe39-4611-4e67-9fc9-cc25d5ca9794.mp4

#### Macro vs Micro

In this most basic understanding of the game there are two types of tasks for the player: Macro and Micro. As the name indicates, Micro refers to more local, specialized events, while Macro concerns the overall flow of the game and the economical side. It is important for every Starcraft player to have a balance of these two.

_**Micro (or micromanagement in full)**_ encompasses managing your army. Moving, attacking, retreating with the ultimate goal of overpowering your opponent. Micro is the ability to control your units individually, in order to make up for pathing or otherwise imperfect AI. For example, splitting Marines in order to suffer fewer loss from a Baneling attack, or being able to perform multiple kills with Mutalisks is considered "Micro". The general theory of micro is to keep as many units alive as possible. For example it is better to have four half-dead Stalkers after a battle, rather than to have two Stalkers at full health and two dead ones.

_**Macro**_ encompasses managing your economy and technology: making sure you have an income (by harvesting resources) and spending said income (by purchasing buildings, upgrades and units). Macro is your ability to produce units, and keep all of your production buildings busy. Generally, the player with the better macro will have the larger army. The other element of macro is your ability to expand at the appropriate times to keep your production of units flowing. A good macro player is able to keep increasing his or her production capability while having the resources to support it.

#### Game operation

All these operations take place in real-time - commands are executed as they are given. This means a player not only benefits from strategical insight, but also from speed and multitask ability, measured by APM (actions per minute). The ability to perform specific actions in limited time is often referred to as Mechanics.

A player has to pick one of three races to play with, Terran, Protoss or Zerg, or choose Random. Each race has different Buildings and Units and consequently different ways of playing with then.

> The above extract was taken from [Liquipedia](https://liquipedia.net/starcraft2/StarCraft), which contains further details about topics such as Hotkeys, Mining, Units and more

## Scripted Bot

### How the Scripted bot is structured

In this bot, the main async function `on_step` runs on a central event loop, that runs several action functions for the bot to run at once. The different functions run synchronously until they hit an await and then they pause, give up control to the event loop, and then let something else happen. 

<p align="center">
  <img src="https://i.imgur.com/nih7oph.jpg" width =600/>
</p>  

In this case, as soon as the game environment tracking variables reach a certain threshold or meet a certain criteria, the appropriate action function is added to the central event loop. For example, via the `expand` asynchronous function, expansion to 3 bases is a priority, if it's affordable. 

```python
async def expand(self):
        if self.townhalls.amount < 3 and self.can_afford(UnitTypeId.NEXUS):
            await self.expand_now()
```

### Capabilities

The Protoss bot is capable of beating `elite` difficulty Zerg and Terran bots

https://user-images.githubusercontent.com/36085864/130297863-edfe234e-2e36-4c8c-a634-94b7fdc99a7e.mp4

https://user-images.githubusercontent.com/36085864/130295837-a46bc6f6-e5ed-4662-850b-77035cbd4c28.mp4

## Reinforcement Learning Bot

### Why Starcraft 2 for Reinforcement Learning

The need to balance short and long-term goals and adapt to unexpected situations, poses a huge challenge for systems that have often tended to be brittle and inflexible. Mastering this problem requires breakthroughs in several AI research challenges including:

- **Game theory**: StarCraft is a game where, just like rock-paper-scissors, there is no single best strategy. As such, an AI training process needs to continually explore and expand the frontiers of strategic knowledge.
- **Imperfect information**: Unlike games like chess or Go where players see everything, crucial information is hidden from a StarCraft player and must be actively discovered by “scouting”.
- **Long term planning**: Like many real-world problems cause-and-effect is not instantaneous. Games can also take anywhere up to one hour to complete, meaning actions taken early in the game may not pay off for a long time.
- **Real time**: Unlike traditional board games where players alternate turns between subsequent moves, StarCraft players must perform actions continually as the game clock progresses.
- **Large action space**: Hundreds of different units and buildings must be controlled at once, in real-time, resulting in a combinatorial space of possibilities. On top of this, actions are hierarchical and can be modified and augmented. Our parameterization of the game has an average of approximately 10 to the 26 legal actions at every time-step.

> The above extract was taken from [Deepmind's Blog Post](https://deepmind.com/blog/article/alphastar-mastering-real-time-strategy-game-starcraft-ii), which contains further details on their Alphastar bot

### How the RL bot is structured

Reinforcement Learning is ultimately built off a Markov Decision process. There is an assumption that the environment is full observable, meaning that there is sufficient information to make a decision in the current state. In this environment, the core Markov Property holds true: _that the future is independent of the past, given the present_. 

The `gym` environment is utilised in this case to provide a standard interface for the Reinforcement Learning process that can function accross other games beyond Starcraft II.

<p align="center">
  <img src="https://i.imgur.com/CS1U2so.jpg" width =600/>
</p>  

As the model is trained, it sends actions to the environment, and receives an observation. The `reset` function is self-explanatory, it resets the state when each `episode` as such is complete. The environment is rebuilt using the `render` function to render the environment after each state step. 

### Capabilities

In a simplified Learning mini-game, [Defeat Zerglings and Banelings](https://github.com/deepmind/pysc2/blob/master/docs/mini_games.md#description-2), results over 50-60 iterations shows some interesting results:

https://user-images.githubusercontent.com/36085864/130316026-12024023-1d8d-450e-8085-4333ef222dd4.mp4

- The Terran units are spread out, with some units being pushed closer to the Zerg
  - The benefits of this, is that 2/4 of the Banelings can be eliminated immediately
  - If the Terran units were all arranged in a line and just moved forward, there is a risk a single Baneling could kill more than 3 units

- The Terran arrangement in a rough randomised arc has two benefits:
  - It allows multiple units to fire on the Zerg at once
  - It increases the movement time for the Zerg units, this is crucial because Terran units can ranged fire while the Zerg units are Melee only

While the obvious human strategy is a focus fired rush by engaging all 9 Terran on the Banelings, this is a unique perspective to see what worked for the algorithm

## How To Use

### Items required

To clone the repository and run both the bots, you'll need 3 key items:
1. [Git](https://git-scm.com) 
2. [Python 3.6+](https://www.python.org/downloads/) (which comes with [Pip](https://pip.pypa.io/en/stable/installation/) which is required to install modules) 
3. [Starcraft 2 Game](https://starcraft2.com/en-gb/) - this requires [Battle.Net](https://www.blizzard.com/en-gb/apps/battle.net/desktop) to be installed 

### Maps

PySC2 has many maps pre-configured, but they need to be downloaded into the SC2 `Maps` directory before they can be played.

Download the [ladder maps](https://github.com/Blizzard/s2client-proto#downloads) and the [mini games](https://github.com/deepmind/pysc2/releases/download/v1.2/mini_games.zip)
and extract them to your `StarcraftII/Maps/` directory.

### Setting up scripted bot

From your command line, set up the environment:

```bash
# Clone this repository
$ git clone https://github.com/kutal10/Starcraft-II-Bot-Studies

# Go into the scripted bot repository
$ cd "scripted bot"

# Set up a virtual environment (you can use Conda or others instead of Venv)
$ python3 -m venv
$ .\env\scripts\activate

# Install the latest version of Python-SC2
$ pip install --upgrade burnysc2
```
  
Change paths.py to point to your Starcraft 2 install location, under the `Windows` field: 

```python
BASEDIR = {
    "Windows": "yourpath/StarCraft II",
    "WSL1": "/mnt/c/Program Files (x86)/StarCraft II",
    "WSL2": "/mnt/c/Program Files (x86)/StarCraft II",
    "Darwin": "/Applications/StarCraft II",
    "Linux": "~/StarCraftII",
    "WineLinux": "~/.wine/drive_c/Program Files (x86)/StarCraft II",
}
```
  
Run the script of your choice and the game should launch in a popup window

```bash
# Run the Protoss bot script
$ python3 yourpath/sc2protoss.py

# Run the Human test script to take control against a docile enemy, and understand the game mechanics
$ python3 yourpath/sc2humantest.py

```
  
### Setting up reinforcement learning bot

From your command line, set up the environment:

```bash
# Clone this repository
$ git clone https://github.com/kutal10/Starcraft-II-Bot-Studies

# Go into the RL bot repository
$ cd "RL Bot"

# Set up a virtual environment (you can use Conda or others instead of Venv)
$ python3 -m venv
$ .\env\scripts\activate

# Install the latest version of OpenAI Gym
$ pip install gym

# Install Abseil
$ pip install absl-py

# Install PyTorch >= 1.8.1
$ pip install torch

# Install Stable Baselines 3
$ pip install stable-baselines3[extra]
```
  
To train a model, simply run the basescript, which should begin running the game, and output training data in the terminal

```bash
$ python3 yourpath/basescript.py
```

To view a trained model's output, firstly modify the gym environment in `defeat_zerglings_banelings_env.py` to be realtime:

```python
class DZBEnv(gym.Env):
    metadata = {'render.modes': ['human']}
    default_settings = {
        'map_name': "DefeatZerglingsAndBanelings",
        'players': [sc2_env.Agent(sc2_env.Race.terran),
                    sc2_env.Bot(sc2_env.Race.zerg, sc2_env.Difficulty.hard)],
        'agent_interface_format': features.AgentInterfaceFormat(
                    action_space=actions.ActionSpace.RAW,
                    use_raw_units=True,
                    raw_resolution=64),
        'realtime': True
    }
```
Then simply run the test policy script, which will run until the game popup is closed:
```bash
$ python3 yourpath/testpolicy.py
```
  
## Credits

The files in this study cover the following open source packages:

- [Python SC2](https://github.com/BurnySc2/python-sc2)
- [Pysc2](https://github.com/deepmind/pysc2)
- [OpenAI gym](https://gym.openai.com/)
- [Stable Baselines 3](https://github.com/DLR-RM/stable-baselines3)

## Further reading 
[Starcraft II Wiki](https://starcraft.fandom.com/wiki/StarCraft_II) - The Wiki on SC2 game fundamentals (e.g. build order, technology trees, maps etc.)  
[Alphastar](https://deepmind.com/blog/article/AlphaStar-Grandmaster-level-in-StarCraft-II-using-multi-agent-reinforcement-learning) - How Google Deepmind built Alphastar   
[Alphastar Paper](https://arxiv.org/abs/1708.04782) - The white paper that details the fundamentals of Alphastar  
[Lowko](https://www.youtube.com/channel/UCZNTsLA6t6bRoj-5QRmqt_w) - Commentary on pro level SC2 games  
[OpenAI Gym fundamentals](https://gym.openai.com/docs/) - Documentation on how openAI can be set up  
[Stable Baselines 3](https://stable-baselines3.readthedocs.io/en/master/) - Documentation on the fundamentals of Stable Baselines 3  
[Starcraft 2 updates](https://news.blizzard.com/en-gb/starcraft2) - Updates and patches to Starcraft 2  
