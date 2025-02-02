# Arctic Blast

A CircuitPython game originally developed by me for dedicated HackaPet ysws it will have specialized hardware and the game was adapted to run on PC using pygame and blinka_displayio_pygamedisplay. Control a seal as it navigates through arctic waters, avoiding hazards while collecting fish and seaweed.

## About

Arctic Blast was originally designed to run on HackaPet's custom hardware , which features a specialized display and control system for educational gaming. This version has been adapted to run on standard PCs while maintaining the core gameplay elements and CircuitPython compatibility.

## Game Features

- Control a swimming seal in an arctic environment
- Dodge environmental hazards (oil spills and garbage)
- Collect food (fish and seaweed)
- Smooth sprite animations
- Simple controls using arrow keys

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## Installation

1. Create and activate a virtual environment:

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

2. Install required packages:

```bash
pip install pygame
pip install blinka_displayio_pygamedisplay
pip install adafruit-circuitpython-display-text
```

3. Download the game assets:
   - Required bitmap (.bmp) files:
     - articbg.bmp (background)
     - sealsheet.bmp (seal sprite sheet)
     - oil.bmp (oil hazard)
     - garbage.bmp (garbage hazard)
     - fish.bmp (fish sprite)
     - seaweed.bmp (seaweed sprite)

4. Place all .bmp files in the same directory as the game script

## Running the Game

1. Make sure your virtual environment is activated
2. Run the game script:
```bash
python game.py
```

## How to Play

- Use LEFT and RIGHT arrow keys to move the seal
- Avoid oil spills and garbage
- Collect fish and seaweed
- Game over occurs when the seal collides with hazards
- Press any key to restart after game over

## Game Configuration

You can adjust these constants at the top of the script to modify gameplay:
- MAX_OIL: Maximum number of oil hazards (default: 1)
- MAX_GARBAGE: Maximum number of garbage hazards (default: 2)
- MAX_FISH: Maximum number of fish (default: 1)
- MAX_SEAWEED: Maximum number of seaweed plants (default: 2)

## Development Notes

This game was originally designed for HackaPet hardware but has been adapted to run on PC using pygame and blinka_displayio_pygamedisplay. The display resolution is set to 128x128 pixels to match the original hardware specifications.

## Known Issues

- Objects only fall when the seal moves
- Sprite movement timing may need adjustment
- Collision detection requires minimum 3px overlap

## Future Improvements

- Add score tracking
- Implement proper game over screen
- Add sound effects
- Optimize object spawning mechanics