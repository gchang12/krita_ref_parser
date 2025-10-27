"""
"""

import unittest
from unittest.mock import patch
from pathlib import Path

from PIL import Image
import bs4

from krita_ref_parser.amputate_images import (
    SampleImageType,
    get_half_of_image_file,
    get_thirds_of_image_file,
    compile_images_from_soup,
    delete_unused_images,
    )

SOURCE_DIR = "./tests/input/docs-krita-org/_build/html/_images/"
TARGET_DIR = "./tests/output/images/"
EXCERPT_DIR = "./tests/output/raw-excerpts/"

class ImageWithDotsTestCase(unittest.TestCase):
    """
    """

class GradientComparisonTestCase(unittest.TestCase):
    """
    """

class NotASampleImageTestCase(unittest.TestCase):
    """
    """

class ImageSoupTestCase(unittest.TestCase):
    """
    """

class ImageDirectoryTestCase(unittest.TestCase):
    """
    """
