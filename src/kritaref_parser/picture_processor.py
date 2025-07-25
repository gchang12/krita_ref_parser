"""
Contains functionality to manipulate sample images from Krita-Docs.
"""

from PIL import Image

from _logging import logger

def halve_image(filename: str, *, get_first_half: bool):
    """
    Returns one of two halves of image specified by `filename`.
    """
    logger.debug("Now halving: %s", filename)
    with Image.open(filename) as img:
        half_width = int(img.size[0] / 2)
        full_height = img.size[1]
        full_width = img.size[0]
        # (top, left, right, bottom)
        if get_first_half:
            box = (0, 0, half_width, full_height)
        else:
            box = (half_width, 0, full_width, full_height)
        half_image = img.crop(box)
    return half_image

if __name__ == "__main__":
    filename = "images/.test.png"
    half_image = halve_image(filename, get_first_half=False)

