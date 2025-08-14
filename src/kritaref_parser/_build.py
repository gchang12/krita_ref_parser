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

def clean_app_directory(dirname):
    """
    Deletes directories in 'app/*'.
    """
    logging.debug("Deleting directories in: %s", dirname)
    for dirpath in filter(
        lambda path: path.is_dir() and "_templates" not in path.parts,
        Path(dirname).iterdir(),
    ):
        shutil.rmtree(dirpath)

def import_parsed_files(src, tgt):
    """
    Copies parsed files from src to tgt.
    """
    parsed_files = (
        "excerpts/",
        "images/",
        #"index.json",
    )
    for parsed_file in parsed_files:
        path_to_parsed_file = Path(src, parsed_file)
        tgt_file = '/'.join([tgt, parsed_file])
        logging.debug("Trying to remove: %s" % tgt_file)
        try:
            shutil.rmtree(tgt_file)
        except FileNotFoundError:
            logging.info("'%s' not found. Skipping.", tgt_file)
            pass
        shutil.copytree(path_to_parsed_file, tgt_file)
    index_filename = "index.json"
    path_to_parsed_file = Path(src, index_filename)
    tgt_file = '/'.join([tgt, index_filename])
    try:
        logging.debug("Trying to remove: %s" % tgt_file)
        Path(tgt_file).unlink()
    except FileNotFoundError:
        logging.info("'%s' not found. Skipping.", tgt_file)
        pass
    shutil.copy(path_to_parsed_file, tgt_file)

def generate_list_items_for_section_with_icon(section, index):
    """
    Generates list items for a section whose subsections can be
    identified by their icons.
    """
    list_items = list(filter(lambda record_: record_['dir'] == section, index))
    if section == "blending_modes/":
        list_items = list(filter(lambda record_: record_['icon'] is not None, list_items))
    for item in list_items:
        if item['icon'] is None:
            continue
        item['icon'] = item['icon'].lstrip('./').replace('images/', '')
    return list_items

def generate_list_items_for_section_without_icon(section, index):
    """
    Generates list items for a section whose subsections cannot be
    identified by their icons.
    """
    list_items = list(filter(lambda record_: record_['dir'] == section, index))
    return list_items

def get_index(filename):
    """
    Returns a dict-object from file.
    """
    with open(filename, encoding="utf-8") as rfile:
        index = json.load(rfile)
    return index

def generate_menu(list_items):
    """
    Generates an HTML string containing a menu.
    """
    return "const menuItems = " + json.dumps(list_items, indent=4) + ";\nexport default menuItems;"

def generate_menu_for_sections(excerpt_dir, index, generate_list_items, sections):
    """
    Generates HTML files for sections.
    """
    for section in sections:
        # Create directory
        Path("app", section).mkdir(exist_ok=True)
        list_items = generate_list_items(section, index)
        menu = generate_menu(list_items)
        menu_file = Path("app", section, "menuItems.tsx")
        logging.debug("Writing to: %s", menu_file)
        menu_file.write_text(menu, encoding="utf-8")

def generate_menu_for_sections_without_icons(excerpt_dir, index):
    """
    Generates HTML files for sections without icons.
    """
    sections = (
        #"brush_engines/",
        #"tools/",
        "brush_settings/",
        "dockers/",
        "filters/",
        "layers_and_masks/",
        "main_menu/",
        "preferences/",
        "resource_management/",
        #"blending_modes/",
    )
    generate_list_items = generate_list_items_for_section_without_icon
    return generate_menu_for_sections(excerpt_dir, index, generate_list_items, sections)

def generate_menu_for_sections_with_icons(excerpt_dir, index):
    """
    Generates HTML files for sections with icons.
    """
    sections = (
        "tools/",
        "brush_engines/",
        #"brush_settings/",
        #"dockers/",
        #"filters/",
        #"layers_and_masks/",
        #"main_menu/",
        #"preferences/",
        #"resource_management/",
        #"blending_modes/",
    )
    generate_list_items = generate_list_items_for_section_with_icon
    return generate_menu_for_sections(excerpt_dir, index, generate_list_items, sections)

def generate_menu_for_blending_modes_without_dots(excerpt_dir, index):
    """
    Generates HTML files for 'blending_modes' section.
    """
    sections = ("blending_modes/",)
    generate_list_items = generate_list_items_for_section_without_icon
    index = filter(lambda record: record['icon'] is None, index)
    #lines = ( '<link rel="stylesheet" href="../../stylesheets/iframe/style.css" type="text/css" />' '<link rel="stylesheet" href="../../stylesheets/iframe/without-icons.css" type="text/css" />')
    generate_menu_for_sections(excerpt_dir, index, generate_list_items, sections)
    output_files = (
        #"page.tsx",
        "menuItems.tsx",
    )
    new_dst = Path("app", sections[0], "without-dots")
    new_dst.mkdir(exist_ok=True)
    for file in output_files:
        Path("app", sections[0], file).rename(new_dst.joinpath(file))
    logging.debug("Moved files to: %s", new_dst)

