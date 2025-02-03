<img src="https://raw.githubusercontent.com/Nibbl-z/GreenGooseHackapet/refs/heads/main/promotional/banner.png" width="768" height="384" style="image-rendering: pixelated;">

### **Goose Odyssey** is a story/adventure game make for Hack Club's [Hackapet.](https://hackapet.hackclub.com/). 

You play as the Goose, who finally wakes up after a nuclear meltdown that occured many years ago. You meet Stella, the only other sane living being left in the city, and learn what has happened to the world.

This game was written in CircuitPython with DisplayIO, and uses Pygame with the `blinka_displayio_pygamedisplay` library to make the game playable on desktop.

# How to Install

`blinka_displayio_pygamedisplay` does not seem to work with a web export or a desktop executable, so you'll have to download the source code and install the necessary libraries to run it... or make a submission to the Hackapet YSWS and get the device that the game is meant to be played on whenever that happens.

1. Download the source code from releases
2. Install Python
3. Run `pip3 install blinka-displayio-pygamedisplay adafruit-circuitpython-display-text adafruit-circuitpython-display_shapes`
4. Run `main.py`

# Controls

- Left Arrow: Move Left
- Up Arrow: Interact/Continue Dialogue
- Right Arrow: Move Right

If stated otherwise, left, middle, and right buttons correspond to the left, up, and right arrow keys.
