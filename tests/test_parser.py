"""
"""

from pathlib import Path
import unittest
#import logging

from bs4 import BeautifulSoup

import parser
from _logging import logger

class BaseSoupTestCase(unittest.TestCase):
    """
    """

    def setUp(self):
        """
        """
        self.htmldir = None

    def assertSoupEqual(self, actual, expected):
        """
        """
        actual = [line.strip() for line in str(actual).splitlines() if line.strip()]
        expected = [line.strip() for line in str(expected).splitlines() if line.strip()]
        filename = ".actual.html"
        with open(filename, encoding="utf-8", mode="w") as wfile:
            wfile.write(str(actual))
        filename = ".expected.html"
        with open(filename, encoding="utf-8", mode="w") as wfile:
            wfile.write(str(expected))
        self.assertListEqual(actual, expected)

    def _test_one(self, path):
        """
        """
        logger.debug("Now inspecting: %s", path)
        with open(path, encoding='utf-8') as rfile:
            soup = BeautifulSoup(rfile, "html.parser")
        actual = self.func_to_test(soup)
        return actual

    def test_ALL(self):
        """
        """
        # check that the excerpt begins with 'section[id]'
        # check that all a[class='internal'] are replaced with a[class='link-to-official-docs' src='docs.krita.org/...']
        # check that pilcrows are removed; log h1 text
        #self.htmldir_for_tools = "_src-html/reference_manual/tools/"
        if self.htmldir is None:
            return
        for path in Path(self.htmldir).iterdir():
            self._test_one(path)

class ToolsTests(BaseSoupTestCase):
    """
    """

    def setUp(self):
        """
        """
        self.htmldir = "_src-html/reference_manual/tools/"
        self.func_to_test = parser.generate_tools_excerpt
        logger.critical("%s", self.id())

    #@unittest.skip("")
    def test_generate_tools_excerpt(self):
        """
        """
        htmldir = self.htmldir
        htmlfile = "assistant.html"
        path_to_html = htmldir + htmlfile
        with open(path_to_html, encoding="utf-8") as rfile:
            soup = BeautifulSoup(rfile, 'html.parser')
        actual = self.func_to_test(soup)
        expected_soup = BeautifulSoup("""<section id="assistant-tool">
<span id="index-0"></span><span id="id1"></span>
<p></p>
<p>Create, edit, and remove drawing assistants on the canvas. There are a number of different assistants that can be used from this tool. The tool options allow you to add new assistants, and to save/load assistants. To add a new assistant, select a type from the tool options and begin clicking on the canvas. Each assistant is created a bit differently. There are also additional controls on existing assistants that allow you to move and delete them.</p>
<p>The set of assistants on the current canvas can be saved to a “*.paintingassistant” file using the <span class="guilabel">Save</span> button in the tool options. These assistants can then be loaded onto a different canvas using the Open button. This functionality is also useful for creating copies of the same drawing assistant(s) on the current canvas.</p>
<p>Check <a class="reference link-to-official-docs" href="https://docs.krita.org/en/user_manual/painting_with_assistants.html#painting-with-assistants"><span class="std std-ref">Painting with Assistants</span></a> for more information.</p>
<section id="tool-options">
<h2>Tool Options<a class="headerlink" href="#tool-options" title="Link to this heading">¶</a></h2>
<div class="versionadded">
<p><span class="versionmodified added">Added in version 4.0.</span></p>
</div>
<dl class="simple">
<dt>Global Color:</dt><dd><p>Global color allows you to set the color and opacity of all assistants at once.</p>
</dd>
</dl>
<div class="versionadded">
<p><span class="versionmodified added">Added in version 4.1.</span></p>
</div>
<dl class="simple">
<dt>Custom Color:</dt><dd><p>Custom color allows you to set a color and opacity per assistant, allowing for different colors on an assistant. To use this functionality, first ‘select’ an assistant by tapping its move widget. Then go to the tool options docker to see the <span class="guilabel">Custom Color</span> check box. Check that, and then use the opacity and color buttons to pick either for this particular assistant.</p>
</dd>
</dl>
<div class="versionadded">
<p><span class="versionmodified added">Added in version 5.0.</span></p>
</div>
<p>Limit assistant to area</p>
<blockquote>
<div><figure class="align-default" id="id2">
<img alt="../../_images/Assistants_2_pointperspective_03.png" src="./images/Assistants_2_pointperspective_03.png" />
<figcaption>
<p><span class="caption-text">In the above image, two extra vanishing points have been added to a 2 point assistant, limiting the area in which the grid is drawn and the brush will snap.</span><a class="headerlink" href="#id2" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<p>This option adds two extra handles to every assistant, for drawing a rectangle which will limit the assistant. This is very useful for comic pages, which may need multiple assistants per page, and will otherwise become very crowded.</p>
</div></blockquote>
</section>
</section>""", 'html.parser').find()
        expected_icon = BeautifulSoup("<img alt='toolassistant' src='./images/assistant_tool.svg' />", 'html.parser').find('img').extract()['src']
        expected = ("Assistant Tool", expected_icon, expected_soup)
        #logger.debug("actual: %s", type(actual[2]))
        #logger.debug("expected: %s", type(expected[2]))
        self.assertTupleEqual(actual[:2], expected[:2])
        #self.assertEqual(actual[2], expected[2])
        a_soup, e_soup = actual[2], expected[2]
        self.assertSoupEqual(a_soup, e_soup)

