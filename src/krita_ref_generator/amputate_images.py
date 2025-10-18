"""
Models sample-image types, partitions images, and deletes images.
"""

import enum

from PIL import Image

from krita_ref_generator._logging import logger

SOURCE_DIR = "./input/docs-krita-org/_build/html/_images/"
TARGET_DIR = "./output/images/"
EXCERPT_DIR = "./output/raw-excerpts/"

class SampleImageType(enum.Enum):
    """
    """
    # VARIOUS
    WITH_DOTS = "_Sample_image_with_dots.png"
    GREY_04_05 = "_Gray_0.4_and_Gray_0.5_n.png"
    LIGHT_BLUE_AND_ORANGE = "_Light_blue_and_orange.png"
    # MODULO
    GRADIENT_COMPARISON = "_Gradient_Comparison.png"
    # BINARY
    MAP = "_map.png"
    GRADIENTS = "_Gradients.png"

    @classmethod
    def get_sample_image_type(cls, filename: str):
        """
        """
        logger.debug("Checking if '%s' is one of the declared SampleImageType enumerations.", filename)
        try:
            matched_sample_image_type = list(filter(lambda image_type: filename.endswith(image_type.value), cls)).pop()
            logger.debug("'%s' matched the %s SampleImageType enumeration; returning latter.", filename, matched_sample_image_type)
            return matched_sample_image_type
        except IndexError as idx_err:
            logger.warning("'%s' does not fall into one of the declared SampleImageType enumerations.", filename)
            raise idx_err

    def get_filename_for_default(self):
        """
        """
        prefix = "."
        filename_for_default_image = prefix + self.value
        logger.debug("Returning: '%s'", filename_for_default_image)
        return filename_for_default_image

    def get_number_of_partitions(self):
        """
        """
        return {
            # (various)
            self.WITH_DOTS: 2,
            self.GREY_04_05: 2,
            self.LIGHT_BLUE_AND_ORANGE: 2,
            # MODULO
            self.GRADIENT_COMPARISON: 3,
            # BINARY
            self.MAP: 3,
            self.GRADIENTS: 3,
        }[self]

def get_half_of_image_file(filename: str, *, get_first_half: bool):
    """
    Returns one of two halves of image specified by `filename`.
    """
    #logger.debug("Now halving: %s", filename)
    logger.debug("Halving: '%s'.", filename)
    with Image.open(filename) as img:
        half_width = int(img.size[0] / 2)
        full_height = img.size[1]
        full_width = img.size[0]
        # (top, left, right, bottom)
        if get_first_half:
            logger.debug("Getting first half.")
            box = (0, 0, half_width, full_height)
        else:
            logger.debug("Getting second half.")
            box = (half_width, 0, full_width, full_height)
        cropped_image = img.crop(box)
    return cropped_image

def get_thirds_of_image_file(filename: str, *, get_last_third: bool):
    """
    """
    logger.debug("Cutting '%s' into thirds.", filename)
    with Image.open(filename) as img:
        full_height = img.size[1]
        full_width = img.size[0]
        two_thirds_width = int(full_width * 2 / 3)
        if get_last_third:
            logger.debug("Getting last third.")
            box = (two_thirds_width, 0, full_width, full_height)
        else:
            logger.debug("Getting first two-thirds.")
            box = (0, 0, two_thirds_width, full_height)
        cropped_image = img.crop(box)
    return cropped_image

def copy_all_images():
    """
    """
    shutil.copytree(SOURCE_DIR, TARGET_DIR)

def compile_used_images():
    """
    """
    raise NotImplementedError
    with open(index_name, encoding="utf-8") as rfile:
        index = json.load(rfile)
    used_images = set(Path(record['icon']).name for record in index if record['icon'] is not None)
    for excerpt_dir in Path(excerptdir_root).iterdir():
        for excerpt_file in excerpt_dir.iterdir():
            with open(excerpt_file, encoding="utf-8") as rfile:
                soup = BeautifulSoup(rfile, "html.parser")
            for img in soup.find_all('img'):
                img_src = Path(img['src']).name
                used_images.add(img_src)

def delete_unused_images(index):
    """
    """
    logger.debug("Found (%d) filenames in index.", len(index))
    image_files = tuple(filter(lambda file: file.is_file(), Path(TARGET_DIR).iterdir()))
    num_image_files = len(image_files)
    logger.debug("Found (%d) image files in '%s'.", num_image_files, TARGET_DIR)
    unused_images = tuple(filter(lambda file: file.name not in index, image_files))
    num_unused_images = len(unused_images)
    logger.debug("Found (%d) unused image files in '%s'.", num_unused_images, TARGET_DIR)
    for imagefile in unused_images:
        imagefile.unlink()
    logger.debug("Deleted images. Number of images remaining: %d", num_image_files - num_unused_images)

if __name__ == "__main__":
    def halve_blendingmode_dots_images():
        """
        """
        for imagefile in filter(lambda imagefile: not str(imagefile).endswith("_with_dots.png"), Path(TARGET_DIR).iterdir()):
            blended_image = get_half_of_image_file(imagefile, get_first_half=False)
            blended_image.save(imagefile)
        og_image = get_half_of_image_file(imagefile, get_first_half=True)
        og_image.save(Path(TARGET_DIR, OG_DOTS_IMAGE))

