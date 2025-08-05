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
    """
    logging.debug("Deleting directories in: %s", dirname)
    for dirpath in filter(
        lambda path: path.is_dir(),
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

# TODO: For each thing, insert into the thing.
'''
<link rel="stylesheet" href="_static/css/theme.css" type="text/css" />
<link rel="stylesheet" href="_static/pygments.css" type="text/css" />
<link rel="stylesheet" href="_static/pygments.css" type="text/css" />
<link rel="stylesheet" href="_static/css/theme.css" type="text/css" />
'''

# 1. Import excerpts/, images/, and 'index.json' from parser module.
# 2. Import 'index.json' from parser module.
# Import rc file from specified folder.

# TODO: Demarcate images by section
# NOTE: There are like three unique templates
# TODO: Erase exceptional icons.
# NOTE: section-imagedir

import sqlite3
import logging
from bs4 import BeautifulSoup 

def generate_list_items_for_section_with_icon(section, index):
    """
    """
    # TODO: Insert code here.
    # insert ul tag
    # inside ul tag, iterate through tools dir
    # for each tool, create li tag with:
    # - key=src, className='menu-item'
    #   - button.data-page=src, onClick={changeDescriptionSource}, alt=header width={iconSize} height={iconSize}
    # - children = header
    # dir, file, header, icon
    # process JSON
    #"tools/", "brush_engines/"
    list_items = []
    for record in filter(lambda record_: record_['dir'] == section, index):
        record['full_path'] = record['dir'] + record['file']
        try:
            record['icon'] = '/' + record['icon'].lstrip('./')
        except AttributeError as err:
            record['icon'] = f"/images/_{section.rstrip('/')}-not-found.svg"
            logging.debug("icon was None. dir: %(dir)s, file: %(file)s, header: %(header)s" % record)
            #raise err
        if record['header'] in ('Chalk Brush Engine', 'Color Sampler Tool'):
            logging.debug("header was None. dir: %(dir)s, file: %(file)s, header: %(header)s" % record)
            record['icon'] = f"/images/_{section.rstrip('/')}-not-found.svg"
        list_item = '''<li key="%(full_path)s" className="menu-item">
  <button data-page="%(full_path)s" onClick={changeDescriptionSource}>
    <img src="%(icon)s" width={iconSize} height={iconSize} alt="Icon for '%(dir)s%(header)s'." />
    <h2>%(header)s</h2>
  </button>
</li>''' % record
        list_items.append(list_item)
    logging.debug("%d items found for '%s'. Returning.", len(list_items), section)
    return list_items

def generate_list_items_for_section_without_icon(section, index):
    """
    """
    # TODO: Insert code here.
    # insert ul tag
    # inside ul tag, iterate through tools dir
    # for each tool, create li tag with:
    # - key=src, className='menu-item'
    #   - button.data-page=src, onClick={changeDescriptionSource}, alt=header width={iconSize} height={iconSize}
    # - children = header
    # dir, file, header, icon
    # process JSON
    list_items = []
    for record in filter(lambda record_: record_['dir'] == section, index):
        record['full_path'] = record['dir'] + record['file']
        try:
            record['icon'] = '/' + record['icon'].lstrip('./')
        except AttributeError as err:
            record['icon'] = f"/images/_{section.rstrip('/')}-not-found.svg"
            #print("icon was None. dir: %s, file: %s, header: %s" % (dir, file, header))
            #raise err
        list_item = '''<li key="%(full_path)s" className="menu-item">
  <button data-page="%(full_path)s" onClick={changeDescriptionSource}>
    <h2>%(header)s</h2>
  </button>
</li>''' % record
        list_items.append(list_item)
    logging.debug("%d items found for '%s'. Returning.", len(list_items), section)
    return list_items

def get_index(filename):
    """
    """
    with open(filename, encoding="utf-8") as rfile:
        index = json.load(rfile)
    return index

def generate_menu(list_items, function_sig):
    """
    """
    unordered_list = [
        function_sig,
        "  return (",
        "    <ul>",
        "    </ul>",
        "  );",
        "}",
        "export default MenuItems;"
    ]
    ul_end = 3
    num_spaces = 6
    unordered_list.insert(
        ul_end,
        textwrap.indent("\n".join(list_items), " " * num_spaces),
    )
    return "\n".join(unordered_list)

def generate_menu_for_sections(excerpt_dir, index, generate_list_items, sections):
    """
    """
    #index = get_index(index_file)
    function_sig = {
        generate_list_items_for_section_without_icon: "function MenuItems({ changeDescriptionSource }) {",
        generate_list_items_for_section_with_icon: "function MenuItems({ changeDescriptionSource, iconSize }) {",
    }[generate_list_items]
    for section in sections:
        # Create directory
        Path("app", section).mkdir(exist_ok=True)
        list_items = generate_list_items(section, index)
        menu = generate_menu(list_items, function_sig)
        menu_file = Path("app", section, "menuItems.tsx")
        logging.debug("Writing to: %s", menu_file)
        menu_file.write_text(menu, encoding="utf-8")
        page_text = ''''use client';
import MenuItems from './menuItems.tsx';
import { useState } from 'react';
const SECTION = "%s";
function Home() {
  const [page, setPage] = useState(`/excerpts/${SECTION}/_how-to-use.html`);
  function changeDescriptionSource(e) {
    const page = e.currentTarget.dataset.page;
    const targetSrc = "/excerpts/" + page;
    const description = document.getElementById(`${SECTION}-description`);
    if (description.src === targetSrc) {
      return;
    }
    setPage(targetSrc);
    console.log(targetSrc);
    document.querySelectorAll(".currently-displayed").forEach(element => element.classList.remove("currently-displayed"));
    e.currentTarget.classList.add("currently-displayed");
  }
  const iconSize = "80";
  const iframeId = `${SECTION}-description`;
  return (
    <main>
      <h1>Tools</h1>
      <div className="menu-without-icon">
        <div id="menu-item-list" className="container" height="400px">
          <MenuItems changeDescriptionSource={changeDescriptionSource} />
        </div>
        <div className="description">
          <h2>Description</h2>
          <iframe src={page} width="1000px" height="400px" id={iframeId}>
          </iframe>
        </div>
      </div>
    </main>
  );
}
export default Home;
''' % section
        function_call = {
            generate_list_items_for_section_without_icon: "<MenuItems changeDescriptionSource={changeDescriptionSource} iconSize={iconSize} />",
            generate_list_items_for_section_with_icon: "<MenuItems changeDescriptionSource={changeDescriptionSource} iconSize={iconSize} />",
        }[generate_list_items]
        page_text.replace("<MenuItems changeDescriptionSource={changeDescriptionSource} />", function_call)
        page_file = Path("app", section, "page.tsx")
        logging.debug("Writing to: %s", page_file)
        page_file.write_text(page_text, encoding="utf-8")
        #prepend_lines_to_section_excerpts(excerpt_dir, section, lines)

def generate_menu_for_sections_without_icons(excerpt_dir, index):
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
    #index = get_index(index_file)
    #lines = ( '<link rel="stylesheet" href="../../stylesheets/iframe/style.css" type="text/css" />' '<link rel="stylesheet" href="../../stylesheets/iframe/without-icons.css" type="text/css" />')
    generate_list_items = generate_list_items_for_section_without_icon
    return generate_menu_for_sections(excerpt_dir, index, generate_list_items, sections)

def generate_menu_for_sections_with_icons(excerpt_dir, index):
    """
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
    #index = get_index(index_file)
    #lines = ( '<link rel="stylesheet" href="../../stylesheets/iframe/style.css" type="text/css" />' '<link rel="stylesheet" href="../../stylesheets/iframe/with-icons.css" type="text/css" />')
    generate_list_items = generate_list_items_for_section_with_icon
    return generate_menu_for_sections(excerpt_dir, index, generate_list_items, sections)

