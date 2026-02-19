"""
Tests functionality of index-compiler.
"""

import unittest
from pathlib import Path
import logging

from bs4 import BeautifulSoup

from krita_ref_parser.compile_index import (
    detect_index_files_for_directories,
    get_header,
    get_section_id,
    get_icon,
    get_figures,
)
from krita_ref_parser._logging import logger
from krita_ref_parser.compile_index import (
    ALL_SECTIONS,
    BLENDING_MODE_SECTIONS,
    BLENDING_MODE_HSX_SECTION,
)

SOURCE_DIR = "./tests/output/raw-excerpts/"
TARGET_DIR = "./tests/output/"

for dirname in (SOURCE_DIR, TARGET_DIR):
    Path(dirname).mkdir(parents=True, exist_ok=True)

#@unittest.skip("Reactivate this upon pulling a new Krita-Docs version.")
class SectionDiffAlerter(unittest.TestCase):
    """
    Tests to see if any new sections have emerged since the last git-pull.
    """

    def setUp(self):
        """
        Declares the directory to check.
        """
        self.path = Path("input", "docs-krita-org", "_build", "html", "reference_manual")

    def test_for_section_diff(self):
        """
        Checks to see if the sections have changed.
        """
        expected = set([
            "blending_modes",
            "blending_modes.html",
            "blending_modes/arithmetic.html",
            "blending_modes/binary.html",
            "blending_modes/darken.html",
            "blending_modes/hsx.html",
            "blending_modes/lighten.html",
            "blending_modes/misc.html",
            "blending_modes/mix.html",
            "blending_modes/modulo.html",
            "blending_modes/negative.html",
            "blending_modes/quadratic.html",
            "brushes",
            "brushes.html",
            "brushes/brush_engines",
            "brushes/brush_engines.html",
            "brushes/brush_settings",
            "brushes/brush_settings.html",
            "brushes/brush_engines/bristle_engine.html",
            "brushes/brush_engines/chalk_engine.html",
            "brushes/brush_engines/clone_engine.html",
            "brushes/brush_engines/color_smudge_engine.html",
            "brushes/brush_engines/curve_engine.html",
            "brushes/brush_engines/deform_brush_engine.html",
            "brushes/brush_engines/dyna_brush_engine.html",
            "brushes/brush_engines/filter_brush_engine.html",
            "brushes/brush_engines/grid_brush_engine.html",
            "brushes/brush_engines/hatching_brush_engine.html",
            "brushes/brush_engines/mypaint_engine.html",
            "brushes/brush_engines/particle_brush_engine.html",
            "brushes/brush_engines/pixel_brush_engine.html",
            "brushes/brush_engines/quick_brush_engine.html",
            "brushes/brush_engines/shape_brush_engine.html",
            "brushes/brush_engines/sketch_brush_engine.html",
            "brushes/brush_engines/spray_brush_engine.html",
            "brushes/brush_engines/tangen_normal_brush_engine.html",
            "brushes/brush_settings/brush_tips.html",
            "brushes/brush_settings/locked_brush_settings.html",
            "brushes/brush_settings/masked_brush.html",
            "brushes/brush_settings/opacity_and_flow.html",
            "brushes/brush_settings/options.html",
            "brushes/brush_settings/tablet_sensors.html",
            "brushes/brush_settings/texture.html",
            "dockers",
            "dockers.html",
            "dockers/add_shape.html",
            "dockers/advanced_color_selector.html",
            "dockers/animation_curves.html",
            "dockers/animation_docker.html",
            "dockers/animation_timeline.html",
            "dockers/arrange.html",
            "dockers/artistic_color_selector.html",
            "dockers/brush_preset_docker.html",
            "dockers/brush_preset_history.html",
            "dockers/channels_docker.html",
            "dockers/color_sliders.html",
            "dockers/compositions.html",
            "dockers/digital_color_mixer.html",
            "dockers/gamut_mask_docker.html",
            "dockers/grids_and_guides.html",
            "dockers/histogram_docker.html",
            "dockers/layers.html",
            "dockers/log_viewer.html",
            "dockers/lut_management.html",
            "dockers/onion_skin.html",
            "dockers/overview.html",
            "dockers/palette_docker.html",
            "dockers/pattern_docker.html",
            "dockers/recorder_docker.html",
            "dockers/reference_images_docker.html",
            "dockers/shape_properties_docker.html",
            "dockers/small_color_selector.html",
            "dockers/snapshot_docker.html",
            "dockers/specific_color_selector.html",
            "dockers/storyboard_docker.html",
            "dockers/task_sets.html",
            "dockers/touch_docker.html",
            "dockers/undo_history.html",
            "dockers/vector_library.html",
            "dockers/wide_gamut_color_selector.html",
            "filters",
            "filters.html",
            "filters/adjust.html",
            "filters/artistic.html",
            "filters/blur.html",
            "filters/colors.html",
            "filters/edge_detection.html",
            "filters/emboss.html",
            "filters/enhance.html",
            "filters/map.html",
            "filters/other.html",
            "filters/wavelet_decompose.html",
            "layers_and_masks",
            "layers_and_masks.html",
            "layers_and_masks/fill_layer_generators",
            "layers_and_masks/fill_layer_generators.html",
            "layers_and_masks/fill_layer_generators/gradient.html",
            "layers_and_masks/fill_layer_generators/multigrid.html",
            "layers_and_masks/fill_layer_generators/pattern_fill.html",
            "layers_and_masks/fill_layer_generators/screentone.html",
            "layers_and_masks/fill_layer_generators/seexpr.html",
            "layers_and_masks/fill_layer_generators/simplex_noise.html",
            "layers_and_masks/clone_layers.html",
            "layers_and_masks/file_layers.html",
            "layers_and_masks/fill_layers.html",
            "layers_and_masks/filter_layers.html",
            "layers_and_masks/filter_masks.html",
            "layers_and_masks/group_layers.html",
            "layers_and_masks/layer_styles.html",
            "layers_and_masks/paint_layers.html",
            "layers_and_masks/selection_masks.html",
            "layers_and_masks/split_alpha.html",
            "layers_and_masks/transformation_masks.html",
            "layers_and_masks/transparency_masks.html",
            "layers_and_masks/vector_layers.html",
            "main_menu",
            "main_menu.html",
            "main_menu/edit_menu.html",
            "main_menu/file_menu.html",
            "main_menu/help_menu.html",
            "main_menu/image_menu.html",
            "main_menu/layers_menu.html",
            "main_menu/select_menu.html",
            "main_menu/settings_menu.html",
            "main_menu/tools_menu.html",
            "main_menu/view_menu.html",
            "main_menu/window_menu.html",
            "preferences",
            "preferences.html",
            "preferences/author_settings.html",
            "preferences/canvas_input_settings.html",
            "preferences/canvas_only_mode.html",
            "preferences/color_management_settings.html",
            "preferences/color_selector_settings.html",
            "preferences/display_settings.html",
            "preferences/general_settings.html",
            "preferences/g_mic_settings.html",
            "preferences/performance_settings.html",
            "preferences/popup_palette_settings.html",
            "preferences/python_plugin_manager.html",
            "preferences/shortcut_settings.html",
            "preferences/tablet_settings.html",
            "resource_management",
            "resource_management.html",
            "resource_management/paintoppresets.html",
            "resource_management/resource_brushtips.html",
            "resource_management/resource_gradients.html",
            "resource_management/resource_patterns.html",
            "resource_management/resource_workspace.html",
            "resource_management/seexpr_scripts.html",
            "tools",
            "tools.html",
            "tools/assistant.html",
            "tools/calligraphy.html",
            "tools/colorize_mask.html",
            "tools/color_sampler.html",
            "tools/contiguous_select.html",
            "tools/crop.html",
            "tools/dyna.html",
            "tools/ellipse.html",
            "tools/elliptical_select.html",
            "tools/enclose_and_fill.html",
            "tools/fill.html",
            "tools/freehand_brush.html",
            "tools/freehand_path.html",
            "tools/freehand_select.html",
            "tools/gradient_draw.html",
            "tools/gradient_edit.html",
            "tools/line.html",
            "tools/magnetic_select.html",
            "tools/measure.html",
            "tools/move.html",
            "tools/multibrush.html",
            "tools/pan.html",
            "tools/path.html",
            "tools/path_select.html",
            "tools/pattern_edit.html",
            "tools/polygonal_select.html",
            "tools/polygon.html",
            "tools/polyline.html",
            "tools/rectangle.html",
            "tools/rectangular_select.html",
            "tools/reference_images_tool.html",
            "tools/shape_edit.html",
            "tools/shape_selection.html",
            "tools/similar_select.html",
            "tools/smart_patch.html",
            "tools/text.html",
            "tools/transform.html",
            "tools/zoom.html",
            # 11-17-2025
        ])
        actual = set()
        def to_relative_path(dirpath, filename):
            """
            """
            return dirpath.joinpath(filename).relative_to(self.path)
        def is_index_file(dirpath, filename):
            """
            """
            return dirpath.joinpath(filename).with_suffix("").is_dir()
        for dirpath, dirnames, filenames in self.path.walk():
            if dirpath == self.path:
                for filename in map(
                    lambda filename: to_relative_path(dirpath, filename),
                    filter(
                        lambda filename: is_index_file(dirpath, filename),
                        filenames,
                    )):
                    actual.add(str(to_relative_path(dirpath, filename)))
                    actual.add(str(to_relative_path(dirpath, filename).with_suffix("")))
                continue
            for filename in filenames:
                actual.add(str(to_relative_path(dirpath, filename)))
                if is_index_file(dirpath, filename):
                    actual.add(str(to_relative_path(dirpath, filename).with_suffix("")))
        self.assertSetEqual(actual, expected)

