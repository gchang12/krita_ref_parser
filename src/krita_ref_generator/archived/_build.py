"""
Automatically generates HTML and images for Krita-reference palette.
"""

import re
import shutil
import textwrap
import json
import logging
from pathlib import Path

from bs4 import BeautifulSoup

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
    )
    dirname = "./frontend/kritaref_palette/_app/"
    old_dirname = "./frontend/kritaref_palette/app/"
    #clean_app_directory(dirname)
    src = "./static/"
    tgt = "./frontend/kritaref_palette/public/"
    import_parsed_files(src, tgt)
    excerpt_dir = "./static/excerpts/"
    #app_dir = "./frontend/kritaref_palette/_app/"
    tgt_imgdir = "./frontend/kritaref_palette/public/images/"
    #generate_menu_for_sections_without_icons(excerpt_dir, index, app_dir)
    #generate_menu_for_sections_with_icons(excerpt_dir, index, app_dir)
    #generate_menu_for_blending_modes_without_dots(excerpt_dir, index, app_dir)
    #generate_menu_for_blending_modes_with_dots(excerpt_dir, index, app_dir)
    append_filler_files(excerpt_dir, tgt_imgdir)
    #have_anchor_tags_reference_source(excerpt_dir)

