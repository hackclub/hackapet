# MinePet ⛏️

MinePet is a game where you control your pet (slime) and can build and break 12 different blocks and "explore" the world.

## Controls

- Basic controls (as shown on the splash screen):
  - Move left: <kbd>Button Left</kbd>
  - Move right: <kbd>Button Right</kbd>
  - Jump: <kbd>Button Middle</kbd> (hold for 10 frames)
  - Open build menu: Press <kbd>Button Left</kbd> while holding <kbd>Button Middle</kbd>
  - Open break menu: Press <kbd>Button Right</kbd> while holding <kbd>Button Middle</kbd>
- Advanced controls:
  - Activate rainbow 🏳️‍🌈 slime mode: Press <kbd>Button Left</kbd> while holding <kbd>Button Right</kbd> (or other way around)
  - Activate noclip mode: Press and hold keys for rainbow mode, while holding press <kbd>Button Middle</kbd> (you can't go down in noclip mode)
  - Force instant fall: While in air, press and hold <kbd>Button Middle</kbd> for about 20 frames
  - Select world seed: On splash screen, select <kbd>Button Left</kbd>, <kbd>Button Middle</kbd> or <kbd>Button Right</kbd> to choose seed for that button

## World generation

There are currently 4 generated features in the world:

- sand pits
- flowers
- trees
- stone starting at between 4 and 14 blocks below surface

The world size is theoretically infinite, especially as only block changes are saved (to RAM) and only the currently visible blocks are loaded.

## Possible future features

- smooth camera and player alignment (aligned to 128x128 pixel grid, not 8x8 block grid)
- more blocks
- gravity for sand
- persistent worlds (save to esp32 storage), with world select screen
- more player animations: e.g on idle, when building, when breaking, when jumping (would require smooth player alignment)
