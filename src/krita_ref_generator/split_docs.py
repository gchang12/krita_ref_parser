"""
Extracts raw excerpts from HTML copy of Krita documentation and splits them into files in the desired filetree.
"""

import re
from pathlib import Path

from bs4 import BeautifulSoup

from krita_ref_generator._logging import logger

SOURCE_DIR = "./input/docs-krita-org/_build/html/reference_manual/"
TARGET_DIR = "./output/raw-excerpts/"

PILCROW = "¶"

def split_from_page(soup: BeautifulSoup):
    """
    """
    sections = [soup.css.select_one("section[id]")]
    logger.debug("(%d) sections found. Returning as list.", len(sections))
    return sections

def split_from_blendingmodes_page(soup: BeautifulSoup):
    """
    """
    sections = list(soup.css.select("section[id] > section[id]"))
    logger.debug("(%d) sections found. Returning as list.", len(sections))
    return sections

def split_from_hsx_blendingmodes_page(soup: BeautifulSoup):
    """
    """
    sections = list(section.css.select("#hsx-blending-modes > section[id]"))
    logger.debug("(%d) sections found. Returning as list.", len(sections))
    return sections

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
    num_lines = len(soup_as_lines)
    logger.debug("(%d) lines were found in soup. Writing.", num_lines)
    Path(filename).write_text(soup_as_str, encoding="utf-8") # returns number of bytes written; unneeded.
    logger.debug("Write operation successful.")
    return num_lines

if __name__ == "__main__":
    def create_main_directories_and_indices():
        """
        Creates main directories and their corresponding index files.
        """
        # create folders, then create index files
        num_directories = 0
        for dirpath in filter(lambda path_: path_.is_dir(), Path(SOURCE_DIR).iterdir()):
            target_subdir = Path(TARGET_DIR, dirpath.name)
            index_path = dirpath.with_suffix(".html")
            # check if directory should be made.
            if not index_path.exists():
                logger.warning("'%s' does not exist. Skipping.", index_path)
                continue
            # create folder
            target_subdir.mkdir(exist_ok=True)
            logger.debug("'%s' now exists.", target_subdir)
            # create index file
            # - get file content
            soup = BeautifulSoup(index_path.read_text(), 'html.parser')
            index_section = split_from_page(soup).pop()
            # - declare filename
            target_indexfile = Path(TARGET_DIR, index_path.name)
            # - write
            num_lines = write_stripped_soup(soup, target_indexfile)
            logger.debug("Wrote (%d) lines to '%s'.", num_lines, target_indexfile)
            num_directories += 1
        logger.info("Created (%d) directories.", num_directories)
    def populate_main_directories():
        """
        """
        for dirpath in filter(lambda path_: path_.is_dir(), Path(SOURCE_DIR).iterdir()):
            logger.info("Populating '%s'.", dirpath)
            num_files = 0
            for filepath in filter(lambda path_: path_.is_file(), dirpath.iterdir()):
                if not filepath.name.endswith(".html"):
                    logger.warning("'%s' is not an HTML file. Skipping.", filepath)
                    continue
                soup = BeautifulSoup(filepath.read_text(), 'html.parser')
                section = split_from_page(soup).pop()
                target_file = Path(TARGET_DIR, dirpath.name, filepath.name)
                num_lines = write_stripped_soup(section, target_file)
                logger.debug("Wrote (%d) lines to '%s'.", num_lines, target_file)
                num_files += 1
            logger.info("(%d) HTML files have been created.", num_files)
    def populate_main_subdirectories():
        """
        """
        for dir_path in filter(lambda path_: path_.is_dir(), Path(SOURCE_DIR).iterdir()):
            # brushes/
            for subdir_path in filter(lambda path_: path_.is_dir(), dir_path.iterdir()):
                # brush_settings/
                target_subsubdir = Path(TARGET_DIR, dir_path.name, subdir_path.name)
                target_subsubdir.mkdir(exist_ok=True)
                logger.info("Populating '%s'.", target_subsubdir)
                num_files = 0
                for filepath in filter(lambda path_: path_.is_file(), subdir_path.iterdir()):
                    if not filepath.name.endswith(".html"):
                        logger.warning("'%s' is not an HTML file. Skipping.", filepath)
                        continue
                    soup = BeautifulSoup(filepath.read_text(), 'html.parser')
                    section = split_from_page(soup).pop()
                    target_file = target_subsubdir.joinpath(filepath.name)
                    num_lines = write_stripped_soup(section, target_file)
                    logger.debug("Wrote (%d) lines to '%s'.", num_lines, target_file)
                    num_files += 1
                logger.info("(%d) HTML files have been created.", num_files)
    def populate_blendingmodes_subdirectories():
        """
        """
        nonalpha_blendingmodes = {
            "Luminosity/Shine (SAI)": "luminosity-shine_sai",
            "Copy Red, Green, Blue": "copy_red-green-blue",
            "P-Norm A": "p-norm_a",
            "P-Norm B": "p-norm_b",
        }
        for filepath in filter(lambda path_: path_.is_file() and path_.name != "hsx.html", Path(TARGET_DIR, "blending_modes").iterdir()):
            # brushes/
            blendingmodes_subdir = Path(TARGET_DIR, "blending_modes", filepath.with_suffix("").name) # TARGET_DIR/'blending_modes'/blending_mode_type/
            blendingmodes_subdir.mkdir(exist_ok=True)
            logger.info("Populating '%s'.", blendingmodes_subdir)
            soup = BeautifulSoup(filepath.read_text(), 'html.parser')
            sections = split_from_blendingmodes_page(soup)
            num_files = 0
            for section in sections:
                #print(section, type(section))
                h2_text = section.find("h2").text.replace(PILCROW, "")
                try:
                    blending_mode = nonalpha_blendingmodes[h2_text]
                except KeyError:
                    blending_mode = h2_text \
                        .replace(" & ", "_and_") \
                        .replace(" - ", "_")
                    blending_mode = re.sub(r" \((.+?)\)", r"_\1", blending_mode)
                    blending_mode = blending_mode \
                        .replace(" ", "-") \
                        .lower()
                target_file = blendingmodes_subdir.joinpath(blending_mode + ".html")
                soup = BeautifulSoup(str(section), 'html.parser')
                num_lines = write_stripped_soup(section, target_file)
                logger.debug("Wrote (%d) lines to '%s'.", num_lines, target_file)
                num_files += 1
            logger.info("(%d) HTML files have been created.", num_files)
    # TODO: Take care of TARGET_DIR/blending_modes/hsx.html

