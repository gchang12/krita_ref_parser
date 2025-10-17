"""
"""

import enum

from PIL import Image

SOURCE_DIR = "../../input/docs-krita-org/_build/html/_images/"
TARGET_DIR = "../../output/images/"

class SampleImage(enum.StrEnum):
    """
    """
    WITH_DOTS = "_Sample_image_with_dots.png"
    GREY_04_05 = "_Gray_0.4_and_Gray_0.5_n.png"
    LIGHT_BLUE_AND_ORANGE = "_Light_blue_and_orange.png"
    GRADIENT_COMPARISON = "_Gradient_Comparison.png"
    MAP = "_map.png"
    GRADIENTS = "_Gradients.png"

# TODO: Figure out the rest of the constants.

def get_half_of_image_file(filename: str, *, get_first_half: bool):
    """
    Returns one of two halves of image specified by `filename`.
    """
    #logger.debug("Now halving: %s", filename)
    with Image.open(filename) as img:
        half_width = int(img.size[0] / 2)
        full_height = img.size[1]
        full_width = img.size[0]
        # (top, left, right, bottom)
        if get_first_half:
            box = (0, 0, half_width, full_height)
        else:
            box = (half_width, 0, full_width, full_height)
        cropped_image = img.crop(box)
    return cropped_image

def get_thirds_of_image_file(filename: str, *, get_last_third: bool):
    """
    """
    with Image.open(filename) as img:
        full_height = img.size[1]
        full_width = img.size[0]
        two_thirds_width = int(full_width * 2 / 3)
        if get_last_third:
            box = (two_thirds_width, 0, full_width, full_height)
        else:
            box = (0, 0, two_thirds_width, full_height)
        cropped_image = img.crop(box)
    return cropped_image

def delete_unused_images(index):
    """
    """
    image_files = filter(lambda file: file.is_file(), Path(TARGET_DIR).iterdir())
    unused_images = filter(lambda file: file.name not in index, image_files)
    for imagefile in unused_images:
        imagefile.unlink()

if __name__ == "__main__":
    def halve_blendingmode_dots_images():
        """
        """
        for imagefile in filter(lambda imagefile: not str(imagefile).endswith("_with_dots.png"), Path(TARGET_DIR).iterdir()):
            blended_image = get_half_of_image_file(imagefile, get_first_half=False)
            blended_image.save(imagefile)
        og_image = get_half_of_image_file(imagefile, get_first_half=True)
        og_image.save(Path(TARGET_DIR, OG_DOTS_IMAGE))
