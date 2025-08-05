"""
Tests for picture manipulation functionality.
"""

import unittest

from PIL import Image

import picture_processor
from _logging import logger

class HalveImageTests(unittest.TestCase):
    """
    Tests if 'halve-image' works as intended for all cases.
    """

    @staticmethod
    def get_dimensions_of_half_image(filename: str):
        """
        """
        with Image.open(filename) as og_image:
            half_width = int(og_image.size[0] / 2)
            full_height = og_image.size[1]
            expected = (half_width, full_height)
        return expected

    def test_halve_image__half1(self):
        """
        Tests if a half-image is returned by function.
        """
        filename = "images/.test.png"
        get_first_half = True
        expected = self.get_dimensions_of_half_image(filename)
        half = picture_processor.halve_image(filename, get_first_half=get_first_half)
        actual = half.size
        self.assertTupleEqual(actual, expected)
        self.assertIsInstance(half, Image.Image)

    def test_halve_image__half2(self):
        """
        Tests if a half-image is returned by function.
        """
        filename = "images/.test.png"
        get_first_half = False
        expected = self.get_dimensions_of_half_image(filename)
        half = picture_processor.halve_image(filename, get_first_half=get_first_half)
        actual = half.size
        self.assertTupleEqual(actual, expected)
        self.assertIsInstance(half, Image.Image)

if __name__ == "__main__":
    unittest.main(
        defaultTest="HalveImageTests",
    )


