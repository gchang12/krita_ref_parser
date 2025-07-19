"""
"""

# IMPORTS

#from collections import OrderedDict
from pathlib import Path
import json
#import logging

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

# CONSTANTS

ROOT = "_src-html/reference_manual/"
REFERENCE_SECTIONS = {
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
REFERENCE_KERNEL = {}

# BUILD

def make_directories():
    # make directories
    logger.debug("Making necessary directories.")
    for ref_section in REFERENCE_SECTIONS:
        path_to_ref = Path(ref_section)
        path_to_excerpt = Path("excerpts", path_to_ref.parts[-1])
        logger.debug("Checking if %s ought to be made.", path_to_excerpt)
        if path_to_ref.is_dir() and not path_to_excerpt.is_dir():
            logger.debug("%s directory does not exist yet. Creating...", path_to_excerpt)
            path_to_excerpt.mkdir()


def compile_items():
    logger.debug("Compiling items for index and HTML.")
    for ref_section, processing_func in REFERENCE_SECTIONS.items():
        path_to_ref = Path(ROOT + ref_section)
        logger.debug("Compiling items from: %s", path_to_ref)
        if path_to_ref.is_dir():
            logger.debug("%s is a directory.", path_to_ref)
            def convert_filename_to_hiconhtml(ref_file):
                """
                """
                with open(ref_file, encoding="utf-8") as rfile:
                    soup = BeautifulSoup(rfile, "html.parser")
                h_icon_html = processing_func(soup)
                return ref_file.name, *h_icon_html
            h_icon_html_list = list(map(convert_filename_to_hiconhtml, path_to_ref.iterdir()))
        elif path_to_ref.is_file():
            logger.debug("%s is a file.", path_to_ref)
            with open(path_to_ref, encoding="utf-8") as rfile:
                soup = BeautifulSoup(rfile, "html.parser")
            # TODO: Need new filenames... Implement here, maybe?
            h_icon_html_list = [(path_to_ref.name, *h_icon_html) for h_icon_html in processing_func(soup)]
        else:
            logger.warning("What the hell kinda file is %s!?", ref_section)
            h_icon_html_list = None
        REFERENCE_KERNEL[ref_section] = h_icon_html_list
        logger.debug("Compilation for %s is complete. (%d) items found.", ref_section, len(h_icon_html_list))
        logger.debug("First item: %s", h_icon_html_list[0])

def write_index():
    # write index
    index_name = "kritaref-index.json"
    def get_file_h_icon(kernel_item):
        """
        """
        key, value = kernel_item
        ref_file, h, icon, html_soup = value
        filename = key + ref_file
        file_h_icon = {
            "filename": filename,
            "header": h,
            "icon": icon,
        }
        return file_h_icon
    out_kernel = list(map(get_file_h_icon, REFERENCE_KERNEL.items()))
    file_h_icon = out_kernel[0]
    logger.debug("Got list whose items are of the form: %s.", file_h_icon)
    logger.debug("Opening file: %s", index_name)
    with open(index_name, mode="w", encoding="utf-8") as wfile:
        logger.debug("Dumping list")
        json.dump(out_kernel, wfile, indent=4)

def write_html_output():
    # write HTML output
    logger.debug("Writing HTML to file.")
    for ref_section, filename_h_icon_htmlsoup in REFERENCE_KERNEL.items():
        # generate dict of sort: {source: ref_section/[filename], header: h, icon: icon}
        path_to_ref = Path(ROOT + ref_section)
        path_to_excerpt = Path("excerpts", path_to_ref.parts[-1])
        logger.debug("Writing to file HTML for %s", ref_section)
        for (filename, header, icon, html_soup) in filename_h_icon_htmlsoup:
            logger.debug("%s/%s: %s", ref_section, filename, header)
            if path_to_ref.is_dir():
                logger.debug("Writing HTML for file: %s%s", path_to_ref, filename)
                html_to_write = clean_html(html_soup)
                path_to_excerptfile = path_to_excerpt.joinpath(filename)
            elif path_to_ref.is_file():
                logger.debug("Writing HTML for file: %s", filename)
                html_to_write = clean_html(html_soup)
                path_to_excerptfile = Path(
                    path_to_excerpt.parts[0],
                    ref_section,
                    #path_to_ref.name,
                )
            else:
                raise Exception("What the hell kinda file is %s!?", ref_section)
            path_to_excerptfile.write_text(html_to_write)

# resources to delete if not referenced:
# - images
# excerpts/*/*.html
# gather image references from all excerpts
# if image references do not exist, then delete them from the static folder

# delete unused images
def delete_unused_images():
    logger.debug("Compiling list of unused images.")
    used_images = set()
    for refdir in Path("excerpts/").iterdir():
        for ref_file in refdir.iterdir():
            logger.debug("Searching for files in %s", ref_file)
            with open(ref_file, encoding='utf-8') as rfile:
                soup = BeautifulSoup(rfile, 'html.parser')
            for img in soup.find_all('img'):
                used_images.add(Path(img['src']))
    logger.debug("List has been compiled. Count: %d", len(used_images))
    for imagefile in filter(
        lambda imagefile_: imagefile_ not in used_images,
        Path("./images/").iterdir(),
    ):
        imagefile.unlink()

# blending-mode dots halving
def halve_blendingmode_dots_images():
    og_dots_image = "./images/.og_dots_image.png"
    logger.debug("Halving blending-mode dots-images.")
    for imagefile in Path("./images/").iterdir():
        if not str(imagefile).endswith("_with_dots.png"):
            continue
        if not Path(og_dots_image).exists():
            logger.debug("OG dot image (%s) not found. Parsing from %s, then saving.", og_dots_image, imagefile)
            og_image = halve_image(og_dots_image, get_first_half=True)
            og_image.save(og_dots_image)
        logger.debug("Saving: %s", imagefile)
        blended_image = halve_image(og_dots_image, get_first_half=False)
        blended_image.save(imagefile)

if __name__ == "__main__":
    pass


