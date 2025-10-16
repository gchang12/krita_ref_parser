"""
Builds images and HTML files from Krita-Docs source.
"""

# IMPORTS

from collections import OrderedDict
from pathlib import Path
import re
import json
import shutil
import os

from bs4 import BeautifulSoup

from parser import (
    generate_tools_excerpt,
    generate_blendingmodes_excerpt,
    generate_hsx_blendingmode_excerpt,
    generate_dockers_excerpt,
    generate_filters_excerpt,
    generate_brushengines_excerpt,
    generate_brushsettings_excerpt,
    generate_layersandmasks_excerpt,
    generate_mainmenu_excerpt,
    generate_preferences_excerpt,
    generate_resourcemanagement_excerpt,
)
from picture_processor import (
    halve_image,
)
from _logging import logger

# BUILD

# VESTIGIAL

def append_filler_files(excerpt_dir, tgt_imgdir):
    """
    Writes placeholder files.
    """
    for subdir in Path(excerpt_dir).iterdir():
        howtouse_file = subdir.joinpath("_how-to-use.html")
        logging.debug("Appending file: %s", howtouse_file)
        howtouse_file.write_text("")
        section = subdir.name
        filler_imgpath = Path(tgt_imgdir, f"_{section}-not-found.svg")
        filler_imgpath.write_text("")
        logging.debug("Making filler image file: %s", filler_imgpath)

def make_directories(root, reference_sections, excerptdir_root, imagedir_root):
    """
    Creates mirror-directory that replicates structure of reference folder.
    """
    Path(excerptdir_root).mkdir(exist_ok=True)
    Path(imagedir_root).mkdir(exist_ok=True)
    for ref_section in reference_sections:
        path_to_source = Path(root, ref_section)
        path_to_target = Path(excerptdir_root, path_to_source.parts[-1])
        if not path_to_target.is_dir() and path_to_source.is_dir():
            path_to_target.mkdir()

# resources to delete if not referenced:
# - images
# excerpts/*/*.html
# gather image references from all excerpts
# if image references do not exist, then delete them from the static folder

if __name__ == "__main__":
    # CONSTANTS
    #ROOT = "_src/reference_manual/"
    ROOT = "./krita-docs/_build/html/reference_manual/"
    INDEX_NAME = "./static/index.json"
    OG_DOTS_IMAGE = "og_dots_image.png"
    EXCERPTDIR_ROOT = "./static/excerpts/"
    IMAGEDIR_ROOT = "./static/images/"
    REFERENCE_SECTIONS = OrderedDict(
        {
            "blending_modes/": generate_blendingmodes_excerpt,
            "blending_modes/hsx.html": generate_hsx_blendingmode_excerpt,
            "brushes/brush_settings/": generate_brushsettings_excerpt,
            "brushes/brush_engines/": generate_brushengines_excerpt,
            "dockers/": generate_dockers_excerpt,
            "filters/": generate_filters_excerpt,
            "layers_and_masks/": generate_layersandmasks_excerpt,
            "main_menu/": generate_mainmenu_excerpt,
            "preferences/": generate_preferences_excerpt,
            "resource_management/": generate_resourcemanagement_excerpt,
            "tools/": generate_tools_excerpt,
        }
    )
    # And... go!
    make_directories(ROOT, REFERENCE_SECTIONS, EXCERPTDIR_ROOT, IMAGEDIR_ROOT)
    buffer = compile_items(ROOT, REFERENCE_SECTIONS)
    write_index(buffer, INDEX_NAME)
    write_html_output(ROOT, buffer, EXCERPTDIR_ROOT)
    transfer_images(ROOT, IMAGEDIR_ROOT)
    delete_unused_images(EXCERPTDIR_ROOT, IMAGEDIR_ROOT, OG_DOTS_IMAGE, INDEX_NAME)
    halve_blendingmode_dots_images(OG_DOTS_IMAGE, IMAGEDIR_ROOT)
