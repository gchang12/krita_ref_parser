"""
Tests parsing and writing functionality of `split_docs`
"""

import unittest
from unittest.mock import patch
from pathlib import Path

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

class GeneralTestCase(unittest.TestCase):
    """
    Tests functionality of module without a file.
    """

    def setUp(self):
        """
        Sets up path to test file.
        """
        self.path_to_test_file = "/".join([SOURCE_DIR, "_DUMMY"])

    def test_write_stripped_soup(self):
        """
        Asserts that an Exception is raised and nothing's been written if `soup` is None.
        """
        soup = None
        filename = self.path_to_test_file
        with self.assertRaises(Exception):
            write_stripped_soup(soup, filename)
        expected = False
        actual = Path(filename).exists()
        self.assertIs(actual, expected)

    def tearDown(self):
        """
        Deletes dummy file in case it was created.
        """
        Path(self.path_to_test_file).unlink(missing_ok=True)

class AssistantToolTestCase(unittest.TestCase):
    """
    Inspects functionality when targeted at 'tools/assistant' module.
    """

    def setUp(self):
        """
        Defines path to test file, a copy of which is initialized.
        """
        subdirectory = "tools/"
        filename = "assistant.html"
        path_to_test_dir = Path(SOURCE_DIR, subdirectory)
        path_to_test_dir.mkdir(exist_ok=True)
        self.path_to_test_file = path_to_test_dir.joinpath(filename)
        test_file_contents = '''<!DOCTYPE html>
<!--[if IE 8]><html class="no-js lt-ie9" lang="en" > <![endif]-->
<!--[if gt IE 8]><!--> <html class="no-js" lang="en" > <!--<![endif]-->
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta property="og:title" name="title" content="Assistant Tool" />
  <meta property="og:site-name" content="Krita Manual" />
  <meta property="og:type" content="article" />
  <meta property="og:locale" content="en" />
  <meta property="og:locale:alternate" content="ca" />
  <meta property="og:locale:alternate" content="fr" />
  <meta property="og:locale:alternate" content="it" />
  <meta property="og:locale:alternate" content="ja" />
  <meta property="og:locale:alternate" content="ko" />
  <meta property="og:locale:alternate" content="nl" />
  <meta property="og:locale:alternate" content="pl" />
  <meta property="og:locale:alternate" content="pt_PT" />
  <meta property="og:locale:alternate" content="pt_BR" />
  <meta property="og:locale:alternate" content="sl" />
  <meta property="og:locale:alternate" content="tr" />
  <meta property="og:locale:alternate" content="uk_UA" />
  <meta property="og:locale:alternate" content="zh_CN" />
  <meta property="og:article:modified_time" content="2025-11-17T09:18:56" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
<meta content="Krita's assistant tool reference." name="description" property="og:description" />
  <title>Assistant Tool &mdash; Krita Manual 5.2.0 documentation</title>
    <link rel="shortcut icon" href="../../../../_static/favicon.ico"/>
    <link rel="canonical" href="en/reference_manual/tools/assistant.html"/>
    <meta property="og:url" content="en/reference_manual/tools/assistant.html" />
    <meta property="og:image" content="en/../../_static/sidebar-logo.png" />
    <link rel="stylesheet" href="../../_static/css/theme.css" type="text/css" />
    <link rel="stylesheet" href="../../_static/pygments.css" type="text/css" />
    <link rel="stylesheet" href="../../_static/pygments.css" type="text/css" />
    <link rel="stylesheet" href="../../_static/css/theme.css" type="text/css" />
    <link rel="index" title="Index" href="../../genindex.html" />
    <link rel="search" title="Search" href="../../search.html" />
    <link rel="next" title="Reference Images Tool" href="reference_images_tool.html" />
    <link rel="prev" title="Smart Patch Tool" href="smart_patch.html" /> 
  <!-- theme and selectors rely on jquery still. currently v3.7.1. Eventually try to migrate off these libraries -->
  <script type="text/javascript" src="../../_static/js/jquery.min.js"></script> 
  <!-- search uses underscore.js to help do some filtering and parsing -->
  <script type="text/javascript" src="../../_static/js/underscore.min.js"></script> 
  <script>
    var $u = _; // Now we can use $u instead of _ throughout your code. (which searchtools.js uses)
  </script>
  <script src="../../_static/js/modernizr.min.js"></script>
</head>
<body class="wy-body-for-nav">
  <div class="wy-grid-for-nav">
    <nav data-toggle="wy-nav-shift" class="wy-nav-side">
      <div class="wy-side-scroll">
        <div class="wy-side-nav-search">
           <a href="../../index.html" class="icon icon-home">
			<img src="../../../../_static/sidebar-logo.png" class="logo" alt="Logo"/>
           	
           <!--	Krita Manual -->
          </a>
<div role="search">
  <form id="rtd-search-form" class="wy-form" action="../../search.html" method="get">
    <input type="text" name="q" placeholder="Search docs" />
    <input type="hidden" name="check_keywords" value="yes" />
    <input type="hidden" name="area" value="default" />
  </form>
</div>
        </div>
        <div class="wy-side-nav-language-selector">
        	<p class="caption-text">
	        	<select id="language-selector-container">
	        		<option value="ca">Català</option>
	        		<option value="en">English</option>
	        		<option value="fr">français</option>
	        		<option value="it">Italiano</option>
	        		<option value="ja">日本語</option>
	        		<option value="ko">한국어</option>
	        		<option value="nl">Nederlands</option>
	        		<option value="pl">Polski</option>
	        		<option value="pt_PT">português</option>
	        		<option value="pt_BR">português brasileiro</option>
                    <option value="sl">slovenščina</option>
                    <option value="tr">Türkçe</option>
	        		<option value="uk_UA">Українська</option>
	        		<option value="zh_CN">简体中文</option>
	        	</select>
        	</p>
        </div>
        <div class="wy-menu wy-menu-vertical" data-spy="affix" role="navigation" aria-label="main navigation">
              <ul class="current">
<li class="toctree-l1"><a class="reference internal" href="../../user_manual.html">User Manual</a></li>
<li class="toctree-l1"><a class="reference internal" href="../../general_concepts.html">General Concepts</a></li>
<li class="toctree-l1 current"><a class="reference internal" href="../../reference_manual.html">Reference Manual</a><ul class="current">
<li class="toctree-l2"><a class="reference internal" href="../audio_for_animation.html">Audio for Animation</a></li>
<li class="toctree-l2"><a class="reference internal" href="../blending_modes.html">Blending Modes</a></li>
<li class="toctree-l2"><a class="reference internal" href="../brushes.html">Brushes</a></li>
<li class="toctree-l2"><a class="reference internal" href="../clones_array.html">Clones Array</a></li>
<li class="toctree-l2"><a class="reference internal" href="../create_new_document.html">Create New Document</a></li>
<li class="toctree-l2"><a class="reference internal" href="../default_python_plugins.html">Pre-installed Python plugins</a></li>
<li class="toctree-l2"><a class="reference internal" href="../dockers.html">Dockers</a></li>
<li class="toctree-l2"><a class="reference internal" href="../dr_minw_debugger.html">Dr. MinGW Debugger</a></li>
<li class="toctree-l2"><a class="reference internal" href="../filters.html">Filters</a></li>
<li class="toctree-l2"><a class="reference internal" href="../hdr_display.html">HDR Display</a></li>
<li class="toctree-l2"><a class="reference internal" href="../image_split.html">Image Split</a></li>
<li class="toctree-l2"><a class="reference internal" href="../import_animation.html">Import Animation</a></li>
<li class="toctree-l2"><a class="reference internal" href="../instant_preview.html">Instant Preview</a></li>
<li class="toctree-l2"><a class="reference internal" href="../krita_4_preset_bundle.html">Krita 4 Preset Bundle Overview</a></li>
<li class="toctree-l2"><a class="reference internal" href="../layers_and_masks.html">Layers and Masks</a></li>
<li class="toctree-l2"><a class="reference internal" href="../linux_command_line.html">Linux Command Line</a></li>
<li class="toctree-l2"><a class="reference internal" href="../main_menu.html">Main Menu</a></li>
<li class="toctree-l2"><a class="reference internal" href="../maths_input.html">Maths Input</a></li>
<li class="toctree-l2"><a class="reference internal" href="../popup-palette.html">Pop-up Palette</a></li>
<li class="toctree-l2"><a class="reference internal" href="../preferences.html">Preferences</a></li>
<li class="toctree-l2"><a class="reference internal" href="../render_animation.html">Render Animation</a></li>
<li class="toctree-l2"><a class="reference internal" href="../resource_management.html">Resource Management</a></li>
<li class="toctree-l2"><a class="reference internal" href="../seexpr.html">SeExpr Quick Reference</a></li>
<li class="toctree-l2"><a class="reference internal" href="../separate_image.html">Separate Image</a></li>
<li class="toctree-l2"><a class="reference internal" href="../sharing_krita_logs.html">Getting Krita logs</a></li>
<li class="toctree-l2"><a class="reference internal" href="../split_layer.html">Split Layer</a></li>
<li class="toctree-l2"><a class="reference internal" href="../storyboard_svg_template.html">SVG Storyboard Export Templates</a></li>
<li class="toctree-l2"><a class="reference internal" href="../stroke_selection.html">Stroke Selection</a></li>
<li class="toctree-l2 current"><a class="reference internal" href="../tools.html">Tools</a><ul class="current">
<li class="toctree-l3"><a class="reference internal" href="shape_selection.html">Shape Selection Tool</a></li>
<li class="toctree-l3"><a class="reference internal" href="shape_edit.html">Shape Edit Tool</a></li>
<li class="toctree-l3"><a class="reference internal" href="text.html">Text Tool</a></li>
<li class="toctree-l3"><a class="reference internal" href="gradient_edit.html">Gradient Editing Tool</a></li>
<li class="toctree-l3"><a class="reference internal" href="pattern_edit.html">Pattern Editing Tool</a></li>
<li class="toctree-l3"><a class="reference internal" href="calligraphy.html">Calligraphy Tool</a></li>
<li class="toctree-l3"><a class="reference internal" href="freehand_brush.html">Freehand Brush Tool</a></li>
<li class="toctree-l3"><a class="reference internal" href="line.html">Straight Line Tool</a></li>
<li class="toctree-l3"><a class="reference internal" href="rectangle.html">Rectangle Tool</a></li>
<li class="toctree-l3"><a class="reference internal" href="ellipse.html">Ellipse Tool</a></li>
<li class="toctree-l3"><a class="reference internal" href="polygon.html">Polygon Tool</a></li>
<li class="toctree-l3"><a class="reference internal" href="polyline.html">Polyline Tool</a></li>
<li class="toctree-l3"><a class="reference internal" href="path.html">Bezier Curve Tool</a></li>
<li class="toctree-l3"><a class="reference internal" href="freehand_path.html">Freehand Path Tool</a></li>
<li class="toctree-l3"><a class="reference internal" href="dyna.html">Dynamic Brush Tool</a></li>
<li class="toctree-l3"><a class="reference internal" href="multibrush.html">Multibrush Tool</a></li>
<li class="toctree-l3"><a class="reference internal" href="crop.html">Crop Tool</a></li>
<li class="toctree-l3"><a class="reference internal" href="move.html">Move Tool</a></li>
<li class="toctree-l3"><a class="reference internal" href="transform.html">Transform Tool</a></li>
<li class="toctree-l3"><a class="reference internal" href="fill.html">Fill Tool</a></li>
<li class="toctree-l3"><a class="reference internal" href="enclose_and_fill.html">Enclose and Fill Tool</a></li>
<li class="toctree-l3"><a class="reference internal" href="gradient_draw.html">Gradient Tool</a></li>
<li class="toctree-l3"><a class="reference internal" href="color_sampler.html">Color Sampler Tool</a></li>
<li class="toctree-l3"><a class="reference internal" href="colorize_mask.html">Colorize Mask</a></li>
<li class="toctree-l3"><a class="reference internal" href="smart_patch.html">Smart Patch Tool</a></li>
<li class="toctree-l3 current"><a class="current reference internal" href="#">Assistant Tool</a><ul>
<li class="toctree-l4"><a class="reference internal" href="#tool-options">Tool Options</a></li>
</ul>
</li>
<li class="toctree-l3"><a class="reference internal" href="reference_images_tool.html">Reference Images Tool</a></li>
<li class="toctree-l3"><a class="reference internal" href="measure.html">Measure Tool</a></li>
<li class="toctree-l3"><a class="reference internal" href="rectangular_select.html">Rectangular Selection Tool</a></li>
<li class="toctree-l3"><a class="reference internal" href="elliptical_select.html">Elliptical Selection Tool</a></li>
<li class="toctree-l3"><a class="reference internal" href="freehand_select.html">Freehand Selection Tool</a></li>
<li class="toctree-l3"><a class="reference internal" href="polygonal_select.html">Polygonal Selection Tool</a></li>
<li class="toctree-l3"><a class="reference internal" href="contiguous_select.html">Contiguous Selection Tool</a></li>
<li class="toctree-l3"><a class="reference internal" href="path_select.html">Path Selection Tool</a></li>
<li class="toctree-l3"><a class="reference internal" href="similar_select.html">Similar Color Selection Tool</a></li>
<li class="toctree-l3"><a class="reference internal" href="magnetic_select.html">Magnetic Selection Tool</a></li>
<li class="toctree-l3"><a class="reference internal" href="zoom.html">Zoom Tool</a></li>
<li class="toctree-l3"><a class="reference internal" href="pan.html">Pan Tool</a></li>
</ul>
</li>
<li class="toctree-l2"><a class="reference internal" href="../welcome_screen.html">Welcome Screen</a></li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="../../tutorials.html">Tutorials and How-tos</a></li>
<li class="toctree-l1"><a class="reference internal" href="../../KritaFAQ.html">Krita FAQ</a></li>
<li class="toctree-l1"><a class="reference internal" href="../../contributors_manual.html">Contributors Manual</a></li>
<li class="toctree-l1"><a class="reference internal" href="../../resources_page.html">Resources</a></li>
</ul>
        </div>
      </div>
    </nav>
    <section data-toggle="wy-nav-shift" class="wy-nav-content-wrap">
	<!-- start top banner area (for fundraisers or messages)
	<div style="text-align: center; background-color: #333">
		<a href="https://krita.org/en/fundraising-2018-campaign/" target="_self" onclick="ga('send', 'event', 'frontpage', 'button', 'Fundraiser 2018');">
			<img src="https://krita.org/wp-content/themes/krita-org-theme/images/decoration/2018-fundraiser-banner.png" style="max-width: 100%">
		</a>
	</div>
	
	 end top banner area -->
      <nav class="wy-nav-top" aria-label="top navigation">
          <i data-toggle="wy-nav-top" class="fa fa-bars"></i>
          <a href="../../index.html">Krita Manual</a>
      </nav>
      <div class="wy-nav-content">
        <div class="rst-content">
<div role="navigation" aria-label="breadcrumbs navigation">
  <ul class="wy-breadcrumbs">
      <li><a href="../../index.html">Docs</a> &raquo;</li>
          <li><a href="../../reference_manual.html">Reference Manual</a> &raquo;</li>
          <li><a href="../tools.html">Tools</a> &raquo;</li>
      <li>Assistant Tool</li>
      <li class="wy-breadcrumbs-aside">
            <a href="../../_sources/reference_manual/tools/assistant.rst.txt" rel="nofollow"> 
              <img src="../../_static/images/source-code.png" />
             <!-- View page source -->
          </a>
      </li>
  </ul>
</div>
          <div role="main" class="document" itemscope="itemscope" itemtype="http://schema.org/Article">
           <div itemprop="articleBody">
  <section id="assistant-tool">
<span id="index-0"></span><span id="id1"></span><h1>Assistant Tool<a class="headerlink" href="#assistant-tool" title="Link to this heading">¶</a></h1>
<p><img alt="toolassistant" src="../../_images/assistant_tool.svg" /></p>
<p>Create, edit, and remove drawing assistants on the canvas. There are a number of different assistants that can be used from this tool. The tool options allow you to add new assistants, and to save/load assistants. To add a new assistant, select a type from the tool options and begin clicking on the canvas. Each assistant is created a bit differently. There are also additional controls on existing assistants that allow you to move and delete them.</p>
<p>The set of assistants on the current canvas can be saved to a “*.paintingassistant” file using the <span class="guilabel">Save</span> button in the tool options. These assistants can then be loaded onto a different canvas using the Open button. This functionality is also useful for creating copies of the same drawing assistant(s) on the current canvas.</p>
<p>Check <a class="reference internal" href="../../user_manual/painting_with_assistants.html#painting-with-assistants"><span class="std std-ref">Painting with Assistants</span></a> for more information.</p>
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
<img alt="../../_images/Assistants_2_pointperspective_03.png" src="../../_images/Assistants_2_pointperspective_03.png" />
<figcaption>
<p><span class="caption-text">In the above image, two extra vanishing points have been added to a 2 point assistant, limiting the area in which the grid is drawn and the brush will snap.</span><a class="headerlink" href="#id2" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<p>This option adds two extra handles to every assistant, for drawing a rectangle which will limit the assistant. This is very useful for comic pages, which may need multiple assistants per page, and will otherwise become very crowded.</p>
</div></blockquote>
</section>
</section>
           </div>
          </div>
          <footer>
    <div class="rst-footer-buttons" role="navigation" aria-label="footer navigation">
        <a href="reference_images_tool.html" class="btn btn-neutral float-right" title="Reference Images Tool" accesskey="n" rel="next"> <!-- Next --> <span class="fa fa-arrow-circle-right"></span></a>
        <a href="smart_patch.html" class="btn btn-neutral" title="Smart Patch Tool" accesskey="p" rel="prev"><span class="fa fa-arrow-circle-left"></span> <!-- Previous  -->  </a>
    </div>
  <hr/>
  <div role="contentinfo">
    <p>
        &copy; Copyright licensed under the GNU Free Documentation License 1.3+ unless stated otherwise.
        <span class="commit">
          Revision <code>v5.2.0-106-g27972506c8</code>.
        </span>
    </p>
  </div>
  Built with <a href="http://sphinx-doc.org/">Sphinx</a> using a modified <a href="https://github.com/rtfd/sphinx_rtd_theme">RTD theme</a>.<br/>
  <a href="https://krita.org" title="Krita official website.">Krita official website</a> |
  <a href="https://invent.kde.org/documentation/docs-krita-org/" title="The Gitlab instance to edit this pages and collaborate.">Git repository for docs.krita.org </a> |
  <a href="https://www.kde.org/community/whatiskde/impressum-en.php" title="To know more about KDE, code of conduct, privacy policy and GDPR.">KDE Impressum</a>.
</footer>
        </div>
      </div>
    </section>
  </div>
      <script src="../../_static/documentation_options.js?v=2dde5210"></script>
      <script src="../../_static/doctools.js?v=9bcbadda"></script>
      <script src="../../_static/sphinx_highlight.js?v=dc90522c"></script>
    <script type="text/javascript" src="../../_static/js/theme.js"></script>
  <script type="text/javascript">
    document.addEventListener("DOMContentLoaded", function() {
          SphinxRtdTheme.Navigation.enableSticky();
    });
  </script> 
 <script type="text/javascript">
	 var _paq=_paq||[];
	 _paq.push(['setCookieDomain','*.krita.org']);
	 _paq.push(['setDomains','*.krita.org']);
	 _paq.push(['setDocumentTitle',document.domain+"/"+document.title]);
	 _paq.push(['trackPageView']);
	 _paq.push(['enableLinkTracking']);
	 (function(){
	 	var u="//stats.kde.org/";
	    _paq.push(['setTrackerUrl',u+'piwik.php']);
	    _paq.push(['setSiteId',13]);
	    var d = document, g = d.createElement('script'),s=d.getElementsByTagName('script')[0];
	    g.type = 'text/javascript';
	    g.async = true;
	    g.defer = true;
	    g.src = u+'piwik.js';
	    s.parentNode.insertBefore(g,s);
	  })();
</script> 
<noscript><p><img src="//stats.kde.org/piwik.php?idsite=13" style="border:0;" alt="" /></p></noscript>
</body>
</html>'''
        self.path_to_test_file.write_text(test_file_contents, encoding="utf-8")

    def test_split_from_page(self):
        """
        Tests functionality to extract a <section> from a page.
        """
        soup = bs4.BeautifulSoup(self.path_to_test_file.read_text(encoding="utf-8"), 'html.parser')
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
    Inspects functionality when targeted at 'blending_modes/arithmetic' index module.
    """

    def setUp(self):
        """
        Defines path to test file and creates it.
        """
        subdirectory = "blending_modes/"
        filename = "arithmetic.html"
        self.number_of_subsections = 5
        path_to_test_dir = Path(SOURCE_DIR, subdirectory)
        path_to_test_dir.mkdir(exist_ok=True)
        self.path_to_test_file = path_to_test_dir.joinpath(filename)
        test_file_contents = '''<!DOCTYPE html>
<!--[if IE 8]><html class="no-js lt-ie9" lang="en" > <![endif]-->
<!--[if gt IE 8]><!--> <html class="no-js" lang="en" > <!--<![endif]-->
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta property="og:title" name="title" content="Arithmetic" />
  <meta property="og:site-name" content="Krita Manual" />
  <meta property="og:type" content="article" />
  <meta property="og:locale" content="en" />
  <meta property="og:locale:alternate" content="ca" />
  <meta property="og:locale:alternate" content="fr" />
  <meta property="og:locale:alternate" content="it" />
  <meta property="og:locale:alternate" content="ja" />
  <meta property="og:locale:alternate" content="ko" />
  <meta property="og:locale:alternate" content="nl" />
  <meta property="og:locale:alternate" content="pl" />
  <meta property="og:locale:alternate" content="pt_PT" />
  <meta property="og:locale:alternate" content="pt_BR" />
  <meta property="og:locale:alternate" content="sl" />
  <meta property="og:locale:alternate" content="tr" />
  <meta property="og:locale:alternate" content="uk_UA" />
  <meta property="og:locale:alternate" content="zh_CN" />
  <meta property="og:article:modified_time" content="2025-11-17T09:18:56" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
<meta content="Page about the arithmetic blending modes in Krita: Addition, Divide, Inverse Subtract, Multiply and Subtract." lang="en" name="description" xml:lang="en" />
  <title>Arithmetic &mdash; Krita Manual 5.2.0 documentation</title>
    <link rel="shortcut icon" href="../../../../_static/favicon.ico"/>
    <link rel="canonical" href="en/reference_manual/blending_modes/arithmetic.html"/>
    <meta property="og:url" content="en/reference_manual/blending_modes/arithmetic.html" />
    <meta property="og:image" content="en/../../_static/sidebar-logo.png" />
    <link rel="stylesheet" href="../../_static/css/theme.css" type="text/css" />
    <link rel="stylesheet" href="../../_static/pygments.css" type="text/css" />
    <link rel="stylesheet" href="../../_static/pygments.css" type="text/css" />
    <link rel="stylesheet" href="../../_static/css/theme.css" type="text/css" />
    <link rel="index" title="Index" href="../../genindex.html" />
    <link rel="search" title="Search" href="../../search.html" />
    <link rel="next" title="Binary" href="binary.html" />
    <link rel="prev" title="Blending Modes" href="../blending_modes.html" /> 
  <!-- theme and selectors rely on jquery still. currently v3.7.1. Eventually try to migrate off these libraries -->
  <script type="text/javascript" src="../../_static/js/jquery.min.js"></script> 
  <!-- search uses underscore.js to help do some filtering and parsing -->
  <script type="text/javascript" src="../../_static/js/underscore.min.js"></script> 
  <script>
    var $u = _; // Now we can use $u instead of _ throughout your code. (which searchtools.js uses)
  </script>
  <script src="../../_static/js/modernizr.min.js"></script>
</head>
<body class="wy-body-for-nav">
  <div class="wy-grid-for-nav">
    <nav data-toggle="wy-nav-shift" class="wy-nav-side">
      <div class="wy-side-scroll">
        <div class="wy-side-nav-search">
           <a href="../../index.html" class="icon icon-home">
			<img src="../../../../_static/sidebar-logo.png" class="logo" alt="Logo"/>
           	
           <!--	Krita Manual -->
          </a>
<div role="search">
  <form id="rtd-search-form" class="wy-form" action="../../search.html" method="get">
    <input type="text" name="q" placeholder="Search docs" />
    <input type="hidden" name="check_keywords" value="yes" />
    <input type="hidden" name="area" value="default" />
  </form>
</div>
        </div>
        <div class="wy-side-nav-language-selector">
        	<p class="caption-text">
	        	<select id="language-selector-container">
	        		<option value="ca">Català</option>
	        		<option value="en">English</option>
	        		<option value="fr">français</option>
	        		<option value="it">Italiano</option>
	        		<option value="ja">日本語</option>
	        		<option value="ko">한국어</option>
	        		<option value="nl">Nederlands</option>
	        		<option value="pl">Polski</option>
	        		<option value="pt_PT">português</option>
	        		<option value="pt_BR">português brasileiro</option>
                    <option value="sl">slovenščina</option>
                    <option value="tr">Türkçe</option>
	        		<option value="uk_UA">Українська</option>
	        		<option value="zh_CN">简体中文</option>
	        	</select>
        	</p>
        </div>
        <div class="wy-menu wy-menu-vertical" data-spy="affix" role="navigation" aria-label="main navigation">
              <ul class="current">
<li class="toctree-l1"><a class="reference internal" href="../../user_manual.html">User Manual</a></li>
<li class="toctree-l1"><a class="reference internal" href="../../general_concepts.html">General Concepts</a></li>
<li class="toctree-l1 current"><a class="reference internal" href="../../reference_manual.html">Reference Manual</a><ul class="current">
<li class="toctree-l2"><a class="reference internal" href="../audio_for_animation.html">Audio for Animation</a></li>
<li class="toctree-l2 current"><a class="reference internal" href="../blending_modes.html">Blending Modes</a><ul class="current">
<li class="toctree-l3"><a class="reference internal" href="../blending_modes.html#favorites">Favorites</a></li>
<li class="toctree-l3"><a class="reference internal" href="../blending_modes.html#hotkeys-associated-with-blending-modes">Hotkeys associated with Blending modes</a></li>
<li class="toctree-l3 current"><a class="reference internal" href="../blending_modes.html#available-blending-modes">Available Blending Modes</a><ul class="current">
<li class="toctree-l4 current"><a class="current reference internal" href="#">Arithmetic</a></li>
<li class="toctree-l4"><a class="reference internal" href="binary.html">Binary</a></li>
<li class="toctree-l4"><a class="reference internal" href="darken.html">Darken</a></li>
<li class="toctree-l4"><a class="reference internal" href="hsx.html">HSX</a></li>
<li class="toctree-l4"><a class="reference internal" href="lighten.html">Lighten</a></li>
<li class="toctree-l4"><a class="reference internal" href="misc.html">Misc</a></li>
<li class="toctree-l4"><a class="reference internal" href="mix.html">Mix</a></li>
<li class="toctree-l4"><a class="reference internal" href="modulo.html">Modulo</a></li>
<li class="toctree-l4"><a class="reference internal" href="negative.html">Negative</a></li>
<li class="toctree-l4"><a class="reference internal" href="quadratic.html">Quadratic</a></li>
</ul>
</li>
</ul>
</li>
<li class="toctree-l2"><a class="reference internal" href="../brushes.html">Brushes</a></li>
<li class="toctree-l2"><a class="reference internal" href="../clones_array.html">Clones Array</a></li>
<li class="toctree-l2"><a class="reference internal" href="../create_new_document.html">Create New Document</a></li>
<li class="toctree-l2"><a class="reference internal" href="../default_python_plugins.html">Pre-installed Python plugins</a></li>
<li class="toctree-l2"><a class="reference internal" href="../dockers.html">Dockers</a></li>
<li class="toctree-l2"><a class="reference internal" href="../dr_minw_debugger.html">Dr. MinGW Debugger</a></li>
<li class="toctree-l2"><a class="reference internal" href="../filters.html">Filters</a></li>
<li class="toctree-l2"><a class="reference internal" href="../hdr_display.html">HDR Display</a></li>
<li class="toctree-l2"><a class="reference internal" href="../image_split.html">Image Split</a></li>
<li class="toctree-l2"><a class="reference internal" href="../import_animation.html">Import Animation</a></li>
<li class="toctree-l2"><a class="reference internal" href="../instant_preview.html">Instant Preview</a></li>
<li class="toctree-l2"><a class="reference internal" href="../krita_4_preset_bundle.html">Krita 4 Preset Bundle Overview</a></li>
<li class="toctree-l2"><a class="reference internal" href="../layers_and_masks.html">Layers and Masks</a></li>
<li class="toctree-l2"><a class="reference internal" href="../linux_command_line.html">Linux Command Line</a></li>
<li class="toctree-l2"><a class="reference internal" href="../main_menu.html">Main Menu</a></li>
<li class="toctree-l2"><a class="reference internal" href="../maths_input.html">Maths Input</a></li>
<li class="toctree-l2"><a class="reference internal" href="../popup-palette.html">Pop-up Palette</a></li>
<li class="toctree-l2"><a class="reference internal" href="../preferences.html">Preferences</a></li>
<li class="toctree-l2"><a class="reference internal" href="../render_animation.html">Render Animation</a></li>
<li class="toctree-l2"><a class="reference internal" href="../resource_management.html">Resource Management</a></li>
<li class="toctree-l2"><a class="reference internal" href="../seexpr.html">SeExpr Quick Reference</a></li>
<li class="toctree-l2"><a class="reference internal" href="../separate_image.html">Separate Image</a></li>
<li class="toctree-l2"><a class="reference internal" href="../sharing_krita_logs.html">Getting Krita logs</a></li>
<li class="toctree-l2"><a class="reference internal" href="../split_layer.html">Split Layer</a></li>
<li class="toctree-l2"><a class="reference internal" href="../storyboard_svg_template.html">SVG Storyboard Export Templates</a></li>
<li class="toctree-l2"><a class="reference internal" href="../stroke_selection.html">Stroke Selection</a></li>
<li class="toctree-l2"><a class="reference internal" href="../tools.html">Tools</a></li>
<li class="toctree-l2"><a class="reference internal" href="../welcome_screen.html">Welcome Screen</a></li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="../../tutorials.html">Tutorials and How-tos</a></li>
<li class="toctree-l1"><a class="reference internal" href="../../KritaFAQ.html">Krita FAQ</a></li>
<li class="toctree-l1"><a class="reference internal" href="../../contributors_manual.html">Contributors Manual</a></li>
<li class="toctree-l1"><a class="reference internal" href="../../resources_page.html">Resources</a></li>
</ul>
        </div>
      </div>
    </nav>
    <section data-toggle="wy-nav-shift" class="wy-nav-content-wrap">
	<!-- start top banner area (for fundraisers or messages)
	<div style="text-align: center; background-color: #333">
		<a href="https://krita.org/en/fundraising-2018-campaign/" target="_self" onclick="ga('send', 'event', 'frontpage', 'button', 'Fundraiser 2018');">
			<img src="https://krita.org/wp-content/themes/krita-org-theme/images/decoration/2018-fundraiser-banner.png" style="max-width: 100%">
		</a>
	</div>
	
	 end top banner area -->
      <nav class="wy-nav-top" aria-label="top navigation">
          <i data-toggle="wy-nav-top" class="fa fa-bars"></i>
          <a href="../../index.html">Krita Manual</a>
      </nav>
      <div class="wy-nav-content">
        <div class="rst-content">
<div role="navigation" aria-label="breadcrumbs navigation">
  <ul class="wy-breadcrumbs">
      <li><a href="../../index.html">Docs</a> &raquo;</li>
          <li><a href="../../reference_manual.html">Reference Manual</a> &raquo;</li>
          <li><a href="../blending_modes.html">Blending Modes</a> &raquo;</li>
      <li>Arithmetic</li>
      <li class="wy-breadcrumbs-aside">
            <a href="../../_sources/reference_manual/blending_modes/arithmetic.rst.txt" rel="nofollow"> 
              <img src="../../_static/images/source-code.png" />
             <!-- View page source -->
          </a>
      </li>
  </ul>
</div>
          <div role="main" class="document" itemscope="itemscope" itemtype="http://schema.org/Article">
           <div itemprop="articleBody">
  <section id="arithmetic">
<span id="bm-cat-arithmetic"></span><h1>Arithmetic<a class="headerlink" href="#arithmetic" title="Link to this heading">¶</a></h1>
<p>These blending modes are based on simple maths.</p>
<section id="addition">
<span id="bm-addition"></span><span id="index-0"></span><h2>Addition<a class="headerlink" href="#addition" title="Link to this heading">¶</a></h2>
<p>Adds the numerical values of two colors together:</p>
<p>Yellow(1, 1, 0) + Blue(0, 0, 1) = White(1, 1, 1)</p>
<p>Darker Gray(0.4, 0.4, 0.4) + Lighter Gray(0.5, 0.5, 0.5) = Even Lighter Gray (0.9, 0.9, 0.9)</p>
<figure class="align-center" id="id1">
<img alt="../../_images/Blending_modes_Addition_Gray_0.4_and_Gray_0.5_n.png" src="../../_images/Blending_modes_Addition_Gray_0.4_and_Gray_0.5_n.png" />
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Addition</strong>.</span><a class="headerlink" href="#id1" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<p>Light Blue(0.1608, 0.6274, 0.8274) + Orange(1, 0.5961, 0.0706) = (1.1608, 1.2235, 0.8980) → Very Light Yellow(1, 1, 0.8980)</p>
<figure class="align-center" id="id2">
<img alt="../../_images/Blending_modes_Addition_Light_blue_and_Orange.png" src="../../_images/Blending_modes_Addition_Light_blue_and_Orange.png" />
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Addition</strong>.</span><a class="headerlink" href="#id2" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<p>Red(1, 0, 0) + Gray(0.5, 0.5, 0.5) = Pink(1, 0.5, 0.5)</p>
<figure class="align-center" id="id3">
<img alt="../../_images/Blending_modes_Addition_Red_plus_gray.png" src="../../_images/Blending_modes_Addition_Red_plus_gray.png" />
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Addition</strong>.</span><a class="headerlink" href="#id3" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<p>When the result of the addition is more than 1, white is the color displayed. Therefore, white plus any other color results in white. On the other hand, black plus any other color results in the added color.</p>
<figure class="align-center" id="id4">
<img alt="../../_images/Blending_modes_Addition_Sample_image_with_dots.png" src="../../_images/Blending_modes_Addition_Sample_image_with_dots.png" />
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
<img alt="../../_images/Blending_modes_Divide_Gray_0.4_and_Gray_0.5_n.png" src="../../_images/Blending_modes_Divide_Gray_0.4_and_Gray_0.5_n.png" />
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Divide</strong>.</span><a class="headerlink" href="#id5" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<p>Light Blue(0.1608, 0.6274, 0.8274) / Orange(1, 0.5961, 0.0706) = (0.1608, 1.0525, 11.7195) → Aqua(0.1608, 1, 1)</p>
<figure class="align-center" id="id6">
<img alt="../../_images/Blending_modes_Divide_Light_blue_and_Orange.png" src="../../_images/Blending_modes_Divide_Light_blue_and_Orange.png" />
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Divide</strong>.</span><a class="headerlink" href="#id6" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<figure class="align-center" id="id7">
<img alt="../../_images/Blending_modes_Divide_Sample_image_with_dots.png" src="../../_images/Blending_modes_Divide_Sample_image_with_dots.png" />
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
<img alt="../../_images/Blending_modes_Inverse_Subtract_Gray_0.4_and_Gray_0.5_n.png" src="../../_images/Blending_modes_Inverse_Subtract_Gray_0.4_and_Gray_0.5_n.png" />
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Inverse Subtract</strong>.</span><a class="headerlink" href="#id8" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<p>Orange(1, 0.5961, 0.0706)_(1_Light Blue(0.1608, 0.6274, 0.8274)) = (0.1608, 0.2235, -0.102) → Dark Green(0.1608, 0.2235, 0)</p>
<figure class="align-center" id="id9">
<img alt="../../_images/Blending_modes_Inverse_Subtract_Light_blue_and_Orange.png" src="../../_images/Blending_modes_Inverse_Subtract_Light_blue_and_Orange.png" />
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Inverse Subtract</strong>.</span><a class="headerlink" href="#id9" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<figure class="align-center" id="id10">
<img alt="../../_images/Blending_modes_Inverse_Subtract_Sample_image_with_dots.png" src="../../_images/Blending_modes_Inverse_Subtract_Sample_image_with_dots.png" />
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
<img alt="../../_images/Blending_modes_Multiply_Gray_0.4_and_Gray_0.5_n.png" src="../../_images/Blending_modes_Multiply_Gray_0.4_and_Gray_0.5_n.png" />
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Multiply</strong>.</span><a class="headerlink" href="#id11" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<p>Light Blue(0.1608, 0.6274, 0.8274) x Orange(1, 0.5961, 0.0706) = Green(0.1608, 0.3740, 0.0584)</p>
<figure class="align-center" id="id12">
<img alt="../../_images/Blending_modes_Multiply_Light_blue_and_Orange.png" src="../../_images/Blending_modes_Multiply_Light_blue_and_Orange.png" />
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Multiply</strong>.</span><a class="headerlink" href="#id12" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<figure class="align-center" id="id13">
<img alt="../../_images/Blending_modes_Multiply_Sample_image_with_dots.png" src="../../_images/Blending_modes_Multiply_Sample_image_with_dots.png" />
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
<img alt="../../_images/Blending_modes_Subtract_Gray_0.4_and_Gray_0.5_n.png" src="../../_images/Blending_modes_Subtract_Gray_0.4_and_Gray_0.5_n.png" />
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Subtract</strong>.</span><a class="headerlink" href="#id14" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<p>Light Blue(0.1608, 0.6274, 0.8274) - Orange(1, 0.5961, 0.0706) = (-0.8392, 0.0313, 0.7568) → Blue(0, 0.0313, 0.7568)</p>
<figure class="align-center" id="id15">
<img alt="../../_images/Blending_modes_Subtract_Light_blue_and_Orange.png" src="../../_images/Blending_modes_Subtract_Light_blue_and_Orange.png" />
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Subtract</strong>.</span><a class="headerlink" href="#id15" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<figure class="align-center" id="id16">
<img alt="../../_images/Blending_modes_Subtract_Sample_image_with_dots.png" src="../../_images/Blending_modes_Subtract_Sample_image_with_dots.png" />
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Subtract</strong>.</span><a class="headerlink" href="#id16" title="Link to this image">¶</a></p>
</figcaption>
</figure>
</section>
</section>
           </div>
          </div>
          <footer>
    <div class="rst-footer-buttons" role="navigation" aria-label="footer navigation">
        <a href="binary.html" class="btn btn-neutral float-right" title="Binary" accesskey="n" rel="next"> <!-- Next --> <span class="fa fa-arrow-circle-right"></span></a>
        <a href="../blending_modes.html" class="btn btn-neutral" title="Blending Modes" accesskey="p" rel="prev"><span class="fa fa-arrow-circle-left"></span> <!-- Previous  -->  </a>
    </div>
  <hr/>
  <div role="contentinfo">
    <p>
        &copy; Copyright licensed under the GNU Free Documentation License 1.3+ unless stated otherwise.
        <span class="commit">
          Revision <code>v5.2.0-106-g27972506c8</code>.
        </span>
    </p>
  </div>
  Built with <a href="http://sphinx-doc.org/">Sphinx</a> using a modified <a href="https://github.com/rtfd/sphinx_rtd_theme">RTD theme</a>.<br/>
  <a href="https://krita.org" title="Krita official website.">Krita official website</a> |
  <a href="https://invent.kde.org/documentation/docs-krita-org/" title="The Gitlab instance to edit this pages and collaborate.">Git repository for docs.krita.org </a> |
  <a href="https://www.kde.org/community/whatiskde/impressum-en.php" title="To know more about KDE, code of conduct, privacy policy and GDPR.">KDE Impressum</a>.
</footer>
        </div>
      </div>
    </section>
  </div>
      <script src="../../_static/documentation_options.js?v=2dde5210"></script>
      <script src="../../_static/doctools.js?v=9bcbadda"></script>
      <script src="../../_static/sphinx_highlight.js?v=dc90522c"></script>
    <script type="text/javascript" src="../../_static/js/theme.js"></script>
  <script type="text/javascript">
    document.addEventListener("DOMContentLoaded", function() {
          SphinxRtdTheme.Navigation.enableSticky();
    });
  </script> 
 <script type="text/javascript">
	 var _paq=_paq||[];
	 _paq.push(['setCookieDomain','*.krita.org']);
	 _paq.push(['setDomains','*.krita.org']);
	 _paq.push(['setDocumentTitle',document.domain+"/"+document.title]);
	 _paq.push(['trackPageView']);
	 _paq.push(['enableLinkTracking']);
	 (function(){
	 	var u="//stats.kde.org/";
	    _paq.push(['setTrackerUrl',u+'piwik.php']);
	    _paq.push(['setSiteId',13]);
	    var d = document, g = d.createElement('script'),s=d.getElementsByTagName('script')[0];
	    g.type = 'text/javascript';
	    g.async = true;
	    g.defer = true;
	    g.src = u+'piwik.js';
	    s.parentNode.insertBefore(g,s);
	  })();
</script> 
<noscript><p><img src="//stats.kde.org/piwik.php?idsite=13" style="border:0;" alt="" /></p></noscript>
</body>
</html>'''
        self.path_to_test_file.write_text(test_file_contents, encoding="utf-8")

    def test_split_from_blendingmodes_pages(self):
        """
        Tests functionality to extract 'blending_modes' subsections from a page.
        """
        soup = bs4.BeautifulSoup(self.path_to_test_file.read_text(encoding="utf-8"), 'html.parser')
        sections = split_from_blendingmodes_page(soup)
        self.assertIsInstance(sections, list)
        self.assertEqual(len(sections), self.number_of_subsections)
        for section in sections:
            self.assertIsNotNone(section)
            self.assertIsInstance(section, bs4.Tag)
            self.assertTrue(section)
            self.assertIsNotNone(section.find("h2"))

class BlendingModesHSXTestCase(unittest.TestCase):
    """
    Inspects functionality when targeted at 'blending_modes/hsx' index module.
    """

    def setUp(self):
        """
        Defines path to test file and creates it.
        """
        subdirectory = "blending_modes/"
        filename = "hsx.html"
        self.number_of_subsections = 11
        path_to_test_dir = Path(SOURCE_DIR, subdirectory)
        path_to_test_dir.mkdir(exist_ok=True)
        self.path_to_test_file = path_to_test_dir.joinpath(filename)
        path_to_og_file = Path(*SOURCE_DIR.split("/")[2:] + [subdirectory, filename])
        test_file_contents = '''<!DOCTYPE html>
<!--[if IE 8]><html class="no-js lt-ie9" lang="en" > <![endif]-->
<!--[if gt IE 8]><!--> <html class="no-js" lang="en" > <!--<![endif]-->
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta property="og:title" name="title" content="HSX" />
  <meta property="og:site-name" content="Krita Manual" />
  <meta property="og:type" content="article" />
  <meta property="og:locale" content="en" />
  <meta property="og:locale:alternate" content="ca" />
  <meta property="og:locale:alternate" content="fr" />
  <meta property="og:locale:alternate" content="it" />
  <meta property="og:locale:alternate" content="ja" />
  <meta property="og:locale:alternate" content="ko" />
  <meta property="og:locale:alternate" content="nl" />
  <meta property="og:locale:alternate" content="pl" />
  <meta property="og:locale:alternate" content="pt_PT" />
  <meta property="og:locale:alternate" content="pt_BR" />
  <meta property="og:locale:alternate" content="sl" />
  <meta property="og:locale:alternate" content="tr" />
  <meta property="og:locale:alternate" content="uk_UA" />
  <meta property="og:locale:alternate" content="zh_CN" />
  <meta property="og:article:modified_time" content="2025-11-17T09:18:56" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
<meta content="Page about the HSX blending modes in Krita, amongst which Hue, Color, Luminosity and Saturation." name="description" />
  <title>HSX &mdash; Krita Manual 5.2.0 documentation</title>
    <link rel="shortcut icon" href="../../../../_static/favicon.ico"/>
    <link rel="canonical" href="en/reference_manual/blending_modes/hsx.html"/>
    <meta property="og:url" content="en/reference_manual/blending_modes/hsx.html" />
    <meta property="og:image" content="en/../../_static/sidebar-logo.png" />
    <link rel="stylesheet" href="../../_static/css/theme.css" type="text/css" />
    <link rel="stylesheet" href="../../_static/pygments.css" type="text/css" />
    <link rel="stylesheet" href="../../_static/pygments.css" type="text/css" />
    <link rel="stylesheet" href="../../_static/css/theme.css" type="text/css" />
    <link rel="index" title="Index" href="../../genindex.html" />
    <link rel="search" title="Search" href="../../search.html" />
    <link rel="next" title="Lighten" href="lighten.html" />
    <link rel="prev" title="Darken" href="darken.html" /> 
  <!-- theme and selectors rely on jquery still. currently v3.7.1. Eventually try to migrate off these libraries -->
  <script type="text/javascript" src="../../_static/js/jquery.min.js"></script> 
  <!-- search uses underscore.js to help do some filtering and parsing -->
  <script type="text/javascript" src="../../_static/js/underscore.min.js"></script> 
  <script>
    var $u = _; // Now we can use $u instead of _ throughout your code. (which searchtools.js uses)
  </script>
  <script src="../../_static/js/modernizr.min.js"></script>
</head>
<body class="wy-body-for-nav">
  <div class="wy-grid-for-nav">
    <nav data-toggle="wy-nav-shift" class="wy-nav-side">
      <div class="wy-side-scroll">
        <div class="wy-side-nav-search">
           <a href="../../index.html" class="icon icon-home">
                        <img src="../../../../_static/sidebar-logo.png" class="logo" alt="Logo"/>
                
           <!--	Krita Manual -->
          </a>
<div role="search">
  <form id="rtd-search-form" class="wy-form" action="../../search.html" method="get">
    <input type="text" name="q" placeholder="Search docs" />
    <input type="hidden" name="check_keywords" value="yes" />
    <input type="hidden" name="area" value="default" />
  </form>
</div>
        </div>
        <div class="wy-side-nav-language-selector">
                <p class="caption-text">
                        <select id="language-selector-container">
                                <option value="ca">Català</option>
                                <option value="en">English</option>
                                <option value="fr">français</option>
                                <option value="it">Italiano</option>
                                <option value="ja">日本語</option>
                                <option value="ko">한국어</option>
                                <option value="nl">Nederlands</option>
                                <option value="pl">Polski</option>
                                <option value="pt_PT">português</option>
                                <option value="pt_BR">português brasileiro</option>
                    <option value="sl">slovenščina</option>
                    <option value="tr">Türkçe</option>
                                <option value="uk_UA">Українська</option>
                                <option value="zh_CN">简体中文</option>
                        </select>
                </p>
        </div>
        <div class="wy-menu wy-menu-vertical" data-spy="affix" role="navigation" aria-label="main navigation">
              <ul class="current">
<li class="toctree-l1"><a class="reference internal" href="../../user_manual.html">User Manual</a></li>
<li class="toctree-l1"><a class="reference internal" href="../../general_concepts.html">General Concepts</a></li>
<li class="toctree-l1 current"><a class="reference internal" href="../../reference_manual.html">Reference Manual</a><ul class="current">
<li class="toctree-l2"><a class="reference internal" href="../audio_for_animation.html">Audio for Animation</a></li>
<li class="toctree-l2 current"><a class="reference internal" href="../blending_modes.html">Blending Modes</a><ul class="current">
<li class="toctree-l3"><a class="reference internal" href="../blending_modes.html#favorites">Favorites</a></li>
<li class="toctree-l3"><a class="reference internal" href="../blending_modes.html#hotkeys-associated-with-blending-modes">Hotkeys associated with Blending modes</a></li>
<li class="toctree-l3 current"><a class="reference internal" href="../blending_modes.html#available-blending-modes">Available Blending Modes</a><ul class="current">
<li class="toctree-l4"><a class="reference internal" href="arithmetic.html">Arithmetic</a></li>
<li class="toctree-l4"><a class="reference internal" href="binary.html">Binary</a></li>
<li class="toctree-l4"><a class="reference internal" href="darken.html">Darken</a></li>
<li class="toctree-l4 current"><a class="current reference internal" href="#">HSX</a></li>
<li class="toctree-l4"><a class="reference internal" href="lighten.html">Lighten</a></li>
<li class="toctree-l4"><a class="reference internal" href="misc.html">Misc</a></li>
<li class="toctree-l4"><a class="reference internal" href="mix.html">Mix</a></li>
<li class="toctree-l4"><a class="reference internal" href="modulo.html">Modulo</a></li>
<li class="toctree-l4"><a class="reference internal" href="negative.html">Negative</a></li>
<li class="toctree-l4"><a class="reference internal" href="quadratic.html">Quadratic</a></li>
</ul>
</li>
</ul>
</li>
<li class="toctree-l2"><a class="reference internal" href="../brushes.html">Brushes</a></li>
<li class="toctree-l2"><a class="reference internal" href="../clones_array.html">Clones Array</a></li>
<li class="toctree-l2"><a class="reference internal" href="../create_new_document.html">Create New Document</a></li>
<li class="toctree-l2"><a class="reference internal" href="../default_python_plugins.html">Pre-installed Python plugins</a></li>
<li class="toctree-l2"><a class="reference internal" href="../dockers.html">Dockers</a></li>
<li class="toctree-l2"><a class="reference internal" href="../dr_minw_debugger.html">Dr. MinGW Debugger</a></li>
<li class="toctree-l2"><a class="reference internal" href="../filters.html">Filters</a></li>
<li class="toctree-l2"><a class="reference internal" href="../hdr_display.html">HDR Display</a></li>
<li class="toctree-l2"><a class="reference internal" href="../image_split.html">Image Split</a></li>
<li class="toctree-l2"><a class="reference internal" href="../import_animation.html">Import Animation</a></li>
<li class="toctree-l2"><a class="reference internal" href="../instant_preview.html">Instant Preview</a></li>
<li class="toctree-l2"><a class="reference internal" href="../krita_4_preset_bundle.html">Krita 4 Preset Bundle Overview</a></li>
<li class="toctree-l2"><a class="reference internal" href="../layers_and_masks.html">Layers and Masks</a></li>
<li class="toctree-l2"><a class="reference internal" href="../linux_command_line.html">Linux Command Line</a></li>
<li class="toctree-l2"><a class="reference internal" href="../main_menu.html">Main Menu</a></li>
<li class="toctree-l2"><a class="reference internal" href="../maths_input.html">Maths Input</a></li>
<li class="toctree-l2"><a class="reference internal" href="../popup-palette.html">Pop-up Palette</a></li>
<li class="toctree-l2"><a class="reference internal" href="../preferences.html">Preferences</a></li>
<li class="toctree-l2"><a class="reference internal" href="../render_animation.html">Render Animation</a></li>
<li class="toctree-l2"><a class="reference internal" href="../resource_management.html">Resource Management</a></li>
<li class="toctree-l2"><a class="reference internal" href="../seexpr.html">SeExpr Quick Reference</a></li>
<li class="toctree-l2"><a class="reference internal" href="../separate_image.html">Separate Image</a></li>
<li class="toctree-l2"><a class="reference internal" href="../sharing_krita_logs.html">Getting Krita logs</a></li>
<li class="toctree-l2"><a class="reference internal" href="../split_layer.html">Split Layer</a></li>
<li class="toctree-l2"><a class="reference internal" href="../storyboard_svg_template.html">SVG Storyboard Export Templates</a></li>
<li class="toctree-l2"><a class="reference internal" href="../stroke_selection.html">Stroke Selection</a></li>
<li class="toctree-l2"><a class="reference internal" href="../tools.html">Tools</a></li>
<li class="toctree-l2"><a class="reference internal" href="../welcome_screen.html">Welcome Screen</a></li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="../../tutorials.html">Tutorials and How-tos</a></li>
<li class="toctree-l1"><a class="reference internal" href="../../KritaFAQ.html">Krita FAQ</a></li>
<li class="toctree-l1"><a class="reference internal" href="../../contributors_manual.html">Contributors Manual</a></li>
<li class="toctree-l1"><a class="reference internal" href="../../resources_page.html">Resources</a></li>
</ul>
        </div>
      </div>
    </nav>
    <section data-toggle="wy-nav-shift" class="wy-nav-content-wrap">
        <!-- start top banner area (for fundraisers or messages)
        <div style="text-align: center; background-color: #333">
                <a href="https://krita.org/en/fundraising-2018-campaign/" target="_self" onclick="ga('send', 'event', 'frontpage', 'button', 'Fundraiser 2018');">
                        <img src="https://krita.org/wp-content/themes/krita-org-theme/images/decoration/2018-fundraiser-banner.png" style="max-width: 100%">
                </a>
        </div>
        
         end top banner area -->
      <nav class="wy-nav-top" aria-label="top navigation">
          <i data-toggle="wy-nav-top" class="fa fa-bars"></i>
          <a href="../../index.html">Krita Manual</a>
      </nav>
      <div class="wy-nav-content">
        <div class="rst-content">
<div role="navigation" aria-label="breadcrumbs navigation">
  <ul class="wy-breadcrumbs">
      <li><a href="../../index.html">Docs</a> &raquo;</li>
          <li><a href="../../reference_manual.html">Reference Manual</a> &raquo;</li>
          <li><a href="../blending_modes.html">Blending Modes</a> &raquo;</li>
      <li>HSX</li>
      <li class="wy-breadcrumbs-aside">
            <a href="../../_sources/reference_manual/blending_modes/hsx.rst.txt" rel="nofollow"> 
              <img src="../../_static/images/source-code.png" />
             <!-- View page source -->
          </a>
      </li>
  </ul>
</div>
          <div role="main" class="document" itemscope="itemscope" itemtype="http://schema.org/Article">
           <div itemprop="articleBody">
  <section id="hsx">
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
<img alt="../../_images/Blending_modes_Color_HSI_Gray_0.4_and_Gray_0.5.png" src="../../_images/Blending_modes_Color_HSI_Gray_0.4_and_Gray_0.5.png" />
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Color HSI</strong>.</span><a class="headerlink" href="#id1" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<figure class="align-center" id="id2">
<img alt="../../_images/Blending_modes_Color_HSI_Light_blue_and_Orange.png" src="../../_images/Blending_modes_Color_HSI_Light_blue_and_Orange.png" />
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Color HSI</strong>.</span><a class="headerlink" href="#id2" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<figure class="align-center" id="id3">
<img alt="../../_images/Blending_modes_Color_HSI_Sample_image_with_dots.png" src="../../_images/Blending_modes_Color_HSI_Sample_image_with_dots.png" />
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Color HSI</strong>.</span><a class="headerlink" href="#id3" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<figure class="align-center" id="id4">
<img alt="../../_images/Blending_modes_Color_HSL_Sample_image_with_dots.png" src="../../_images/Blending_modes_Color_HSL_Sample_image_with_dots.png" />
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Color HSL</strong>.</span><a class="headerlink" href="#id4" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<figure class="align-center" id="id5">
<img alt="../../_images/Blending_modes_Color_HSV_Sample_image_with_dots.png" src="../../_images/Blending_modes_Color_HSV_Sample_image_with_dots.png" />
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Color HSV</strong>.</span><a class="headerlink" href="#id5" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<figure class="align-center" id="id6">
<img alt="../../_images/Blending_modes_Color_Sample_image_with_dots.png" src="../../_images/Blending_modes_Color_Sample_image_with_dots.png" />
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
<img alt="../../_images/Blending_modes_Hue_HSI_Sample_image_with_dots.png" src="../../_images/Blending_modes_Hue_HSI_Sample_image_with_dots.png" />
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Hue HSI</strong>.</span><a class="headerlink" href="#id7" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<figure class="align-center" id="id8">
<img alt="../../_images/Blending_modes_Hue_HSL_Sample_image_with_dots.png" src="../../_images/Blending_modes_Hue_HSL_Sample_image_with_dots.png" />
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Hue HSL</strong>.</span><a class="headerlink" href="#id8" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<figure class="align-center" id="id9">
<img alt="../../_images/Blending_modes_Hue_HSV_Sample_image_with_dots.png" src="../../_images/Blending_modes_Hue_HSV_Sample_image_with_dots.png" />
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Hue HSV</strong>.</span><a class="headerlink" href="#id9" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<figure class="align-center" id="id10">
<img alt="../../_images/Blending_modes_Hue_Sample_image_with_dots.png" src="../../_images/Blending_modes_Hue_Sample_image_with_dots.png" />
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
<img alt="../../_images/Blending_modes_Increase_Intensity_Sample_image_with_dots.png" src="../../_images/Blending_modes_Increase_Intensity_Sample_image_with_dots.png" />
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Increase Intensity</strong>.</span><a class="headerlink" href="#id11" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<figure class="align-center" id="id12">
<img alt="../../_images/Blending_modes_Increase_Lightness_Sample_image_with_dots.png" src="../../_images/Blending_modes_Increase_Lightness_Sample_image_with_dots.png" />
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Increase Lightness</strong>.</span><a class="headerlink" href="#id12" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<figure class="align-center" id="id13">
<img alt="../../_images/Blending_modes_Increase_Value_Sample_image_with_dots.png" src="../../_images/Blending_modes_Increase_Value_Sample_image_with_dots.png" />
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Increase Value</strong>.</span><a class="headerlink" href="#id13" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<figure class="align-center" id="id14">
<img alt="../../_images/Blending_modes_Increase_Luminosity_Sample_image_with_dots.png" src="../../_images/Blending_modes_Increase_Luminosity_Sample_image_with_dots.png" />
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
<img alt="../../_images/Blending_modes_Increase_Saturation_HSI_Sample_image_with_dots.png" src="../../_images/Blending_modes_Increase_Saturation_HSI_Sample_image_with_dots.png" />
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Increase Saturation HSI</strong>.</span><a class="headerlink" href="#id15" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<figure class="align-center" id="id16">
<img alt="../../_images/Blending_modes_Increase_Saturation_HSL_Sample_image_with_dots.png" src="../../_images/Blending_modes_Increase_Saturation_HSL_Sample_image_with_dots.png" />
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Increase Saturation HSL</strong>.</span><a class="headerlink" href="#id16" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<figure class="align-center" id="id17">
<img alt="../../_images/Blending_modes_Increase_Saturation_HSV_Sample_image_with_dots.png" src="../../_images/Blending_modes_Increase_Saturation_HSV_Sample_image_with_dots.png" />
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Increase Saturation HSV</strong>.</span><a class="headerlink" href="#id17" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<figure class="align-center" id="id18">
<img alt="../../_images/Blending_modes_Increase_Saturation_Sample_image_with_dots.png" src="../../_images/Blending_modes_Increase_Saturation_Sample_image_with_dots.png" />
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Increase Saturation</strong>.</span><a class="headerlink" href="#id18" title="Link to this image">¶</a></p>
</figcaption>
</figure>
</section>
<section id="intensity">
<span id="bm-intensity"></span><h3>Intensity<a class="headerlink" href="#intensity" title="Link to this heading">¶</a></h3>
<p>Takes the Hue and Saturation of the lower layer and outputs them with the intensity of the upper layer.</p>
<figure class="align-center" id="id19">
<img alt="../../_images/Blending_modes_Intensity_Sample_image_with_dots.png" src="../../_images/Blending_modes_Intensity_Sample_image_with_dots.png" />
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Intensity</strong>.</span><a class="headerlink" href="#id19" title="Link to this image">¶</a></p>
</figcaption>
</figure>
</section>
<section id="value">
<span id="bm-value"></span><h3>Value<a class="headerlink" href="#value" title="Link to this heading">¶</a></h3>
<p>Takes the Hue and Saturation of the lower layer and outputs them with the Value of the upper layer.</p>
<figure class="align-center" id="id20">
<img alt="../../_images/Blending_modes_Value_Sample_image_with_dots.png" src="../../_images/Blending_modes_Value_Sample_image_with_dots.png" />
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Value</strong>.</span><a class="headerlink" href="#id20" title="Link to this image">¶</a></p>
</figcaption>
</figure>
</section>
<section id="lightness">
<span id="bm-lightness"></span><h3>Lightness<a class="headerlink" href="#lightness" title="Link to this heading">¶</a></h3>
<p>Takes the Hue and Saturation of the lower layer and outputs them with the Lightness of the upper layer.</p>
<figure class="align-center" id="id21">
<img alt="../../_images/Blending_modes_Lightness_Sample_image_with_dots.png" src="../../_images/Blending_modes_Lightness_Sample_image_with_dots.png" />
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
<img alt="../../_images/Blending_modes_Luminosity_Sample_image_with_dots.png" src="../../_images/Blending_modes_Luminosity_Sample_image_with_dots.png" />
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Luminosity</strong>.</span><a class="headerlink" href="#id22" title="Link to this image">¶</a></p>
</figcaption>
</figure>
</section>
<section id="saturation-hsi-hsv-hsl-hsy">
<span id="bm-hsy-saturation"></span><span id="bm-hsi-saturation"></span><span id="bm-hsl-saturation"></span><span id="bm-hsv-saturation"></span><span id="bm-saturation"></span><h3>Saturation HSI, HSV, HSL, HSY<a class="headerlink" href="#saturation-hsi-hsv-hsl-hsy" title="Link to this heading">¶</a></h3>
<p>Takes the Intensity and Hue of the lower layer, and outputs them with the HSI saturation of the upper layer.</p>
<figure class="align-center" id="id23">
<img alt="../../_images/Blending_modes_Saturation_HSI_Sample_image_with_dots.png" src="../../_images/Blending_modes_Saturation_HSI_Sample_image_with_dots.png" />
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Saturation HSI</strong>.</span><a class="headerlink" href="#id23" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<figure class="align-center" id="id24">
<img alt="../../_images/Blending_modes_Saturation_HSL_Sample_image_with_dots.png" src="../../_images/Blending_modes_Saturation_HSL_Sample_image_with_dots.png" />
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Saturation HSL</strong>.</span><a class="headerlink" href="#id24" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<figure class="align-center" id="id25">
<img alt="../../_images/Blending_modes_Saturation_HSV_Sample_image_with_dots.png" src="../../_images/Blending_modes_Saturation_HSV_Sample_image_with_dots.png" />
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Saturation HSV</strong>.</span><a class="headerlink" href="#id25" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<figure class="align-center" id="id26">
<img alt="../../_images/Blending_modes_Saturation_Sample_image_with_dots.png" src="../../_images/Blending_modes_Saturation_Sample_image_with_dots.png" />
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
<img alt="../../_images/Blending_modes_Decrease_Intensity_Gray_0.4_and_Gray_0.5.png" src="../../_images/Blending_modes_Decrease_Intensity_Gray_0.4_and_Gray_0.5.png" />
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Decrease Intensity</strong>.</span><a class="headerlink" href="#id27" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<figure class="align-center" id="id28">
<img alt="../../_images/Blending_modes_Decrease_Intensity_Light_blue_and_Orange.png" src="../../_images/Blending_modes_Decrease_Intensity_Light_blue_and_Orange.png" />
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Decrease Intensity</strong>.</span><a class="headerlink" href="#id28" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<figure class="align-center" id="id29">
<img alt="../../_images/Blending_modes_Decrease_Intensity_Sample_image_with_dots.png" src="../../_images/Blending_modes_Decrease_Intensity_Sample_image_with_dots.png" />
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Decrease Intensity</strong>.</span><a class="headerlink" href="#id29" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<figure class="align-center" id="id30">
<img alt="../../_images/Blending_modes_Decrease_Lightness_Sample_image_with_dots.png" src="../../_images/Blending_modes_Decrease_Lightness_Sample_image_with_dots.png" />
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Decrease Lightness</strong>.</span><a class="headerlink" href="#id30" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<figure class="align-center" id="id31">
<img alt="../../_images/Blending_modes_Decrease_Value_Sample_image_with_dots.png" src="../../_images/Blending_modes_Decrease_Value_Sample_image_with_dots.png" />
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Decrease Value</strong>.</span><a class="headerlink" href="#id31" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<figure class="align-center" id="id32">
<img alt="../../_images/Blending_modes_Decrease_Luminosity_Sample_image_with_dots.png" src="../../_images/Blending_modes_Decrease_Luminosity_Sample_image_with_dots.png" />
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
<img alt="../../_images/Blending_modes_Decrease_Saturation_HSI_Gray_0.4_and_Gray_0.5.png" src="../../_images/Blending_modes_Decrease_Saturation_HSI_Gray_0.4_and_Gray_0.5.png" />
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Decrease Saturation HSI</strong>.</span><a class="headerlink" href="#id33" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<figure class="align-center" id="id34">
<img alt="../../_images/Blending_modes_Decrease_Saturation_HSI_Light_blue_and_Orange.png" src="../../_images/Blending_modes_Decrease_Saturation_HSI_Light_blue_and_Orange.png" />
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Decrease Saturation HSI</strong>.</span><a class="headerlink" href="#id34" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<figure class="align-center" id="id35">
<img alt="../../_images/Blending_modes_Decrease_Saturation_HSI_Sample_image_with_dots.png" src="../../_images/Blending_modes_Decrease_Saturation_HSI_Sample_image_with_dots.png" />
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Decrease Saturation HSI</strong>.</span><a class="headerlink" href="#id35" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<figure class="align-center" id="id36">
<img alt="../../_images/Blending_modes_Decrease_Saturation_HSL_Sample_image_with_dots.png" src="../../_images/Blending_modes_Decrease_Saturation_HSL_Sample_image_with_dots.png" />
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Decrease Saturation HSL</strong>.</span><a class="headerlink" href="#id36" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<figure class="align-center" id="id37">
<img alt="../../_images/Blending_modes_Decrease_Saturation_HSV_Sample_image_with_dots.png" src="../../_images/Blending_modes_Decrease_Saturation_HSV_Sample_image_with_dots.png" />
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Decrease Saturation HSV</strong>.</span><a class="headerlink" href="#id37" title="Link to this image">¶</a></p>
</figcaption>
</figure>
<figure class="align-center" id="id38">
<img alt="../../_images/Blending_modes_Decrease_Saturation_Sample_image_with_dots.png" src="../../_images/Blending_modes_Decrease_Saturation_Sample_image_with_dots.png" />
<figcaption>
<p><span class="caption-text">Left: <strong>Normal</strong>. Right: <strong>Decrease Saturation</strong>.</span><a class="headerlink" href="#id38" title="Link to this image">¶</a></p>
</figcaption>
</figure>
</section>
</section>
</section>
           </div>
          </div>
          <footer>
    <div class="rst-footer-buttons" role="navigation" aria-label="footer navigation">
        <a href="lighten.html" class="btn btn-neutral float-right" title="Lighten" accesskey="n" rel="next"> <!-- Next --> <span class="fa fa-arrow-circle-right"></span></a>
        <a href="darken.html" class="btn btn-neutral" title="Darken" accesskey="p" rel="prev"><span class="fa fa-arrow-circle-left"></span> <!-- Previous  -->  </a>
    </div>
  <hr/>
  <div role="contentinfo">
    <p>
        &copy; Copyright licensed under the GNU Free Documentation License 1.3+ unless stated otherwise.
        <span class="commit">
          Revision <code>v5.2.0-106-g27972506c8</code>.
        </span>
    </p>
  </div>
  Built with <a href="http://sphinx-doc.org/">Sphinx</a> using a modified <a href="https://github.com/rtfd/sphinx_rtd_theme">RTD theme</a>.<br/>
  <a href="https://krita.org" title="Krita official website.">Krita official website</a> |
  <a href="https://invent.kde.org/documentation/docs-krita-org/" title="The Gitlab instance to edit this pages and collaborate.">Git repository for docs.krita.org </a> |
  <a href="https://www.kde.org/community/whatiskde/impressum-en.php" title="To know more about KDE, code of conduct, privacy policy and GDPR.">KDE Impressum</a>.
</footer>
        </div>
      </div>
    </section>
  </div>
      <script src="../../_static/documentation_options.js?v=2dde5210"></script>
      <script src="../../_static/doctools.js?v=9bcbadda"></script>
      <script src="../../_static/sphinx_highlight.js?v=dc90522c"></script>
    <script type="text/javascript" src="../../_static/js/theme.js"></script>
  <script type="text/javascript">
    document.addEventListener("DOMContentLoaded", function() {
          SphinxRtdTheme.Navigation.enableSticky();
    });
  </script> 
 <script type="text/javascript">
         var _paq=_paq||[];
         _paq.push(['setCookieDomain','*.krita.org']);
         _paq.push(['setDomains','*.krita.org']);
         _paq.push(['setDocumentTitle',document.domain+"/"+document.title]);
         _paq.push(['trackPageView']);
         _paq.push(['enableLinkTracking']);
         (function(){
                var u="//stats.kde.org/";
            _paq.push(['setTrackerUrl',u+'piwik.php']);
            _paq.push(['setSiteId',13]);
            var d = document, g = d.createElement('script'),s=d.getElementsByTagName('script')[0];
            g.type = 'text/javascript';
            g.async = true;
            g.defer = true;
            g.src = u+'piwik.js';
            s.parentNode.insertBefore(g,s);
          })();
</script> 
<noscript><p><img src="//stats.kde.org/piwik.php?idsite=13" style="border:0;" alt="" /></p></noscript>
</body>
</html>'''
        self.path_to_test_file.write_text(test_file_contents, encoding="utf-8")

    def test_split_from_hsx_blendingmodes_pages(self):
        """
        Tests functionality to extract 'blending_modes/hsx' subsubsections.
        """
        soup = bs4.BeautifulSoup(self.path_to_test_file.read_text(encoding="utf-8"), 'html.parser')
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
    Inspects functionality when targeted at 'tools/calligraphy' module.
    """

    def setUp(self):
        """
        Defines path to test file and creates it.
        """
        subdirectory = "tools/"
        filename = "calligraphy.html"
        path_to_test_dir = Path(SOURCE_DIR, subdirectory)
        path_to_test_dir.mkdir(exist_ok=True)
        self.path_to_test_file = path_to_test_dir.joinpath(filename)
        self.path_to_test_file.write_text
        test_file_contents = '''<!DOCTYPE html>
<!--[if IE 8]><html class="no-js lt-ie9" lang="en" > <![endif]-->
<!--[if gt IE 8]><!--> <html class="no-js" lang="en" > <!--<![endif]-->
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta property="og:title" name="title" content="Calligraphy Tool" />
  <meta property="og:site-name" content="Krita Manual" />
  <meta property="og:type" content="article" />
  <meta property="og:locale" content="en" />
  <meta property="og:locale:alternate" content="ca" />
  <meta property="og:locale:alternate" content="fr" />
  <meta property="og:locale:alternate" content="it" />
  <meta property="og:locale:alternate" content="ja" />
  <meta property="og:locale:alternate" content="ko" />
  <meta property="og:locale:alternate" content="nl" />
  <meta property="og:locale:alternate" content="pl" />
  <meta property="og:locale:alternate" content="pt_PT" />
  <meta property="og:locale:alternate" content="pt_BR" />
  <meta property="og:locale:alternate" content="sl" />
  <meta property="og:locale:alternate" content="tr" />
  <meta property="og:locale:alternate" content="uk_UA" />
  <meta property="og:locale:alternate" content="zh_CN" />
  <meta property="og:article:modified_time" content="2025-11-17T09:18:56" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
<meta content="Krita's calligraphy tool reference." lang="en" name="description" xml:lang="en" />
  <title>Calligraphy Tool &mdash; Krita Manual 5.2.0 documentation</title>
    <link rel="shortcut icon" href="../../../../_static/favicon.ico"/>
    <link rel="canonical" href="en/reference_manual/tools/calligraphy.html"/>
    <meta property="og:url" content="en/reference_manual/tools/calligraphy.html" />
    <meta property="og:image" content="en/../../_static/sidebar-logo.png" />
    <link rel="stylesheet" href="../../_static/css/theme.css" type="text/css" />
    <link rel="stylesheet" href="../../_static/pygments.css" type="text/css" />
    <link rel="stylesheet" href="../../_static/pygments.css" type="text/css" />
    <link rel="stylesheet" href="../../_static/css/theme.css" type="text/css" />
    <link rel="index" title="Index" href="../../genindex.html" />
    <link rel="search" title="Search" href="../../search.html" />
    <link rel="next" title="Freehand Brush Tool" href="freehand_brush.html" />
    <link rel="prev" title="Pattern Editing Tool" href="pattern_edit.html" /> 
  <!-- theme and selectors rely on jquery still. currently v3.7.1. Eventually try to migrate off these libraries -->
  <script type="text/javascript" src="../../_static/js/jquery.min.js"></script> 
  <!-- search uses underscore.js to help do some filtering and parsing -->
  <script type="text/javascript" src="../../_static/js/underscore.min.js"></script> 
  <script>
    var $u = _; // Now we can use $u instead of _ throughout your code. (which searchtools.js uses)
  </script>
  <script src="../../_static/js/modernizr.min.js"></script>
</head>
<body class="wy-body-for-nav">
  <div class="wy-grid-for-nav">
    <nav data-toggle="wy-nav-shift" class="wy-nav-side">
      <div class="wy-side-scroll">
        <div class="wy-side-nav-search">
           <a href="../../index.html" class="icon icon-home">
			<img src="../../../../_static/sidebar-logo.png" class="logo" alt="Logo"/>
           	
           <!--	Krita Manual -->
          </a>
<div role="search">
  <form id="rtd-search-form" class="wy-form" action="../../search.html" method="get">
    <input type="text" name="q" placeholder="Search docs" />
    <input type="hidden" name="check_keywords" value="yes" />
    <input type="hidden" name="area" value="default" />
  </form>
</div>
        </div>
        <div class="wy-side-nav-language-selector">
        	<p class="caption-text">
	        	<select id="language-selector-container">
	        		<option value="ca">Català</option>
	        		<option value="en">English</option>
	        		<option value="fr">français</option>
	        		<option value="it">Italiano</option>
	        		<option value="ja">日本語</option>
	        		<option value="ko">한국어</option>
	        		<option value="nl">Nederlands</option>
	        		<option value="pl">Polski</option>
	        		<option value="pt_PT">português</option>
	        		<option value="pt_BR">português brasileiro</option>
                    <option value="sl">slovenščina</option>
                    <option value="tr">Türkçe</option>
	        		<option value="uk_UA">Українська</option>
	        		<option value="zh_CN">简体中文</option>
	        	</select>
        	</p>
        </div>
        <div class="wy-menu wy-menu-vertical" data-spy="affix" role="navigation" aria-label="main navigation">
              <ul class="current">
<li class="toctree-l1"><a class="reference internal" href="../../user_manual.html">User Manual</a></li>
<li class="toctree-l1"><a class="reference internal" href="../../general_concepts.html">General Concepts</a></li>
<li class="toctree-l1 current"><a class="reference internal" href="../../reference_manual.html">Reference Manual</a><ul class="current">
<li class="toctree-l2"><a class="reference internal" href="../audio_for_animation.html">Audio for Animation</a></li>
<li class="toctree-l2"><a class="reference internal" href="../blending_modes.html">Blending Modes</a></li>
<li class="toctree-l2"><a class="reference internal" href="../brushes.html">Brushes</a></li>
<li class="toctree-l2"><a class="reference internal" href="../clones_array.html">Clones Array</a></li>
<li class="toctree-l2"><a class="reference internal" href="../create_new_document.html">Create New Document</a></li>
<li class="toctree-l2"><a class="reference internal" href="../default_python_plugins.html">Pre-installed Python plugins</a></li>
<li class="toctree-l2"><a class="reference internal" href="../dockers.html">Dockers</a></li>
<li class="toctree-l2"><a class="reference internal" href="../dr_minw_debugger.html">Dr. MinGW Debugger</a></li>
<li class="toctree-l2"><a class="reference internal" href="../filters.html">Filters</a></li>
<li class="toctree-l2"><a class="reference internal" href="../hdr_display.html">HDR Display</a></li>
<li class="toctree-l2"><a class="reference internal" href="../image_split.html">Image Split</a></li>
<li class="toctree-l2"><a class="reference internal" href="../import_animation.html">Import Animation</a></li>
<li class="toctree-l2"><a class="reference internal" href="../instant_preview.html">Instant Preview</a></li>
<li class="toctree-l2"><a class="reference internal" href="../krita_4_preset_bundle.html">Krita 4 Preset Bundle Overview</a></li>
<li class="toctree-l2"><a class="reference internal" href="../layers_and_masks.html">Layers and Masks</a></li>
<li class="toctree-l2"><a class="reference internal" href="../linux_command_line.html">Linux Command Line</a></li>
<li class="toctree-l2"><a class="reference internal" href="../main_menu.html">Main Menu</a></li>
<li class="toctree-l2"><a class="reference internal" href="../maths_input.html">Maths Input</a></li>
<li class="toctree-l2"><a class="reference internal" href="../popup-palette.html">Pop-up Palette</a></li>
<li class="toctree-l2"><a class="reference internal" href="../preferences.html">Preferences</a></li>
<li class="toctree-l2"><a class="reference internal" href="../render_animation.html">Render Animation</a></li>
<li class="toctree-l2"><a class="reference internal" href="../resource_management.html">Resource Management</a></li>
<li class="toctree-l2"><a class="reference internal" href="../seexpr.html">SeExpr Quick Reference</a></li>
<li class="toctree-l2"><a class="reference internal" href="../separate_image.html">Separate Image</a></li>
<li class="toctree-l2"><a class="reference internal" href="../sharing_krita_logs.html">Getting Krita logs</a></li>
<li class="toctree-l2"><a class="reference internal" href="../split_layer.html">Split Layer</a></li>
<li class="toctree-l2"><a class="reference internal" href="../storyboard_svg_template.html">SVG Storyboard Export Templates</a></li>
<li class="toctree-l2"><a class="reference internal" href="../stroke_selection.html">Stroke Selection</a></li>
<li class="toctree-l2 current"><a class="reference internal" href="../tools.html">Tools</a><ul class="current">
<li class="toctree-l3"><a class="reference internal" href="shape_selection.html">Shape Selection Tool</a></li>
<li class="toctree-l3"><a class="reference internal" href="shape_edit.html">Shape Edit Tool</a></li>
<li class="toctree-l3"><a class="reference internal" href="text.html">Text Tool</a></li>
<li class="toctree-l3"><a class="reference internal" href="gradient_edit.html">Gradient Editing Tool</a></li>
<li class="toctree-l3"><a class="reference internal" href="pattern_edit.html">Pattern Editing Tool</a></li>
<li class="toctree-l3 current"><a class="current reference internal" href="#">Calligraphy Tool</a><ul>
<li class="toctree-l4"><a class="reference internal" href="#tool-options">Tool Options</a></li>
</ul>
</li>
<li class="toctree-l3"><a class="reference internal" href="freehand_brush.html">Freehand Brush Tool</a></li>
<li class="toctree-l3"><a class="reference internal" href="line.html">Straight Line Tool</a></li>
<li class="toctree-l3"><a class="reference internal" href="rectangle.html">Rectangle Tool</a></li>
<li class="toctree-l3"><a class="reference internal" href="ellipse.html">Ellipse Tool</a></li>
<li class="toctree-l3"><a class="reference internal" href="polygon.html">Polygon Tool</a></li>
<li class="toctree-l3"><a class="reference internal" href="polyline.html">Polyline Tool</a></li>
<li class="toctree-l3"><a class="reference internal" href="path.html">Bezier Curve Tool</a></li>
<li class="toctree-l3"><a class="reference internal" href="freehand_path.html">Freehand Path Tool</a></li>
<li class="toctree-l3"><a class="reference internal" href="dyna.html">Dynamic Brush Tool</a></li>
<li class="toctree-l3"><a class="reference internal" href="multibrush.html">Multibrush Tool</a></li>
<li class="toctree-l3"><a class="reference internal" href="crop.html">Crop Tool</a></li>
<li class="toctree-l3"><a class="reference internal" href="move.html">Move Tool</a></li>
<li class="toctree-l3"><a class="reference internal" href="transform.html">Transform Tool</a></li>
<li class="toctree-l3"><a class="reference internal" href="fill.html">Fill Tool</a></li>
<li class="toctree-l3"><a class="reference internal" href="enclose_and_fill.html">Enclose and Fill Tool</a></li>
<li class="toctree-l3"><a class="reference internal" href="gradient_draw.html">Gradient Tool</a></li>
<li class="toctree-l3"><a class="reference internal" href="color_sampler.html">Color Sampler Tool</a></li>
<li class="toctree-l3"><a class="reference internal" href="colorize_mask.html">Colorize Mask</a></li>
<li class="toctree-l3"><a class="reference internal" href="smart_patch.html">Smart Patch Tool</a></li>
<li class="toctree-l3"><a class="reference internal" href="assistant.html">Assistant Tool</a></li>
<li class="toctree-l3"><a class="reference internal" href="reference_images_tool.html">Reference Images Tool</a></li>
<li class="toctree-l3"><a class="reference internal" href="measure.html">Measure Tool</a></li>
<li class="toctree-l3"><a class="reference internal" href="rectangular_select.html">Rectangular Selection Tool</a></li>
<li class="toctree-l3"><a class="reference internal" href="elliptical_select.html">Elliptical Selection Tool</a></li>
<li class="toctree-l3"><a class="reference internal" href="freehand_select.html">Freehand Selection Tool</a></li>
<li class="toctree-l3"><a class="reference internal" href="polygonal_select.html">Polygonal Selection Tool</a></li>
<li class="toctree-l3"><a class="reference internal" href="contiguous_select.html">Contiguous Selection Tool</a></li>
<li class="toctree-l3"><a class="reference internal" href="path_select.html">Path Selection Tool</a></li>
<li class="toctree-l3"><a class="reference internal" href="similar_select.html">Similar Color Selection Tool</a></li>
<li class="toctree-l3"><a class="reference internal" href="magnetic_select.html">Magnetic Selection Tool</a></li>
<li class="toctree-l3"><a class="reference internal" href="zoom.html">Zoom Tool</a></li>
<li class="toctree-l3"><a class="reference internal" href="pan.html">Pan Tool</a></li>
</ul>
</li>
<li class="toctree-l2"><a class="reference internal" href="../welcome_screen.html">Welcome Screen</a></li>
</ul>
</li>
<li class="toctree-l1"><a class="reference internal" href="../../tutorials.html">Tutorials and How-tos</a></li>
<li class="toctree-l1"><a class="reference internal" href="../../KritaFAQ.html">Krita FAQ</a></li>
<li class="toctree-l1"><a class="reference internal" href="../../contributors_manual.html">Contributors Manual</a></li>
<li class="toctree-l1"><a class="reference internal" href="../../resources_page.html">Resources</a></li>
</ul>
        </div>
      </div>
    </nav>
    <section data-toggle="wy-nav-shift" class="wy-nav-content-wrap">
	<!-- start top banner area (for fundraisers or messages)
	<div style="text-align: center; background-color: #333">
		<a href="https://krita.org/en/fundraising-2018-campaign/" target="_self" onclick="ga('send', 'event', 'frontpage', 'button', 'Fundraiser 2018');">
			<img src="https://krita.org/wp-content/themes/krita-org-theme/images/decoration/2018-fundraiser-banner.png" style="max-width: 100%">
		</a>
	</div>
	
	 end top banner area -->
      <nav class="wy-nav-top" aria-label="top navigation">
          <i data-toggle="wy-nav-top" class="fa fa-bars"></i>
          <a href="../../index.html">Krita Manual</a>
      </nav>
      <div class="wy-nav-content">
        <div class="rst-content">
<div role="navigation" aria-label="breadcrumbs navigation">
  <ul class="wy-breadcrumbs">
      <li><a href="../../index.html">Docs</a> &raquo;</li>
          <li><a href="../../reference_manual.html">Reference Manual</a> &raquo;</li>
          <li><a href="../tools.html">Tools</a> &raquo;</li>
      <li>Calligraphy Tool</li>
      <li class="wy-breadcrumbs-aside">
            <a href="../../_sources/reference_manual/tools/calligraphy.rst.txt" rel="nofollow"> 
              <img src="../../_static/images/source-code.png" />
             <!-- View page source -->
          </a>
      </li>
  </ul>
</div>
          <div role="main" class="document" itemscope="itemscope" itemtype="http://schema.org/Article">
           <div itemprop="articleBody">
  <section id="calligraphy-tool">
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
</section>
           </div>
          </div>
          <footer>
    <div class="rst-footer-buttons" role="navigation" aria-label="footer navigation">
        <a href="freehand_brush.html" class="btn btn-neutral float-right" title="Freehand Brush Tool" accesskey="n" rel="next"> <!-- Next --> <span class="fa fa-arrow-circle-right"></span></a>
        <a href="pattern_edit.html" class="btn btn-neutral" title="Pattern Editing Tool" accesskey="p" rel="prev"><span class="fa fa-arrow-circle-left"></span> <!-- Previous  -->  </a>
    </div>
  <hr/>
  <div role="contentinfo">
    <p>
        &copy; Copyright licensed under the GNU Free Documentation License 1.3+ unless stated otherwise.
        <span class="commit">
          Revision <code>v5.2.0-106-g27972506c8</code>.
        </span>
    </p>
  </div>
  Built with <a href="http://sphinx-doc.org/">Sphinx</a> using a modified <a href="https://github.com/rtfd/sphinx_rtd_theme">RTD theme</a>.<br/>
  <a href="https://krita.org" title="Krita official website.">Krita official website</a> |
  <a href="https://invent.kde.org/documentation/docs-krita-org/" title="The Gitlab instance to edit this pages and collaborate.">Git repository for docs.krita.org </a> |
  <a href="https://www.kde.org/community/whatiskde/impressum-en.php" title="To know more about KDE, code of conduct, privacy policy and GDPR.">KDE Impressum</a>.
</footer>
        </div>
      </div>
    </section>
  </div>
      <script src="../../_static/documentation_options.js?v=2dde5210"></script>
      <script src="../../_static/doctools.js?v=9bcbadda"></script>
      <script src="../../_static/sphinx_highlight.js?v=dc90522c"></script>
    <script type="text/javascript" src="../../_static/js/theme.js"></script>
  <script type="text/javascript">
    document.addEventListener("DOMContentLoaded", function() {
          SphinxRtdTheme.Navigation.enableSticky();
    });
  </script> 
 <script type="text/javascript">
	 var _paq=_paq||[];
	 _paq.push(['setCookieDomain','*.krita.org']);
	 _paq.push(['setDomains','*.krita.org']);
	 _paq.push(['setDocumentTitle',document.domain+"/"+document.title]);
	 _paq.push(['trackPageView']);
	 _paq.push(['enableLinkTracking']);
	 (function(){
	 	var u="//stats.kde.org/";
	    _paq.push(['setTrackerUrl',u+'piwik.php']);
	    _paq.push(['setSiteId',13]);
	    var d = document, g = d.createElement('script'),s=d.getElementsByTagName('script')[0];
	    g.type = 'text/javascript';
	    g.async = true;
	    g.defer = true;
	    g.src = u+'piwik.js';
	    s.parentNode.insertBefore(g,s);
	  })();
</script> 
<noscript><p><img src="//stats.kde.org/piwik.php?idsite=13" style="border:0;" alt="" /></p></noscript>
</body>
</html>'''
        self.path_to_test_file.write_text(test_file_contents, encoding="utf-8")

    @patch("pathlib.Path.write_text")
    def test_write_stripped_soup(self, MOCK_write_text):
        """
        Tests functionality to write HTML after whitespace has been stripped.
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

