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

PILCROW = "¶"
CLASS_FOR_LINKS_TO_OFFICIAL_DOCS = "link-to-official-docs"
BLENDINGMODE_LIST = (
    "Color",
    "Hue",
    "Increase",
    "Increase Saturation",
    "Intensity",
    "Value",
    "Lightness",
    "Luminosity",
    "Saturation",
    "Decrease",
    "Decrease Saturation",
)

# -AUXILIARY-

def _reset_anchor_tag_sources(section):
    """
    Sets href for <a> to links s.t. they reference official Krita docs.
    """
    # have all anchor tags reference the actual Krita-Docs website
    # from: '../../'
    # to: 'https://docs.krita.org/en/'
    # for reference: view-source:https://docs.krita.org/en/reference_manual/tools/assistant.html
    # (and add an additional class to this while you're at it)
    external_root = 'https://docs.krita.org/en/'
    #logger.debug("Setting <a> hrefs to reference '%s' instead of '../../'.", external_root)
    for a in filter(lambda a_: "internal" in a_['class'], section.find_all('a')):
        #href_path = a['href'].split('/')
        #a['href'] = external_root + '/'.join(href_path[2:])
        #a['class'].remove("internal")
        #a['class'].append(CLASS_FOR_LINKS_TO_OFFICIAL_DOCS)
        pass

def _extract_h_tag(section, *, h_level: int):
    """
    Pops <h[1-6]> tag from HTML soup `section` and returns it.
    """
    # https://www.crummy.com/software/BeautifulSoup/bs4/doc/#extract
    # extract header tag
    # store filename-header pairs as JSON to be returned
    #logger.debug("Searching for tag: h%d", h_level)
    h = section.find('h%d' % h_level).extract().text
    #logger.debug("Searching for pilcrow in: '%s'", h)
    pilcrow_loc = h.index(PILCROW)
    h = h[:pilcrow_loc]
    #logger.debug("Returning: %r", h)
    return h

def _replace_img_sources(section, *, levels):
    """
    Replaces src attributes in <img> tags to match new filetree.
    """
    # https://www.crummy.com/software/BeautifulSoup/bs4/doc/#changing-tag-names-and-attributes
    # change all image sources:
    # - from: '../../_images/'
    # - to: './images/'
    #logger.debug("Replacing `img-src` to ./images/`img-src[%d:]`", levels)
    for img in section.find_all("img"):
        img_src = img['src'].split('/')
        #logger.debug("Found `img-src`: %s", img['src'])
        # TODO: Delete leading './'
        new_img_src = "../../images/" + '/'.join(img_src[levels:])
        img['src'] = new_img_src
        #logger.debug("Set `img-src`: %s", new_img_src)

# TODO: Remember why I needed this.
#caption = section.find("span", class_="caption-text").extract()
#for caption in section.find_all("figcaption"): caption.extract()
#caption = section.find.extract()

def _extract_dotsimg(section):
    """
    Pops first dots-img tag in a section.
    """
    dotsimg = None
    #logger.debug("Searching for <img> tag where src.endswith('_with_dots.png')")
    for img in section.find_all("img"):
        if img['src'].endswith("_with_dots.png"):
            dotsimg = img.extract()
            #logger.debug("Dots-image found: %s. Returning.", dotsimg)
            break
    return dotsimg

def _generate_excerpt_with_icon(soup: BeautifulSoup, *, levels, h_level, exclude=()):
    """
    Given a BS object, returns a tuple (header: str, icon: str, section_html: bs4.Tag)

    This function is for pages whose content has icons.
    """
    section = soup.select_one("section[id]")
    _reset_anchor_tag_sources(section)
    h1 = _extract_h_tag(section, h_level=h_level)
    _replace_img_sources(section, levels=levels)
    if section['id'] in exclude:
        icon = None
    else:
        try:
            icon = section.find('img').extract()['src']
        except AttributeError:
            #logger.info("Unable to find 'img' in '%s' section.", h1)
            icon = None
    return (h1, icon, section)

# TOOLS

def generate_tools_excerpt(soup: BeautifulSoup):
    """
    Generates HTML excerpt and returns it alongside header and icon.
    """
    return _generate_excerpt_with_icon(soup, h_level=1, levels=3, exclude=['color-sampler-tool'])

# BLENDING MODES

def generate_blendingmodes_excerpt(soup: BeautifulSoup):
    """
    Compiles list of (header, dotsimg-src, html-soup) objects from `soup`.

    This works for all subsections except for HSX.
    """
    sections = []
    #logger.debug("Compiling list of (header, icon, section_html) objects.")
    for section in soup.css.select("section[id]")[1:]:
        _reset_anchor_tag_sources(section)
        _replace_img_sources(section, levels=3)
        try:
            h_tag = _extract_h_tag(section, h_level=2)
        except AttributeError:
            #logger.info("No <h2> tag was found. Getting <h3>.")
            h_tag = _extract_h_tag(section, h_level=3)
        dotsimg = _extract_dotsimg(section)
        if dotsimg is not None:
            dotsimg_src = dotsimg['src']
        else:
            dotsimg_src = None
        #logger.debug("Header: %s, Dots-Image: %s, Section.Length: %d", h_tag, dotsimg_src, len(section))
        sections.append((h_tag, dotsimg_src, section))
    #logger.debug("(%d) sections found in soup.", len(sections))
    return sections

