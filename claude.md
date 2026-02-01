# Forever War

A simplified Clash Royale-like 2D game built with Python and Pygame.

## Quick Start

```bash
make install   # Set up virtual environment and install dependencies
make run       # Run the game
make stop      # Stop any running game instance
```

## Project Structure

```
forever_war/
├── main.py              # Entry point
├── requirements.txt     # Dependencies (pygame>=2.5.0)
├── requirements.lock    # Locked dependency versions
├── Makefile             # Build/run commands
├── .python-version      # Python 3.13.11 (pyenv)
└── src/
    ├── __init__.py
    ├── constants.py     # Colors, dimensions, unit stats, settings
    ├── game.py          # Main Game class and game loop
    ├── unit.py          # Unit and UnitType classes
    ├── player.py        # Player class (mana, spawning)
    ├── ai.py            # AI opponent logic
    ├── card.py          # Card and Deck UI classes
    ├── battlefield.py   # Lane management and rendering
    └── ui.py            # Mana bar, header, footer, game over screen
```

## Game Overview

- **Orientation**: Vertical (600x900)
- **Battlefield**: 3 vertical lanes
- **Objective**: First to get a unit to the enemy base wins
- **Player base**: Bottom of screen
- **Enemy base**: Top of screen

## Controls

- Click a card at the bottom to select it
- Click a lane on the battlefield to deploy the unit
- ESC to quit
- SPACE to restart after game over

## Unit Types

| Unit | HP | Damage | Speed | Range | Cost | Shape | Color |
|------|-----|--------|-------|-------|------|-------|-------|
| Soldier | 100 | 15 | 80 | 40 | 2 | Rect | Blue |
| Tank | 250 | 10 | 40 | 35 | 4 | Rect | Gray |
| Archer | 60 | 20 | 60 | 150 | 3 | Circle | Green |
| Knight | 150 | 25 | 70 | 45 | 5 | Rect | Yellow |
| Assassin | 80 | 40 | 120 | 30 | 4 | Circle | Purple |
| Giant | 400 | 35 | 30 | 50 | 7 | Rect | Orange |

## Mana System

- Max mana: 10
- Starting mana: 5
- Regeneration: 1 mana/second

## AI Strategy

- **Decision interval**: 1.5 seconds
- **Defend**: If lane threat > 70%, spawn tank/soldier/knight
- **Reinforce**: If winning a lane, 60% chance to push with offensive units
- **Attack**: If mana >= 5, spawn random unit in random lane

## Key Technical Details

- Frame-independent movement: `y += direction * speed * dt`
- Direction: -1 (player, moving up), +1 (enemy, moving down)
- Combat: Units auto-attack nearest enemy in range
- Win condition: Unit y-position reaches enemy base

## Environment

- Python 3.13.11 (via pyenv)
- Virtual environment: `.venv/` (via uv)
- pygame 2.6.1