class BlendingModeTests(BaseSoupTestCase):
    """
    """

    def setUp(self):
        """
        """
        self.htmldir = "_src-html/reference_manual/blending_modes/"
        self.func_to_test = parser.generate_blendingmodes_excerpt
        logger.critical("%s", self.id())

    def test_generate_blendingmodes_excerpt(self):
        """
        """
        htmldir = self.htmldir
        htmlfile = "arithmetic.html"
        path_to_html = htmldir + htmlfile
        with open(path_to_html, encoding="utf-8") as rfile:
            soup = BeautifulSoup(rfile, 'html.parser')
        actual = self.func_to_test(soup)
        expected_dotsimg_src = [
            './images/Blending_modes_Addition_Sample_image_with_dots.png',
            './images/Blending_modes_Divide_Sample_image_with_dots.png',
            './images/Blending_modes_Inverse_Subtract_Sample_image_with_dots.png',
            './images/Blending_modes_Multiply_Sample_image_with_dots.png',
            './images/Blending_modes_Subtract_Sample_image_with_dots.png',
        ]
        expected_soups = (
            """<section id="addition">
<span id="bm-addition"></span><span id="index-0"></span>
<p>Adds the numerical values of two colors together:</p>
<p>Yellow(1, 1, 0) + Blue(0, 0, 1) = White(1, 1, 1)</p>
<p>Darker Gray(0.4, 0.4, 0.4) + Lighter Gray(0.5, 0.5, 0.5) = Even Lighter Gray (0.9, 0.9, 0.9)</p>
<figure class="align-center" id="id1">
<img alt="../../_images/Blending_modes_Addition_Gray_0.4_and_Gray_0.5_n.png" src="./images/Blending_modes_Addition_Gray_0.4_and_Gray_0.5_n.png" />
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Addition</strong>.</span><a class="headerlink" href="#id1" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<p>Light Blue(0.1608, 0.6274, 0.8274) + Orange(1, 0.5961, 0.0706) = (1.1608, 1.2235, 0.8980) → Very Light Yellow(1, 1, 0.8980)</p>
<figure class="align-center" id="id2">
<img alt="../../_images/Blending_modes_Addition_Light_blue_and_Orange.png" src="./images/Blending_modes_Addition_Light_blue_and_Orange.png" />
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Addition</strong>.</span><a class="headerlink" href="#id2" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<p>Red(1, 0, 0) + Gray(0.5, 0.5, 0.5) = Pink(1, 0.5, 0.5)</p>
<figure class="align-center" id="id3">
<img alt="../../_images/Blending_modes_Addition_Red_plus_gray.png" src="./images/Blending_modes_Addition_Red_plus_gray.png" />
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Addition</strong>.</span><a class="headerlink" href="#id3" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<p>When the result of the addition is more than 1, white is the color displayed. Therefore, white plus any other color results in white. On the other hand, black plus any other color results in the added color.</p>
<figure class="align-center" id="id4">
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Addition</strong>.</span><a class="headerlink" href="#id4" title="Link to this image">¶</a></p>
</figcaption>
</figure>
</section>""",
            """<section id="divide">
<span id="bm-divide"></span>
<p>Divides the numerical value from the lower color by the upper color.</p>
<p>Red(1, 0, 0) / Gray(0.5, 0.5, 0.5) = (2, 0, 0) → Red(1, 0, 0)</p>
<p>Darker Gray(0.4, 0.4, 0.4) / Lighter Gray(0.5, 0.5, 0.5) = Even Lighter Gray (0.8, 0.8, 0.8)</p>
<figure class="align-center" id="id5">
<img alt="../../_images/Blending_modes_Divide_Gray_0.4_and_Gray_0.5_n.png" src="./images/Blending_modes_Divide_Gray_0.4_and_Gray_0.5_n.png" />
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Divide</strong>.</span><a class="headerlink" href="#id5" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<p>Light Blue(0.1608, 0.6274, 0.8274) / Orange(1, 0.5961, 0.0706) = (0.1608, 1.0525, 11.7195) → Aqua(0.1608, 1, 1)</p>
<figure class="align-center" id="id6">
<img alt="../../_images/Blending_modes_Divide_Light_blue_and_Orange.png" src="./images/Blending_modes_Divide_Light_blue_and_Orange.png" />
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Divide</strong>.</span><a class="headerlink" href="#id6" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<figure class="align-center" id="id7">
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Divide</strong>.</span><a class="headerlink" href="#id7" title="Link to this image">¶</a></p>
</figcaption>
</figure>
</section>""",
            """<section id="inverse-subtract">
<span id="bm-inverse-subtract"></span>
<p>This inverts the lower layer before subtracting it from the upper layer.</p>
<p>Lighter Gray(0.5, 0.5, 0.5)_(1_Darker Gray(0.4, 0.4, 0.4)) = (-0.1, -0.1, -0.1) → Black(0, 0, 0)</p>
<figure class="align-center" id="id8">
<img alt="../../_images/Blending_modes_Inverse_Subtract_Gray_0.4_and_Gray_0.5_n.png" src="./images/Blending_modes_Inverse_Subtract_Gray_0.4_and_Gray_0.5_n.png" />
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Inverse Subtract</strong>.</span><a class="headerlink" href="#id8" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<p>Orange(1, 0.5961, 0.0706)_(1_Light Blue(0.1608, 0.6274, 0.8274)) = (0.1608, 0.2235, -0.102) → Dark Green(0.1608, 0.2235, 0)</p>
<figure class="align-center" id="id9">
<img alt="../../_images/Blending_modes_Inverse_Subtract_Light_blue_and_Orange.png" src="./images/Blending_modes_Inverse_Subtract_Light_blue_and_Orange.png" />
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Inverse Subtract</strong>.</span><a class="headerlink" href="#id9" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<figure class="align-center" id="id10">
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Inverse Subtract</strong>.</span><a class="headerlink" href="#id10" title="Link to this image">¶</a></p>
</figcaption>
</figure>
</section>""",
            """<section id="multiply">
<span id="bm-multiply"></span>
<p>Multiplies the two colors with each other, but does not go beyond the upper limit.</p>
<p>This is often used to color in a black and white lineart.
One puts the black and white lineart on top, sets the layer to ‘Multiply’, and then draws in color on a layer beneath. Multiply will allow all the color to go through.</p>
<p>White(1,1,1) x White(1, 1, 1) = White(1, 1, 1)</p>
<p>White(1, 1, 1) x Gray(0.5, 0.5, 0.5) = Gray(0.5, 0.5, 0.5)</p>
<p>Darker Gray(0.4, 0.4, 0.4) x Lighter Gray(0.5, 0.5, 0.5) = Even Darker Gray (0.2, 0.2, 0.2)</p>
<figure class="align-center" id="id11">
<img alt="../../_images/Blending_modes_Multiply_Gray_0.4_and_Gray_0.5_n.png" src="./images/Blending_modes_Multiply_Gray_0.4_and_Gray_0.5_n.png" />
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Multiply</strong>.</span><a class="headerlink" href="#id11" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<p>Light Blue(0.1608, 0.6274, 0.8274) x Orange(1, 0.5961, 0.0706) = Green(0.1608, 0.3740, 0.0584)</p>
<figure class="align-center" id="id12">
<img alt="../../_images/Blending_modes_Multiply_Light_blue_and_Orange.png" src="./images/Blending_modes_Multiply_Light_blue_and_Orange.png" />
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Multiply</strong>.</span><a class="headerlink" href="#id12" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<figure class="align-center" id="id13">
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Multiply</strong>.</span><a class="headerlink" href="#id13" title="Link to this image">¶</a></p>
</figcaption>
</figure>
</section>""",
            """<section id="subtract">
<span id="bm-subtract"></span>
<p>Subtracts the top layer from the bottom layer.</p>
<p>White(1, 1, 1)_White(1, 1, 1) = Black(0, 0, 0)</p>
<p>White(1, 1, 1)_Gray(0.5, 0.5, 0.5) = Gray(0.5, 0.5, 0.5)</p>
<p>Darker Gray(0.4, 0.4, 0.4)_Lighter Gray(0.5, 0.5, 0.5) = (-0.1, -0.1, -0.1) → Black(0, 0, 0)</p>
<figure class="align-center" id="id14">
<img alt="../../_images/Blending_modes_Subtract_Gray_0.4_and_Gray_0.5_n.png" src="./images/Blending_modes_Subtract_Gray_0.4_and_Gray_0.5_n.png" />
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Subtract</strong>.</span><a class="headerlink" href="#id14" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<p>Light Blue(0.1608, 0.6274, 0.8274) - Orange(1, 0.5961, 0.0706) = (-0.8392, 0.0313, 0.7568) → Blue(0, 0.0313, 0.7568)</p>
<figure class="align-center" id="id15">
<img alt="../../_images/Blending_modes_Subtract_Light_blue_and_Orange.png" src="./images/Blending_modes_Subtract_Light_blue_and_Orange.png" />
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Subtract</strong>.</span><a class="headerlink" href="#id15" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<figure class="align-center" id="id16">
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Subtract</strong>.</span><a class="headerlink" href="#id16" title="Link to this image">¶</a></p>
</figcaption>
</figure>
</section>
</section>
"""
)
        expected_h_texts = (
            "Addition",
            "Divide",
            "Inverse Subtract",
            "Multiply",
            "Subtract",
        )
        expected = list(zip(expected_h_texts, expected_dotsimg_src, [BeautifulSoup(soup, 'html.parser') for soup in expected_soups]))
        self.assertListEqual([a[:2] for a in actual], [e[:2] for e in expected])
        for (_, _, a_soup), (_, _, e_soup) in zip(actual, expected):
            self.assertSoupEqual(a_soup, e_soup)