class ExcerptDirectoryTestCase(unittest.TestCase):
    """
    Tests functionality on excerpt directory.
    """

    def setUp(self):
        """
        Creates content directories and complementary index files for each one.
        """
        mock_dir = Path(TARGET_DIR, "TEST-for-excerpts-directory")
        mock_dir.mkdir(exist_ok=False)
        self.mock_dir = mock_dir
        self.subdirectories = (
            "blending_modes",
            "tools",
            "main_menu",
        )
        for dirname in self.subdirectories:
            subdir = self.mock_dir.joinpath(dirname)
            subdir.mkdir(exist_ok=False)
            subdir.with_suffix(".html").write_text("")

    def test_detect_index_files_for_directories__HAS_COMPLEMENTING_INDEX_FILE(self):
        """
        Asserts that directories with index files are logged.
        """
        with self.assertLogs(logger='krita_ref_parser', level='INFO'):
            detect_index_files_for_directories(source_dir=self.mock_dir)

    def test_detect_index_files_for_directories__NO_COMPLEMENTING_INDEX_FILE(self):
        """
        Asserts exceptions are raised for directories without index files.
        """
        self.mock_dir.joinpath(self.subdirectories[0]).with_suffix('.html').unlink()
        with self.assertRaises(FileNotFoundError):
            detect_index_files_for_directories(source_dir=self.mock_dir)

    def tearDown(self):
        """
        Removes content directories and complementary index files.
        """
        for dirpath in filter(lambda path: path.is_dir(), self.mock_dir.iterdir()):
            dirpath.rmdir()
        for filepath in filter(lambda path: path.is_file(), self.mock_dir.iterdir()):
            filepath.unlink()
        self.mock_dir.rmdir()