def generate_menu_for_blending_modes_with_dots(excerpt_dir, index):
    """
    Generates HTML files for 'blending_modes' dots-subsections.
    """
    index = filter(lambda record: record['icon'] is not None, index)
    section = "blending_modes/"
    list_items = []
    keys = set(["HSX Blending Modes"])
    for record in filter(
        lambda record_: record_['dir'] == section,
        index,
    ):
        #print(record)
        header = record['header']
        try:
            record['icon'] = record['icon'].lstrip('./').replace('images/', '')
        except AttributeError:
            #print(f"'{header}' blending mode has no icon.")
            #icon = "_blending_modes-not-found%d.svg" % key_counter
            #key_counter += 1
            #print(header)
            continue
        if header in keys:
            #print(f"{header} is already in keys.")
            continue
        keys.add(record['header'])
        # TODO: Incorporate this into bm template-function
        list_item = '''<li key="%(header)s" id="%(header)s">
  <div className="title-and-image">
    <h2>%(header)s<input type="checkbox" onClick={moveToQueue} data-header="%(header)s" data-image="%(icon)s" /></h2>
    <img src="/images/%(icon)s" alt="The '%(header)s' blending-mode as applied to dots" width={iconWidth} height={iconHeight} />
  </div>''' % record
        excerpt_text = Path(f"{excerpt_dir}/{section}/{record['file']}") \
            .read_text(encoding="utf-8") \
            .replace('{', '&#123;').replace('}', '&#125;') \
            .replace('class', 'className')
        pattern = 'style="(.*)"'
        repl = ''
        excerpt_text = re.sub(pattern, repl, excerpt_text)
        pattern = 'src="../../images/'
        repl = 'src="/images/'
        excerpt_text = re.sub(pattern, repl, excerpt_text)
        list_items.append(record)
    target_dir = Path("app", section, "with-dots")
    target_dir.mkdir(exist_ok=True)
    target_file = target_dir.joinpath("menuItems.tsx")
    buffer = "const menuItems = " + json.dumps(list_items, indent=4) + ";\nexport default menuItems;"
    target_file.write_text(buffer, encoding="utf-8")
    #target_file.write_text("\n".join(buffer), encoding="utf-8")
    #lines = ( '<link rel="stylesheet" href="../../stylesheets/iframe/style.css" type="text/css" />' '<link rel="stylesheet" href="../../stylesheets/iframe/without-icons.css" type="text/css" />')
    #prepend_lines_to_section_excerpts(excerpt_dir, section, lines)
    logging.debug("Moved files to: %s", target_dir)

def prepend_lines_to_section_excerpt(excerpt_dir, section, lines):
    """
    Prepends CSS links to HTML excerpt files.
    """
    for htmlfile in filter(
        lambda filepath: filepath.is_file(),
        Path(excerpt_dir, section).iterdir(),
    ):
        filetext = htmlfile.read_text(encoding='utf-8').splitlines()
        new_filetext = lines + filetext
        htmlfile.write_text(
            "\n".join(new_filetext),
            encoding="utf-8",
        )