def generate_hsx_blendingmode_excerpt(soup: BeautifulSoup):
    """
    Compiles list of (header, dotsimg-src, html-soup) objects from `soup`.

    This works only for the HSX subsections.
    """
    # I L V Y
    # the usual ministrations
    section = soup.find("section", id="hsx")
    _reset_anchor_tag_sources(section)
    _replace_img_sources(section, levels=3)
    # compile HS[ILVY] p-text
    def compile_hsx_paragraph(hsx):
        """
        Gets paragraph text for a given HSX type.
        """
        return (hsx, section
            .find("section", id=hsx)
            .find('p')
            .text,
        )
    hsx_paragraphs = OrderedDict(
        map(
            compile_hsx_paragraph,
            ("hsi", "hsl", "hsv", "hsy"),
        )
    )
    # assemble complementary text and image URLs also
    # get blending mode dot-images and soup
    blendingmode_sections = section.css.select("#hsx-blending-modes > section[id]")
    assert len(BLENDINGMODE_LIST) == len(blendingmode_sections)
    def get_blendingmode_images_and_soup(namesection):
        """
        Gets images and soup from name-section tuple.
        """
        name, subsection = namesection
        dots_images = []
        #logger.debug("Getting images and soup for: %s", name)
        num_images = 0
        for img in filter(
            lambda img_: img_['src'].endswith("_with_dots.png"),
            subsection.find_all('img'),
        ):
            dots_image = img.extract()['src']
            dots_images.append(dots_image)
            num_images += 1
        #logger.debug("(%d) images found.", num_images)
        return (name, (dots_images, subsection))
    images_and_soup = dict(
        map(
            get_blendingmode_images_and_soup,
            zip(BLENDINGMODE_LIST, blendingmode_sections),
        )
    )
    # end: get blending mode dot-images
    subsections = []
    # process the exceptions first
    for hsx, blending_mode in (
        ("hsi", "Intensity"),
        ("hsl", "Lightness"),
        ("hsv", "Value"),
        ("hsy", "Luminosity"),
    ):
        dots_images, subsection = images_and_soup.pop(blending_mode)
        # keys: images, soup
        hsx_paragraph = BeautifulSoup().new_tag(
            "p",
            attrs={"class": "hsx-paragraph"},
            string=hsx_paragraphs[hsx],
        )
        subsection.append(hsx_paragraph)
        subsection.attrs['class'] = []
        subsection['class'].append(blending_mode.lower())
        subsection['class'].append(hsx)
        #logger.debug("Compiling (header, dotsimg_src, section) for (%s, %s).", hsx, blending_mode)
        dotsimg_src = dots_images.pop(0)
        num_figures = 0
        for figure in subsection.find_all("figure"):
            figure.extract()
            num_figures += 1
        #logger.debug("(%d) figures deleted.", num_figures)
        h_tag = blending_mode
        subsections.append((h_tag, dotsimg_src, subsection))
    for blending_mode, (dots_images, subsection_) in images_and_soup.items():
        for (hsx, hsx_paragraph), dotsimg_src in zip(hsx_paragraphs.items(), dots_images):
            hsx_paragraph = BeautifulSoup().new_tag(
                name="p",
                attrs={"class": "hsx-paragraph"},
                string=hsx_paragraph,
            )
            subsection = copy.copy(subsection_)
            subsection.attrs['class'] = []
            subsection['class'].append(
                blending_mode.lower().replace(' ', '-'),
            )
            subsection['class'].append(hsx)
            subsection.append(hsx_paragraph)
            if hsx != "hsy":
                h_tag = "%s - %s" % (blending_mode, hsx.upper())
            else:
                h_tag = {
                    "Color": "Color",
                    "Hue": "Hue",
                    "Increase": "Increase Luminosity",
                    "Increase Saturation": "Increase Saturation",
                    "Saturation": "Saturation",
                    "Decrease": "Decrease Luminosity",
                    "Decrease Saturation": "Decrease Saturation",
                }[blending_mode]
            num_figures = 0
            for figure in subsection.find_all("figure"):
                figure.extract()
                num_figures += 1
            #logger.debug("(%d) figures deleted.", num_figures)
            subsections.append((h_tag, dotsimg_src, subsection))
    return subsections

def _generate_excerpt_without_icon(soup: BeautifulSoup, *, h_level, levels):
    """
    Returns a (header, icon, section) object for a section without a header icon.

    Must provide `h_level` to specify the type of subsection header to extract.
    Must provide `levels` to specify how deep into the filetree the file for the section is.
    """
    section = soup.css.select("section[id]")[0]
    _reset_anchor_tag_sources(section)
    h_tag = _extract_h_tag(section, h_level=h_level)
    _replace_img_sources(section, levels=levels)
    icon = None
    return (h_tag, icon, section)

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

