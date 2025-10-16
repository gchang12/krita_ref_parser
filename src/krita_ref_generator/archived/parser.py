"""
Defines functions to parse Krita-Reference HTML files and extract section, header, and icon data from them.
_reset_anchor_tag_sources: Sets href for <a> tags to reference official site.
_extract_h_tag: Pops <h[1-6]> tag from HTML soup and returns it.
_replace_img_sources: Sets src attribute of <img> tags in accordance with new filetree structure.
_extract_dotsimg: Pops <img> tags for dot-images and returns their sources. 
generate_*_excerpt: Given a BS object, returns a tuple (header: str, icon: str, section_html: bs4.Tag)
- tools
- blendingmodes: Returns list of normal return-value
- hsx_blendingmode: Returns list of normal return-value
- dockers
- filters
- brushengines
- brushsettings
- layersandmasks
- mainmenu
- preferences
- resourcemanagement
"""

import copy
from collections import OrderedDict
from pathlib import Path

from bs4 import BeautifulSoup

from _logging import logger

# -AUXILIARY-

# TODO: Remember why I needed this.
#caption = section.find("span", class_="caption-text").extract()
#for caption in section.find_all("figcaption"): caption.extract()
#caption = section.find.extract()

# TOOLS

def generate_tools_excerpt(soup: BeautifulSoup):
    """
    Generates HTML excerpt and returns it alongside header and icon.
    """
    return _generate_excerpt_with_icon(soup, h_level=1, levels=3, exclude=['color-sampler-tool'])

# BLENDING MODES

# DOCKERS

def generate_dockers_excerpt(soup: BeautifulSoup):
    """
    For 'Dockers' section.
    """
    return _generate_excerpt_without_icon(soup, h_level=1, levels=3)

# FILTERS

def generate_filters_excerpt(soup: BeautifulSoup):
    """
    For 'Filters' section.
    """
    return _generate_excerpt_without_icon(soup, h_level=1, levels=3)

# BRUSH ENGINES

def generate_brushengines_excerpt(soup: BeautifulSoup):
    """
    For 'Brush Engines' section.
    """
    return _generate_excerpt_with_icon(soup, levels=4, h_level=1, exclude=['chalk-brush-engine'])

# BRUSH SETTINGS

def generate_brushsettings_excerpt(soup: BeautifulSoup):
    """
    For 'Brush Settings' section.
    """
    return _generate_excerpt_without_icon(soup, h_level=1, levels=4)

# LAYERS AND MASKS

def generate_layersandmasks_excerpt(soup: BeautifulSoup):
    """
    For 'Layers and Masks' section.
    """
    return _generate_excerpt_without_icon(soup, h_level=1, levels=3)

# MAIN MENU

def generate_mainmenu_excerpt(soup: BeautifulSoup):
    """
    For 'Main Menu' section.
    """
    return _generate_excerpt_without_icon(soup, levels=3, h_level=1)

# PREFERENCES

def generate_preferences_excerpt(soup: BeautifulSoup):
    """
    For 'Preferences' section.
    """
    return _generate_excerpt_without_icon(soup, levels=3, h_level=1)

# RESOURCE MANAGEMENT

def generate_resourcemanagement_excerpt(soup: BeautifulSoup):
    """
    For 'Resource Management' section.
    """
    return _generate_excerpt_without_icon(soup, levels=3, h_level=1)

if __name__ == "__main__":
    path = "_src/reference_manual/blending_modes/hsx.html"
    with open(path, encoding="utf-8") as rfile:
        soup = BeautifulSoup(rfile, 'html.parser')
    subsections = generate_hsx_blendingmode_excerpt(soup)
    for h_tag, icon, subsection in subsections:
        break