def prepend_lines_to_all_section_excerpts(excerpt_dir, index):
    """
    Prepends CSS links to all HTML excerpt files.
    """
    sections_without_icons = (
        #"brush_engines/",
        #"tools/",
        "brush_settings/",
        "dockers/",
        "filters/",
        "layers_and_masks/",
        "main_menu/",
        "preferences/",
        "resource_management/",
        #"blending_modes/",
    )
    lines = [
        '<link rel="stylesheet" href="../../stylesheets/iframe/style.css" type="text/css" />',
        '<link rel="stylesheet" href="../../stylesheets/iframe/without-icon.css" type="text/css" />',
    ]
    logging.debug("Prepending <link ...> lines to sans-icon sections.")
    for section in sections_without_icons:
        prepend_lines_to_section_excerpt(excerpt_dir, section, lines)
    sections_with_icons = (
        "tools/",
        "brush_engines/",
        #"brush_settings/",
        #"dockers/",
        #"filters/",
        #"layers_and_masks/",
        #"main_menu/",
        #"preferences/",
        #"resource_management/",
        #"blending_modes/",
    )
    lines = [
        '<link rel="stylesheet" href="../../stylesheets/iframe/style.css" type="text/css" />',
        '<link rel="stylesheet" href="../../stylesheets/iframe/with-icon.css" type="text/css" />',
    ]
    logging.debug("Prepending <link ...> lines to sections with icons.")
    for section in sections_with_icons:
        prepend_lines_to_section_excerpt(excerpt_dir, section, lines)
    bm_index1 = filter(lambda record: record['dir'] == "blending_modes/", index)
    logging.debug("Prepending <link ...> lines to files in 'blending_modes/*'.")
    lines = [
        '<link rel="stylesheet" href="../../stylesheets/iframe/style.css" type="text/css" />',
        '<link rel="stylesheet" href="../../stylesheets/iframe/without-icon.css" type="text/css" />',
    ]
    for record in filter(lambda record: record['icon'] is None, bm_index1):
        htmlfile = Path("public", "excerpts", "blending_modes", record['file'])
        filetext = htmlfile.read_text(encoding='utf-8').splitlines()
        new_filetext = lines + filetext
        htmlfile.write_text(
            "\n".join(new_filetext),
            encoding="utf-8",
        )
    lines = [
        '<link rel="stylesheet" href="../../stylesheets/iframe/style.css" type="text/css" />',
        '<link rel="stylesheet" href="../../stylesheets/iframe/blending_modes.css" type="text/css" />',
    ]
    #print(list(index))
    bm_index2 = filter(lambda record: record['icon'] is not None and record['dir'] == "blending_modes/", index)
    for record in bm_index2:
        #print(record)
        htmlfile = Path("public", "excerpts", "blending_modes", record['file'])
        filetext = htmlfile.read_text(encoding='utf-8').splitlines()
        new_filetext = lines + filetext
        htmlfile.write_text(
            "\n".join(new_filetext),
            encoding="utf-8",
        )

def append_filler_files(excerpt_dir):
    """
    Writes placeholder files.
    """
    for subdir in Path(excerpt_dir).iterdir():
        howtouse_file = subdir.joinpath("_how-to-use.html")
        logging.debug("Appending file: %s", howtouse_file)
        howtouse_file.write_text("")
        section = subdir.name
        filler_img = f"./public/images/_{section}-not-found.svg"
        Path(filler_img).write_text("")
        logging.debug("Making filler image file: %s", filler_img)

def have_excerpt_anchors_open_new_tab(excerpt_dir):
    """
    Hacks into anchor tags and changes the 'target' of each one to '_blank'.
    """
    sections = (
        "brush_engines/",
        "tools/",
        "brush_settings/",
        "dockers/",
        "filters/",
        "layers_and_masks/",
        "main_menu/",
        "preferences/",
        "resource_management/",
        "blending_modes/",
    )
    logging.debug("Changing a[target='_blank'] for all a.")
    for section in sections:
        path_to_section = Path(excerpt_dir, section)
        for htmlfile in filter(lambda path: path.is_file(), path_to_section.iterdir()):
            htmltext = htmlfile.read_text(encoding='utf-8')
            soup = BeautifulSoup(htmltext, 'html.parser')
            for a in soup.find_all("a"):
                a['target'] = "_blank"
            htmlfile.write_text(str(soup), encoding='utf-8')

def have_anchor_tags_reference_source(excerpt_dir):
    """
    """
    sections = (
        "brush_engines/",
        "tools/",
        "brush_settings/",
        "dockers/",
        "filters/",
        "layers_and_masks/",
        "main_menu/",
        "preferences/",
        "resource_management/",
        "blending_modes/",
    )
    root = "https://docs.krita.org/en"
    logging.debug("Changing a[src] to source where 'internal' in a[class].")
    for section in sections:
        path_to_section = Path(excerpt_dir, section)
        for htmlfile in filter(lambda path: path.is_file(), path_to_section.iterdir()):
            htmltext = htmlfile.read_text(encoding='utf-8')
            soup = BeautifulSoup(htmltext, 'html.parser')
            for a in soup.find_all("a"):
                if "internal" not in a['class']:
                    continue
                a['href'] = root + "/" + a['href'].lstrip('./')
            htmlfile.write_text(str(soup), encoding='utf-8')

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
    )
    dirname = "./app/"
    clean_app_directory(dirname)
    src = "../../python/kritaref_palette/"
    tgt = "./public/"
    import_parsed_files(src, tgt)
    excerpt_dir = "./public/excerpts/"
    index = get_index("./public/index.json")
    generate_menu_for_sections_without_icons(excerpt_dir, index)
    generate_menu_for_sections_with_icons(excerpt_dir, index)
    generate_menu_for_blending_modes_without_dots(excerpt_dir, index)
    generate_menu_for_blending_modes_with_dots(excerpt_dir, index)
    prepend_lines_to_all_section_excerpts(excerpt_dir, index)
    append_filler_files(excerpt_dir)
    have_excerpt_anchors_open_new_tab(excerpt_dir)
    #have_anchor_tags_reference_source(excerpt_dir)

