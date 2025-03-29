
from PIL import Image

# Open the original PNG file
input_path = "character.png"
output_path_4bit = "character_smalll.bmp"

# Open and process the image
image = Image.open(input_path)
image = image.resize((32, 32))  # Ensure it's 128x128
image = image.convert("P", palette=Image.ADAPTIVE, colors=16)  # Convert to 4-bit palette

# Save as BMP
image.save(output_path_4bit, format="BMP")
