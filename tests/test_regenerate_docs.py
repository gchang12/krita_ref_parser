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
    update_references_to_blending_modes_sections,
    a_href_exists,
    update_img_src,
    normalize_internal_href,
    internal_link_must_be_replaced_with_official_docs_link,
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
from krita_ref_parser._logging import logger

LINK_TO_OFFICIAL_DOCS_CLASSNAME = "link-to-official-docs"
OFFICIAL_DOCS_ROOT = "https://docs.krita.org/en/"

SOURCE_DIR = "./tests/output/raw-excerpts/"
TARGET_DIR = "./tests/output/excerpts/"

for dirname in (SOURCE_DIR, TARGET_DIR):
    Path(dirname).mkdir(parents=True, exist_ok=True)

# AUXILIARY-FUNCTIONS

def get_soup(html_source: str | Path):
    """
    """
    if isinstance(html_source, str):
        soup = BeautifulSoup(html_source, "html.parser")
    elif isinstance(html_source, Path):
        soup = BeautifulSoup(html_source.read_text(encoding="utf-8"), "html.parser")
    else:
        raise TypeError('Must pass either raw-HTML or path to HTML file as argument. Type of argument passed: %r' % type(html_source))
    return soup

# TEST-CASES

# - has_ref_to_blending_modes_ref: ???
@unittest.skip("This has been already tested.")
class GeneralTestCase(unittest.TestCase):
    """
    """
    # All file-text should:
    # - have headers
    # - be prepended with CSS <link> lines
    # - have all references to blending_modes/* subsections corrected to fit new file structure.

    def setUp(self):
        """
        """
        html_source_lines = (
            "<section id='GeneralTestCase'>",
            "<img src='/images/nonexistent-image.svg' />",
            "<h1>General Test Case</h1>",
            "<ul>",
            "</ul>",
            "<div id='empty-tag'></div>"
            "</section>",
        )
        soup = get_soup("\n".join(html_source_lines))
        blending_modes = (
            'addition',
            'divide',
            'inverse-subtract',
            'multiply',
            'subtract',
            )
        for blending_mode in blending_modes:
            index_item_tag = soup.new_tag("a", class_=["internal"])
            index_item_tag.string = blending_mode
            index_item_tag['href'] = '../../blending_modes/arithmetic.html#%s' % blending_mode
            li_tag = soup.new_tag('li')
            li_tag.append(index_item_tag)
            soup.ul.append(li_tag)
        self.soup = soup
        self.blending_modes = blending_modes

    #@unittest.skip("")
    def test_prepend_link_tags_to_soup(self):
        """
        """
        href_list = (
            "/stylesheets/iframe/general.css",
            "/stylesheets/iframe/index.css",
            )
        soup = self.soup
        prepend_link_tags_to_soup(soup, href_list)
        num_links = 0
        for link in soup.find_all("link"):
            logger.debug("Checking if href #%d is as expected.", num_links)
            actual = link['href']
            expected = href_list[num_links]
            with self.subTest():
                self.assertEqual(actual, expected)
            logger.debug("Checking if 'rel' property #%d is as expected.", num_links)
            actual = link['rel']
            expected = ["stylesheet"]
            with self.subTest():
                self.assertEqual(actual, expected)
            logger.debug("Checking if 'type' property #%d is as expected.", num_links)
            actual = link['type']
            expected = "text/css"
            with self.subTest():
                self.assertEqual(actual, expected)
            num_links += 1

    #@unittest.skip("")
    def test_extract_h_tag(self):
        """
        """
        h_level = 1
        soup = self.soup
        actual = soup.find("h1")
        self.assertIsNotNone(actual)
        extract_h_tag(soup, h_level=h_level)
        actual = soup.find("h1")
        self.assertIsNone(actual)

    #@unittest.skip("")
    def test_extract_icon(self):
        """
        """
        soup = self.soup
        actual = soup.find("img")
        self.assertIsNotNone(actual)
        extract_icon(soup)
        actual = soup.find("img")
        self.assertIsNone(actual)

    #@unittest.skip("")
    def test_remove_empty_tags(self):
        """
        """
        soup = self.soup
        div_contents = soup.find('div').find()
        logger.debug("Contents of only div[id='empty-tag'] tag: %r", div_contents)
        self.assertIsNone(div_contents)
        remove_empty_tags(soup)
        actual = soup.find('div')
        self.assertIsNone(actual)

    def test_update_references_to_blending_modes_sections(self):
        """
        """
        soup = self.soup
        for internal_a in soup.find_all('a'):
            update_references_to_blending_modes_sections(TARGET_DIR, internal_a)
        for blending_mode, internal_a in zip(self.blending_modes, soup.find_all('a')):
            expected = "/blending_modes/arithmetic/%s.html" % blending_mode
            actual = internal_a['href']
            with self.subTest():
                self.assertEqual(actual, expected)

    def test_replace_a_tags_with_reactlink_tags(self):
        """
        """
        soup = self.soup
        expected = []
        for a in soup.find_all("a"):
            expected.append((a.text, a['href']))
        replace_a_tags_with_reactlink_tags(soup)
        actual = []
        for Link in soup.find_all("Link"):
            actual.append(Link.text, Link['to'])
        self.assertListEqual(actual, expected)

