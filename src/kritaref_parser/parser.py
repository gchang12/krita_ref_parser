"""
"""

# resources to parse:
# - raw html soup
# resources to replace with actual thing:
# - anchors

from pathlib import Path
from collections import OrderedDict
from copy import copy

from bs4 import BeautifulSoup

from _logging import logger

PILCROW = "¶"
CLASS_FOR_LINKS_TO_OFFICIAL_DOCS = "link-to-official-docs"

# TOOLS

def _reset_anchor_tag_sources(section):
    """
    """
    external_root = 'https://docs.krita.org/en/'
    logger.debug("Setting <a> hrefs to reference '%s' instead of '../../'.", external_root)
    for a in section.find_all('a'):
        if "internal" in a['class']:
            href_path = a['href'].split('/')
            a['href'] = external_root + '/'.join(href_path[2:])
            a['class'].remove("internal")
            a['class'].append(CLASS_FOR_LINKS_TO_OFFICIAL_DOCS)
        else:
            logger.debug("The 'class' attribute of the <a> tag: '%s', does not contain 'internal'.", a.string)

def _extract_h_tag(section, *, h_level: int):
    """
    """
    logger.debug("Attempting to find h%d.", h_level)
    h = section.find('h%d' % h_level).extract().text
    logger.debug("Attempting to find pilcrow in: '%s'", h)
    pilcrow_loc = h.index(PILCROW)
    h = h[:pilcrow_loc]
    return h

def _replace_img_sources(section, *, levels=3):
    """
    """
    for img in section.find_all("img"):
        img_src = img['src'].split('/')
        logger.debug("old img_src: %s", img['src'])
        new_img_src = "./images/" + '/'.join(img_src[levels:])
        img['src'] = new_img_src
        logger.debug("new img_src: %s", new_img_src)
        #img['alt'] = new_img_src

def generate_tools_excerpt(soup: BeautifulSoup):
    """
    """
    # get first section[id]
    sections = soup.css.select("section[id]")
    section = sections[0]
    # have all anchor tags reference the actual Krita-Docs website
    # from: '../../'
    # to: 'https://docs.krita.org/en/'
    # for reference: view-source:https://docs.krita.org/en/reference_manual/tools/assistant.html
    # (and add an additional class to this while you're at it)
    _reset_anchor_tag_sources(section)
    # https://www.crummy.com/software/BeautifulSoup/bs4/doc/#extract
    # extract header tag
    # store filename-header pairs as JSON to be returned
    h1 = _extract_h_tag(section, h_level=1)
    # https://www.crummy.com/software/BeautifulSoup/bs4/doc/#changing-tag-names-and-attributes
    # change all image sources:
    # - from: '../../_images/'
    # - to: './images/'
    _replace_img_sources(section)
    # extract icon tag
    try:
        icon = section.find('img').extract()['src']
    except AttributeError:
        logger.warning("Unable to find 'img' in '%s' section.", h1)
        icon = None
    #print(h1, section)
    return (h1, icon, section)

# BLENDING MODES

def _extract_dotsimg(section):
    """
    """
    #caption = section.find("span", class_="caption-text").extract()
    #for caption in section.find_all("figcaption"): caption.extract()
    #caption = section.find.extract()
    dotsimg = None
    for img in section.find_all("img"):
        if img['src'].endswith("_with_dots.png"):
            dotsimg = img.extract()
            logger.debug("Found a dots-image: %s", dotsimg)
            break
    for figure in section.find_all('figure'):
        if figure.find() is None:
            figure.extract()
    #logger.debug("dotsimg: %s", type(dotsimg))
    return dotsimg

def generate_blendingmodes_excerpt(soup: BeautifulSoup):
    """
    """
    # get all section[id] tags
    sections = soup.css.select("section[id]")
    #logger.debug("sections: %s", type(sections))
    subsections = []
    for subsection in sections[1:]:
        #logger.debug("section: %s", type(subsection))
        _reset_anchor_tag_sources(subsection)
        _replace_img_sources(subsection)
        try:
            h_tag = _extract_h_tag(subsection, h_level=2)
        except AttributeError:
            logger.info("No h2 tag was found. Attempting to find h3.")
            h_tag = _extract_h_tag(subsection, h_level=3)
        dotsimg = _extract_dotsimg(subsection)
        if dotsimg is not None:
            dotsimg_src = dotsimg['src']
        else:
            dotsimg_src = None
        subsections.append((h_tag, dotsimg_src, subsection))
        #logger.debug("%s", section)
    return subsections

