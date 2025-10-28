"""
"""

import unittest
from pathlib import Path

from krita_ref_parser.compile_index import (
    compile_directories,
    compile_filenames,
    get_header,
    get_hero_image,
    get_figures,
)

SOURCE_DIR = "./tests/output/raw-excerpts/"
TARGET_DIR = "./tests/output/"

for dirname in (SOURCE_DIR, TARGET_DIR):
    Path(dirname).mkdir(parents=True, exist_ok=True)

class ExcerptDirectoryTestCase(unittest.TestCase):
    """
    """

    def setUp(self):
        """
        """
        mock_dir = Path(SOURCE_DIR, "TEST-for-excerpts-directory")
        mock_dir.mkdir(exist_ok=False)
        self.mock_dir = mock_dir
        self.subdirectories = (
            "blending_modes/",
            "tools/",
            "main_menu/",
        )
        for dirname in self.subdirectories:
            self.mock_dir.joinpath(dirname).mkdir(exist_ok=False)

    def test_compile_directories(self):
        """
        """
        expected = set(self.subdirectories)
        actual = compile_directories(source_dir=self.mock_dir)
        self.assertSetEqual(actual, expected)

    def tearDown(self):
        """
        """
        for dirpath in self.mock_dir.iterdir():
            dirpath.rmdir()
        self.mock_dir.rmdir()

class ToolExcerptSubdirectoryTestCase(unittest.TestCase):
    """
    """

    def setUp(self):
        """
        """
        mock_dir = Path(SOURCE_DIR, "TEST-for-tool-excerpts-subdirectory")
        mock_dir.mkdir(exist_ok=False)
        self.mock_dir = mock_dir

    def test_compile_filenames(self):
        """
        """
        filenames = (
            "foo.txt",
            "bar.png",
            "bacon.php",
            "eggs.apartheid",
        )
        for filename in filenames:
            self.mock_dir.joinpath(filename).write_text("")
        expected = set(filenames)
        actual = compile_filenames(self.mock_dir)
        self.assertSetEqual(actual, expected)

    def tearDown(self):
        """
        """
        for filepath in self.mock_dir.iterdir():
            filepath.unlink()
        self.mock_dir.rmdir()

# SOUP INSPECTION #


class BlendingModesAdditionFileTestCase(unittest.TestCase):
    """
    """

    def setUp(self):
        """
        """
        subdirectory = "blending_modes/arithmetic/"
        filename = "addition.html"
        path_to_test_dir = Path(SOURCE_DIR, subdirectory)
        path_to_test_dir.mkdir(exist_ok=True, parents=True)
        self.path_to_test_file = path_to_test_dir.joinpath(filename)
        path_to_og_file = Path(*SOURCE_DIR.split("/")[2:] + [subdirectory, filename])
        shutil.copyfile(path_to_og_file, self.path_to_test_file)


class BlendingModesHSXFileTestCase(unittest.TestCase):
    """
    """

    def setUp(self):
        """
        """
        subdirectory = "blending_modes/hsx/"
        filename = "intensity.html"
        path_to_test_dir = Path(SOURCE_DIR, subdirectory)
        path_to_test_dir.mkdir(exist_ok=True, parents=True)
        self.path_to_test_file = path_to_test_dir.joinpath(filename)
        path_to_og_file = Path(*SOURCE_DIR.split("/")[2:] + [subdirectory, filename])
        shutil.copyfile(path_to_og_file, self.path_to_test_file)


class HeroImageFileTestCase(unittest.TestCase):
    """
    """

    def setUp(self):
        """
        """
        subdirectory = "tools/"
        filename = "gradient_draw.html"
        path_to_test_dir = Path(SOURCE_DIR, subdirectory)
        path_to_test_dir.mkdir(exist_ok=True)
        self.path_to_test_file = path_to_test_dir.joinpath(filename)
        path_to_og_file = Path(*SOURCE_DIR.split("/")[2:] + [subdirectory, filename])
        shutil.copyfile(path_to_og_file, self.path_to_test_file)

    def test_get_hero_image(self):
        """
        """

    def test_get_header(self):
        """
        """

    def test_get_figures(self):
        """
        """

class NoHeroImageFileTestCase(unittest.TestCase):
    """
    """

    def setUp(self):
        """
        """
        subdirectory = "layers_and_masks/"
        filename = "clone_layers.html"
        path_to_test_dir = Path(SOURCE_DIR, subdirectory)
        path_to_test_dir.mkdir(exist_ok=True)
        self.path_to_test_file = path_to_test_dir.joinpath(filename)
        path_to_og_file = Path(*SOURCE_DIR.split("/")[2:] + [subdirectory, filename])
        shutil.copyfile(path_to_og_file, self.path_to_test_file)

class FigureFileTestCase(BlendingModesAdditionFileTestCase):
    """
    """
    def setUp(self):
        """
        """
        logger.debug("FigureFileTestCase: Inheriting from BlendingModesAdditionFileTestCase because the cases are identical.")
        super().setUp()

class NoFigureFileTestCase(unittest.TestCase):
    """
    """

    def setUp(self):
        """
        """
        subdirectory = "layers_and_masks/"
        filename = "filters_masks.html"
        path_to_test_dir = Path(SOURCE_DIR, subdirectory)
        path_to_test_dir.mkdir(exist_ok=True, parents=True)
        self.path_to_test_file = path_to_test_dir.joinpath(filename)
        path_to_og_file = Path(*SOURCE_DIR.split("/")[2:] + [subdirectory, filename])
        shutil.copyfile(path_to_og_file, self.path_to_test_file)

