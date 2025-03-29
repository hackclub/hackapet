# Mock the 'board' module if not using hardware
try:
    import board
except ImportError:
    print("No hardware platform detected. Using mock board.")

import displayio
import adafruit_displayio_pygamedisplay

# This line will now run without hardware-related warnings or issues
print("blinka-displayio-pygamedisplay is installed correctly!")