# SOUP INSPECTION #

class BlendingModesAdditionFileTestCase(unittest.TestCase):
    """
    Tests functionality on index file of newly created 'blending_modes' subsection.
    """

    def setUp(self):
        """
        Initializes sample HTML.
        """
        #subdirectory = "blending_modes/arithmetic/"
        #filename = "addition.html"
        #path_to_test_dir = Path(TARGET_DIR, subdirectory)
        #path_to_test_dir.mkdir(exist_ok=True, parents=True)
        #self.path_to_test_file = path_to_test_dir.joinpath(filename)
        #self.path_to_test_file.write_text("", encoding="utf-8")
        self.soup_as_str = """<section id="addition">
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
"""

    def test_get_header(self):
        """
        Tests 'get_header' on sample HTML.
        """
        expected = "Addition"
        soup = BeautifulSoup(self.soup_as_str, 'html.parser')
        actual = get_header(soup, h_level=2)
        self.assertEqual(actual, expected)

    def test_get_section_id(self):
        """
        Tests 'get_section_id' on sample HTML.
        """
        expected = "#addition"
        soup = BeautifulSoup(self.soup_as_str, 'html.parser')
        actual = get_section_id(soup, h_level=2)
        self.assertEqual(actual, expected)

    @unittest.skip("The first image of each 'blending_modes/*' file is invalid as a hero-image.")
    def test_get_icon(self):
        """
        Tests 'get_icon' on sample HTML.
        """

    def test_get_figures(self):
        """
        Tests 'get_figures' on sample HTML.
        """
        soup = BeautifulSoup(self.soup_as_str, 'html.parser')
        expected = [
            {
                "img": "Blending_modes_Addition_Gray_0.4_and_Gray_0.5_n.png",
                "figcaption": "Left: Normal. Right: Addition."
            },
            {
                "img": "Blending_modes_Addition_Light_blue_and_Orange.png",
                "figcaption": "Left: Normal. Right: Addition."
            },
            {
                "img": "Blending_modes_Addition_Red_plus_gray.png",
                "figcaption": "Left: Normal. Right: Addition.",
            },
            {
                "img": "Blending_modes_Addition_Sample_image_with_dots.png",
                "figcaption": "Left: Normal. Right: Addition."
            },
        ]
        actual = get_figures(soup)
        self.assertListEqual(actual, expected)


