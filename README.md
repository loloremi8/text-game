# Text Game

## Overview
This text-based game allows players to explore different rooms, interact with characters, and embark on adventures. The game is designed to be easily expandable, with a modular structure that separates different components.

## Project Structure
```
text-game
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