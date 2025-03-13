help:
	echo "make images - turn .pngs into .bmps"

images: spaceship.bmp

%.bmp: %.png
	magick $< +dither -colors 2 -type palette BMP3:$@