def generate_menu_for_blending_modes_without_dots(excerpt_dir, index):
    """
    """
    sections = ("blending_modes",)
    section = sections[0]
    generate_list_items = generate_list_items_for_section_without_icon
    index = filter(lambda record: record['icon'] is None, index)
    #lines = ( '<link rel="stylesheet" href="../../stylesheets/iframe/style.css" type="text/css" />' '<link rel="stylesheet" href="../../stylesheets/iframe/without-icons.css" type="text/css" />')
    generate_menu_for_sections(excerpt_dir, index, generate_list_items, sections)
    output_files = (
        "page.tsx",
        "menuItems.tsx",
    )
    new_dst = Path("app", section, "without-dots")
    new_dst.mkdir(exist_ok=True)
    for file in output_files:
        Path("app", section, file).rename(new_dst.joinpath(file))
    logging.debug("Moved files to: %s", new_dst)

def generate_menu_for_blending_modes_with_dots(excerpt_dir, index):
    """
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
        list_items.append("\n".join([list_item, textwrap.indent(excerpt_text, " " * 2), "</li>"]))
    num_spaces = 6
    buffer = (
        "function MenuItems({ moveToQueue, iconWidth, iconHeight }) {",
        "  return (",
        "    <ul>",
        textwrap.indent("\n".join(list_items), " " * num_spaces),
        "    </ul>",
        "  );",
        "}",
        "export default MenuItems",
    )
    target_dir = Path("app", section, "with-dots")
    target_dir.mkdir(exist_ok=True)
    target_file = target_dir.joinpath("menuItems.tsx")
    target_file.write_text("\n".join(buffer), encoding="utf-8")
    #lines = ( '<link rel="stylesheet" href="../../stylesheets/iframe/style.css" type="text/css" />' '<link rel="stylesheet" href="../../stylesheets/iframe/without-icons.css" type="text/css" />')
    #prepend_lines_to_section_excerpts(excerpt_dir, section, lines)
    target_dir.joinpath("page.tsx").write_text(''''use client';
import Image from "next/image";
import { useState } from 'react';
import MenuItems from './menuItems.tsx';
const SECTION = "blending_modes";
function Home() {
  let iconHeight = 220;
  let iconWidth = 421;
  const scaleFactor = 1;
  iconHeight *= scaleFactor;
  iconWidth *= scaleFactor;
  const [queue, setQueue] = useState([]);
  function moveToQueue(e) {
    const checkbox = e.currentTarget;
    const imageSrc = checkbox.dataset.image;
    const imageHeader = checkbox.dataset.header;
    const image = {src: imageSrc, header: imageHeader};
    if (queue.length === 3 && !queue.some(image_ => image_.src === image.src)) {
        alert("You may not insert more than three images into the queue.");
        checkbox.checked = false;
    } else if (queue.some(image_ => image_.src === image.src)) {
        setQueue(queue.filter(image_ => image_.src !== image.src));
    } else {
      setQueue([...queue, image]);
    }
  }
  const queueItems = queue.map(
    image => {
      return (
        <li key={image.src}>
          <div className="title-and-text">
            <h2>{image.header}</h2>
            <Image src={"/images/" + image.src} width={iconWidth} height={iconHeight} alt="Dots image" />
          </div>
        </li>
      );
    }
  );
  return (
    <main>
      <h1>Blending Modes</h1>
      <div id="blending_modes-gallery">
        <ul>
          <li>
            <div className="title-and-text">
              <h2>Original</h2>
              <Image src="/images/og_dots_image.png" width={iconWidth} height={iconHeight} alt="Original dots image" />
            </div>
          </li>
          {queueItems}
        </ul>
        <div id="blending_modes-selector">
          <MenuItems moveToQueue={moveToQueue} iconWidth={iconWidth} iconHeight={iconHeight} />
        </div>
      </div>
    </main>
  );
}
export default Home;''')
    logging.debug("Moved files to: %s", target_dir)

def prepend_lines_to_section_excerpt(excerpt_dir, section, lines):
    """
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
    index = filter(lambda record: record['dir'] == "blending_modes/", index)
    logging.debug("Prepending <link ...> lines to files in 'blending_modes/*'.")
    for record in index:
        if record['icon'] is not None:
            lines = [
                '<link rel="stylesheet" href="../../stylesheets/iframe/style.css" type="text/css" />',
                '<link rel="stylesheet" href="../../stylesheets/iframe/blending_modes.css" type="text/css" />',
            ]
        else:
            lines = [
                '<link rel="stylesheet" href="../../stylesheets/iframe/style.css" type="text/css" />',
                '<link rel="stylesheet" href="../../stylesheets/iframe/without-icon.css" type="text/css" />',
            ]
        prepend_lines_to_section_excerpt(excerpt_dir, section, lines)

def append_filler_files(excerpt_dir):
    """
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

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
    )
    dirname = "./app/"
    clean_app_directory(dirname)
    src = "../../python/kritaref_parser/"
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


