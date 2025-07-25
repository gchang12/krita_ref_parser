"""
Builds images and HTML files from Krita-Docs source.
"""

# IMPORTS

from collections import OrderedDict
from pathlib import Path
import json

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

def make_directories(root, reference_sections):
    """
    Creates mirror-directory that replicates structure of reference folder.
    """
    logger.debug("Making necessary directories.")
    for ref_section in reference_sections:
        path_to_source = Path(root, ref_section)
        path_to_target = Path("excerpts", path_to_source.parts[-1])
        #logger.debug("Checking if %s ought to be made.", path_to_excerpt)
        if not path_to_target.is_dir() and path_to_source.is_dir():
            logger.debug("Creating %s directory.", path_to_target)
            path_to_target.mkdir()

def compile_item(root, ref_section, processing_func):
    """
    Compiles list of 4-tuples.
    """
    path_to_source = Path(root, ref_section)
    logger.debug("Compiling items from: %s", path_to_source)
    if path_to_source.is_dir():
        logger.debug("%s is a directory.", path_to_source)
        def convert_path_to_headericonhtml(ref_file):
            """
            """
            with open(ref_file, encoding="utf-8") as rfile:
                soup = BeautifulSoup(rfile, "html.parser")
            header_icon_html = processing_func(soup)
            #logger.debug("header_icon_html: %r", header_icon_html)
            return ref_file.name, *header_icon_html
        h_icon_html_list = list(
            map(
                convert_path_to_headericonhtml,
                filter(
                    lambda ref_file: ref_file.is_file(),
                    path_to_source.iterdir(),
                ),
            )
        )
    elif path_to_source.is_file():
        logger.debug("%s is a file.", path_to_ref)
        def convert_path_to_headericonhtml(headericonhtml):
            """
            For each HSX section, creates a pseudonym to use as a filename, then returns the object in the ideal format.
            """
            header, icon, soup = headericonhtml
            filename = path_to_ref.with_suffix("").parts[-1] \
                + header.replace(' - ', '-') \
                + ".html"
            filename = filename.lower()
            #assert len(filename, header,icon,html) == 4
            return (filename, header, icon, soup)
        with open(path_to_ref, encoding="utf-8") as rfile:
            soup = BeautifulSoup(rfile, "html.parser")
        h_icon_html_list = list(
            map(
                convert_path_to_headericonhtml,
                processing_func(soup),
            ),
        )
    else:
        logger.warning("What the hell kinda file is %s!?", ref_section)
        h_icon_html_list = None
    return h_icon_html_list

def compile_item_from_list(root, ref_section, processing_func):
    """
    Compiles list of 4-tuples.
    """
    path_to_source = Path(root, ref_section)
    logger.debug("Compiling items from: %s", path_to_source)
    h_icon_html_list = []
    def extend_3tuple_list(path, headericonhtml_list):
        """
        Extends local list variable with 4-tuples using pathlib.Path and list[(..., ..., ...)] as arguments.
        """
        filename_ = path.parts[-1]
        for header, icon, html_soup in headericonhtml_list:
            h_icon_html_list.append(
                (filename_, header, icon, html_soup),
            )
    def convert_path_to_headericonhtml(headericonhtml):
        """
        For each HSX section, creates a pseudonym to use as a filename, then returns the object in the ideal format.
        """
        header, icon, soup = headericonhtml
        filename = path_to_source.with_suffix("").parts[-1] \
            + header.replace(' - ', '-') \
            + ".html"
        filename = filename.lower()
        #assert len(filename, header,icon,html) == 4
        return (filename, header, icon, soup)
    if path_to_source.is_dir():
        for itemfile in path_to_source.iterdir():
            with open(itemfile, encoding="utf-8") as rfile:
                soup = BeautifulSoup(rfile, "html.parser")
            extend_3tuple_list(itemfile, processing_func(soup))
    elif path_to_source.is_file():
        with open(path_to_source, encoding="utf-8") as rfile:
            soup = BeautifulSoup(rfile, "html.parser")
        h_icon_html_list.extend(list(map(convert_path_to_headericonhtml, processing_func(soup))))
    else:
        logger.warning("What the hell kinda file is %s!?", ref_section)
        h_icon_html_list = None
    return h_icon_html_list

