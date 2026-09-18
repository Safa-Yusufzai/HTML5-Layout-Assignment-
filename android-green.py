from PIL import Image

input_file = "android.png"
output_file = "android-green.png"

img = Image.open(input_file).convert("RGBA")
pixels = img.load()

width, height = img.size

for y in range(height):
    for x in range(width):
        r, g, b, a = pixels[x, y]

        if a == 0:
            continue

        # Light/grey button area -> green
        if r > 110 and g > 110 and b > 110:
            pixels[x, y] = (164, 198, 57, a)

img.save(output_file, "PNG")

print("DONE: android-green.png")