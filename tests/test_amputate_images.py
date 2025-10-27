"""
"""

import unittest
from unittest.mock import patch
from pathlib import Path
import shutil

from PIL import Image
from bs4 import BeautifulSoup

from krita_ref_parser.amputate_images import (
    SampleImageType,
    get_half_of_image_file,
    get_thirds_of_image_file,
    compile_images_from_soup,
    delete_unused_images,
    )

SOURCE_DIR = "./tests/input/docs-krita-org/_build/html/_images/"
TARGET_DIR = "./tests/output/images/"

class ImageWithDotsTestCase(unittest.TestCase):
    """
    """

    def setUp(self):
        """
        """
        filename = "Blending_modes_Addition_Sample_image_with_dots.png"
        self.number_of_partitions = 2
        path_to_og_file = Path(*SOURCE_DIR.split("/")[2:] + [filename])
        self.filename = "/".join([SOURCE_DIR, filename])
        shutil.copyfile(path_to_og_file, self.filename)

    def test_get_sample_image_type(self):
        """
        """
        expected = SampleImageType.WITH_DOTS
        actual = SampleImageType.get_sample_image_type("/".join([SOURCE_DIR, self.filename]))
        self.assertEqual(actual, expected)

    def test_get_filename_for_default(self):
        """
        """
        prefix = "?"
        expected = prefix + "_Sample_image_with_dots.png"
        actual = SampleImageType.WITH_DOTS.get_filename_for_default(prefix=prefix)
        self.assertEqual(actual, expected)

    def test_get_number_of_partitions(self):
        """
        """
        expected = self.number_of_partitions
        actual = SampleImageType.WITH_DOTS.get_number_of_partitions()
        self.assertEqual(actual, expected)

    def test_get_half_of_image_file1(self):
        """
        """
        filename = self.filename
        with Image.open(filename) as img:
            full_width = img.size[0]
            full_height = img.size[1]
            half_width = int(full_width / 2)
            box = (0, 0, half_width, full_height)
            expected = img.crop(box)
        actual = get_half_of_image_file(filename, get_first_half=True)
        self.assertEqual(actual, expected)
        with Image.open(filename) as img:
            self.assertEqual(img.size[0], full_width)
            self.assertEqual(img.size[1], full_height)

    def test_get_half_of_image_file2(self):
        """
        """
        filename = self.filename
        with Image.open(filename) as img:
            full_width = img.size[0]
            full_height = img.size[1]
            half_width = int(full_width / 2)
            box = (half_width, 0, full_width, full_height)
            expected = img.crop(box)
        actual = get_half_of_image_file(filename, get_first_half=False)
        self.assertEqual(actual, expected)
        with Image.open(filename) as img:
            self.assertEqual(img.size[0], full_width)
            self.assertEqual(img.size[1], full_height)