def generate_hsx_blendingmode_excerpt(soup: BeautifulSoup):
    """
    """
    # I L V Y
    # the usual ministrations
    main_section = soup.find("section", id="hsx")
    _reset_anchor_tag_sources(main_section)
    _replace_img_sources(main_section)
    # compile HS[ILVY] p-text
    hsx_descriptions = OrderedDict(
        {
            "hsi": None,
            "hsl": None,
            "hsv": None,
            "hsy": None,
        }
    )
    for hsx_type in hsx_descriptions:
        hsx_description = main_section.find("section", id=hsx_type)
        p_text = hsx_description.find('p').text
        hsx_descriptions[hsx_type] = p_text
        #print(hsx_type, p_text, "\n")
    # assemble complementary text and image URLs also
    blending_modes = {
        "Color": {},
        "Hue": {},
        "Increase": {},
        "Increase Saturation": {},
        "Intensity": {},
        "Value": {},
        "Lightness": {},
        "Luminosity": {},
        "Saturation": {},
        "Decrease": {},
        "Decrease Saturation": {},
    }
    blendingmode_sections = main_section.css.select("#hsx-blending-modes > section[id]")
    assert len(blending_modes) == len(blendingmode_sections)
    for blending_mode, section in zip(blending_modes, blendingmode_sections):
        # get images
        logger.debug("getting image data.")
        images = []
        for img in section.find_all('img'):
            if img['src'].endswith("_with_dots.png"):
                images.append(img.extract()['src'])
        blending_modes[blending_mode]["images"] = images.copy()
        images.clear()
        # get text
        blending_modes[blending_mode]["soup"] = section
    subsections = []
    # process the exceptions first
    id_to_custom_h3 = OrderedDict(
        {
            "hsi": "Intensity",
            "hsl": "Lightness",
            "hsv": "Value",
            "hsy": "Luminosity",
        }
    )
    for id_, h_tag in id_to_custom_h3.items():
        soupimages_data = blending_modes.pop(h_tag)
        subsection = soupimages_data["soup"]
        # keys: images, soup
        new_p_tag = BeautifulSoup().new_tag(
            "p",
            attrs={"class": "hsx-description"},
            string=hsx_descriptions[id_],
        )
        subsection.append(new_p_tag)
        dotsimg_src = soupimages_data['images'].pop(0)
        for figure in subsection.find_all("figure"):
            fig = figure.extract()
            logger.debug("Extracted figure: %s", fig)
        subsections.append((h_tag, dotsimg_src, subsection))
    for htag_prefix, soupimages_data in blending_modes.items():
        soup = soupimages_data['soup']
        for hsx_type, dotsimg_src in zip(hsx_descriptions, soupimages_data['images']):
            hsx_description = hsx_descriptions[hsx_type]
            new_p_tag = BeautifulSoup().new_tag(
                name="p",
                #class_="hsx-description",
                attrs={"class": "hsx-description"},
                string=hsx_description,
            )
            subsection = copy(soup)
            subsection.append(new_p_tag)
            subsection['class'] "%s %s" % (htag_prefix.lower().replace(' ', '-'), hsx_type)
            if hsx_type != "hsy":
                h_tag = "%s - %s" % (htag_prefix, hsx_type.upper())
            else:
                h_tag = {
                    "Color": "Color",
                    "Hue": "Hue",
                    "Increase": "Increase Luminosity",
                    "Increase Saturation": "Increase Saturation",
                    "Saturation": "Saturation",
                    "Decrease": "Decrease Luminosity",
                    "Decrease Saturation": "Decrease Saturation",
                }[htag_prefix]
            for figure in subsection.find_all("figure"):
                fig = figure.extract()
                logger.debug("Extracted figure: %s", fig)
            subsections.append((h_tag, dotsimg_src, subsection))
    # process the others next
    #return hsx_descriptions, blending_modes
    # we assemble the soup.
    #subsections = []
    #subsections.append((h_tag, dotsimg_src, subsection))
    return subsections

# DOCKERS

def generate_dockers_excerpt(soup: BeautifulSoup):
    """
    """
    section = soup.css.select("section[id]")[0]
    _reset_anchor_tag_sources(section)
    h_tag = _extract_h_tag(section, h_level=1)
    _replace_img_sources(section)
    icon = None
    return (h_tag, icon, section)

# FILTERS

def generate_filters_excerpt(soup: BeautifulSoup):
    """
    """
    section = soup.css.select("section[id]")[0]
    _reset_anchor_tag_sources(section)
    h_tag = _extract_h_tag(section, h_level=1)
    _replace_img_sources(section)
    icon = None
    return (h_tag, icon, section)

# BRUSH ENGINES

def generate_brushengines_excerpt(soup: BeautifulSoup):
    """
    """
    # get first section[id]
    sections = soup.css.select("section[id]")
    section = sections[0]
    # have all anchor tags reference the actual Krita-Docs website
    # from: '../../'
    # to: 'https://docs.krita.org/en/'
    # for reference: view-source:https://docs.krita.org/en/reference_manual/tools/assistant.html
    # (and add an additional class to this while you're at it)
    _reset_anchor_tag_sources(section)
    # https://www.crummy.com/software/BeautifulSoup/bs4/doc/#extract
    # extract header tag
    # store filename-header pairs as JSON to be returned
    h1 = _extract_h_tag(section, h_level=1)
    # https://www.crummy.com/software/BeautifulSoup/bs4/doc/#changing-tag-names-and-attributes
    # change all image sources:
    # - from: '../../_images/'
    # - to: './images/'
    _replace_img_sources(section, levels=4)
    # extract icon tag
    try:
        icon = section.find('img').extract()['src']
    except AttributeError:
        logger.warning("Unable to find 'img' in '%s' section.", h1)
        icon = None
    #print(h1, section)
    return (h1, icon, section)

