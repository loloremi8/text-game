# Text Game

## Overview
This text-based game allows players to explore different rooms, interact with characters, and embark on adventures. The game is designed to be easily expandable, with a modular structure that separates different components.

## Project Structure
```
text-game
├── game executables
│    ├── text-game_Linux         # Standalone executable for Linux
│    └── text-game_Windows.exe   # Standalone executable for Windows
├── src
│    ├── main.py                 # Entry point for the game
│    ├── core
│    │    ├── character.py       # Player class, stats, and item usage
│    │    ├── game.py            # Main game loop and screen rendering
│    │    └── inventory.py       # Inventory, equipment, and item management
│    ├── combat
│    │    ├── combat.py          # Turn-based combat system
│    │    ├── magic.py           # Spell definitions
│    │    └── monsters.py        # Monster classes and loot tables
│    ├── items
│    │    └── loot.py            # Room-specific loot generation
│    ├── rooms
│    │    ├── room.py            # Room class and dungeon layout
│    │    ├── armory.py          # Armory room event
│    │    ├── dining_hall.py     # Dining hall room event
│    │    ├── fountain.py        # Fountain room event
│    │    ├── garden.py          # Garden room event
│    │    ├── kitchen.py         # Kitchen room event
│    │    ├── library.py         # Library room event
│    │    ├── throne_room.py     # Throne room boss encounter
│    │    └── treasure_room.py   # Treasure room event
│    └── utils
│         └── helpers.py         # Utility functions
└── README.md                    # Project documentation
```

## Running the Executables

Pre-built executables are available in the `game executables/` folder — no Python installation required.

**Windows:** `text-game_Windows.exe` can be run directly by double-clicking it.

**Linux:** `text-game_Linux` needs to be made executable first, then run from a terminal:
```
chmod +x "game executables/text-game_Linux"
./"game executables/text-game_Linux"
```

## Setup Instructions
1. Clone the repository:
   ```
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```
   cd text-game
   ```

## Gameplay
- Start the game by running `src/main.py`.
- Follow the prompts to choose actions, explore rooms, and interact with characters.
- Use the provided commands to navigate and make choices.