class HSXBlendingModeTests(BaseSoupTestCase):
    """
    A file so convoluted that it need its own function.
    """

    def setUp(self):
        """
        """

    def test_ALL(self):
        """
        """
        path = "_src-html/reference_manual/blending_modes/hsx.html"
        with open(path, encoding="utf-8") as rfile:
            soup = BeautifulSoup(rfile, 'html.parser')
        subsections = parser.generate_hsx_blendingmode_excerpt(soup)
        logger.debug("h_tag dotsimg_src subsection")
        for h_tag, dotsimg_src, subsection in subsections:
            self.assertIsInstance(h_tag, str)
            self.assertIsInstance(dotsimg_src, str)
            logger.debug("%s %s %s", h_tag, dotsimg_src, type(subsection))
            logger.debug("subsection: %s", subsection)
            self.assertIsNone(subsection.find('figure'))
            if " - " in h_tag:
                header_suffix = h_tag.split(" - ")[1]
                header_text = h_tag.split(" - ")[0].replace(' ', '_')
                self.assertIn(header_text.lower(), dotsimg_src.lower())
                try:
                    self.assertIn(header_suffix.lower(), dotsimg_src.lower())
                except AssertionError:
                    header_suffix = {
                        "HSI": "Intensity",
                        "HSL": "Lightness",
                        "HSV": "Value",
                    }[header_suffix]
                    self.assertIn(header_suffix.lower(), dotsimg_src.lower())
            else:
                header_text = h_tag.replace(' ', '_')
                self.assertIn(header_text.lower(), dotsimg_src.lower())
            #print("Now searching through images.")
            for img in subsection.find_all("img"):
                #print(img)
                self.assertIs(img['src'].endswith("_with_dots.png"), False)

