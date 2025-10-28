"""
Models sample-image types, partitions images, and deletes images.
"""

import enum
import shutil
from pathlib import Path

from PIL import Image
from bs4 import BeautifulSoup

from krita_ref_parser._logging import logger

SOURCE_DIR = "./input/docs-krita-org/_build/html/_images/"
TARGET_DIR = "./output/images/"
EXCERPT_DIR = "./output/raw-excerpts/"

class SampleImageType(enum.Enum):
    """
    """
    # BLENDING_MODES
    WITH_DOTS = "_Sample_image_with_dots.png"
    # VARIOUS
    GREY_04_05 = "_Gray_0.4_and_Gray_0.5.png"
    GREY_04_05_N = "_Gray_0.4_and_Gray_0.5_n.png"
    LIGHT_BLUE_AND_ORANGE = "_Light_blue_and_Orange.png"
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
        except IndexError:
            logger.debug("'%s' does not fall into one of the declared SampleImageType enumerations.", filename)
            return None

    def get_filename_for_default(self, *, prefix):
        """
        """
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
            self.GREY_04_05_N: 2,
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
    # box – The crop rectangle, as a (left, upper, right, lower)-tuple.
    with Image.open(filename) as img:
        full_width = img.size[0]
        full_height = img.size[1]
        half_width = int(full_width / 2)
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
        full_width = img.size[0]
        full_height = img.size[1]
        two_thirds_width = int(full_width * 2 / 3)
        if get_last_third:
            logger.debug("Getting last third.")
            box = (two_thirds_width, 0, full_width, full_height)
        else:
            logger.debug("Getting first two-thirds.")
            box = (0, 0, two_thirds_width, full_height)
        cropped_image = img.crop(box)
    return cropped_image

def compile_images_from_soup(soup: BeautifulSoup):
    """
    """
    images = set()
    for img in soup.find_all("img"):
        images.add(Path(img['src']).name)
    return images

def delete_unused_images(index, *, target_dir):
    """
    """
    logger.debug("Found (%d) filenames in index.", len(index))
    image_files = tuple(filter(lambda file: file.is_file(), Path(target_dir).iterdir()))
    num_image_files = len(image_files)
    logger.debug("Found (%d) image files in '%s'.", num_image_files, target_dir)
    unused_images = map(
        lambda file: file.name,
        tuple(
            filter(
                lambda file: file.name not in index,
                image_files,
            )
        )
    )
    num_unused_images = 0
    for image_name in unused_images:
        imagefile = Path(target_dir, image_name)
        imagefile.unlink()
        num_unused_images += 1
    logger.debug("Deleted %d unused image files in '%s'. Number of images remaining: %d.", num_unused_images, target_dir, num_image_files - num_unused_images)

if __name__ == "__main__":
    GENERIC_IMAGE_PREFIX = "."

    # Copy images directory from source to target.
    def copy_all_images():
        """
        """
        shutil.rmtree(TARGET_DIR, ignore_errors=True)
        shutil.copytree(SOURCE_DIR, TARGET_DIR)
        logger.info("'%s' has been copied to '%s'", SOURCE_DIR, TARGET_DIR)

    # Compile list of used images and delete them.
    def compile_and_delete_used_images():
        """
        """
        images = set()
        for (dirpath, dirs, filenames) in Path(EXCERPT_DIR).walk():
            logger.info("Looking for image references in '%s'.", dirpath)
            for filename in filenames:
                filepath = dirpath.joinpath(filename)
                soup = BeautifulSoup(filepath.read_text(), 'html.parser')
                images.update(compile_images_from_soup(soup))
        logger.info("Compiled (%d) images being referenced in HTML.", len(images))
        delete_unused_images(images, target_dir=TARGET_DIR)

    # Generate generic blending-mode images
    def generate_default_blendingmodes_images():
        """
        """
        for sample_image_type in SampleImageType:
            number_of_partitions = sample_image_type.get_number_of_partitions()
            logger.debug("%s should be divided into (%d) parts.", sample_image_type, number_of_partitions)
            partitioning_func, kwds = {
                2: (get_half_of_image_file, {"get_first_half": True}),
                3: (get_thirds_of_image_file, {"get_last_third": False}),
            }[number_of_partitions]
            sample_img_filename = list(filter(lambda path: path.name.endswith(sample_image_type.value), Path(TARGET_DIR).iterdir())).pop()
            logger.debug("Extracting generic part from sample file: '%s'.", sample_img_filename)
            cropped_image = partitioning_func(sample_img_filename, **kwds)
            target_filename = sample_image_type.get_filename_for_default(prefix=GENERIC_IMAGE_PREFIX)
            #cropped_image.filename = "/".join([TARGET_DIR, target_filename])
            target_path = Path(TARGET_DIR, target_filename)
            cropped_image.save(target_path)
            logger.info("Generic %s image has been saved to: '%s'", sample_image_type, target_path)

    # Partition the existing images in-place.
    def partition_blendingmodes_images_inplace():
        """
        """
        partition_log = {}
        for imgtype in SampleImageType:
            partition_log[imgtype] = 0
        for imagefile in filter(
            lambda path: SampleImageType.get_sample_image_type(path.name) is not None and not path.name.startswith(GENERIC_IMAGE_PREFIX),
            Path(TARGET_DIR).iterdir(),
        ):
            sample_image_type = SampleImageType.get_sample_image_type(imagefile.name)
            number_of_partitions = sample_image_type.get_number_of_partitions()
            partitioning_func, kwds = {
                2: (get_half_of_image_file, {"get_first_half": False}),
                3: (get_thirds_of_image_file, {"get_last_third": True}),
            }[number_of_partitions]
            cropped_image = partitioning_func(imagefile, **kwds)
            cropped_image.save(imagefile)
            partition_log[sample_image_type] += 1
        logger.info("Partition complete. Report: %s", partition_log)

    def amputate_images():
        """
        """
        copy_all_images()
        compile_and_delete_used_images()
        generate_default_blendingmodes_images()
        partition_blendingmodes_images_inplace()

    amputate_images()

