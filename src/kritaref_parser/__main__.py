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

def _format_target_filename(filename_root, header):
    """
    """
    #filename_root = path_to_source.name
    #logger.debug("filename: %s, header: %s", filename, header)
    filename =  filename_root.replace('.html', '') \
        + "_" \
        + header.replace(' - ', '-').replace(' ', '-') \
        + ".html"
    filename = filename.replace(' ', '_').lower()
    filename = re.sub("[^a-z0-9_.-]", "", filename)
    return filename

# BUILD

def make_directories(root, reference_sections):
    """
    Creates mirror-directory that replicates structure of reference folder.
    """
    #logger.debug("Making necessary directories.")
    Path("excerpts").mkdir(exist_ok=True)
    Path("images").mkdir(exist_ok=True)
    for ref_section in reference_sections:
        path_to_source = Path(root, ref_section)
        path_to_target = Path("excerpts", path_to_source.parts[-1])
        #logger.debug("Checking if %s ought to be made.", path_to_excerpt)
        if not path_to_target.is_dir() and path_to_source.is_dir():
            #logger.debug("Creating %s directory.", path_to_target)
            path_to_target.mkdir()

def compile_item(root, ref_section, processing_func):
    """
    Compiles list of 4-tuples.
    """
    path_to_source = Path(root, ref_section)
    #logger.debug("Compiling items from: %s", path_to_source)
    if path_to_source.is_dir():
        #logger.debug("%s is a directory.", path_to_source)
        def convert_path_to_headericonhtml(ref_file):
            """
            """
            with open(ref_file, encoding="utf-8") as rfile:
                soup = BeautifulSoup(rfile, "html.parser")
            header_icon_html = processing_func(soup)
            #logger.debug("header_icon_html: %r", header_icon_html)
            header, icon, soup = header_icon_html
            #header = header_icon_html[0]
            #logger.debug("filename: %s", filename)
            #logger.debug('header: %s', header)
            filename = ref_file.name
            return filename, filename, *header_icon_html
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
        #logger.debug("%s is a file.", path_to_ref)
        def convert_path_to_headericonhtml(headericonhtml):
            """
            For each HSX section, creates a pseudonym to use as a filename, then returns the object in the ideal format.
            """
            header, icon, soup = headericonhtml
            filename = filename.lower()
            #logger.debug('filename: %s', filename)
            #logger.debug('header: %s', header)
            #assert len(filename, header,icon,html) == 4
            return (filename, filename, header, icon, soup)
        with open(path_to_ref, encoding="utf-8") as rfile:
            soup = BeautifulSoup(rfile, "html.parser")
        h_icon_html_list = list(
            map(
                convert_path_to_headericonhtml,
                processing_func(soup),
            ),
        )
    else:
        #logger.warning("What the hell kinda file is %s!?", ref_section)
        h_icon_html_list = None
    return h_icon_html_list

def compile_item_from_list(root, ref_section, processing_func):
    """
    Compiles list of 4-tuples.
    """
    path_to_source = Path(root, ref_section)
    #logger.debug("Compiling items from: %s", path_to_source)
    h_icon_html_list = []
    def extend_3tuple_list(path, headericonhtml_list):
        """
        Extends local list variable with 4-tuples using pathlib.Path and list[(..., ..., ...)] as arguments.
        """
        filename_root = path.parts[-1]
        for header, icon, html_soup in headericonhtml_list:
            filename = _format_target_filename(filename_root, header)
            h_icon_html_list.append(
                (filename_root, filename, header, icon, html_soup),
            )
            #logger.debug("filename: %s, header: %s", filename_root, header)
    def convert_path_to_headericonhtml(headericonhtml):
        """
        For each HSX section, creates a pseudonym to use as a filename, then returns the object in the ideal format.
        """
        header, icon, soup = headericonhtml
        #logger.debug("path_to_source: %s", path_to_source)
        filename_root = path_to_source.name
        #logger.debug("filename: %s, header: %s", filename, header)
        filename = _format_target_filename(filename_root, header)
        return (filename_root, filename, header, icon, soup)
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
        #logger.warning("What the hell kinda file is %s!?", ref_section)
        h_icon_html_list = None
    return h_icon_html_list