class BlendingModesHSXFileTestCase(unittest.TestCase):
    """
    Tests functionality on index file of newly created 'blending_modes/hsx' subsection.
    """

    def setUp(self):
        """
        Initializes sample HTML.
        """
        #subdirectory = "blending_modes/hsx/"
        #filename = "intensity.html"
        #path_to_test_dir = Path(SOURCE_DIR, subdirectory)
        #path_to_test_dir.mkdir(exist_ok=True, parents=True)
        #self.path_to_test_file = path_to_test_dir.joinpath(filename)
        self.soup_as_str = """<section id="intensity">
<span id="bm-intensity"></span><h3>Intensity<a class="headerlink" href="#intensity" title="Link to this heading">¶</a></h3>
<p>Takes the Hue and Saturation of the lower layer and outputs them with the intensity of the upper layer.</p>
<figure class="align-center" id="id19">
<img alt="../../_images/Blending_modes_Intensity_Sample_image_with_dots.png" src="../../_images/Blending_modes_Intensity_Sample_image_with_dots.png"/>
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Intensity</strong>.</span><a class="headerlink" href="#id19" title="Link to this image">¶</a></p>
</figcaption>
</figure>
</section>"""

    def test_get_header(self):
        """
        Tests 'get_header' on sample HTML; note: h_level=3.
        """
        expected = "Intensity"
        soup = BeautifulSoup(self.soup_as_str, 'html.parser')
        actual = get_header(soup, h_level=3)
        self.assertEqual(actual, expected)

    def test_get_header__GET_H2_FAIL(self):
        """
        Tests 'get_header' on sample HTML; note: h_level=2.
        """
        soup = BeautifulSoup(self.soup_as_str, 'html.parser')
        with self.assertRaises(AttributeError):
            get_header(soup, h_level=2)

    @unittest.skip("The first image of each 'blending_modes/*' file is invalid as a hero-image.")
    def test_get_icon(self):
        """
        Tests 'get_icon' on sample HTML.
        """

    def test_get_figures(self):
        """
        Tests 'get_figures' on sample HTML; affirms that figcaption-text distinguishes between generic and non-generic sample images.
        """
        soup = BeautifulSoup(self.soup_as_str, 'html.parser')
        expected = [
            {
                "img": "Blending_modes_Intensity_Sample_image_with_dots.png",
                "figcaption": "Left: Normal. Right: Intensity."
            },
        ]
        actual = get_figures(soup)
        self.assertListEqual(actual, expected)