# - with icon: tools/assistant.html
@unittest.skip("This has already been covered.")
class ContainsIconTestCase(unittest.TestCase):
    """
    """

    def setUp(self):
        """
        """
        html_source_lines = (
            "<section id='GeneralTestCase'>",
            "<img src='/images/nonexistent-image.svg' />",
            "<h1>General Test Case</h1>",
            "<ul>",
            "</ul>",
            "<div id='empty-tag'></div>"
            "</section>",
        )
        soup = get_soup("\n".join(html_source_lines))
        #soup = get_soup(Path(TARGET_DIR, "tools", "assistant.html"))
        self.soup = soup

    #@unittest.skip("")
    def test_extract_icon(self):
        """
        """
        soup = self.soup
        actual = soup.find("img")
        self.assertIsNotNone(actual)
        extract_icon(soup)
        actual = soup.find("img")
        self.assertIsNone(actual)

# - without icon: dockers/add_shape.html
class DoesNotContainsIconTestCase(unittest.TestCase):
    """
    """
    # Some file-text should:
    # - lack icons

    def setUp(self):
        """
        """
        soup = get_soup(Path(TARGET_DIR, "dockers", "add_shape.html"))
        self.soup = soup

    @unittest.skip("...Do I want to make sure that no images have been accidentally added?")
    def test_extract_icon(self):
        """
        """
        soup = self.soup
        actual = soup.find("img")
        self.assertIsNone(actual)
        extract_icon(soup)
        actual = soup.find("img")
        self.assertIsNone(actual)

# - blending_modes: arithmetic.html
class BlendingModeIndexTestCase(unittest.TestCase):
    """
    """
    # Some file-text should:
    # - have certain subsections removed

    def setUp(self):
        """
        """
        soup = get_soup(Path(TARGET_DIR, "blending_modes", "arithmetic.html"))
        self.soup = soup

    def test_extract_subsections(self):
        """
        """
        actual = tuple(soup.css.select("section[id] > section[id]"))
        logger.debug("Now you see them...")
        self.assertTrue(actual)
        extract_subsections(soup)
        logger.debug("And now you don't.")
        actual = tuple(soup.css.select("section[id] > section[id]"))
        self.assertFalse(actual)

# - blending_modes: arithmetic/addition.html
class BlendingModeArticleTestCase(unittest.TestCase):
    """
    """

    def setUp(self):
        """
        """
        soup = get_soup(Path(TARGET_DIR, "arithmetic", "addition.html"))
        self.soup = soup

    def test_update_img_src(self):
        """
        """
        for img in self.soup.find_all("img"):
            expected = "/images/" + Path(img['src']).name
            update_img_src(img)
            actual = img['src']
            with self.subTest():
                self.assertEqual(actual, expected)

# - blending_modes: hsx.html
# - is_blending_modes_hsx: blending_modes/hsx.html
class BlendingModeHSXIndexTestCase(unittest.TestCase):
    """
    """
    # Some file-text should:
    # - have certain subsections removed

    def setUp(self):
        """
        """
        soup = get_soup(Path(TARGET_DIR, "blending_modes", "hsx.html"))
        self.soup = soup

    def test_MANUALLY_REMOVE_SUBSECTIONS(self):
        """
        """
        section = soup.find(id="hsx-blending-modes")
        section.extract()
        expected = set(["HSI", "HSL", "HSV", "HSY"])
        actual = set(section.find('h2').text[:-1] for section in soup.css.select("section[id] > section[id]"))
        self.assertSetEqual(actual, expected)
        actual = soup.find(id="hsx-blending-modes")
        self.assertIsNone(actual)

