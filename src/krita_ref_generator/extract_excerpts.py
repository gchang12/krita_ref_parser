"""
Extracts raw excerpts from HTML copy of Krita documentation.
"""

from bs4 import BeautifulSoup

from krita_ref_generator.logging import logger

SOURCE_DIR = "../../input/docs-krita-org/_build/html/reference_manual/"
TARGET_DIR = "../../output/excerpts/"

def from_page(soup: BeautifulSoup):
    """
    """
    sections = [soup.css.select_one("section[id]")]
    logger.debug("(%d) sections found. Returning as list.", len(sections))
    return sections

def from_blendingmodes_page(soup: BeautifulSoup):
    """
    """
    sections = list(soup.css.select("section[id]")[1:])
    logger.debug("(%d) sections found. Returning as list.", len(sections))
    return sections

def from_hsx_blendingmodes_page(soup: BeautifulSoup):
    """
    """
    sections = list(section.css.select("#hsx-blending-modes > section[id]"))
    logger.debug("(%d) sections found. Returning as list.", len(sections))
    return sections