class HeroImageFileTestCase(unittest.TestCase):
    """
    Tests index-compiler functionality on file with a hero image.
    """

    def setUp(self):
        """
        Initializes sample HTML of mock-file.
        """
        #subdirectory = "tools/"
        #filename = "gradient_draw.html"
        #path_to_test_dir = Path(SOURCE_DIR, subdirectory)
        #path_to_test_dir.mkdir(exist_ok=True)
        #self.path_to_test_file = path_to_test_dir.joinpath(filename)
        self.soup_as_str = """<section id="gradient-tool">
<span id="index-0"></span><span id="id1"></span><h1>Gradient Tool<a class="headerlink" href="#gradient-tool" title="Link to this heading">¶</a></h1>
<p><img alt="toolgradient" src="../../_images/gradient_drawing_tool.svg"/></p>
<p>The Gradient tool is found in the Tools Panel. Left-Click dragging this tool over the active portion of the canvas will draw out the current gradient.  If there is an active selection then, similar to the <a class="reference internal" href="fill.html#fill-tool"><span class="std std-ref">Fill Tool</span></a>, the paint action will be confined to the selection’s borders.</p>
<section id="tool-options">
<h2>Tool Options<a class="headerlink" href="#tool-options" title="Link to this heading">¶</a></h2>
<dl>
<dt>Shape:</dt><dd><dl>
<dt>Linear</dt><dd><p>This will draw a straight gradient.</p>
<figure class="align-default" id="id2">
<img alt="Linear Gradient." src="../../_images/linear.png"/>
<figcaption>
<p><span class="caption-text">Left: <strong>None</strong>. Middle: <strong>Forwards</strong>. Right: <strong>Alternating</strong>.</span><a class="headerlink" href="#id2" title="Link to this image">¶</a></p>
</figcaption>
</figure>
</dd>
<dt>Bilinear</dt><dd><p>This will draw a straight gradient, mirrored along the axis.</p>
<figure class="align-default" id="id3">
<img alt="../../_images/bilinear.png" src="../../_images/bilinear.png"/>
<figcaption>
<p><span class="caption-text">Left: <strong>None</strong>. Middle: <strong>Forwards</strong>. Right: <strong>Alternating</strong>.</span><a class="headerlink" href="#id3" title="Link to this image">¶</a></p>
</figcaption>
</figure>
</dd>
<dt>Radial</dt><dd><p>This will draw the gradient from a center, defined by where you start the stroke.</p>
<figure class="align-default" id="id4">
<img alt="../../_images/radial.png" src="../../_images/radial.png"/>
<figcaption>
<p><span class="caption-text">Left: <strong>None</strong>. Middle: <strong>Forwards</strong>. Right: <strong>Alternating</strong>.</span><a class="headerlink" href="#id4" title="Link to this image">¶</a></p>
</figcaption>
</figure>
</dd>
<dt>Square</dt><dd><p>This will draw the gradient from a center in a square shape, defined by where you start the stroke.</p>
<figure class="align-default" id="id5">
<img alt="../../_images/square.png" src="../../_images/square.png"/>
<figcaption>
<p><span class="caption-text">Left: <strong>None</strong>. Middle: <strong>Forwards</strong>. Right: <strong>Alternating</strong>.</span><a class="headerlink" href="#id5" title="Link to this image">¶</a></p>
</figcaption>
</figure>
</dd>
<dt>Conical</dt><dd><p>This will wrap the gradient around a center, defined by where you start the stroke.</p>
<figure class="align-default" id="id6">
<img alt="../../_images/conical.png" src="../../_images/conical.png"/>
<figcaption>
<p><span class="caption-text">Left: <strong>None</strong>. Middle: <strong>Forwards</strong>. Right: <strong>Alternating</strong>.</span><a class="headerlink" href="#id6" title="Link to this image">¶</a></p>
</figcaption>
</figure>
</dd>
<dt>Conical-symmetric</dt><dd><p>This will wrap the gradient around a center, defined by where you start the stroke, but will mirror the wrap once.</p>
<figure class="align-default" id="id7">
<img alt="../../_images/conical_symmetric.png" src="../../_images/conical_symmetric.png"/>
<figcaption>
<p><span class="caption-text">Left: <strong>None</strong>. Middle: <strong>Forwards</strong>. Right: <strong>Alternating</strong>.</span><a class="headerlink" href="#id7" title="Link to this image">¶</a></p>
</figcaption>
</figure>
</dd>
<dt>Spiral</dt><dd><p>This will draw the gradient spiral from a center, defined by where you start the stroke.</p>
<figure class="align-default" id="id8">
<img alt="../../_images/spiral.png" src="../../_images/spiral.png"/>
<figcaption>
<p><span class="caption-text">Left: <strong>None</strong>. Middle: <strong>Forwards</strong>. Right: <strong>Alternating</strong>.</span><a class="headerlink" href="#id8" title="Link to this image">¶</a></p>
</figcaption>
</figure>
</dd>
<dt>Reverse Spiral</dt><dd><p>This will draw the gradient spiral from a center, defined by where you start the stroke, but direction is flipped perpendicular to the direction of stroke.</p>
<figure class="align-default" id="id9">
<img alt="../../_images/reverse_spiral.png" src="../../_images/reverse_spiral.png"/>
<figcaption>
<p><span class="caption-text">Left: <strong>None</strong>. Middle: <strong>Forwards</strong>. Right: <strong>Alternating</strong>.</span><a class="headerlink" href="#id9" title="Link to this image">¶</a></p>
</figcaption>
</figure>
</dd>
<dt>Shaped</dt><dd><p>This will shape the gradient depending on the selection or layer.</p>
<figure class="align-default">
<img alt="../../_images/shaped.png" src="../../_images/shaped.png"/>
</figure>
</dd>
</dl>
</dd>
<dt>Repeat:</dt><dd><dl class="simple">
<dt>None</dt><dd><p>This will extend the gradient into infinity.</p>
</dd>
<dt>Forward</dt><dd><p>This will repeat the gradient into one direction.</p>
</dd>
<dt>Alternating</dt><dd><p>This will repeat the gradient, alternating the normal direction and the reversed.</p>
</dd>
</dl>
</dd>
<dt>Antialias threshold</dt><dd><p>Controls how smooth is the border between repetitions.</p>
<ul class="simple">
<li><p>A value equal to 0 means there is no smoothing. The border is aliased.</p></li>
<li><p>A value greater than 0 tells Krita how many pixels to each side of the border should be smoothed.</p></li>
</ul>
<figure class="align-default" id="id10">
<img alt="../../_images/antialias_threshold.png" src="../../_images/antialias_threshold.png"/>
<figcaption>
<p><span class="caption-text">Left: <strong>0</strong>. Middle: <strong>0.5</strong>. Right: <strong>1</strong>.</span><a class="headerlink" href="#id10" title="Link to this image">¶</a></p>
</figcaption>
</figure>
</dd>
<dt>Reverse</dt><dd><p>Reverses the direction of the gradient.</p>
</dd>
<dt>Dither</dt><dd><div class="versionadded">
<p><span class="versionmodified added">Added in version 5.0.</span></p>
</div>
<p>8 bits of color depth is not enough depth to make a truly smooth gradient. This option alleviates this by adding blue noise style dithering to gradients in 8 bit.</p>
<figure class="align-default" id="id11">
<img alt="Example showing gradients with and without dithering." src="../../_images/krita_gradient_dithering.svg"/>
<figcaption>
<p><span class="caption-text">In the above example, the topleft is a subtle gradient without dithering. The bottom left is with blue noise dithering. The right two examples are the same as the left, but with a contrast filter applied so the blue noise dithering pattern becomes obvious.</span><a class="headerlink" href="#id11" title="Link to this image">¶</a></p>
</figcaption>
</figure>
</dd>
</dl>
</section>
</section>"""

    def test_get_icon(self):
        """
        Tests 'get_icon' on sample HTML; affirms SVG suffix.
        """
        expected = "gradient_drawing_tool.svg"
        soup = BeautifulSoup(self.soup_as_str, 'html.parser')
        actual = get_icon(soup)
        self.assertEqual(actual, expected)

    def test_get_header(self):
        """
        Tests 'get_header' on sample HTML; note: h_level=1.
        """
        expected = "Gradient Tool"
        soup = BeautifulSoup(self.soup_as_str, 'html.parser')
        actual = get_header(soup, h_level=1)
        self.assertEqual(actual, expected)

    def test_get_figures(self):
        """
        Tests 'get_figures' on sample HTML and affirms that figcaption-text distinguishes between generic and non-generic images.
        """
        soup = BeautifulSoup(self.soup_as_str, 'html.parser')
        expected = [
            {
                "img": "linear.png",
                "figcaption": "Left: None. Middle: Forwards. Right: Alternating.",
            },
            {
                "img": "bilinear.png",
                "figcaption": "Left: None. Middle: Forwards. Right: Alternating.",
            },
            {
                "img": "radial.png",
                "figcaption": "Left: None. Middle: Forwards. Right: Alternating.",
            },
            {
                "img": "square.png",
                "figcaption": "Left: None. Middle: Forwards. Right: Alternating.",
            },
            {
                "img": "conical.png",
                "figcaption": "Left: None. Middle: Forwards. Right: Alternating.",
            },
            {
                "img": "conical_symmetric.png",
                "figcaption": "Left: None. Middle: Forwards. Right: Alternating.",
            },
            {
                "img": "spiral.png",
                "figcaption": "Left: None. Middle: Forwards. Right: Alternating.",
            },
            {
                "img": "reverse_spiral.png",
                "figcaption": "Left: None. Middle: Forwards. Right: Alternating.",
            },
            {
                "img": "shaped.png",
                "figcaption": None,
            },
            {
                "img": "antialias_threshold.png",
                "figcaption": "Left: 0. Middle: 0.5. Right: 1.",
            },
            {
                "img": "krita_gradient_dithering.svg",
                "figcaption": "In the above example, the topleft is a subtle gradient without dithering. The bottom left is with blue noise dithering. The right two examples are the same as the left, but with a contrast filter applied so the blue noise dithering pattern becomes obvious.",
            },
        ]
        actual = get_figures(soup)
        self.assertListEqual(actual, expected)

