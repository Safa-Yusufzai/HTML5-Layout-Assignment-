from PIL import Image
from collections import deque
import os

# Folder containing your PNG images
IMAGE_FOLDER = "."

# Images whose BLACK OUTER background should be removed
FILES = [
    "channels.png",
    "features.png",
    "messages.png",
    "future.png",
    "catchub-icon.png",
    "catchub-logo.png",
    "peratude-logo.png",
    "android.png",
    "applestore.png",
]

# Black threshold
# Pixels connected to the outside edge and darker than this
# will become transparent.
BLACK_THRESHOLD = 45


def is_black(pixel):
    r, g, b, a = pixel

    return (
        r <= BLACK_THRESHOLD
        and g <= BLACK_THRESHOLD
        and b <= BLACK_THRESHOLD
    )


def remove_outer_black_background(input_path, output_path):

    image = Image.open(input_path).convert("RGBA")

    pixels = image.load()

    width, height = image.size

    visited = set()

    queue = deque()


    # ---------------------------------
    # ADD EDGE PIXELS TO QUEUE
    # ---------------------------------

    for x in range(width):

        if is_black(pixels[x, 0]):
            queue.append((x, 0))

        if is_black(pixels[x, height - 1]):
            queue.append((x, height - 1))


    for y in range(height):

        if is_black(pixels[0, y]):
            queue.append((0, y))

        if is_black(pixels[width - 1, y]):
            queue.append((width - 1, y))


    # ---------------------------------
    # FLOOD FILL BLACK OUTER BACKGROUND
    # ---------------------------------

    while queue:

        x, y = queue.popleft()

        if (x, y) in visited:
            continue

        visited.add((x, y))


        if not is_black(pixels[x, y]):
            continue


        # Make background transparent
        r, g, b, a = pixels[x, y]

        pixels[x, y] = (r, g, b, 0)


        # Check surrounding pixels
        neighbours = [

            (x + 1, y),
            (x - 1, y),
            (x, y + 1),
            (x, y - 1),

            (x + 1, y + 1),
            (x - 1, y - 1),
            (x + 1, y - 1),
            (x - 1, y + 1),

        ]


        for nx, ny in neighbours:

            if (
                0 <= nx < width
                and 0 <= ny < height
                and (nx, ny) not in visited
            ):

                if is_black(pixels[nx, ny]):

                    queue.append((nx, ny))


    # ---------------------------------
    # SAVE REAL TRANSPARENT PNG
    # ---------------------------------

    image.save(output_path, "PNG")

    print("DONE:", output_path)


# =====================================
# PROCESS ALL IMAGES
# =====================================

for filename in FILES:

    input_path = os.path.join(
        IMAGE_FOLDER,
        filename
    )


    if not os.path.exists(input_path):

        print("SKIPPED - NOT FOUND:", input_path)

        continue


    name, extension = os.path.splitext(filename)


    output_filename = name + "-transparent.png"


    output_path = os.path.join(
        IMAGE_FOLDER,
        output_filename
    )


    remove_outer_black_background(
        input_path,
        output_path
    )


print("\nALL DONE")