class DockersTests(BaseSoupTestCase):
    """
    """

    def setUp(self):
        """
        """
        self.htmldir = "_src-html/reference_manual/dockers/"
        self.func_to_test = parser.generate_dockers_excerpt
        logger.critical("%s", self.id())

    def test_layers(self):
        """
        """
        path = self.htmldir + "layers.html"
        self._test_one(path)

    def _test_one(self, path):
        """
        """
        h_tag, icon, section = super()._test_one(path)
        logger.debug("%s %s %s", h_tag, icon, type(section))
        self.assertTrue(section)
        self.assertIsNone(section.find('h1'))
        self.assertIsNone(icon)

class FiltersTests(BaseSoupTestCase):
    """
    """

    def setUp(self):
        """
        """
        self.htmldir = "_src-html/reference_manual/filters/"
        self.func_to_test = parser.generate_filters_excerpt
        logger.critical("%s", self.id())

    def test_colors(self):
        """
        """
        path = self.htmldir + "colors.html"
        self._test_one(path)

    def _test_one(self, path):
        """
        """
        h_tag, icon, section = super()._test_one(path)
        logger.debug("%s %s %s", h_tag, icon, type(section))
        self.assertTrue(section)
        self.assertIsNone(section.find('h1'))
        self.assertIsNone(icon)

