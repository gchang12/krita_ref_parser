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
        self.directories = (
            "blending_modes/",
            "tools/",
            "main_menu/",
        )
        for dirname in self.directories:
            Path(SOURCE_DIR, dirname).mkdir(exist_ok=True)

class ToolExcerptSubdirectoryTestCase(unittest.TestCase):
    """
    """

class GradientToolFileTestCase(unittest.TestCase):
    """
    """