def compile_items(root, reference_sections):
    """
    Compiles all page items.
    """
    buffer = []
    for ref_section, processing_func in reference_sections.items():
        #logger.debug("Compiling items for %s.", ref_section)
        if "blending_modes/" not in ref_section:
            fileheadericonhtml_list = compile_item(root, ref_section, processing_func)
        else:
            fileheadericonhtml_list = compile_item_from_list(root, ref_section, processing_func)
        if ref_section.count('/') == 1 and "hsx.html" not in ref_section:
            directory = ref_section
        else:
            directory = ref_section.split('/')[-2]
        for value in fileheadericonhtml_list:
            #logger.debug("Must unpack value into %d arguments: %r", len(value), [type(attr) for attr in value])
            (source, target, header, icon, soup) = value
            #filename = filename.replace('.html', '') + "_" + header.replace(' ', "_") + '.html'
            #filename = filename.lower()
            buffer.append(
                (directory, source, target, header, icon, soup)
            )
        #logger.debug("Compilation complete. (%d) items found.", len(fileheadericonhtml_list))
        #logger.debug("First item: %s", fileheadericonhtml_list[0])
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
        directory, source, target, header, icon, _ = kernel_item
        fileheadericon = {
            "dir": directory.rstrip('/') + "/",
            "file": target,
            "header": header,
            "icon": icon,
        }
        return fileheadericon
    out_kernel = list(map(get_fileheadericon, buffer))
    #logger.debug("Dumping list into file: %s", index_name)
    with open(index_name, mode="w", encoding="utf-8") as wfile:
        json.dump(out_kernel, wfile, indent=4)

def write_html_output(root, buffer, targetdir):
    """
    Formats and then writes HTML output.
    """
    # write HTML output
    #logger.debug("Writing HTML to file.")
    for directory, source, target, header, _, soup in buffer:
        # generate dict of sort: {source: ref_section/[filename], header: h, icon: icon}
        path_to_source = Path(root, directory, source)
        path_to_target = Path(targetdir, directory, target)
        #logger.debug("Writing HTML from %s to %s", path_to_source, path_to_target)
        if path_to_target.is_file():
            logger.warning("%s already exists for %s-%s: %s", path_to_target, source, header, soup)
        # clean html
        html_to_write = "\n".join([line.strip() for line in str(soup).splitlines() if line.strip()])
        #logger.debug("html: %d", len(html_to_write))
        path_to_target.write_text(html_to_write, encoding="utf-8")

# resources to delete if not referenced:
# - images
# excerpts/*/*.html
# gather image references from all excerpts
# if image references do not exist, then delete them from the static folder

def transfer_images(root, imagedir_root):
    """
    Copies all images from source to output.
    """
    #os.chmod(imagedir_root, 0o555)
    for imagefile in Path(root, "..", "_images").iterdir():
        shutil.copyfile(imagefile, Path(imagedir_root, imagefile.name))

# delete unused images
def delete_unused_images(excerptdir_root, imagedir_root, og_dots_image, index_name):
    """
    Deletes images that are not referenced by the compiled HTML files.
    """
    #logger.debug("Compiling list of unused images.")
    #used_images = set()
    with open(index_name, encoding="utf-8") as rfile:
        index = json.load(rfile)
    #print(index)
    used_images = set(Path(record['icon']).name for record in index if record['icon'] is not None)
    #logger.debug("List has been compiled. Count: %d", len(used_images))
    #print(used_images)
    for excerpt_dir in Path(excerptdir_root).iterdir():
        for excerpt_file in excerpt_dir.iterdir():
            with open(excerpt_file, encoding="utf-8") as rfile:
                soup = BeautifulSoup(rfile, "html.parser")
            for img in soup.find_all('img'):
                img_src = Path(img['src']).name
                used_images.add(img_src)
    for imagefile in Path(imagedir_root).iterdir():
        if imagefile.name == og_dots_image:
            continue
        if imagefile.is_dir():
            continue
        if imagefile.name in used_images:
            continue
        imagefile.unlink()

def halve_blendingmode_dots_images(og_dots_image, imagedir):
    """
    Produces collection of dot-images by blending mode.
    """
    #logger.debug("Halving blending-mode dots-images.")
    for imagefile in Path(imagedir).iterdir():
        if not str(imagefile).endswith("_with_dots.png"):
            continue
        if imagefile.name == og_dots_image:
            continue
        if not Path(imagedir, og_dots_image).exists():
            #logger.debug("OG dot image (%s) not found. Parsing from %s, then saving.", og_dots_image, imagefile)
            og_image = halve_image(imagefile, get_first_half=True)
            og_image.save('/'.join([imagedir, og_dots_image]))
        #logger.debug("Saving: %s", imagefile)
        blended_image = halve_image(imagefile, get_first_half=False)
        blended_image.save(imagefile)

if __name__ == "__main__":
    # CONSTANTS
    #ROOT = "_src/reference_manual/"
    ROOT = "../../krita-docs/_build/html/reference_manual/"
    INDEX_NAME = "index.json"
    OG_DOTS_IMAGE = "og_dots_image.png"
    EXCERPTDIR_ROOT = "../../static/excerpts/"
    IMAGEDIR_ROOT = "../../static/images/"
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
    transfer_images(ROOT, IMAGEDIR_ROOT)
    delete_unused_images(EXCERPTDIR_ROOT, IMAGEDIR_ROOT, OG_DOTS_IMAGE, INDEX_NAME)
    halve_blendingmode_dots_images(OG_DOTS_IMAGE, IMAGEDIR_ROOT)
    #exit()

