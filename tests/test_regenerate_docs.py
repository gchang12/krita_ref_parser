"""
"""

import io
import unittest
from unittest.mock import patch
from pathlib import Path

from bs4 import BeautifulSoup

from krita_ref_parser.regenerate_docs import (
    # for inserting and removing content
    prepend_link_tags_to_soup,
    extract_h_tag,
    extract_icon,
    remove_empty_tags,
    # for updating paths and references
    a_href_exists,
    update_img_src,
    replace_links_with_official_docs_links,
    update_references_to_blending_modes_sections,
    replace_internal_reference_with_official,
    # for changing behavior of links themselves
    replace_a_tags_with_reactlink_tags,
    have_a_tag_open_new_tab,
    # for renovating index files
    extract_subsections,
    remove_links_from_index,
    #replace_blending_modes_index_file,
    # for renaming files
    update_filename,
    update_references_to_filename,
    update_filename_record_of_index,
    )

SOURCE_DIR = "./tests/input/docs-krita-org/_build/html/reference_manual/"
TARGET_DIR = "./tests/output/excerpts/"

for dirname in (SOURCE_DIR, TARGET_DIR):
    Path(dirname).mkdir(parents=True, exist_ok=True)

# AUXILIARY-FUNCTIONS

def get_soup(raw_html_or_html_filepath: str | Path):
    """
    """
    if isinstance(raw_html_or_html_filepath, str):
        soup = BeautifulSoup(raw_html_or_html_filepath, "html.parser")
    elif isinstance(raw_html_or_html_filepath, Path):
        soup = BeautifulSoup(raw_html_or_html_filepath.read_text(encoding="utf-8"), "html.parser")
    else:
        raise TypeError('Must pass either raw-HTML or path to HTML file as argument. Type of argument passed: %r' % type(raw_html_or_html_filepath))
    return soup

# TEST-CASES

# - with icon: tools/assistant.html
class ContainsIconTestCase(unittest.TestCase):
    """
    """

# - without icon: dockers/add_shape.html
class DoesNotContainsIconTestCase(unittest.TestCase):
    """
    """
    # Some file-text should:
    # - lack icons

# - blending_modes: arithmetic.html
class BlendingModeIndexTestCase(unittest.TestCase):
    """
    """
    # Some file-text should:
    # - have certain subsections removed

# - blending_modes: arithmetic/addition.html
class BlendingModeArticleTestCase(unittest.TestCase):
    """
    """

# - blending_modes: hsx.html
# - is_blending_modes_hsx: blending_modes/hsx.html
class BlendingModeHSXIndexTestCase(unittest.TestCase):
    """
    """
    # Some file-text should:
    # - have certain subsections removed

# - blending_modes/hsx: blending_modes/hsx/intensity.html
class BlendingModeHSXArticleTestCase(unittest.TestCase):
    """
    """

# - has_external_link: fill_layer_generators/seexpr.html
class ContainsExternalLinkTestCase(unittest.TestCase):
    """
    """
    # All file-text should:
    # - have external links that are opened in new tabs

# - has_link_to_krita_non-refman_article: main_menu/settings_menu.html
class ContainsOfficialDocsLinkTestCase(unittest.TestCase):
    """
    """
    # Some file-text should:
    # - have links that point to different parts of this website.
    # - have links that point to parts of the krita-docs that aren't in reference_manual/*

# - has_link_to_krita_refman_article: dockers/animation_curves.html
class ContainsInternalLinkTestCase(unittest.TestCase):
    """
    """

# - is_index_file: fill_layers.html
class IndexTestCase(unittest.TestCase):
    """
    """

# - exception1: layers_and_masks/fill_layers.html
class MovedFileTestCase(unittest.TestCase):
    """
    """
    # All file-text should:
    # - have all references to moved files corrected

    def setUp(self):
        """
        """
        self.dirname = "layers_and_masks"
        self.filename = "fill_layers.html"
        self.mock_index = [
            {},
            {},
        ]

    def test_update_filename(self):
        """
        """

    def test_update_references_to_filename(self):
        """
        """

    def test_update_filename_record_of_index(self):
        """
        """

# - contains_image: filters/artistic.html
class ContainsImageTestCase(unittest.TestCase):
    """
    """

# - has_ref_to_blending_modes_ref: ???
class GeneralTestCase(unittest.TestCase):
    """
    """

    # All file-text should:
    # - have headers
    # - be prepended with CSS <link> lines
    # - have all references to blending_modes/* subsections corrected to fit new file structure.

