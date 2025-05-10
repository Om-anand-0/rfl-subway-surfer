from PIL import Image

# Open the full screenshot
img = Image.open("full_screen.png")

# Crop the game area based on coordinates
left = 209
top = 27
right = 1168
bottom = 565

cropped = img.crop((left, top, right, bottom))
cropped.save("game_area.png")
print("Game area cropped and saved!")
