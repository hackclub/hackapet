# Colour Bounce

Colour Bounce is a game where you have to get to the button by travelling through colours. 

## How to play

On keyboard the three buttons used are Z, X and C. You can start the game with X. 

Inside the game, you use Z and C to move the colour grid around.  After 8 moves, your position will randomly change.

You can use X to move randomly to the same colour adjacent to you. If there are no colours adjacent to you, you will stay in the same place. If there are multiple colours adjacent to you, you will move to a random one.

To win the game, you need to get to the button. You can use X to go to the button if you're next to it, even if it's on a different colour.

Once you finish the game, you can restart by pressing X again.

## How to run the game

### UV

```bash
uv sync
uv run colourbounce
```

### Pip

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -e .
python3 -m colourbounce
```