# - blending_modes/hsx: blending_modes/hsx/intensity.html
class BlendingModeHSXArticleTestCase(unittest.TestCase):
    """
    """

    def setUp(self):
        """
        """
        soup = get_soup(Path(TARGET_DIR, "blending_modes", "hsx", "intensity.html"))
        self.soup = soup

    #@unittest.skip("")
    def test_extract_h_tag(self):
        """
        """
        h_level = 3
        soup = self.soup
        actual = soup.find("h3")
        self.assertIsNotNone(actual)
        extract_h_tag(soup, h_level=h_level)
        actual = soup.find("h3")
        self.assertIsNone(actual)

# - has_external_link: fill_layer_generators/seexpr.html
class ContainsExternalLinkTestCase(unittest.TestCase):
    """
    """
    # All file-text should:
    # - have external links that are opened in new tabs

    def setUp(self):
        """
        """
        soup = get_soup(Path(TARGET_DIR, "layers_and_masks", "fill_layer_generators", "seexpr.html"))
        self.soup = soup

    def test_have_a_tag_open_new_tab(self):
        """
        """
        expected = "_blank"
        for a in self.soup.css.select("a[class='external']"):
            have_a_tag_open_new_tab(a)
            actual = a['target']
            with self.subTest():
                self.assertEqual(actual, expected)

# - has_link_to_krita_non-refman_article: main_menu/settings_menu.html
class ContainsOfficialDocsLinkTestCase(unittest.TestCase):
    """
    """
    # Some file-text should:
    # - have links that point to different parts of this website.
    # - have links that point to parts of the krita-docs that aren't in reference_manual/*

    def setUp(self):
        """
        """
        soup = get_soup(Path(TARGET_DIR, "layers_and_masks", "fill_layer_generators", "seexpr.html"))
        self.soup = soup

    def test_internal_link_must_be_replaced_with_official_docs_link(self):
        """
        """
        expected = True
        num_levels = 3
        href = "../../../tutorials/seexpr.html#seexpr-tut-intro"
        a = soup.find("a", href=href)
        actual = internal_link_must_be_replaced_with_official_docs_link(a, num_levels=num_levels)
        self.assertIs(actual, expected)

    def test_replace_internal_reference_with_official(self):
        """
        """
        soup = self.soup
        href = "../../../tutorials/seexpr.html#seexpr-tut-intro"
        a = soup.find("a", href=href)
        replace_internal_reference_with_official(a)
        expected = "https://docs.krita.org/en/tutorials/seexpr.html#seexpr-tut-intro"
        logger.debug("Searching for just the right tag.")
        for a in soup.find_all("a"):
            if a.text == "Introduction to SeExpr":
                break
        actual = a['href']
        self.assertEqual(actual, expected)
        expected = set(["link-to-official-docs", "external"])
        actual = set(a['class']) # iterable
        self.asserSetEqual(actual, expected)

# - has_link_to_krita_refman_article: dockers/animation_curves.html
class ContainsInternalLinkTestCase(unittest.TestCase):
    """
    """

    def setUp(self):
        """
        """
        soup = get_soup(Path(TARGET_DIR, "dockers", "animation_curves.html"))
        self.soup = soup

    def test_internal_link_must_be_replaced_with_official_docs_link(self):
        """
        """
        soup = self.soup
        expected = False
        num_levels = 2
        href = "../layers_and_masks/transformation_masks.html#transformation-masks"
        a = soup.find("a", href=href)
        actual = internal_link_must_be_replaced_with_official_docs_link(a, num_levels=num_levels)
        self.assertIs(actual, expected)

    def test_normalize_internal_href(self):
        """
        """
        soup = self.soup
        href = "../layers_and_masks/transformation_masks.html#transformation-masks"
        a = soup.find("a", href=href)
        normalize_internal_href(a)
        expected = "/layers_and_masks/transformation_masks.html#transformation-masks"
        actual = a['href']
        self.assertEqual(actual, expected)

