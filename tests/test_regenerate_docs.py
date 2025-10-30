"""
"""

import io
import unittest
from unittest.mock import patch
from pathlib import Path
import shutil

from bs4 import BeautifulSoup

from krita_ref_parser.regenerate_docs import (
    # for inserting and removing content
    prepend_link_tags_to_soup,
    extract_h_tag,
    extract_icon,
    remove_empty_tags,
    replace_section_with_div,
    # for updating paths and references
    update_references_to_blending_modes_sections,
    a_href_exists,
    update_img_src,
    normalize_internal_href,
    internal_link_should_stay_internal,
    replace_internal_reference_with_official,
    # for changing behavior of links themselves
    replace_a_tags_with_reactlink_tags,
    have_a_tag_open_new_tab,
    # for renovating index files
    extract_subsections,
    remove_links_from_index,
    is_index_file,
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
    if not isinstance(html_source, str):
        raise TypeError('Must pass raw-HTML as str. Type of argument passed: %r' % type(html_source))
    soup = BeautifulSoup(html_source, "html.parser")
    return soup

# TEST-CASES

# - has_ref_to_blending_modes_ref: ???
#@unittest.skip("This has been already tested.")
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

    def test_replace_section_with_div(self):
        """
        """
        html_source_lines = (
            "<div id='GeneralTestCase'>",
            "<img src='/images/nonexistent-image.svg' />",
            "<h1>General Test Case</h1>",
            "<ul>",
            "</ul>",
            "<div id='empty-tag'></div>"
            "</div>",
        )
        expected = get_soup("\n".join(html_source_lines))
        replace_section_with_div(self.soup)
        actual = self.soup
        self.assertEqual(actual, expected)

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
#@unittest.skip("This has already been covered.")
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
class DoesNotContainIconTestCase(unittest.TestCase):
    """
    """
    # Some file-text should:
    # - lack icons

    def setUp(self):
        """
        """
        soup = get_soup('''<section id="add-shape">
<span id="add-shape-docker"></span><h1>Add Shape<a class="headerlink" href="#add-shape" title="Link to this heading">¶</a></h1>
<img alt="../../_images/Krita_Add_Shape_Docker.png" src="../../_images/Krita_Add_Shape_Docker.png"/>
<p>A docker for adding KOffice shapes to a Vector Layers.</p>
<div class="deprecated">
<p><span class="versionmodified deprecated">Deprecated since version 4.0: </span>This got removed in 4.0, the <a class="reference internal" href="vector_library.html#vector-library-docker"><span class="std std-ref">Symbol Libraries</span></a> replacing it.</p>
</div>
</section>''')
        self.soup = soup

    #@unittest.skip("...Do I want to make sure that no images have been accidentally added?")
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
        soup = get_soup('''<section id="arithmetic">
<span id="bm-cat-arithmetic"></span><h1>Arithmetic<a class="headerlink" href="#arithmetic" title="Link to this heading">¶</a></h1>
<p>These blending modes are based on simple maths.</p>
<section id="addition">
<span id="bm-addition"></span><span id="index-0"></span><h2>Addition<a class="headerlink" href="#addition" title="Link to this heading">¶</a></h2>
<p>Adds the numerical values of two colors together:</p>
<p>Yellow(1, 1, 0) + Blue(0, 0, 1) = White(1, 1, 1)</p>
<p>Darker Gray(0.4, 0.4, 0.4) + Lighter Gray(0.5, 0.5, 0.5) = Even Lighter Gray (0.9, 0.9, 0.9)</p>
<figure class="align-center" id="id1">
<img alt="../../_images/Blending_modes_Addition_Gray_0.4_and_Gray_0.5_n.png" src="../../_images/Blending_modes_Addition_Gray_0.4_and_Gray_0.5_n.png"/>
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Addition</strong>.</span><a class="headerlink" href="#id1" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<p>Light Blue(0.1608, 0.6274, 0.8274) + Orange(1, 0.5961, 0.0706) = (1.1608, 1.2235, 0.8980) → Very Light Yellow(1, 1, 0.8980)</p>
<figure class="align-center" id="id2">
<img alt="../../_images/Blending_modes_Addition_Light_blue_and_Orange.png" src="../../_images/Blending_modes_Addition_Light_blue_and_Orange.png"/>
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Addition</strong>.</span><a class="headerlink" href="#id2" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<p>Red(1, 0, 0) + Gray(0.5, 0.5, 0.5) = Pink(1, 0.5, 0.5)</p>
<figure class="align-center" id="id3">
<img alt="../../_images/Blending_modes_Addition_Red_plus_gray.png" src="../../_images/Blending_modes_Addition_Red_plus_gray.png"/>
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Addition</strong>.</span><a class="headerlink" href="#id3" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<p>When the result of the addition is more than 1, white is the color displayed. Therefore, white plus any other color results in white. On the other hand, black plus any other color results in the added color.</p>
<figure class="align-center" id="id4">
<img alt="../../_images/Blending_modes_Addition_Sample_image_with_dots.png" src="../../_images/Blending_modes_Addition_Sample_image_with_dots.png"/>
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Addition</strong>.</span><a class="headerlink" href="#id4" title="Link to this image">¶</a></p>
</figcaption>
</figure>
</section>
<section id="divide">
<span id="bm-divide"></span><h2>Divide<a class="headerlink" href="#divide" title="Link to this heading">¶</a></h2>
<p>Divides the numerical value from the lower color by the upper color.</p>
<p>Red(1, 0, 0) / Gray(0.5, 0.5, 0.5) = (2, 0, 0) → Red(1, 0, 0)</p>
<p>Darker Gray(0.4, 0.4, 0.4) / Lighter Gray(0.5, 0.5, 0.5) = Even Lighter Gray (0.8, 0.8, 0.8)</p>
<figure class="align-center" id="id5">
<img alt="../../_images/Blending_modes_Divide_Gray_0.4_and_Gray_0.5_n.png" src="../../_images/Blending_modes_Divide_Gray_0.4_and_Gray_0.5_n.png"/>
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Divide</strong>.</span><a class="headerlink" href="#id5" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<p>Light Blue(0.1608, 0.6274, 0.8274) / Orange(1, 0.5961, 0.0706) = (0.1608, 1.0525, 11.7195) → Aqua(0.1608, 1, 1)</p>
<figure class="align-center" id="id6">
<img alt="../../_images/Blending_modes_Divide_Light_blue_and_Orange.png" src="../../_images/Blending_modes_Divide_Light_blue_and_Orange.png"/>
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Divide</strong>.</span><a class="headerlink" href="#id6" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<figure class="align-center" id="id7">
<img alt="../../_images/Blending_modes_Divide_Sample_image_with_dots.png" src="../../_images/Blending_modes_Divide_Sample_image_with_dots.png"/>
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Divide</strong>.</span><a class="headerlink" href="#id7" title="Link to this image">¶</a></p>
</figcaption>
</figure>
</section>
<section id="inverse-subtract">
<span id="bm-inverse-subtract"></span><h2>Inverse Subtract<a class="headerlink" href="#inverse-subtract" title="Link to this heading">¶</a></h2>
<p>This inverts the lower layer before subtracting it from the upper layer.</p>
<p>Lighter Gray(0.5, 0.5, 0.5)_(1_Darker Gray(0.4, 0.4, 0.4)) = (-0.1, -0.1, -0.1) → Black(0, 0, 0)</p>
<figure class="align-center" id="id8">
<img alt="../../_images/Blending_modes_Inverse_Subtract_Gray_0.4_and_Gray_0.5_n.png" src="../../_images/Blending_modes_Inverse_Subtract_Gray_0.4_and_Gray_0.5_n.png"/>
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Inverse Subtract</strong>.</span><a class="headerlink" href="#id8" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<p>Orange(1, 0.5961, 0.0706)_(1_Light Blue(0.1608, 0.6274, 0.8274)) = (0.1608, 0.2235, -0.102) → Dark Green(0.1608, 0.2235, 0)</p>
<figure class="align-center" id="id9">
<img alt="../../_images/Blending_modes_Inverse_Subtract_Light_blue_and_Orange.png" src="../../_images/Blending_modes_Inverse_Subtract_Light_blue_and_Orange.png"/>
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Inverse Subtract</strong>.</span><a class="headerlink" href="#id9" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<figure class="align-center" id="id10">
<img alt="../../_images/Blending_modes_Inverse_Subtract_Sample_image_with_dots.png" src="../../_images/Blending_modes_Inverse_Subtract_Sample_image_with_dots.png"/>
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Inverse Subtract</strong>.</span><a class="headerlink" href="#id10" title="Link to this image">¶</a></p>
</figcaption>
</figure>
</section>
<section id="multiply">
<span id="bm-multiply"></span><h2>Multiply<a class="headerlink" href="#multiply" title="Link to this heading">¶</a></h2>
<p>Multiplies the two colors with each other, but does not go beyond the upper limit.</p>
<p>This is often used to color in a black and white lineart.
One puts the black and white lineart on top, sets the layer to ‘Multiply’, and then draws in color on a layer beneath. Multiply will allow all the color to go through.</p>
<p>White(1,1,1) x White(1, 1, 1) = White(1, 1, 1)</p>
<p>White(1, 1, 1) x Gray(0.5, 0.5, 0.5) = Gray(0.5, 0.5, 0.5)</p>
<p>Darker Gray(0.4, 0.4, 0.4) x Lighter Gray(0.5, 0.5, 0.5) = Even Darker Gray (0.2, 0.2, 0.2)</p>
<figure class="align-center" id="id11">
<img alt="../../_images/Blending_modes_Multiply_Gray_0.4_and_Gray_0.5_n.png" src="../../_images/Blending_modes_Multiply_Gray_0.4_and_Gray_0.5_n.png"/>
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Multiply</strong>.</span><a class="headerlink" href="#id11" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<p>Light Blue(0.1608, 0.6274, 0.8274) x Orange(1, 0.5961, 0.0706) = Green(0.1608, 0.3740, 0.0584)</p>
<figure class="align-center" id="id12">
<img alt="../../_images/Blending_modes_Multiply_Light_blue_and_Orange.png" src="../../_images/Blending_modes_Multiply_Light_blue_and_Orange.png"/>
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Multiply</strong>.</span><a class="headerlink" href="#id12" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<figure class="align-center" id="id13">
<img alt="../../_images/Blending_modes_Multiply_Sample_image_with_dots.png" src="../../_images/Blending_modes_Multiply_Sample_image_with_dots.png"/>
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Multiply</strong>.</span><a class="headerlink" href="#id13" title="Link to this image">¶</a></p>
</figcaption>
</figure>
</section>
<section id="subtract">
<span id="bm-subtract"></span><h2>Subtract<a class="headerlink" href="#subtract" title="Link to this heading">¶</a></h2>
<p>Subtracts the top layer from the bottom layer.</p>
<p>White(1, 1, 1)_White(1, 1, 1) = Black(0, 0, 0)</p>
<p>White(1, 1, 1)_Gray(0.5, 0.5, 0.5) = Gray(0.5, 0.5, 0.5)</p>
<p>Darker Gray(0.4, 0.4, 0.4)_Lighter Gray(0.5, 0.5, 0.5) = (-0.1, -0.1, -0.1) → Black(0, 0, 0)</p>
<figure class="align-center" id="id14">
<img alt="../../_images/Blending_modes_Subtract_Gray_0.4_and_Gray_0.5_n.png" src="../../_images/Blending_modes_Subtract_Gray_0.4_and_Gray_0.5_n.png"/>
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Subtract</strong>.</span><a class="headerlink" href="#id14" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<p>Light Blue(0.1608, 0.6274, 0.8274) - Orange(1, 0.5961, 0.0706) = (-0.8392, 0.0313, 0.7568) → Blue(0, 0.0313, 0.7568)</p>
<figure class="align-center" id="id15">
<img alt="../../_images/Blending_modes_Subtract_Light_blue_and_Orange.png" src="../../_images/Blending_modes_Subtract_Light_blue_and_Orange.png"/>
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Subtract</strong>.</span><a class="headerlink" href="#id15" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<figure class="align-center" id="id16">
<img alt="../../_images/Blending_modes_Subtract_Sample_image_with_dots.png" src="../../_images/Blending_modes_Subtract_Sample_image_with_dots.png"/>
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Subtract</strong>.</span><a class="headerlink" href="#id16" title="Link to this image">¶</a></p>
</figcaption>
</figure>
</section>
</section>''')
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
        soup = get_soup('''<section id="addition">
<span id="bm-addition"></span><span id="index-0"></span><h2>Addition<a class="headerlink" href="#addition" title="Link to this heading">¶</a></h2>
<p>Adds the numerical values of two colors together:</p>
<p>Yellow(1, 1, 0) + Blue(0, 0, 1) = White(1, 1, 1)</p>
<p>Darker Gray(0.4, 0.4, 0.4) + Lighter Gray(0.5, 0.5, 0.5) = Even Lighter Gray (0.9, 0.9, 0.9)</p>
<figure class="align-center" id="id1">
<img alt="../../_images/Blending_modes_Addition_Gray_0.4_and_Gray_0.5_n.png" src="../../_images/Blending_modes_Addition_Gray_0.4_and_Gray_0.5_n.png"/>
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Addition</strong>.</span><a class="headerlink" href="#id1" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<p>Light Blue(0.1608, 0.6274, 0.8274) + Orange(1, 0.5961, 0.0706) = (1.1608, 1.2235, 0.8980) → Very Light Yellow(1, 1, 0.8980)</p>
<figure class="align-center" id="id2">
<img alt="../../_images/Blending_modes_Addition_Light_blue_and_Orange.png" src="../../_images/Blending_modes_Addition_Light_blue_and_Orange.png"/>
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Addition</strong>.</span><a class="headerlink" href="#id2" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<p>Red(1, 0, 0) + Gray(0.5, 0.5, 0.5) = Pink(1, 0.5, 0.5)</p>
<figure class="align-center" id="id3">
<img alt="../../_images/Blending_modes_Addition_Red_plus_gray.png" src="../../_images/Blending_modes_Addition_Red_plus_gray.png"/>
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Addition</strong>.</span><a class="headerlink" href="#id3" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<p>When the result of the addition is more than 1, white is the color displayed. Therefore, white plus any other color results in white. On the other hand, black plus any other color results in the added color.</p>
<figure class="align-center" id="id4">
<img alt="../../_images/Blending_modes_Addition_Sample_image_with_dots.png" src="../../_images/Blending_modes_Addition_Sample_image_with_dots.png"/>
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Addition</strong>.</span><a class="headerlink" href="#id4" title="Link to this image">¶</a></p>
</figcaption>
</figure>
</section>''')
        section = ("arithmetic", "addition.html")
        self.soup = soup
        self.section = section

    def test_is_index_file(self):
        """
        """
        filename = Path(*self.section)
        expected = False
        actual = is_index_file(filename)
        self.assertIs(actual, expected)

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
        soup = get_soup('''<section id="hsx">
<span id="bm-cat-hsx"></span><span id="index-0"></span><h1>HSX<a class="headerlink" href="#hsx" title="Link to this heading">¶</a></h1>
<p>Krita has four different HSX coordinate systems. The difference between them is how they handle tone.</p>
<section id="hsi">
<h2>HSI<a class="headerlink" href="#hsi" title="Link to this heading">¶</a></h2>
<p>HSI is a color coordinate system, using Hue, Saturation and Intensity to categorize a color.
Hue is roughly the wavelength, whether the color is red, yellow, green, cyan, blue or purple. It is measured in 360°, with 0 being red.
Saturation is the measurement of how close a color is to gray.
Intensity, in this case, is the tone of the color. What makes intensity special is that it recognizes yellow (rgb:1,1,0) having a higher combined rgb value than blue (rgb:0,0,1). This is a non-linear tone dimension, which means it’s gamma-corrected.</p>
</section>
<section id="hsl">
<h2>HSL<a class="headerlink" href="#hsl" title="Link to this heading">¶</a></h2>
<p>HSL is a color coordinate system that describes colors in Hue, Saturation and Lightness.
Lightness specifically puts both yellow (rgb:1,1,0), blue (rgb:0,0,1) and middle gray (rgb:0.5,0.5,0.5) at the same lightness (0.5).</p>
</section>
<section id="hsv">
<h2>HSV<a class="headerlink" href="#hsv" title="Link to this heading">¶</a></h2>
<p>HSV, occasionally called HSB, is a color coordinate system that measures colors in Hue, Saturation, and Value (also called Brightness).
Value or Brightness specifically refers to strength at which the pixel-lights on your monitor have to shine. It sets Yellow (rgb:1,1,0), Blue (rgb:0,0,1) and White (rgb:1,1,1) at the same Value (100%).</p>
</section>
<section id="hsy">
<h2>HSY<a class="headerlink" href="#hsy" title="Link to this heading">¶</a></h2>
<p>HSY is a color coordinate system categorizing colors in Hue, Saturation and Luminosity. Well, not really, it uses Luma instead of true luminosity, the difference being that Luminosity is linear while Luma is gamma-corrected and just weights the rgb components.
Luma is based on scientific studies of how much light a color reflects in real-life. While like intensity it acknowledges that yellow (rgb:1,1,0) is lighter than blue (rgb:0,0,1), it also acknowledges that yellow (rgb:1,1,0) is lighter than cyan (rgb:0,1,1), based on these studies.</p>
</section>
<section id="hsx-blending-modes">
<h2>HSX Blending Modes<a class="headerlink" href="#hsx-blending-modes" title="Link to this heading">¶</a></h2>
<section id="color-hsv-hsi-hsl-hsy">
<span id="bm-hsy-color"></span><span id="bm-hsi-color"></span><span id="bm-hsl-color"></span><span id="bm-hsv-color"></span><span id="bm-color"></span><h3>Color, HSV, HSI, HSL, HSY<a class="headerlink" href="#color-hsv-hsi-hsl-hsy" title="Link to this heading">¶</a></h3>
<p>This takes the Luminosity/Value/Intensity/Lightness of the colors on the lower layer, and combines them with the Saturation and Hue of the upper pixels. We refer to Color HSY as ‘Color’ in line with other applications.</p>
<figure class="align-center" id="id1">
<img alt="../../_images/Blending_modes_Color_HSI_Gray_0.4_and_Gray_0.5.png" src="../../_images/Blending_modes_Color_HSI_Gray_0.4_and_Gray_0.5.png"/>
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Color HSI</strong>.</span><a class="headerlink" href="#id1" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<figure class="align-center" id="id2">
<img alt="../../_images/Blending_modes_Color_HSI_Light_blue_and_Orange.png" src="../../_images/Blending_modes_Color_HSI_Light_blue_and_Orange.png"/>
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Color HSI</strong>.</span><a class="headerlink" href="#id2" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<figure class="align-center" id="id3">
<img alt="../../_images/Blending_modes_Color_HSI_Sample_image_with_dots.png" src="../../_images/Blending_modes_Color_HSI_Sample_image_with_dots.png"/>
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Color HSI</strong>.</span><a class="headerlink" href="#id3" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<figure class="align-center" id="id4">
<img alt="../../_images/Blending_modes_Color_HSL_Sample_image_with_dots.png" src="../../_images/Blending_modes_Color_HSL_Sample_image_with_dots.png"/>
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Color HSL</strong>.</span><a class="headerlink" href="#id4" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<figure class="align-center" id="id5">
<img alt="../../_images/Blending_modes_Color_HSV_Sample_image_with_dots.png" src="../../_images/Blending_modes_Color_HSV_Sample_image_with_dots.png"/>
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Color HSV</strong>.</span><a class="headerlink" href="#id5" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<figure class="align-center" id="id6">
<img alt="../../_images/Blending_modes_Color_Sample_image_with_dots.png" src="../../_images/Blending_modes_Color_Sample_image_with_dots.png"/>
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Color</strong>.</span><a class="headerlink" href="#id6" title="Link to this image">¶</a></p>
</figcaption>
</figure>
</section>
<section id="hue-hsv-hsi-hsl-hsy">
<span id="bm-hsy-hue"></span><span id="bm-hsi-hue"></span><span id="bm-hsl-hue"></span><span id="bm-hsv-hue"></span><span id="bm-hue"></span><h3>Hue HSV, HSI, HSL, HSY<a class="headerlink" href="#hue-hsv-hsi-hsl-hsy" title="Link to this heading">¶</a></h3>
<p>Takes the saturation and tone of the lower layer and combines them with the hue of the upper-layer.
Tone in this case being either Value, Lightness, Intensity or Luminosity.</p>
<figure class="align-center" id="id7">
<img alt="../../_images/Blending_modes_Hue_HSI_Sample_image_with_dots.png" src="../../_images/Blending_modes_Hue_HSI_Sample_image_with_dots.png"/>
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Hue HSI</strong>.</span><a class="headerlink" href="#id7" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<figure class="align-center" id="id8">
<img alt="../../_images/Blending_modes_Hue_HSL_Sample_image_with_dots.png" src="../../_images/Blending_modes_Hue_HSL_Sample_image_with_dots.png"/>
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Hue HSL</strong>.</span><a class="headerlink" href="#id8" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<figure class="align-center" id="id9">
<img alt="../../_images/Blending_modes_Hue_HSV_Sample_image_with_dots.png" src="../../_images/Blending_modes_Hue_HSV_Sample_image_with_dots.png"/>
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Hue HSV</strong>.</span><a class="headerlink" href="#id9" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<figure class="align-center" id="id10">
<img alt="../../_images/Blending_modes_Hue_Sample_image_with_dots.png" src="../../_images/Blending_modes_Hue_Sample_image_with_dots.png"/>
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Hue</strong>.</span><a class="headerlink" href="#id10" title="Link to this image">¶</a></p>
</figcaption>
</figure>
</section>
<section id="increase-value-lightness-intensity-or-luminosity">
<span id="bm-increase-luminosity"></span><span id="bm-increase-intensity"></span><span id="bm-increase-lightness"></span><span id="bm-increase-value"></span><h3>Increase Value, Lightness, Intensity or Luminosity.<a class="headerlink" href="#increase-value-lightness-intensity-or-luminosity" title="Link to this heading">¶</a></h3>
<p>Similar to Lighten, but specific to tone.
Checks whether the upper layer’s pixel has a higher tone than the lower layer’s pixel. If so, the tone is increased, if not, the lower layer’s tone is maintained.</p>
<figure class="align-center" id="id11">
<img alt="../../_images/Blending_modes_Increase_Intensity_Sample_image_with_dots.png" src="../../_images/Blending_modes_Increase_Intensity_Sample_image_with_dots.png"/>
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Increase Intensity</strong>.</span><a class="headerlink" href="#id11" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<figure class="align-center" id="id12">
<img alt="../../_images/Blending_modes_Increase_Lightness_Sample_image_with_dots.png" src="../../_images/Blending_modes_Increase_Lightness_Sample_image_with_dots.png"/>
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Increase Lightness</strong>.</span><a class="headerlink" href="#id12" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<figure class="align-center" id="id13">
<img alt="../../_images/Blending_modes_Increase_Value_Sample_image_with_dots.png" src="../../_images/Blending_modes_Increase_Value_Sample_image_with_dots.png"/>
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Increase Value</strong>.</span><a class="headerlink" href="#id13" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<figure class="align-center" id="id14">
<img alt="../../_images/Blending_modes_Increase_Luminosity_Sample_image_with_dots.png" src="../../_images/Blending_modes_Increase_Luminosity_Sample_image_with_dots.png"/>
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Increase Luminosity</strong>.</span><a class="headerlink" href="#id14" title="Link to this image">¶</a></p>
</figcaption>
</figure>
</section>
<section id="increase-saturation-hsi-hsv-hsl-hsy">
<span id="bm-increase-hsy-saturation"></span><span id="bm-increase-hsi-saturation"></span><span id="bm-increase-hsl-saturation"></span><span id="bm-increase-hsv-saturation"></span><span id="bm-increase-saturation"></span><h3>Increase Saturation HSI, HSV, HSL, HSY<a class="headerlink" href="#increase-saturation-hsi-hsv-hsl-hsy" title="Link to this heading">¶</a></h3>
<p>Similar to Lighten, but specific to Saturation.
Checks whether the upper layer’s pixel has a higher Saturation than the lower layer’s pixel. If so, the Saturation is increased, if not, the lower layer’s Saturation is maintained.</p>
<figure class="align-center" id="id15">
<img alt="../../_images/Blending_modes_Increase_Saturation_HSI_Sample_image_with_dots.png" src="../../_images/Blending_modes_Increase_Saturation_HSI_Sample_image_with_dots.png"/>
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Increase Saturation HSI</strong>.</span><a class="headerlink" href="#id15" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<figure class="align-center" id="id16">
<img alt="../../_images/Blending_modes_Increase_Saturation_HSL_Sample_image_with_dots.png" src="../../_images/Blending_modes_Increase_Saturation_HSL_Sample_image_with_dots.png"/>
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Increase Saturation HSL</strong>.</span><a class="headerlink" href="#id16" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<figure class="align-center" id="id17">
<img alt="../../_images/Blending_modes_Increase_Saturation_HSV_Sample_image_with_dots.png" src="../../_images/Blending_modes_Increase_Saturation_HSV_Sample_image_with_dots.png"/>
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Increase Saturation HSV</strong>.</span><a class="headerlink" href="#id17" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<figure class="align-center" id="id18">
<img alt="../../_images/Blending_modes_Increase_Saturation_Sample_image_with_dots.png" src="../../_images/Blending_modes_Increase_Saturation_Sample_image_with_dots.png"/>
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Increase Saturation</strong>.</span><a class="headerlink" href="#id18" title="Link to this image">¶</a></p>
</figcaption>
</figure>
</section>
<section id="intensity">
<span id="bm-intensity"></span><h3>Intensity<a class="headerlink" href="#intensity" title="Link to this heading">¶</a></h3>
<p>Takes the Hue and Saturation of the lower layer and outputs them with the intensity of the upper layer.</p>
<figure class="align-center" id="id19">
<img alt="../../_images/Blending_modes_Intensity_Sample_image_with_dots.png" src="../../_images/Blending_modes_Intensity_Sample_image_with_dots.png"/>
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Intensity</strong>.</span><a class="headerlink" href="#id19" title="Link to this image">¶</a></p>
</figcaption>
</figure>
</section>
<section id="value">
<span id="bm-value"></span><h3>Value<a class="headerlink" href="#value" title="Link to this heading">¶</a></h3>
<p>Takes the Hue and Saturation of the lower layer and outputs them with the Value of the upper layer.</p>
<figure class="align-center" id="id20">
<img alt="../../_images/Blending_modes_Value_Sample_image_with_dots.png" src="../../_images/Blending_modes_Value_Sample_image_with_dots.png"/>
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Value</strong>.</span><a class="headerlink" href="#id20" title="Link to this image">¶</a></p>
</figcaption>
</figure>
</section>
<section id="lightness">
<span id="bm-lightness"></span><h3>Lightness<a class="headerlink" href="#lightness" title="Link to this heading">¶</a></h3>
<p>Takes the Hue and Saturation of the lower layer and outputs them with the Lightness of the upper layer.</p>
<figure class="align-center" id="id21">
<img alt="../../_images/Blending_modes_Lightness_Sample_image_with_dots.png" src="../../_images/Blending_modes_Lightness_Sample_image_with_dots.png"/>
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Lightness</strong>.</span><a class="headerlink" href="#id21" title="Link to this image">¶</a></p>
</figcaption>
</figure>
</section>
<section id="luminosity">
<span id="bm-luminosity"></span><h3>Luminosity<a class="headerlink" href="#luminosity" title="Link to this heading">¶</a></h3>
<p>As explained above, actually Luma, but called this way as it’s in line with the terminology in other applications.
Takes the Hue and Saturation of the lower layer and outputs them with the Luminosity of the upper layer.
The most preferred one of the four Tone blending modes, as this one gives fairly intuitive results for the Tone of a hue.</p>
<figure class="align-center" id="id22">
<img alt="../../_images/Blending_modes_Luminosity_Sample_image_with_dots.png" src="../../_images/Blending_modes_Luminosity_Sample_image_with_dots.png"/>
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Luminosity</strong>.</span><a class="headerlink" href="#id22" title="Link to this image">¶</a></p>
</figcaption>
</figure>
</section>
<section id="saturation-hsi-hsv-hsl-hsy">
<span id="bm-hsy-saturation"></span><span id="bm-hsi-saturation"></span><span id="bm-hsl-saturation"></span><span id="bm-hsv-saturation"></span><span id="bm-saturation"></span><h3>Saturation HSI, HSV, HSL, HSY<a class="headerlink" href="#saturation-hsi-hsv-hsl-hsy" title="Link to this heading">¶</a></h3>
<p>Takes the Intensity and Hue of the lower layer, and outputs them with the HSI saturation of the upper layer.</p>
<figure class="align-center" id="id23">
<img alt="../../_images/Blending_modes_Saturation_HSI_Sample_image_with_dots.png" src="../../_images/Blending_modes_Saturation_HSI_Sample_image_with_dots.png"/>
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Saturation HSI</strong>.</span><a class="headerlink" href="#id23" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<figure class="align-center" id="id24">
<img alt="../../_images/Blending_modes_Saturation_HSL_Sample_image_with_dots.png" src="../../_images/Blending_modes_Saturation_HSL_Sample_image_with_dots.png"/>
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Saturation HSL</strong>.</span><a class="headerlink" href="#id24" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<figure class="align-center" id="id25">
<img alt="../../_images/Blending_modes_Saturation_HSV_Sample_image_with_dots.png" src="../../_images/Blending_modes_Saturation_HSV_Sample_image_with_dots.png"/>
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Saturation HSV</strong>.</span><a class="headerlink" href="#id25" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<figure class="align-center" id="id26">
<img alt="../../_images/Blending_modes_Saturation_Sample_image_with_dots.png" src="../../_images/Blending_modes_Saturation_Sample_image_with_dots.png"/>
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Saturation</strong>.</span><a class="headerlink" href="#id26" title="Link to this image">¶</a></p>
</figcaption>
</figure>
</section>
<section id="decrease-value-lightness-intensity-or-luminosity">
<span id="bm-decrease-luminosity"></span><span id="bm-decrease-intensity"></span><span id="bm-decrease-lightness"></span><span id="bm-decrease-value"></span><h3>Decrease Value, Lightness, Intensity or Luminosity<a class="headerlink" href="#decrease-value-lightness-intensity-or-luminosity" title="Link to this heading">¶</a></h3>
<p>Similar to Darken, but specific to tone.
Checks whether the upper layer’s pixel has a lower tone than the lower layer’s pixel. If so, the tone is decreased, if not, the lower layer’s tone is maintained.</p>
<figure class="align-center" id="id27">
<img alt="../../_images/Blending_modes_Decrease_Intensity_Gray_0.4_and_Gray_0.5.png" src="../../_images/Blending_modes_Decrease_Intensity_Gray_0.4_and_Gray_0.5.png"/>
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Decrease Intensity</strong>.</span><a class="headerlink" href="#id27" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<figure class="align-center" id="id28">
<img alt="../../_images/Blending_modes_Decrease_Intensity_Light_blue_and_Orange.png" src="../../_images/Blending_modes_Decrease_Intensity_Light_blue_and_Orange.png"/>
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Decrease Intensity</strong>.</span><a class="headerlink" href="#id28" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<figure class="align-center" id="id29">
<img alt="../../_images/Blending_modes_Decrease_Intensity_Sample_image_with_dots.png" src="../../_images/Blending_modes_Decrease_Intensity_Sample_image_with_dots.png"/>
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Decrease Intensity</strong>.</span><a class="headerlink" href="#id29" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<figure class="align-center" id="id30">
<img alt="../../_images/Blending_modes_Decrease_Lightness_Sample_image_with_dots.png" src="../../_images/Blending_modes_Decrease_Lightness_Sample_image_with_dots.png"/>
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Decrease Lightness</strong>.</span><a class="headerlink" href="#id30" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<figure class="align-center" id="id31">
<img alt="../../_images/Blending_modes_Decrease_Value_Sample_image_with_dots.png" src="../../_images/Blending_modes_Decrease_Value_Sample_image_with_dots.png"/>
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Decrease Value</strong>.</span><a class="headerlink" href="#id31" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<figure class="align-center" id="id32">
<img alt="../../_images/Blending_modes_Decrease_Luminosity_Sample_image_with_dots.png" src="../../_images/Blending_modes_Decrease_Luminosity_Sample_image_with_dots.png"/>
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Decrease Luminosity</strong>.</span><a class="headerlink" href="#id32" title="Link to this image">¶</a></p>
</figcaption>
</figure>
</section>
<section id="decrease-saturation-hsi-hsv-hsl-hsy">
<span id="bm-decrease-hsy-saturation"></span><span id="bm-decrease-hsi-saturation"></span><span id="bm-decrease-hsl-saturation"></span><span id="bm-decrease-hsv-saturation"></span><span id="bm-decrease-saturation"></span><h3>Decrease Saturation HSI, HSV, HSL, HSY<a class="headerlink" href="#decrease-saturation-hsi-hsv-hsl-hsy" title="Link to this heading">¶</a></h3>
<p>Similar to Darken, but specific to Saturation.
Checks whether the upper layer’s pixel has a lower Saturation than the lower layer’s pixel. If so, the Saturation is decreased, if not, the lower layer’s Saturation is maintained.</p>
<figure class="align-center" id="id33">
<img alt="../../_images/Blending_modes_Decrease_Saturation_HSI_Gray_0.4_and_Gray_0.5.png" src="../../_images/Blending_modes_Decrease_Saturation_HSI_Gray_0.4_and_Gray_0.5.png"/>
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Decrease Saturation HSI</strong>.</span><a class="headerlink" href="#id33" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<figure class="align-center" id="id34">
<img alt="../../_images/Blending_modes_Decrease_Saturation_HSI_Light_blue_and_Orange.png" src="../../_images/Blending_modes_Decrease_Saturation_HSI_Light_blue_and_Orange.png"/>
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Decrease Saturation HSI</strong>.</span><a class="headerlink" href="#id34" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<figure class="align-center" id="id35">
<img alt="../../_images/Blending_modes_Decrease_Saturation_HSI_Sample_image_with_dots.png" src="../../_images/Blending_modes_Decrease_Saturation_HSI_Sample_image_with_dots.png"/>
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Decrease Saturation HSI</strong>.</span><a class="headerlink" href="#id35" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<figure class="align-center" id="id36">
<img alt="../../_images/Blending_modes_Decrease_Saturation_HSL_Sample_image_with_dots.png" src="../../_images/Blending_modes_Decrease_Saturation_HSL_Sample_image_with_dots.png"/>
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Decrease Saturation HSL</strong>.</span><a class="headerlink" href="#id36" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<figure class="align-center" id="id37">
<img alt="../../_images/Blending_modes_Decrease_Saturation_HSV_Sample_image_with_dots.png" src="../../_images/Blending_modes_Decrease_Saturation_HSV_Sample_image_with_dots.png"/>
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Decrease Saturation HSV</strong>.</span><a class="headerlink" href="#id37" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<figure class="align-center" id="id38">
<img alt="../../_images/Blending_modes_Decrease_Saturation_Sample_image_with_dots.png" src="../../_images/Blending_modes_Decrease_Saturation_Sample_image_with_dots.png"/>
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Decrease Saturation</strong>.</span><a class="headerlink" href="#id38" title="Link to this image">¶</a></p>
</figcaption>
</figure>
</section>
</section>
</section>''')
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
        soup = get_soup('''<section id="intensity">
<span id="bm-intensity"></span><h3>Intensity<a class="headerlink" href="#intensity" title="Link to this heading">¶</a></h3>
<p>Takes the Hue and Saturation of the lower layer and outputs them with the intensity of the upper layer.</p>
<figure class="align-center" id="id19">
<img alt="../../_images/Blending_modes_Intensity_Sample_image_with_dots.png" src="../../_images/Blending_modes_Intensity_Sample_image_with_dots.png"/>
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Intensity</strong>.</span><a class="headerlink" href="#id19" title="Link to this image">¶</a></p>
</figcaption>
</figure>
</section>''')
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
        soup = get_soup('''<section id="seexpr">
<span id="seexpr-fill-layer"></span><span id="index-0"></span><h1>SeExpr<a class="headerlink" href="#seexpr" title="Link to this heading">¶</a></h1>
<div class="versionadded">
<p><span class="versionmodified added">Added in version 4.4.</span></p>
</div>
<img alt="../../../_images/SeExpr-David-Revoy.jpg" src="../../../_images/SeExpr-David-Revoy.jpg"/>
<p>Fills the layer with a pattern specified through Disney Animation’s
<a class="reference external" href="https://wdas.github.io/SeExpr">SeExpr expression language</a>.</p>
<div class="admonition seealso">
<p class="admonition-title">See also</p>
<ul class="simple">
<li><p><a class="reference internal" href="../../../tutorials/seexpr.html#seexpr-tut-intro"><span class="std std-ref">Introduction to SeExpr</span></a></p></li>
<li><p><a class="reference internal" href="../../seexpr.html#seexpr"><span class="std std-ref">SeExpr Quick Reference</span></a></p></li>
<li><p><a class="reference internal" href="../../resource_management/seexpr_scripts.html#resource-seexpr-scripts"><span class="std std-ref">SeExpr Scripts</span></a></p></li>
<li><p><a class="reference external" href="https://krita-artists.org/t/procedural-texture-generator-example-and-wishes/7638">“Procedural texture generator (example and wishes)” on Krita Artists</a></p></li>
<li><p><a class="reference external" href="https://iquilezles.org/www/index.htm">Inigo Quilez’s articles</a></p></li>
<li><p><a class="reference external" href="https://thebookofshaders.com/">The Book of Shaders</a></p></li>
</ul>
</div>
<p>SeExpr is an embeddable, arithmetic expression language that enables you to
write shader-like scripts. Through this language, Krita can add dynamically
generated textures like lava (example above), force fields, wood, marble,
etc. to your layers.</p>
<p>As with Patterns, you can create your own and use those as well.
For some examples, please check out the thread <a class="reference external" href="https://krita-artists.org/t/procedural-texture-generator-example-and-wishes/7638">“Procedural texture generator (example and wishes)” on Krita Artists</a>.
You can download them as a bundle through <a class="reference external" href="https://www.amyspark.me/blog/posts/2020/07/03/third-alpha-release.html">Amyspark’s blog</a>.</p>
<dl>
<dt>Script</dt><dd><p>Select the desired preset out of any existing bundled presets.
This tab is identical to the Pattern preset selector.</p>
<img alt="../../../_images/SeExpr_script.png" src="../../../_images/SeExpr_script.png"/>
</dd>
<dt>Options</dt><dd><p>This tab allows you to edit the selected preset, and apply its script
to the layer.</p>
<img alt="../../../_images/SeExpr_editor.png" src="../../../_images/SeExpr_editor.png"/>
<p>There are three sections. The first bar allows you to edit and save the selected preset:</p>
<img alt="../../../_images/SeExpr_editor_preset_mgmt.png" src="../../../_images/SeExpr_editor_preset_mgmt.png"/>
<p>If your script is syntactically correct, the middle box lets you
adjust its variables through widgets.</p>
<img alt="../../../_images/SeExpr_editor_widgets.png" src="../../../_images/SeExpr_editor_widgets.png"/>
<p>The lower box contains the script text, and shows the detected syntax
errors, if any.</p>
<img alt="../../../_images/SeExpr_editor_script_error.png" src="../../../_images/SeExpr_editor_script_error.png"/>
<p>You can adjust how much space the latter two boxes have through their
splitter.</p>
</dd>
</dl>
</section>''')
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
        soup = get_soup('''<section id="seexpr">
<span id="seexpr-fill-layer"></span><span id="index-0"></span><h1>SeExpr<a class="headerlink" href="#seexpr" title="Link to this heading">¶</a></h1>
<div class="versionadded">
<p><span class="versionmodified added">Added in version 4.4.</span></p>
</div>
<img alt="../../../_images/SeExpr-David-Revoy.jpg" src="../../../_images/SeExpr-David-Revoy.jpg"/>
<p>Fills the layer with a pattern specified through Disney Animation’s
<a class="reference external" href="https://wdas.github.io/SeExpr">SeExpr expression language</a>.</p>
<div class="admonition seealso">
<p class="admonition-title">See also</p>
<ul class="simple">
<li><p><a class="reference internal" href="../../../tutorials/seexpr.html#seexpr-tut-intro"><span class="std std-ref">Introduction to SeExpr</span></a></p></li>
<li><p><a class="reference internal" href="../../seexpr.html#seexpr"><span class="std std-ref">SeExpr Quick Reference</span></a></p></li>
<li><p><a class="reference internal" href="../../resource_management/seexpr_scripts.html#resource-seexpr-scripts"><span class="std std-ref">SeExpr Scripts</span></a></p></li>
<li><p><a class="reference external" href="https://krita-artists.org/t/procedural-texture-generator-example-and-wishes/7638">“Procedural texture generator (example and wishes)” on Krita Artists</a></p></li>
<li><p><a class="reference external" href="https://iquilezles.org/www/index.htm">Inigo Quilez’s articles</a></p></li>
<li><p><a class="reference external" href="https://thebookofshaders.com/">The Book of Shaders</a></p></li>
</ul>
</div>
<p>SeExpr is an embeddable, arithmetic expression language that enables you to
write shader-like scripts. Through this language, Krita can add dynamically
generated textures like lava (example above), force fields, wood, marble,
etc. to your layers.</p>
<p>As with Patterns, you can create your own and use those as well.
For some examples, please check out the thread <a class="reference external" href="https://krita-artists.org/t/procedural-texture-generator-example-and-wishes/7638">“Procedural texture generator (example and wishes)” on Krita Artists</a>.
You can download them as a bundle through <a class="reference external" href="https://www.amyspark.me/blog/posts/2020/07/03/third-alpha-release.html">Amyspark’s blog</a>.</p>
<dl>
<dt>Script</dt><dd><p>Select the desired preset out of any existing bundled presets.
This tab is identical to the Pattern preset selector.</p>
<img alt="../../../_images/SeExpr_script.png" src="../../../_images/SeExpr_script.png"/>
</dd>
<dt>Options</dt><dd><p>This tab allows you to edit the selected preset, and apply its script
to the layer.</p>
<img alt="../../../_images/SeExpr_editor.png" src="../../../_images/SeExpr_editor.png"/>
<p>There are three sections. The first bar allows you to edit and save the selected preset:</p>
<img alt="../../../_images/SeExpr_editor_preset_mgmt.png" src="../../../_images/SeExpr_editor_preset_mgmt.png"/>
<p>If your script is syntactically correct, the middle box lets you
adjust its variables through widgets.</p>
<img alt="../../../_images/SeExpr_editor_widgets.png" src="../../../_images/SeExpr_editor_widgets.png"/>
<p>The lower box contains the script text, and shows the detected syntax
errors, if any.</p>
<img alt="../../../_images/SeExpr_editor_script_error.png" src="../../../_images/SeExpr_editor_script_error.png"/>
<p>You can adjust how much space the latter two boxes have through their
splitter.</p>
</dd>
</dl>
</section>''')
        self.soup = soup

    def test_internal_link_should_stay_internal(self):
        """
        """
        expected = False
        num_levels = 2
        href = "../../../tutorials/seexpr.html#seexpr-tut-intro"
        a = soup.find("a", href=href)
        actual = internal_link_should_stay_internal(a, num_levels=num_levels)
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
        soup = get_soup('''<section id="animation-curves-docker">
<span id="index-0"></span><span id="id1"></span><h1>Animation Curves Docker<a class="headerlink" href="#animation-curves-docker" title="Link to this heading">¶</a></h1>
<p><strong class="program">Krita</strong>’s <em class="dfn">Animation Curves Docker</em> allows artists to animate the values of some properties over time.</p>
<p>When animating a complex cut, it’s not unusual to want to animate things that would be difficult or inefficient to do through drawing alone. In traditional pen-and-paper animation dating back to the 1920s, special lighting rigs and purpose-built devices like multiplane cameras were used to pull off special effects that changed animation forever! Likewise, Krita’s Animation Curves docker allows us to animate more than just the lines on your canvas, such as a layer’s opacity or the position, rotation and scale of a <a class="reference internal" href="../layers_and_masks/transformation_masks.html#transformation-masks"><span class="std std-ref">Transform Mask</span></a>.</p>
<p>Because most things can be boiled down to numeric values (for example, opacity as a percentage or the position of a Transform Mask), and because computers are great with maths and automation, we can plot and visualize the change in values over time on a simple 2D graph. What’s more, we can also draw lines and curves that show the computer how we want it to calculate the values in between each of our plotted keyframe values; a technique known as interpolation or <em class="dfn">tweening</em>.</p>
<img alt="../../_images/Animation_Curves_Docker.png" src="../../_images/Animation_Curves_Docker.png"/>
<section id="overview">
<h2>Overview<a class="headerlink" href="#overview" title="Link to this heading">¶</a></h2>
<p>As shown in the image above, Krita’s Animation Curves Docker can be thought of as different sections:</p>
<ol class="upperalpha simple">
<li><p><em class="dfn">Utilities</em> – The left side of the toolbar gives animators quick access to all of the widgets that are critical to their workflow; <em class="dfn">transport controls</em> (previous, play/pause, stop and next buttons), a frame counter, preview controls (speed and drop frames), buttons for adding and removing <em class="dfn">scalar keyframes</em>, buttons for changing the <em class="dfn">interpolation mode</em> and <em class="dfn">tangent mode</em> of the selected keyframe, a box for setting the selected keyframe to a specific value, as well as buttons to help zoom and navigate the main graph view.</p></li>
<li><p><em class="dfn">Settings</em> – While all of the high-traffic controls are presented directly, the right end of the toolbar also contains buttons for opening submenus for things like onion skins and settings that you can generally set and forget (for example, <em class="dfn">playback range</em>, <em class="dfn">frame rate</em> and <em class="dfn">autokey mode</em>).</p></li>
<li><p><em class="dfn">Channels List</em> – This area shows the various channels of the current layer that are currently being animated within the Animation Curves Docker. Each independent channel is associated with a unique color and its visibility within the graph view can be toggled by clicking on the eyeball icon.</p></li>
<li><p><em class="dfn">Graph View</em> – Last but not least is the <em class="dfn">graph view</em>, the big graph of values and times that we use to animate the value of parameters over time. When a <a class="reference internal" href="animation_timeline.html#term-Keyframe"><span class="xref std std-term">keyframe</span></a> is added to the current channel at the current time it will appear as a colored circle within the graph view. After clicking on the keyframe to select it, you can change the value by dragging the circle vertically or by entering a specific value into the value box on the toolbar. Similarly, you can change the time of the selected frame by dragging it horizontally. Finally, when the select keyframe is using <span class="guilabel">bezier curve interpolation</span>, selecting it will cause one or more <em class="dfn">curve handles</em> to appear, which can be used to change the shape of the interpolation curve over time.</p></li>
</ol>
</section>
<section id="animating-opacity">
<h2>Animating Opacity<a class="headerlink" href="#animating-opacity" title="Link to this heading">¶</a></h2>
<p>Starting with <strong class="program">Krita 5</strong>, we can use the Animation Curves Docker to animate a layer’s <a class="reference internal" href="layers.html#term-Opacity"><span class="xref std std-term">opacity</span></a> and, with the help of a <a class="reference internal" href="../layers_and_masks/transformation_masks.html#transformation-masks"><span class="std std-ref">Transform Mask</span></a>, its <em class="dfn">position</em>, <em class="dfn">rotation</em>, <em class="dfn">scale</em> and <em class="dfn">shear</em>.</p>
<div class="admonition warning">
<p class="admonition-title">Warning</p>
<p>Though the design is pretty similar to the <a class="reference internal" href="animation_timeline.html#timeline-docker"><span class="std std-ref">Animation Timeline Docker</span></a>, the Animation Curves Docker may be a bit confusing or intimidating when you first open it, especially if you haven’t done digital animation before.</p>
</div>
<p>Let’s look first at <em>animating a layer’s opacity</em>:</p>
<p>Say you want to animate something like an expanding cloud of dust that gradually becomes more transparent as it dissipates, or maybe a haunting ghost that seems to materialize out of thin air. These types of effects are pretty hard to get right by traditionally animated line drawings alone, and that’s exactly where the Animation Curves Docker can step in.</p>
<p>After <em>selecting the layer</em> that you want to animate the opacity of, you need to <em>select the frame time you want the opacity to start changing at</em> by clicking somewhere on the <a class="reference internal" href="animation_timeline.html#term-Frame-Timing-Header"><span class="xref std std-term">frame timing header</span></a> at the top of the graph view. Just like the <a class="reference internal" href="animation_timeline.html#timeline-docker"><span class="std std-ref">Animation Timeline Docker</span></a>, we can click and drag anywhere on the timing header to “scrub” across your animation and preview the results.</p>
<p>Next we create our first scalar <a class="reference internal" href="animation_timeline.html#term-Keyframe"><span class="xref std std-term">keyframe</span></a> by clicking on the <span class="guilabel">add keyframe</span> button on the docker’s titlebar.</p>
<p>When you do this you’ll notice two things happen. First, a new <span class="guilabel">opacity channel</span> will appear in the <em class="dfn">channels list</em> on the left-hand side, next to a colored mark that’s associated with the color of the keyframes and curves in the <em class="dfn">graph view</em>. Second, a single keyframe will appear somewhere inside the graph view at the currently active time.</p>
<p>Of course it takes more than a single point to make a line or curve, so we have a little bit more work to do.</p>
<p>Just like our first keyframe, we need to make a second keyframe. Let’s change the active frame time again (by clicking or scrubbing across the timing header) and add another keyframe at that new time (by clicking on the <span class="guilabel">add keyframe</span> button). As you’d expect, a second keyframe has appeared at the new time and a straight line has appeared between them.</p>
<p>With the active time still over our new keyframe, you’ll find that as you change the <em class="dfn">opacity slider</em> above the <a class="reference internal" href="layers.html#layer-docker"><span class="std std-ref">Layers</span></a> the new keyframe that we’ve created will move up and down. Likewise, moving the keyframe up and down will cause the opacity <em>at that time</em> to change.</p>
<p>And just like that, when you press the <span class="guilabel">play button</span> you’ll see the opacity of the layer animate over time!</p>
<blockquote>
<div><div class="admonition warning">
<p class="admonition-title">Warning</p>
<p>Unlike traditional methods, animating with curves can cause values to change across every frame of your animation. This can be more demanding on your machine and cause the caching process to take a little bit more time, as it calculates and stores each frame.</p>
</div>
</div></blockquote>
<p><em>Before we move on</em>, let’s use <em class="dfn">interpolation curves</em> instead of a straight line to change the timing and general feel of our opacity animation.</p>
<p>If you select the first keyframe (the one on the left-hand side) of your line segment and click on the <span class="guilabel">bezier curve interpolation</span> button in the utilities section of the titlebar, you’ll notice that the keyframe will appear as a hollow circle on the graph view. That hollow circle is a <em class="dfn">handle</em>, and by clicking on it and dragging in different directions you can change the arc of the curve between your two keyframes.</p>
<p>Similarly, you can click on the <span class="guilabel">linear interpolation</span> button to change your curve back into a line, or the <span class="guilabel">constant</span> button to turn off interpolation altogether, causing values to jump suddenly between keyframes.</p>
<blockquote>
<div><div class="admonition note">
<p class="admonition-title">Note</p>
<p>It’s important to be aware of which animation frame is selected and active, as shown by the highlighted vertical line on the graph view. The keyframe that changes as you make adjustments elsewhere in the program will always be dependent on the active frame time!</p>
</div>
</div></blockquote>
<p><em>Ok, it’s a bit tough to put in writing…</em> But it’s not so bad once you get the hang of it!</p>
</section>
<section id="animating-transform-masks">
<h2>Animating Transform Masks<a class="headerlink" href="#animating-transform-masks" title="Link to this heading">¶</a></h2>
<p>Now let’s talk a bit about how we can use a <a class="reference internal" href="../layers_and_masks/transformation_masks.html#transformation-masks"><span class="std std-ref">Transform Masks</span></a> to <em>animate our layer’s position, rotation, scale and shear</em> for <em class="dfn">“tweening”</em> effects:</p>
<p>Animating a transform mask is a lot like animating opacity, but first we need to <em>add a Transform Mask</em>. (You can do this by <img alt="mouseright" src="../../_images/Krita_mouse_right.png"/> on the layer that you want to animate, and then <span class="menuselection">Add ‣ Transform Mask</span>.)</p>
<p>Transform Masks allow us to <em class="dfn">transform</em> (translate, rotate, scale, or shear) the layer that they are attached to, without affecting its original position. And (starting with Krita 5) they also allow us to animate a layer’s transform!</p>
<p>Much like how we animated opacity above, we need to add our first transformation keyframe. To do this, <em>first make sure that you have your layer’s Transform Mask selected</em>, and then click on the <span class="guilabel">add keyframe</span> button at the top of the docker.</p>
<blockquote>
<div><div class="admonition warning">
<p class="admonition-title">Warning</p>
<p>Remember (as of Krita 5.0) we can only <em>directly</em> animate the opacity curve of a layer. In order to animate a layer’s position, rotation, scale and shear, we need to attach a Transform Mask and animate it instead.</p>
<p>As such, <em>when you have a regular paint layer selected</em> the Animation Curves Docker will automatically add opacity keyframes, and <em>when you have a transform mask selected</em> the Animation Curves Docker will automatically add transformation keyframes.</p>
<p>Try to always keep in mind what type of layer you have selected when animating curves in Krita!</p>
</div>
</div></blockquote>
<p>You should see a whole bunch of channels appear in the channels list, each with a unique name and color, as well as a number of corresponding keyframes.</p>
<p>If you want to you can edit these key frames directly in the graph view, but it’s probably more intuitive to do it directly on the canvas. So now, when you use the <a class="reference internal" href="../tools/transform.html#transform-tool"><span class="std std-ref">Transform Tool</span></a> on your <a class="reference internal" href="../layers_and_masks/transformation_masks.html#transformation-masks"><span class="std std-ref">Transform Masks</span></a>, you should see the various keyframes of each channel moving around in the graph view to reflect the changes.</p>
<blockquote>
<div><div class="admonition tip">
<p class="admonition-title">Tip</p>
<p>Animating a Transform Mask spawns a lot of channels but, depending on your goals, you may only want to work with a small number of them at a time. <em>Hiding</em> and <em>soloing</em> channels in the channels list can make it much easier to see and edit curves, especially since you can use the <span class="guilabel">zoom to channel</span> and <span class="guilabel">zoom to curve</span> buttons at the top of the docker to fit the graph view to the currently visible channels.</p>
<p>Navigating by click-dragging on the zoomable scrollbars and <em>values header</em> (on the left-hand side of the graph view) can also really help with editing curves!</p>
</div>
</div></blockquote>
<p>Finally, click or scrub to a different frame time, add another keyframe, and use the Transform Tool on the same Transform Mask again.</p>
<p>Press the <span class="guilabel">play button</span> and (after a little bit of caching) there you have it, a layer with an animated Transform Mask!</p>
</section>
<section id="controls">
<h2>Controls<a class="headerlink" href="#controls" title="Link to this heading">¶</a></h2>
<ol class="arabic">
<li><p><em class="dfn">Channels List</em></p>
<blockquote>
<div><ul class="simple">
<li><p><img alt="mouseleft" src="../../_images/Krita_mouse_left.png"/> on Eye Icon: Toggle show/hide channel.</p></li>
<li><p><kbd class="kbd compound docutils literal notranslate"><kbd class="kbd docutils literal notranslate">Shift</kbd> <kbd class="kbd docutils literal notranslate">+</kbd></kbd> <img alt="mouseleft" src="../../_images/Krita_mouse_left.png"/> on Eye Icon: Solo channel.</p></li>
<li><p><img alt="mouseright" src="../../_images/Krita_mouse_right.png"/> : Open layer or channel context menu. [Reset Channel(s)]</p></li>
</ul>
</div></blockquote>
</li>
<li><p><em class="dfn">Graph View</em></p>
<blockquote>
<div><ul class="simple">
<li><p><img alt="mouseleft" src="../../_images/Krita_mouse_left.png"/> : Select keyframe.</p></li>
<li><p><img alt="mouseleft" src="../../_images/Krita_mouse_left.png"/> <kbd class="kbd compound docutils literal notranslate"><kbd class="kbd docutils literal notranslate">+</kbd> <kbd class="kbd docutils literal notranslate">drag</kbd></kbd> : <em>Move</em> frame(s).</p></li>
<li><p><img alt="mouseleft" src="../../_images/Krita_mouse_left.png"/> double-click : Select all keyframes at time.</p></li>
<li><p><kbd class="kbd compound docutils literal notranslate"><kbd class="kbd docutils literal notranslate">Alt</kbd> <kbd class="kbd docutils literal notranslate">+</kbd></kbd> <img alt="mouseleft" src="../../_images/Krita_mouse_left.png"/> double-click : Select all keyframes of channel.</p></li>
<li><p><kbd class="kbd compound docutils literal notranslate"><kbd class="kbd docutils literal notranslate">Space</kbd> <kbd class="kbd docutils literal notranslate">+</kbd></kbd> <img alt="mouseleft" src="../../_images/Krita_mouse_left.png"/> : Pan.</p></li>
<li><p><kbd class="kbd compound docutils literal notranslate"><kbd class="kbd docutils literal notranslate">Space</kbd> <kbd class="kbd docutils literal notranslate">+</kbd></kbd> <img alt="mouseright" src="../../_images/Krita_mouse_right.png"/> : Zoom.</p></li>
</ul>
</div></blockquote>
</li>
<li><p><em class="dfn">Frame Timing Header</em></p>
<blockquote>
<div><ul class="simple">
<li><p><img alt="mouseleft" src="../../_images/Krita_mouse_left.png"/> : Move to time and select frame of the active layer.</p></li>
<li><p><img alt="mouseleft" src="../../_images/Krita_mouse_left.png"/> <kbd class="kbd compound docutils literal notranslate"><kbd class="kbd docutils literal notranslate">+</kbd> <kbd class="kbd docutils literal notranslate">drag</kbd></kbd> : Scrub through time and select frame of the active layer.</p></li>
</ul>
</div></blockquote>
</li>
<li><p><em class="dfn">Value Header</em></p>
<blockquote>
<div><ul class="simple">
<li><p><img alt="mouseleft" src="../../_images/Krita_mouse_left.png"/> <kbd class="kbd compound docutils literal notranslate"><kbd class="kbd docutils literal notranslate">+</kbd> <kbd class="kbd docutils literal notranslate">drag</kbd></kbd> : Zoom graph view.</p></li>
<li><p><kbd class="kbd compound docutils literal notranslate"><kbd class="kbd docutils literal notranslate">Space</kbd> <kbd class="kbd docutils literal notranslate">+</kbd></kbd> <img alt="mouseleft" src="../../_images/Krita_mouse_left.png"/> <kbd class="kbd compound docutils literal notranslate"><kbd class="kbd docutils literal notranslate">+</kbd> <kbd class="kbd docutils literal notranslate">drag</kbd></kbd> : Pan graph view.</p></li>
</ul>
</div></blockquote>
</li>
</ol>
</section>
</section>''')
        self.soup = soup

    def test_internal_link_should_stay_internal(self):
        """
        """
        soup = self.soup
        expected = True
        num_levels = 1
        href = "../layers_and_masks/transformation_masks.html#transformation-masks"
        a = soup.find("a", href=href)
        actual = internal_link_should_stay_internal(a, num_levels=num_levels)
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
        soup = get_soup('''<section id="fill-layers">
<span id="index-0"></span><span id="id1"></span><h1>Fill Layers<a class="headerlink" href="#fill-layers" title="Link to this heading">¶</a></h1>
<p>A Fill Layer is a special layer that Krita generates on-the-fly that can contain either a pattern or a solid color.</p>
<img alt="../../_images/Fill_Layer.png" src="../../_images/Fill_Layer.png"/>
<p>By default, the dialog selects the flat color fill. This fills the layer with a singular color. Newly created colored fill layers will be assigned to the currently active foreground color, unless they were made by drag-and-dropping a <a class="reference internal" href="../dockers/palette_docker.html#palette-docker"><span class="std std-ref">palette swatch</span></a> onto the <a class="reference internal" href="../dockers/layers.html#layer-docker"><span class="std std-ref">layer stack</span></a>.</p>
<p>However, there are many more options, with more complex features:</p>
<div class="toctree-wrapper compound">
<ul>
<li class="toctree-l1"><a class="reference internal" href="fill_layer_generators/gradient.html">Gradient Fill</a></li>
<li class="toctree-l1"><a class="reference internal" href="fill_layer_generators/multigrid.html">Multigrid</a></li>
<li class="toctree-l1"><a class="reference internal" href="fill_layer_generators/pattern_fill.html">Pattern Fill</a></li>
<li class="toctree-l1"><a class="reference internal" href="fill_layer_generators/screentone.html">Screentone</a></li>
<li class="toctree-l1"><a class="reference internal" href="fill_layer_generators/seexpr.html">SeExpr</a></li>
<li class="toctree-l1"><a class="reference internal" href="fill_layer_generators/simplex_noise.html">Simplex Noise</a></li>
</ul>
</div>
<section id="painting-on-a-fill-layer">
<h2>Painting on a fill layer<a class="headerlink" href="#painting-on-a-fill-layer" title="Link to this heading">¶</a></h2>
<p>A fill-layer is a single-channel layer, meaning it only has transparency. Therefore, you can erase and paint on fill-layers to make them semi-opaque, or for when you want to have a particular color only. Being single channel, fill-layers are also a little bit less memory-consuming than regular 4-channel paint layers.</p>
</section>
</section>''')
        self.soup = soup
        self.section = (self.root_dirname, "fill_layers.html")

    def test_is_index_file(self):
        """
        """
        filename = Path(*self.section)
        expected = True
        actual = is_index_file(filename)
        self.assertIs(actual, expected)

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
        soup = get_soup('''<section id="artistic">
<span id="artistic-filters"></span><span id="index-0"></span><h1>Artistic<a class="headerlink" href="#artistic" title="Link to this heading">¶</a></h1>
<p>The artistic filter are characterised by taking an input, and doing a deformation on them.</p>
<section id="halftone">
<h2>Halftone<a class="headerlink" href="#halftone" title="Link to this heading">¶</a></h2>
<img alt="../../_images/Krita_halftone_filter.jpg" src="../../_images/Krita_halftone_filter.jpg"/>
<p>The <a class="reference external" href="https://en.wikipedia.org/wiki/Halftone">halftone</a> filter tries to replicate the continuous-tone of the original image through the use of simple shapes that vary in size.</p>
<dl>
<dt>Mode</dt><dd><dl class="simple">
<dt>Intensity</dt><dd><p>In this mode the image is first converted to grayscale and then the halftoning is applied. The resulting effect is like the one used in black and white newspaper images.</p>
</dd>
<dt>Independent Channels</dt><dd><p>This allows applying the halftoning to each channel of the image independently, potentially with different parameters, giving an effect similar to the one in colored magazine images.</p>
</dd>
<dt>Alpha</dt><dd><p>With this option the halftoning is applied only to the alpha channel (you may see no change when all the pixels of the image are fully opaque). This is useful to add texture to the smooth semi-transparent borders of a layer.</p>
</dd>
</dl>
</dd>
<dt>Halftoning Options</dt><dd><p>When the selected mode is <em>Independent Channels</em>, multiple tabs for the different channels appear to let the user choose different options for each one; otherwise no tabs for the channels appear and there is only one set of options.
The halftoning process works by making a pattern image (commonly named <em>screen</em>) that is combined with the original image in a specific way.</p>
<dl>
<dt>Screen Generator</dt><dd><p>The filter uses the <em>fill layer generators</em> to create the screen (pattern) image instead of using a predefined set of patterns and options. This way the range of possible results can grow as new generators are added to Krita. Also the user can make his own patterns by using the pattern generator and custom pattern images. For more information see <a class="reference internal" href="../layers_and_masks/fill_layers.html#fill-layers"><span class="std std-ref">this page on fill layer generators and their options</span></a>.</p>
</dd>
<dt>Postprocessing</dt><dd><p>These options apply to the result of combining the screen image with the original image.</p>
<dl class="simple">
<dt>Hardness</dt><dd><p>Controls how hard or soft are the borders of the halftone shapes.</p>
</dd>
<dt>Invert</dt><dd><p>Invert the resulting image/channel.</p>
</dd>
<dt>Foreground &amp; Background</dt><dd><p>Change what color and opacity are used for the foreground (part of the image formed by the pattern shapes) and the background.</p>
</dd>
</dl>
</dd>
</dl>
</dd>
</dl>
</section>
<section id="index-color">
<h2>Index Color<a class="headerlink" href="#index-color" title="Link to this heading">¶</a></h2>
<p>The index color filter maps specific user selected colors to the grayscale value of the artwork. You can see the example below, the strip below the black and white gradient has index color applied to it so that the black and white gradient gets the color selected to different values.</p>
<img alt="../../_images/Gradient-pixelart.png" src="../../_images/Gradient-pixelart.png"/>
<p>You can choose the required colors and ramps in the index color filter dialog as shown below .</p>
<img alt="../../_images/Index-color-filter.png" src="../../_images/Index-color-filter.png"/>
<p>You can create index painting such as one shown below with the help of this filter.</p>
<img alt="../../_images/Kiki-pixel-art.png" src="../../_images/Kiki-pixel-art.png"/>
</section>
<section id="pixelize">
<h2>Pixelize<a class="headerlink" href="#pixelize" title="Link to this heading">¶</a></h2>
<p>Makes the input-image pixely by creating small cells and inputting an average color.</p>
<img alt="../../_images/Pixelize-filter.png" src="../../_images/Pixelize-filter.png"/>
</section>
<section id="raindrops">
<h2>Raindrops<a class="headerlink" href="#raindrops" title="Link to this heading">¶</a></h2>
<p>Adds random raindrop-deformations to the input-image.</p>
</section>
<section id="oilpaint">
<h2>Oilpaint<a class="headerlink" href="#oilpaint" title="Link to this heading">¶</a></h2>
<p>Does semi-posterisation to the input-image, with the ‘brush-size’ determining the size of the fields.</p>
<img alt="../../_images/Oilpaint-filter.png" src="../../_images/Oilpaint-filter.png"/>
<dl class="simple">
<dt>Brush-size</dt><dd><p>Determines how large the individual patches are. The lower, the more detailed.</p>
</dd>
<dt>Smoothness</dt><dd><p>Determines how much each patch’s outline is smoothed out.</p>
</dd>
</dl>
</section>
<section id="posterize">
<h2>Posterize<a class="headerlink" href="#posterize" title="Link to this heading">¶</a></h2>
<p>This filter decreases the amount of colors in an image. It does this per component (channel).</p>
<img alt="../../_images/Posterize-filter.png" src="../../_images/Posterize-filter.png"/>
<p>The <span class="guilabel">Steps</span> parameter determines how many colors are allowed per component.</p>
</section>
</section>''')
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
