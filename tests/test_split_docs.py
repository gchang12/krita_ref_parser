"""
"""

import unittest
from unittest.mock import patch
from pathlib import Path
from tempfile import NamedTemporaryFile

import bs4

from krita_ref_parser.split_docs import (
    split_from_page,
    split_from_blendingmodes_page,
    split_from_hsx_blendingmodes_page,
    write_stripped_soup,
    )
from krita_ref_parser._logging import logger

SOURCE_DIR = "./tests/input/docs-krita-org/_build/html/reference_manual/"
TARGET_DIR = "./tests/output/raw-excerpts/"

for dirname in (SOURCE_DIR, TARGET_DIR):
    Path(dirname).mkdir(parents=True, exist_ok=True)

class AssistantToolTestCase(unittest.TestCase):
    """
    """

    def setUp(self):
        """
        """
        subdirectory = "tools/"
        filename = "assistant.html"
        path_to_test_dir = Path(SOURCE_DIR, subdirectory)
        path_to_test_dir.mkdir(exist_ok=True)
        self.path_to_test_file = path_to_test_dir.joinpath(filename)
        path_to_og_file = Path(*SOURCE_DIR.split("/")[2:] + [subdirectory, filename])
        shutil.copyfile(path_to_og_file, self.path_to_test_file)

    def test_split_from_page(self):
        """
        """
        soup = bs4.BeautifulSoup(self.path_to_test_file.read_text(encoding="utf-8"))
        sections = split_from_page(soup)
        self.assertIsInstance(sections, list)
        self.assertEqual(len(sections), 1)
        section = sections[0]
        self.assertIsNotNone(section)
        self.assertIsInstance(section, bs4.Tag)
        self.assertTrue(section)
        self.assertIsNotNone(section.find("h2"))

class ArithmeticBlendingModeTestCase(unittest.TestCase):
    """
    """

    def setUp(self):
        """
        """
        subdirectory = "blending_modes/"
        filename = "arithmetic.html"
        self.number_of_subsections = 5
        path_to_test_dir = Path(SOURCE_DIR, subdirectory)
        path_to_test_dir.mkdir(exist_ok=True)
        self.path_to_test_file = path_to_test_dir.joinpath(filename)
        path_to_og_file = Path(*SOURCE_DIR.split("/")[2:] + [subdirectory, filename])
        shutil.copyfile(path_to_og_file, self.path_to_test_file)

    def test_split_from_blendingmodes_pages(self):
        """
        """
        soup = bs4.BeautifulSoup(self.path_to_test_file.read_text(encoding="utf-8"))
        sections = split_from_blendingmodes_page(soup)
        self.assertIsInstance(sections, list)
        self.assertEqual(len(sections), self.number_of_subsections)
        for section in sections:
            self.assertIsNotNone(section)
            self.assertIsInstance(section, bs4.Tag)
            self.assertTrue(section)
            self.assertIsNotNone(section.find("h2"))

class AssistantToolTestCase(unittest.TestCase):
    """
    """

    def setUp(self):
        """
        """
        subdirectory = "blending_modes/"
        filename = "hsx.html"
        self.number_of_subsections = 11
        path_to_test_dir = Path(SOURCE_DIR, subdirectory)
        path_to_test_dir.mkdir(exist_ok=True)
        self.path_to_test_file = path_to_test_dir.joinpath(filename)
        path_to_og_file = Path(*SOURCE_DIR.split("/")[2:] + [subdirectory, filename])
        shutil.copyfile(path_to_og_file, self.path_to_test_file)

    def test_split_from_hsx_blendingmodes_pages(self):
        """
        """
        soup = bs4.BeautifulSoup(self.path_to_test_file.read_text(encoding="utf-8"))
        sections = split_from_hsx_blendingmodes_page(soup)
        self.assertIsInstance(sections, list)
        self.assertEqual(len(sections), self.number_of_subsections)
        for section in sections:
            self.assertIsNotNone(section)
            self.assertIsInstance(section, bs4.Tag)
            self.assertTrue(section)
            self.assertIsNotNone(section.find("h3"))

class CalligraphyToolTestCase(unittest.TestCase):
    """
    """

    def setUp(self):
        """
        """
        subdirectory = "tools/"
        filename = "calligraphy.html"
        path_to_test_dir = Path(SOURCE_DIR, subdirectory)
        path_to_test_dir.mkdir(exist_ok=True)
        self.path_to_test_file = path_to_test_dir.joinpath(filename)
        path_to_og_file = Path(*SOURCE_DIR.split("/")[2:] + [subdirectory, filename])
        shutil.copyfile(path_to_og_file, self.path_to_test_file)

    @patch("pathlib.Path.write_text")
    def test_write_stripped_soup(self, MOCK_write_text):
        """
        """
        soup = bs4.BeautifulSoup("""<section id="calligraphy-tool">
<span id="index-0"></span><span id="id1"></span><h1>Calligraphy Tool<a class="headerlink" href="#calligraphy-tool" title="Link to this heading">¶</a></h1>
<p><img alt="toolcalligraphy" src="../../_images/calligraphy_tool.svg" /></p>
<p>The Calligraphy tool allows for variable width lines, with input managed by the tablet.
Press down with the stylus/left mouse button on the canvas to make a line, lifting the stylus/mouse button ends the stroke.</p>
<section id="tool-options">
<h2>Tool Options<a class="headerlink" href="#tool-options" title="Link to this heading">¶</a></h2>
<p><strong>Fill</strong></p>
<p>Doesn’t actually do anything.</p>
<p><strong>Calligraphy</strong></p>
<p>The drop-down menu holds your saved presets, the <span class="guilabel">Save</span> button next to it allows you to save presets.</p>
<dl class="simple">
<dt>Follow Selected Path</dt><dd><p>If a stroke has been selected with the default tool, the calligraphy tool will follow this path.</p>
</dd>
<dt>Use Tablet Pressure</dt><dd><p>Uses tablet pressure to control the stroke width.</p>
</dd>
<dt>Thinning</dt><dd><p>This allows you to set how much thinner a line becomes when speeding up the stroke. Using a negative value makes it thicker.</p>
</dd>
<dt>Width</dt><dd><p>Base width for the stroke.</p>
</dd>
<dt>Use Tablet Angle</dt><dd><p>Allows you to use the tablet angle to control the stroke, only works for tablets supporting it.</p>
</dd>
<dt>Angle</dt><dd><p>The angle of the dab.</p>
</dd>
<dt>Fixation</dt><dd><p>The ratio of the dab. 1 is thin, 0 is round.</p>
</dd>
<dt>Caps</dt><dd><p>Whether or not an stroke will end with a rounding or flat.</p>
</dd>
<dt>Mass</dt><dd><p>How much weight the stroke has. With drag set to 0, high mass increases the ‘orbit’.</p>
</dd>
<dt>Drag</dt><dd><p>How much the stroke follows the cursor, when set to 0 the stroke will orbit around the cursor path.</p>
</dd>
</dl>
<div class="admonition note">
<p class="admonition-title">Note</p>
<p>The calligraphy tool can be edited by the edit-line tool, but currently you can’t add or remove nodes without converting it to a normal path.</p>
</div>
</section>
</section>""", 'html.parser')
        num_lines = write_stripped_soup(soup, self.path_to_test_file)
        self.assertEqual(num_lines, 39)
        MOCK_write_text.assert_called_once()