class NoHeroImageFileTestCase(unittest.TestCase):
    """
    Tests index-compiler functionality on file without any hero image candidates.
    """

    def setUp(self):
        """
        Initializes sample HTML of mock-file.
        """
        #subdirectory = "layers_and_masks/"
        #filename = "clone_layers.html"
        #path_to_test_dir = Path(SOURCE_DIR, subdirectory)
        #path_to_test_dir.mkdir(exist_ok=True)
        #self.path_to_test_file = path_to_test_dir.joinpath(filename)
        #path_to_og_file = Path(*SOURCE_DIR.split("/")[2:] + [subdirectory, filename])
        self.soup_as_str = """<section id="clone-layers">
<span id="index-0"></span><span id="id1"></span><h1>Clone Layers<a class="headerlink" href="#clone-layers" title="Link to this heading">¶</a></h1>
<p>A clone layer is a layer that keeps an up-to-date copy of another layer. You cannot draw or paint on it directly, but it can be used to create effects by applying different types of layers and masks (e.g. filter layers or masks).</p>
<section id="example-uses-of-clone-layers">
<h2>Example uses of Clone Layers<a class="headerlink" href="#example-uses-of-clone-layers" title="Link to this heading">¶</a></h2>
<p>For example, if you were painting a picture of some magic person and wanted to create a glow around them that was updated as you updated your character, you could:</p>
<ol class="arabic simple">
<li><p>Have a Paint Layer where you draw your character</p></li>
<li><p>Use the Clone Layer feature to create a clone of the layer that you drew your character on</p></li>
<li><p>Apply an HSV filter mask to the clone layer to make the shapes on it white (or blue, or green etc.)</p></li>
<li><p>Apply a blur filter mask to the clone layer so it looks like a “glow”.</p></li>
</ol>
<p>As you keep painting and adding details, erasing on the first layer, Krita will automatically update the clone layer, making your “glow” apply to every change you make.</p>
</section>
<section id="changing-the-source-of-clone-layers">
<h2>Changing the source of Clone Layers<a class="headerlink" href="#changing-the-source-of-clone-layers" title="Link to this heading">¶</a></h2>
<p>You can change the source of one or more Clone Layers in the Layers Docker. To do so, select one or more Clone Layers in the docker (hold <kbd class="kbd docutils literal notranslate">Ctrl</kbd> or <kbd class="kbd docutils literal notranslate">Shift</kbd> and left-click the layers). Then, right-click on any selected layer. In the context menu, there is an action named <span class="guilabel">Set Copy From</span>. Click it. A dialog will pop up and there is a drop-down menu with all possible layers to be set as the source of all selected Clone Layers. If the current source of them consists of multiple layers, the default activated selection in the drop-down menu will be blank. Otherwise, it would be the common source of selected Clone Layers.</p>
<p>Possible target layers are determined through the following criteria:</p>
<ol class="arabic simple">
<li><p>Any Clone Layer that is selected is invalid.</p></li>
<li><p>A parent or clone of any invalid layer is invalid.</p></li>
<li><p>All other layers are valid.</p></li>
</ol>
<p>If you select one layer in the drop-down menu, a preview of the canvas will be shown. Click <span class="guilabel">OK</span> to apply the changes. Click <span class="guilabel">Cancel</span> to discard the changes. If you make changes to the image outside the dialog, the changes will be applied and the dialog will be automatically closed.</p>
</section>
</section>"""

    def test_get_header(self):
        """
        Tests 'get_header' on sample HTML.
        """
        expected = "Clone Layers"
        soup = BeautifulSoup(self.soup_as_str, 'html.parser')
        actual = get_header(soup, h_level=1)
        self.assertEqual(actual, expected)

    def test_get_icon(self):
        """
        Tests 'get_icon' on sample HTML; asserts that the return-value is None.
        """
        soup = BeautifulSoup(self.soup_as_str, 'html.parser')
        actual = get_icon(soup)
        self.assertIsNone(actual)

