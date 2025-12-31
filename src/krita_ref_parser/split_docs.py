"""
Extracts raw excerpts from HTML copy of Krita documentation and splits them into files in the desired filetree.
"""

import re
from pathlib import Path

from bs4 import BeautifulSoup

from krita_ref_parser._logging import logger

PILCROW = "¶"

SOURCE_DIR = "./input/docs-krita-org/_build/html/reference_manual/"
TARGET_DIR = "./output/raw-excerpts/"

def split_from_page(soup: BeautifulSoup):
    """
    Returns first <section> in `soup` in a list.
    """
    sections = [soup.css.select_one("section[id]")]
    logger.debug("(%d) sections found. Returning as list.", len(sections))
    return sections

def split_from_blendingmodes_page(soup: BeautifulSoup):
    """
    Returns all <section> parented by <section> from `soup`.
    """
    sections = list(soup.css.select("section[id] > section[id]"))
    logger.debug("(%d) sections found. Returning as list.", len(sections))
    return sections

def split_from_hsx_blendingmodes_page(soup: BeautifulSoup):
    """
    Returns all <section> parented by '#hsx-blending-modes' in `soup`.
    """
    sections = list(soup.css.select("#hsx-blending-modes > section[id]"))
    logger.debug("(%d) sections found. Returning as list.", len(sections))
    return sections

def write_stripped_soup(soup: BeautifulSoup, filename: str):
    """
    Strips whitespace from `soup` and writes it to `filename`.
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
    import subprocess

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
            target_subdir.mkdir(exist_ok=True, parents=True)
            logger.debug("'%s' now exists.", target_subdir)
            # create index file
            # - get file content
            soup = BeautifulSoup(index_path.read_text(), 'html.parser')
            section = split_from_page(soup).pop()
            # - declare filename
            target_indexfile = Path(TARGET_DIR, index_path.name)
            # - write
            num_lines = write_stripped_soup(section, target_indexfile)
            logger.debug("Wrote (%d) lines to '%s'.", num_lines, target_indexfile)
            num_directories += 1
        logger.info("Created (%d) directories.", num_directories)

    def populate_main_directories():
        """
        Parses first-level <section> from source and writes each <section> to one file.
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
        Parses most second-level <section> and writes each <section> to a file.
        """
        for dir_path in filter(lambda path_: path_.is_dir(), Path(SOURCE_DIR).iterdir()):
            # brushes/
            for subdir_path in filter(lambda path_: path_.is_dir(), dir_path.iterdir()):
                # brush_settings/
                target_subsubdir = Path(TARGET_DIR, dir_path.name, subdir_path.name)
                target_subsubdir.mkdir(exist_ok=True, parents=True)
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
        Creates new 'blending_modes' subdirectories and populates them.
        """
        for filepath in filter(lambda path_: path_.is_file() and path_.name != "hsx.html", Path(TARGET_DIR, "blending_modes").iterdir()):
            # brushes/
            blendingmodes_subdir = Path(TARGET_DIR, "blending_modes", filepath.with_suffix("").name) # TARGET_DIR/'blending_modes'/blending_mode_type/
            blendingmodes_subdir.mkdir(exist_ok=True, parents=True)
            logger.info("Populating '%s'.", blendingmodes_subdir)
            soup = BeautifulSoup(filepath.read_text(), 'html.parser')
            sections = split_from_blendingmodes_page(soup)
            num_files = 0
            for section in sections:
                blending_mode = section['id']
                target_file = blendingmodes_subdir.joinpath(blending_mode + ".html")
                soup = BeautifulSoup(str(section), 'html.parser')
                num_lines = write_stripped_soup(section, target_file)
                logger.debug("Wrote (%d) lines to '%s'.", num_lines, target_file)
                num_files += 1
            logger.info("(%d) HTML files have been created.", num_files)

    def populate_hsx_blendingmodes_subdirectories():
        """
        Creates HSX 'blending_modes' subdirectory and populates it.
        """
        filepath = Path(TARGET_DIR, "blending_modes", "hsx.html")
        hsx_blendingmode_subdir = filepath.with_suffix("")
        hsx_blendingmode_subdir.mkdir(exist_ok=True, parents=True)
        logger.info("Populating '%s'.", hsx_blendingmode_subdir)
        soup = BeautifulSoup(filepath.read_text(), 'html.parser')
        sections = split_from_hsx_blendingmodes_page(soup)
        num_files = 0
        for section in sections:
            blending_mode = section['id']
            target_file = hsx_blendingmode_subdir.joinpath(blending_mode + ".html")
            soup = BeautifulSoup(str(section), 'html.parser')
            num_lines = write_stripped_soup(section, target_file)
            logger.debug("Wrote (%d) lines to '%s'.", num_lines, target_file)
            num_files += 1
        logger.info("(%d) HTML files have been created.", num_files)

    def inspect_output(filename: str, to_inspect: bool):
        """
        Pauses program to let user inspect text output via 'vim '.
        """
        args = ["vi"]
        root_dir = "output/raw-excerpts"
        args.append("/".join([TARGET_DIR, filename]))
        if to_inspect:
            subprocess.run(args)
        else:
            logger.debug("Skipped execution of command: %s", " ".join(args))

    def split_docs(*, to_inspect: bool):
        """
        Populates `TARGET_DIR` while mostly retaining original filetree structure.
        """
        filename: str
        create_main_directories_and_indices()
        print("Created main directories and indices in: '%s'" % TARGET_DIR)
        filename = "dockers.html"
        inspect_output(filename, to_inspect=to_inspect)
        populate_main_directories()
        print("Populated main directories.")
        filename = "filters/map.html"
        inspect_output(filename, to_inspect=to_inspect)
        populate_main_subdirectories()
        print("Populated main subdirectories.")
        filename = "brushes/brush_settings/options.html"
        inspect_output(filename, to_inspect=to_inspect)
        populate_blendingmodes_subdirectories()
        print("Populated blending-mode subdirectories.")
        filename = "blending_modes/arithmetic/addition.html"
        inspect_output(filename, to_inspect=to_inspect)
        populate_hsx_blendingmodes_subdirectories()
        print("Populated blending-mode-hsx subdirectory.")
        filename = "blending_modes/hsx/increase-value_lightness-intensity-luminosity.html"
        inspect_output(filename, to_inspect=to_inspect)

    def scan_files_for_script_nodes():
        """
        Raises Exception if any parsed content contains a <script> node.
        """
        logger.info("Now scanning all <section> contents for <script> nodes.")
        for dirpath, dirnames, filenames in Path(TARGET_DIR).walk():
            logger.debug("Scanning files in '%s'.", dirpath)
            for filename in filenames:
                filepath = dirpath.joinpath(filename)
                soup = BeautifulSoup(filepath.read_text(encoding="utf-8"), "html.parser")
                script_node = soup.css.select_one("script")
                if script_node is None:
                    continue
                raise Exception("'%s' contains a <script> tag." % filepath)
            logger.debug("'%s' contained no files with <script> nodes.", dirpath)
        logger.info("No <section> contained a <script> tag.")

    split_docs(to_inspect=False)
    scan_files_for_script_nodes()