# - is_index_file: layers_and_masks/fill_layers.html
class IndexTestCase(unittest.TestCase):
    """
    """

    def setUp(self):
        """
        """
        self.root_dirname = "layers_and_masks"
        soup = get_soup(Path(TARGET_DIR, self.root_dirname, "fill_layers.html"))
        self.soup = soup

    def test_remove_links_from_index(self):
        """
        """
        soup = self.soup
        root_dirname = self.root_dirname
        with self.subTest():
            actual = list(
                map(lambda a: a['href'], filter(
                    lambda a: a['href'].startswith(root_dirname),
                    soup.find_all("a"),
                    )
                )
            )
            self.assertTrue(actual)
            actual = soup.find("ul")
            self.assertIsNotNone(actual)
            actual = list(soup.css.select("ul > li"))
            self.assertTrue(actual)
        remove_links_from_index(soup, root_dirname)
        with self.subTest():
            actual = list(
                map(lambda a: a['href'], filter(
                    lambda a: a['href'].startswith(root_dirname),
                    soup.find_all("a"),
                    )
                )
            )
            self.assertFalse(actual)
            actual = soup.find("ul")
            self.assertIsNone(actual)
            actual = list(soup.css.select("ul > li"))
            self.assertFalse(actual)

# - exception1: layers_and_masks/fill_layers.html
#@unittest.skip("Not ready yet.")
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
            {
                "path": [
                    "layers_and_masks",
                    "fill_layers.html",
                ],
                "header": "Fill Layers",
                "section": "#fill-layers",
                "icon": None,
                "figures": None,
            },
        ]
        shutil.copy_file(
            Path(SOURCE_DIR, self.dirname, self.filename),
            Path(TARGET_DIR, self.dirname, self.filename),
        )
        self.soup = get_soup("""<section id='dummy'>
<h1>References Fill Layer</h1>
<p><a href='layers_and_masks/fill_layers.html'>On Fill Layers</a></p>
</section>""")

    def test_update_filename(self):
        """
        """
        root_dir = TARGET_DIR
        src_path = Path(self.dirname, self.filename)
        tgt_path = Path(self.dirname, "fill_layer_generators.html")
        with self.subTest():
            expected = True
            actual = Path(root_dir, src_path).exists()
            before_text = Path(root_dir, src_path).read_text(encoding="utf-8")
            self.assertIs(actual, expected)
            expected = False
            actual = Path(root_dir, tgt_path).exists()
        update_filename(root_dir, src_path, tgt_path)
        with self.subTest():
            expected = False
            actual = Path(root_dir, src_path).exists()
            self.assertIs(actual, expected)
            expected = True
            actual = Path(root_dir, tgt_path).exists()
            after_text = Path(root_dir, tgt_path).read_text(encoding="utf-8")
        self.assertEqual(before_text, after_text)

    def test_update_references_to_filename(self):
        """
        """
        soup = self.soup
        root_dir = "layers_and_masks"
        src_path = "fill_layers.html"
        tgt_path = "fill_layer_generators.html"
        update_references_to_filename(soup, root_dir, src_path, tgt_path)
        with self.subTest():
            actual = soup.find("a", href='%s/%s' % (root_dir, tgt_path))
            self.assertIsNotNone(actual)
        with self.subTest():
            actual = soup.find("a", href='%s/%s' % (root_dir, src_path))
            self.assertIsNone(actual)

    def test_update_filename_record_of_index(self):
        """
        """
        index = self.mock_index
        new_record = self.mock_index[0].copy()
        new_record['path'] = [self.dirname, self.filename]
        new_record['header'] = "Fill Layer Generators"
        path_id = ["layers_and_masks", "fill_layers.html"]
        update_filename_record_of_index(index, path_id, new_record)
        actual = self.mock_index[0].copy()
        expected = new_record
        self.assertDictEqual(actual, expected)

# - contains_image: filters/artistic.html
class ContainsImageTestCase(unittest.TestCase):
    """
    """

    def setUp(self):
        """
        """
        soup = get_soup(Path(TARGET_DIR, "filters", "artistic.html"))
        self.soup = soup

    def test_update_img_src(self):
        """
        """
        soup = self.soup
        expected = []
        actual = []
        for img in soup.find_all('img'):
            expected.append('/images/' + Path(img['src']).name)
            update_img_src(img)
            actual.append(img['src'])
        self.assertListEqual(actual, expected)