class GradientComparisonTestCase(unittest.TestCase):
    """
    """

    def setUp(self):
        """
        """
        filename = "Blending_modes_Divisive_Modulo_Gradient_Comparison.png"
        self.number_of_partitions = 3
        path_to_og_file = Path(*SOURCE_DIR.split("/")[2:] + [filename])
        self.filename = "/".join([SOURCE_DIR, filename])
        shutil.copyfile(path_to_og_file, self.filename)

    def test_get_sample_image_type(self):
        """
        """
        expected = SampleImageType.GRADIENT_COMPARISON
        actual = SampleImageType.get_sample_image_type("/".join([SOURCE_DIR, self.filename]))
        self.assertEqual(actual, expected)

    def test_get_filename_for_default(self):
        """
        """
        prefix = "!"
        expected = prefix + "_Gradient_Comparison.png"
        actual = SampleImageType.GRADIENT_COMPARISON.get_filename_for_default(prefix=prefix)
        self.assertEqual(actual, expected)

    def test_get_number_of_partitions(self):
        """
        """
        expected = self.number_of_partitions
        actual = SampleImageType.GRADIENT_COMPARISON.get_number_of_partitions()
        self.assertEqual(actual, expected)

    def test_get_thirds_of_image_file23(self):
        """
        """
        filename = self.filename
        with Image.open(filename) as img:
            full_width = img.size[0]
            full_height = img.size[1]
            two_thirds_width = int(full_width * 2 / 3)
            box = (0, 0, two_thirds_width, full_height)
            expected = img.crop(box)
        actual = get_thirds_of_image_file(filename, get_last_third=False)
        self.assertEqual(actual, expected)
        with Image.open(filename) as img:
            self.assertEqual(img.size[0], full_width)
            self.assertEqual(img.size[1], full_height)

    def test_get_thirds_of_image_file13(self):
        """
        """
        filename = self.filename
        with Image.open(filename) as img:
            full_width = img.size[0]
            full_height = img.size[1]
            two_thirds_width = int(full_width * 2 / 3)
            box = (two_thirds_width, 0, full_width, full_height)
            expected = img.crop(box)
        actual = get_thirds_of_image_file(filename, get_last_third=True)
        self.assertEqual(actual, expected)
        with Image.open(filename) as img:
            self.assertEqual(img.size[0], full_width)
            self.assertEqual(img.size[1], full_height)

class NotASampleImageTestCase(unittest.TestCase):
    """
    """

    def setUp(self):
        """
        """
        filename = "Color-adjustment-curve.png"
        path_to_og_file = Path(*SOURCE_DIR.split("/")[2:] + [filename])
        self.filename = "/".join([SOURCE_DIR, filename])
        shutil.copyfile(path_to_og_file, self.filename)

    def test_get_sample_image_type(self):
        """
        """
        actual = SampleImageType.get_sample_image_type("/".join([SOURCE_DIR, self.filename]))
        self.assertIsNone(actual)

class ImageDirectoryTestCase(unittest.TestCase):
    """
    """

    def setUp(self):
        """
        """
        filenames = (
            "Blending_modes_Addition_Sample_image_with_dots.png",
            "Blending_modes_Divisive_Modulo_Gradient_Comparison.png",
            "Color-adjustment-curve.png",
        )
        for filename in filenames:
            path_to_og_file = Path(*SOURCE_DIR.split("/")[2:] + [filename])
            self.filename = "/".join([SOURCE_DIR, filename])
            shutil.copyfile(path_to_og_file, self.filename)

    @patch("pathlib.Path.iterdir")
    @patch("pathlib.Path.unlink")
    def test_delete_unused_images(self, mock_unlink, mock_iterdir):
        """
        """
        index = ["Color-adjustment-curve.png"]
        mock_iterdir.return_value = (
            Path(SOURCE_DIR, name) for name in [
                "Blending_modes_Addition_Sample_image_with_dots.png",
                "Blending_modes_Divisive_Modulo_Gradient_Comparison.png",
                "Color-adjustment-curve.png",
            ]
        )
        expected = 2
        delete_unused_images(index, target_dir=TARGET_DIR)
        actual = mock_unlink.call_count
        self.assertEqual(actual, expected)

class ImageSoupTestCase(unittest.TestCase):
    """
    """

    def setUp(self):
        """
        """
        self.soup_as_str = """<article id='img-soup'>
<h2>Image Soup</h2>
</article>"""

    def test_compile_images_from_soup(self):
        """
        """
        soup = BeautifulSoup(self.soup_as_str, 'html.parser')
        expected = set(
            name + ".png" for name in [
                "foo",
                "bar",
                "eggs",
                "green",
                "ham",
                "bottle",
            ]
        )
        soup.article.extend([BeautifulSoup("<img src='completely/nonsensical/and/nonexistent/dir/%s' />" % name, 'html.parser') for name in expected])
        actual = compile_images_from_soup(soup)
        self.assertSetEqual(actual, expected)

