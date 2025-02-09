# Smokey

Smokey the bear is getting ready for hibernation and needs your help to stock up for the winter!

- Collect food to make sure Smokey doesn't become hungry
- Prioritize food with higher values to maximize your 25 second time limit per game
- Don't touch the bombs- they lower your points

### Running the game on desktop

1. Make sure you have Python, developed originally with Python 3.13.1
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Configure `hw_accel=False`, it's disabled by default
6. Run the game: `python app.py`

### Controls
- **Left:** move Smokey left
- **Middle/Up:** start or restart the game
- **Right::** move Smokey right

### Points for different foods

- **Bomb:** -4
- **Fish:** +2
- **Acorn:**: +4
- **Blueberry:**: +6