def compile_items(root, reference_sections):
    """
    Compiles all page items.
    """
    buffer = []
    logger.debug("Compiling items for index and HTML.")
    for ref_section, processing_func in reference_sections.items():
        logger.debug("Compiling items for %s.", ref_section)
        if "blending_modes/" not in ref_section:
            fileheadericonhtml_list = compile_item(root, ref_section, processing_func)
        else:
            fileheadericonhtml_list = compile_item_from_list(root, ref_section, processing_func)
        if ref_section.count('/') == 1 and "hsx.html" not in ref_section:
            directory = ref_section
        else:
            directory = ref_section.split('/')[-2]
        for value in fileheadericonhtml_list:
            logger.debug("Must unpack value into %d arguments: %r", len(value), [type(attr) for attr in value])
            (filename, header, icon, soup) = value
            buffer.append(
                (directory, filename, header, icon, soup)
            )
        logger.debug("Compilation complete. (%d) items found.", len(fileheadericonhtml_list))
        logger.debug("First item: %s", fileheadericonhtml_list[0])
    return buffer

def write_index(buffer, index_name):
    """
    Writes directory, filename, header, icon to JSON
    """
    #index_name = "kritaref-index.json"
    def get_fileheadericon(kernel_item):
        """
        Turns 4-tuple into dict
        """
        # expect: 5-tuple of the form: directory, (filename, header, icon, soup)
        directory, filename, header, icon, _ = kernel_item
        fileheadericon = {
            "dir": directory,
            "file": filename,
            "header": header,
            "icon": icon,
        }
        return fileheadericon
    out_kernel = list(map(get_fileheadericon, buffer))
    logger.debug("Dumping list into file: %s", index_name)
    with open(index_name, mode="w", encoding="utf-8") as wfile:
        json.dump(out_kernel, wfile, indent=4)

def write_html_output(root, buffer, targetdir):
    """
    Formats and then writes HTML output.
    """
    # write HTML output
    logger.debug("Writing HTML to file.")
    for directory, filename, header, _, soup in buffer:
        # generate dict of sort: {source: ref_section/[filename], header: h, icon: icon}
        path_to_source = Path(root, directory, filename)
        path_to_target = Path(targetdir, directory, filename)
        logger.debug("Writing HTML from %s to %s", path_to_source, path_to_target)
        if path_to_target.is_file():
            logger.warning("%s already exists. Skipping.", path_to_target)
        else:
            # clean html
            html_to_write = "\n".join([line.strip() for line in str(soup).splitlines() if line.strip()])
            logger.debug("html: %d", len(html_to_write))
            path_to_target.write_text(html_to_write, encoding="utf-8")

# resources to delete if not referenced:
# - images
# excerpts/*/*.html
# gather image references from all excerpts
# if image references do not exist, then delete them from the static folder

# delete unused images
def delete_unused_images(excerptdir_root, imagedir_root):
    """
    Deletes images that are not referenced by the compiled HTML files.
    """
    logger.debug("Compiling list of unused images.")
    used_images = set()
    for excerptdir in Path(excerptdir_root).iterdir():
        logger.debug("Searching for files in %s", excerptdir)
        for excerpt_file in excerptdir.iterdir():
            logger.debug("Searching for img['src'] in in %s", excerpt_file)
            with open(excerpt_file, encoding='utf-8') as rfile:
                soup = BeautifulSoup(rfile, 'html.parser')
            for img in soup.find_all('img'):
                used_images.add(Path(img['src']))
    logger.debug("List has been compiled. Count: %d", len(used_images))
    for imagefile in filter(
        lambda imagefile_: imagefile_ not in used_images and not imagefile_.name.startswith('.'),
        Path(imagedir_root).iterdir(),
    ):
        imagefile.unlink()

def halve_blendingmode_dots_images(og_dots_image, imagedir):
    """
    Produces collection of dot-images by blending mode.
    """
    logger.debug("Halving blending-mode dots-images.")
    for imagefile in Path(imagedir).iterdir():
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
    # CONSTANTS
    ROOT = "_src-html/reference_manual/"
    INDEX_NAME = "index.json"
    OG_DOTS_IMAGE = "og_dots_image.png"
    EXCERPTDIR_ROOT = "./excerpts/"
    IMAGEDIR_ROOT = "./images/"
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
    make_directories(ROOT, REFERENCE_SECTIONS)
    buffer = compile_items(ROOT, REFERENCE_SECTIONS)
    write_index(buffer, INDEX_NAME)
    write_html_output(ROOT, buffer, EXCERPTDIR_ROOT)
    delete_unused_images(EXCERPTDIR_ROOT, IMAGEDIR_ROOT)
    halve_blendingmode_dots_images(OG_DOTS_IMAGE, IMAGEDIR_ROOT)