@unittest.skip("Inheriting from BlendingModesAdditionFileTestCase because the cases are identical.")
class FigureFileTestCase(BlendingModesAdditionFileTestCase):
    """
    Tests figure-compilation functionality on a file that has figures.
    """

    def setUp(self):
        """
        Reinitializes another test-case.
        """
        logger.debug("FigureFileTestCase: Inheriting from BlendingModesAdditionFileTestCase because the cases are identical.")
        super().setUp()

class NoFigureFileTestCase(unittest.TestCase):
    """
    Tests figure-compilation functionality on a file that lacks figures.
    """

    def setUp(self):
        """
        Initializes sample HTML.
        """
        #subdirectory = "layers_and_masks/"
        #filename = "filter_masks.html"
        #path_to_test_dir = Path(SOURCE_DIR, subdirectory)
        #path_to_test_dir.mkdir(exist_ok=True, parents=True)
        #self.path_to_test_file = path_to_test_dir.joinpath(filename)
        self.soup_as_str = """<section id="filter-masks">
<span id="index-0"></span><span id="id1"></span><h1>Filter Masks<a class="headerlink" href="#filter-masks" title="Link to this heading">¶</a></h1>
<p>Filter masks show an area of their layer with a filter (such as blur, levels, brightness / contrast etc.). For example, if you select an area of a paint layer and add a Filter Mask, you will be asked to choose a filter. If you choose the blur filter, you will see the area you selected blurred.</p>
<a class="reference internal image-reference" href="../../_images/Krita_ghostlady_2.png"><img alt="../../_images/Krita_ghostlady_2.png" class="align-center" src="../../_images/Krita_ghostlady_2.png" style="width: 800px;"/>
</a>
<p>With filter masks, we can for example make this ghost-lady more ethereal by putting a clone layer underneath, and setting a lens-blur filter on it.</p>
<a class="reference internal image-reference" href="../../_images/Krita_ghostlady_3.png"><img alt="../../_images/Krita_ghostlady_3.png" class="align-center" src="../../_images/Krita_ghostlady_3.png" style="width: 800px;"/>
</a>
<p>Set the blending mode of the clone layer to <span class="guilabel">Color Dodge</span> and she becomes really spooky!</p>
<p>Unlike applying a filter to a section of a paint layer directly, filter masks do not permanently alter the original image. This means you can tweak the filter (or the area it applies to) at any time. Changes can always be altered or removed.</p>
<p>Unlike filter layers, filter masks apply only to the area you have selected (the mask).</p>
<p>You can edit the settings for a filter mask at any time by double clicking on it in the Layers docker. You can also change the selection that the filter mask affects by selecting the filter mask in the Layers docker and then using the paint tools in the main window. Painting white includes the area, painting black excludes it, and all other colors are turned into a shade of gray which applies proportionally.</p>
</section>"""

    def test_get_header(self):
        """
        Tests 'get_header' on sample HTML.
        """
        expected = "Filter Masks"
        soup = BeautifulSoup(self.soup_as_str, 'html.parser')
        actual = get_header(soup, h_level=1)
        self.assertEqual(actual, expected)

    def test_get_figures(self):
        """
        Tests 'get_figures' on sample HTML and asserts the return-value to be None.
        """
        soup = BeautifulSoup(self.soup_as_str, 'html.parser')
        actual = get_figures(soup)
        self.assertIsNone(actual)

