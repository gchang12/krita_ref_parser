"""
Defines function for rewriting soup objects to HTML files.
"""

from bs4 import BeautifulSoup

from krita_ref_generator.logging import logger

def format_filename_of_target(filename: str, h2_text: str):
    """
    """
    logger.debug("Old filename: '%s'", filename)
    new_filename = filename.replace('.html', '') \
        + "_" \
        + h2_text.replace(' - ', '-').replace(' ', '-') \
        + ".html"
    logger.debug("Filename after appending header: '%s'", new_filename)
    new_filename = new_filename.replace(' ', '_').lower()
    logger.debug("Filename after replacing ' ' with '_': '%s'", new_filename)
    # remove invalid filename characters
    new_filename = re.sub("[^a-z0-9_.-]", "", new_filename)
    logger.debug("Filename after erasing invalid characters: '%s'. Returning: '%s'", new_filename, new_filename)
    return new_filename

def write_stripped_soup(soup: BeautifulSoup, filename: str):
    """
    """
    logger.debug("Writing lines to '%s'. Calculating number of lines.", filename)
    soup_as_lines = [line.strip() for line in str(soup).splitlines() if line.strip()]
    soup_as_str = "\n".join(soup_as_lines)
    logger.debug("(%d) lines were found in soup. Writing.", len(soup_as_lines))
    Path(filename).write_text(soup_as_str, encoding="utf-8") # returns number of bytes written; unneeded.
    logger.debug("Write operation successful.")
    return