class BrushEnginesTests(BaseSoupTestCase):
    """
    """

    def setUp(self):
        """
        """
        self.htmldir = "_src-html/reference_manual/brushes/brush_engines/"
        self.func_to_test = parser.generate_brushengines_excerpt
        logger.critical("%s", self.id())

    def _test_one(self, path):
        """
        """
        h_tag, icon, section = super()._test_one(path)
        logger.debug("%s %s %s", h_tag, icon, type(section))
        self.assertTrue(section)
        self.assertIsNone(section.find('h1'))
        logger.debug("icon: %s, %s", icon, type(icon))
        for img in section.find_all('img'):
            rootdir = img['src'].split('/')[1]
            self.assertEqual(rootdir, "images")
        #self.assertIsInstance(icon, str)
        #self.assertIs(icon.endswith(".svg"), True)

class BrushSettingsTests(BaseSoupTestCase):
    """
    """

    def setUp(self):
        """
        """
        self.htmldir = "_src-html/reference_manual/brushes/brush_settings/"
        self.func_to_test = parser.generate_brushsettings_excerpt
        logger.critical("%s", self.id())

    def _test_one(self, path):
        """
        """
        h_tag, icon, section = super()._test_one(path)
        logger.debug("%s %s %s", h_tag, icon, type(section))
        self.assertTrue(section)
        self.assertIsNone(section.find('h1'))
        self.assertIsNone(icon)
        for img in section.find_all('img'):
            rootdir = img['src'].split('/')[1]
            self.assertEqual(rootdir, "images")

class LayersAndMasksTests(BaseSoupTestCase):
    """
    """

    def setUp(self):
        """
        """
        self.htmldir = "_src-html/reference_manual/layers_and_masks/"
        self.func_to_test = parser.generate_layersandmasks_excerpt
        logger.critical("%s", self.id())

    def _test_one(self, path):
        """
        """
        if path.is_dir():
            logger.debug("Path %s is a directory. Nothing to see here.", path)
            return
        h_tag, icon, section = super()._test_one(path)
        logger.debug("%s %s %s", h_tag, icon, type(section))
        self.assertTrue(section)
        self.assertIsNone(section.find('h1'))
        self.assertIsNone(icon)
        for img in section.find_all('img'):
            rootdir = img['src'].split('/')[1]
            self.assertEqual(rootdir, "images")

class MainMenuTests(BaseSoupTestCase):
    """
    """

    def setUp(self):
        """
        """
        self.htmldir = "_src-html/reference_manual/main_menu/"
        self.func_to_test = parser.generate_mainmenu_excerpt
        logger.critical("%s", self.id())

class PreferencesTests(BaseSoupTestCase):
    """
    """

    def setUp(self):
        """
        """
        self.htmldir = "_src-html/reference_manual/preferences/"
        self.func_to_test = parser.generate_preferences_excerpt
        logger.critical("%s", self.id())

class ResourceManagementTests(BaseSoupTestCase):
    """
    """

    def setUp(self):
        """
        """
        self.htmldir = "_src-html/reference_manual/resource_management/"
        self.func_to_test = parser.generate_resourcemanagement_excerpt
        logger.critical("%s", self.id())



if __name__ == "__main__":
    #logging.basicConfig(
        #level=logging.DEBUG,
        #filename=".kritaref_parser.log",
    #)
    unittest.main(
        defaultTest="HSXBlendingModeTests",
    )