# BRUSH SETTINGS

def generate_brushsettings_excerpt(soup: BeautifulSoup):
    """
    """
    section = soup.css.select("section[id]")[0]
    _reset_anchor_tag_sources(section)
    h_tag = _extract_h_tag(section, h_level=1)
    _replace_img_sources(section, levels=4)
    icon = None
    return (h_tag, icon, section)

# LAYERS AND MASKS

def generate_layersandmasks_excerpt(soup: BeautifulSoup):
    """
    """
    section = soup.css.select("section[id]")[0]
    _reset_anchor_tag_sources(section)
    h_tag = _extract_h_tag(section, h_level=1)
    _replace_img_sources(section)
    icon = None
    return (h_tag, icon, section)

# MAIN MENU

def generate_mainmenu_excerpt(soup: BeautifulSoup):
    """
    """
    # get first section[id]
    sections = soup.css.select("section[id]")
    section = sections[0]
    # have all anchor tags reference the actual Krita-Docs website
    # from: '../../'
    # to: 'https://docs.krita.org/en/'
    # for reference: view-source:https://docs.krita.org/en/reference_manual/tools/assistant.html
    # (and add an additional class to this while you're at it)
    _reset_anchor_tag_sources(section)
    # https://www.crummy.com/software/BeautifulSoup/bs4/doc/#extract
    # extract header tag
    # store filename-header pairs as JSON to be returned
    h1 = _extract_h_tag(section, h_level=1)
    # https://www.crummy.com/software/BeautifulSoup/bs4/doc/#changing-tag-names-and-attributes
    # change all image sources:
    # - from: '../../_images/'
    # - to: './images/'
    _replace_img_sources(section)
    # extract icon tag
    try:
        icon = section.find('img').extract()['src']
    except AttributeError:
        logger.warning("Unable to find 'img' in '%s' section.", h1)
        icon = None
    #print(h1, section)
    return (h1, icon, section)

# PREFERENCES

def generate_preferences_excerpt(soup: BeautifulSoup):
    """
    """
    # get first section[id]
    sections = soup.css.select("section[id]")
    section = sections[0]
    # have all anchor tags reference the actual Krita-Docs website
    # from: '../../'
    # to: 'https://docs.krita.org/en/'
    # for reference: view-source:https://docs.krita.org/en/reference_manual/tools/assistant.html
    # (and add an additional class to this while you're at it)
    _reset_anchor_tag_sources(section)
    # https://www.crummy.com/software/BeautifulSoup/bs4/doc/#extract
    # extract header tag
    # store filename-header pairs as JSON to be returned
    h1 = _extract_h_tag(section, h_level=1)
    # https://www.crummy.com/software/BeautifulSoup/bs4/doc/#changing-tag-names-and-attributes
    # change all image sources:
    # - from: '../../_images/'
    # - to: './images/'
    _replace_img_sources(section)
    # extract icon tag
    try:
        icon = section.find('img').extract()['src']
    except AttributeError:
        logger.warning("Unable to find 'img' in '%s' section.", h1)
        icon = None
    #print(h1, section)
    return (h1, icon, section)

# RESOURCE MANAGEMENT

def generate_resourcemanagement_excerpt(soup: BeautifulSoup):
    """
    """
    # get first section[id]
    sections = soup.css.select("section[id]")
    section = sections[0]
    # have all anchor tags reference the actual Krita-Docs website
    # from: '../../'
    # to: 'https://docs.krita.org/en/'
    # for reference: view-source:https://docs.krita.org/en/reference_manual/tools/assistant.html
    # (and add an additional class to this while you're at it)
    _reset_anchor_tag_sources(section)
    # https://www.crummy.com/software/BeautifulSoup/bs4/doc/#extract
    # extract header tag
    # store filename-header pairs as JSON to be returned
    h1 = _extract_h_tag(section, h_level=1)
    # https://www.crummy.com/software/BeautifulSoup/bs4/doc/#changing-tag-names-and-attributes
    # change all image sources:
    # - from: '../../_images/'
    # - to: './images/'
    _replace_img_sources(section)
    # extract icon tag
    try:
        icon = section.find('img').extract()['src']
    except AttributeError:
        logger.warning("Unable to find 'img' in '%s' section.", h1)
        icon = None
    #print(h1, section)
    return (h1, icon, section)

if __name__ == "__main__":
    #import logging
    #logging.basicConfig(
        #level=logging.DEBUG,
        #filename=".kritaref_parser.log",
    #)
    # rudimentary test here.
    path = "_src-html/reference_manual/blending_modes/hsx.html"
    with open(path, encoding="utf-8") as rfile:
        soup = BeautifulSoup(rfile, 'html.parser')
    subsections = generate_hsx_blendingmode_excerpt(soup)
    for h_tag, icon, subsection in subsections:
        print(subsection)
        break

