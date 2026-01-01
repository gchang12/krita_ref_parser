"""
"""

from io import open
import shutil
import json
from pathlib import Path

import bs4
from bs4 import BeautifulSoup

#from krita_ref_parser.amputate_images import SampleImageType
from krita_ref_parser.compile_index import (
    ALL_SECTIONS,
    SECTIONS_WITHOUT_ICONS,
    SECTIONS_WITH_ICONS,
    BLENDING_MODE_SECTIONS,
    BLENDING_MODE_HSX_SECTION,
    )
from krita_ref_parser._logging import logger

PILCROW = "¶"

OFFICIAL_DOCS_ROOT = "https://docs.krita.org/en/"
LINK_TO_OFFICIAL_DOCS_CLASSNAME = "link-to-official-docs"

SOURCE_DIR = "./output/raw-excerpts/"
TARGET_DIR = "./output/excerpts/"
INDEX_FILE = "./output/index.json"

# ADD-AND-DELETE CONTENT

# - Prepend CSS link lines for files of these types: with-icon, without-icon, blending_modes, blending_mode-hsx
def prepend_link_tags_to_soup(soup: bs4.BeautifulSoup, href_list: list[str], *, container="section"):
    """
    """
    for href in href_list:
        tag = soup.new_tag("link", rel="stylesheet", type="text/css", href=href)
        soup.find(container).insert_before(tag)

# - Extract h_ tags. Note that this also extracts the href.
def extract_h_tag(soup: bs4.BeautifulSoup, *, h_level: int):
    """
    """
    h_tag = "h%d" % h_level
    soup.find(h_tag).decompose()

# - Extract icons
def extract_icon(soup: bs4.BeautifulSoup):
    """
    """
    soup.find("img").decompose()

def replace_section_with_div(soup: bs4.BeautifulSoup, *, og_repl=("section[id]", "div")):
    """
    """
    og, repl = og_repl
    section = soup.css.select_one(og)
    section.name = repl
    section['class'] = "excerpt"

def remove_empty_tags(soup: bs4.BeautifulSoup):
    """
    """
    for tag in filter(
        lambda tag: \
            not tag.contents \
            and 'id' not in tag.attrs,
        soup.find_all(),
    ):
        tag.decompose()

def promote_h_tags(soup: bs4.BeautifulSoup, *, h_levels: tuple[int]):
    """
    """
    og_level, tgt_level = og_and_tgt_levels
    h_tag_name = "h%d" % og_level
    for h_ in soup.find_all(h_tag_name):
        h_.name = "h%d" % tgt_level

# REFERENCE MANAGEMENT

# - check if a-href exists.
def a_href_exists(a: bs4.Tag, *, root_dir: Path | str):
    """
    """
    a_href = a['href']
    stripped_a_href = a_href.lstrip('./')
    if "blending_modes/" in stripped_a_href and "/" in stripped_a_href[stripped_a_href.index("blending_modes/"):]:
        stripped_a_href = stripped_a_href.replace('.html#', '/') + '.html'
    if "#" in stripped_a_href:
        stripped_a_href = stripped_a_href[:stripped_a_href.index("#")]
    normalized_a_href = Path(root_dir, stripped_a_href)
    return normalized_a_href.exists()

# - Change image sources to /images/{filename}
def update_img_src(img: bs4.Tag):
    """
    """
    #for img in soup.find_all("img"):
    try:
        img['src'] = "/images/" + Path(img['src']).name
    except KeyError as key_err:
        logger.error("%s has no 'src' attribute. Inspect.", img)
        raise key_err

def normalize_internal_href(a: bs4.Tag):
    """
    """
    a['href'] = "/" + a['href'].lstrip('./')

# - Change documentation links to official docs website as needed; add extra class denoting a link as an official-docs link.
# NOTE: Isn't this accomplished already by 'a_href_exists'?
def internal_link_should_become_external(a: bs4.Tag, *, num_levels: int):
    """
    """
    #for a in filter(lambda a: "internal" in a['class'], soup.find_all("a")):
    href_path = a['href'].split('/')
    logger.debug("Checking if '%s' has %d instances of '..'", a['href'], num_levels)
    return href_path.count('..') == num_levels

# - Delete references to extracted sections
def update_references_to_blending_modes_sections(root_dir: Path | str, internal_a: bs4.Tag):
    """
    """
    normalized_href = internal_a['href'].lstrip('./')
    renormalized_href = normalized_href.replace(".html#", "/") + ".html"
    full_path_to_tgt = Path(root_dir, renormalized_href)
    logger.debug("Checking if '%s' exists.", full_path_to_tgt)
    if not full_path_to_tgt.exists():
        raise FileNotFoundError("Fatal error: '%s' should exist, but it doesn't." % full_path_to_tgt)
    internal_a['href'] = "/" + renormalized_href
    # normalize link to blending_modes/* section
    # if link exists: further normalize
    # o.w.: raise Exception | replace with link to official docs.

def get_correct_blending_modes_path(file_id: str, root_dir: Path | str):
    """
    """
    for dirpath, dirnames, filenames in Path(root_dir).walk():
        if "blending_modes" not in dirpath.parts:
            continue
        for filename in filenames:
            filepath = dirpath.joinpath(filename)
            soup = BeautifulSoup(
                filepath.read_text(encoding="utf-8"),
                "html.parser",
                )
            matching_elt = soup.css.select_one(file_id)
            if matching_elt is None:
                continue
            return (dirpath.name, filename, file_id)
    raise KeyError("'%s' not found in '%s/blending_modes/**'" % (file_id, root_dir))

# - Delete references to extracted sections
def replace_internal_reference_with_official(internal_a: bs4.Tag):
    """
    """
    # check if references are dead.
    # if yes: raise Exception | replace with link to official docs.
    # if no: normalize link
    #for a in soup.css.select("a[class='internal']"):
    internal_a['href'] = '/'.join([OFFICIAL_DOCS_ROOT.rstrip('/'), internal_a['href'].lstrip('./')])
    internal_a['class'].remove("internal")
    internal_a['class'].append(LINK_TO_OFFICIAL_DOCS_CLASSNAME)
    internal_a['class'].append("external")

# MODIFY LINK BEHAVIOR

# - Change documentation links to official docs website as needed; add extra class denoting a link as an official-docs link.
def replace_a_tags_with_reactlink_tags(soup: bs4.BeautifulSoup, *, new_name="Link", new_href_name="to"):
    """
    """
    # NOTE: May change depending on web interface implementation
    for a in filter(lambda a: "internal" in a['class'], soup.find_all("a")):
        a.name = new_name
        a[new_href_name] = a.attrs.pop('href')

# - Have links to external/official pages open new tabs.
def have_a_tag_open_new_tab(a: bs4.Tag):
    """
    """
    #for a in filter(lambda a: "external" in a['class'], soup.find_all("a")):
    a['target'] = "_blank"

# INDEX-FILE MANAGEMENT

def is_index_file(filename: Path | str):
    """
    """
    return Path(filename).with_suffix("").is_dir()

# - Extract blending_modes/* subsections.
def extract_subsections(soup: bs4.BeautifulSoup):
    """
    """
    for section in soup.css.select("section[id] > section[id]"):
        section.decompose()

def remove_links_from_index(soup: bs4.BeautifulSoup, section: str):
    """
    """
    for a in soup.css.select("ul > li > a"):
        logger.debug("Checking if a['href'] ('%s') starts with '%s'.", a['href'], section)
        if not a['href'].startswith(section):
            continue
        a.decompose()
        logger.debug("Decomposed.")
    for li in filter(lambda li: not li.contents, soup.css.select("ul > li")):
        li.decompose()
    for ul in soup.css.select("ul"):
        are_blanks = [not str(content).strip() for content in ul.contents]
        if all(are_blanks):
            ul.decompose()

# RENAMING FILES
# - mv 'layers_and_masks/fill_layers.html' to 'layers_and_masks/fill_layer_generators.html'

def update_filename(root_dir: Path | str, src_path: Path | str, tgt_path: Path | str):
    """
    """
    #src_path = Path("layers_and_masks", "fill_layers.html")
    #tgt_path = Path("layers_and_masks", "fill_layer_generators.html")
    #root_dir = TARGET_DIR
    shutil.move(
        Path(root_dir, src_path),
        Path(root_dir, tgt_path),
    )
# - and change header to 'Fill Layer Generators'

def update_references_to_filename(
        soup: bs4.BeautifulSoup,
        section: Path | str,
        src_name: Path | str,
        tgt_name: Path | str,
    ):
    """
    """
    src_path = '/'.join([str(section), str(src_name)])
    for internal_a in soup.css.select("a"):
        logger.debug("Checking if '%s' is present in '%s' (type=%r).", src_path, internal_a['href'], type(internal_a['href']))
        if src_path not in str(internal_a['href']):
            continue
        dots = filter(lambda href: href == '..', internal_a['href'].split('/'))
        internal_a['href'] = '/'.join(list(dots) + [str(section), str(tgt_name)])
        logger.debug("Present.")
    #logger.debug("Last internal a found: %s.", internal_a)
    #src_path = Path("layers_and_masks", "fill_layers.html")
    #tgt_path = Path("layers_and_masks", "fill_layer_generators.html")

def update_filename_record_of_index(index: list[dict], path_id: list[str], new_record: dict):
    """
    """
    #src_path=["layers_and_masks", "fill_layers.html"]
    #tgt_path=
    #new_record = {
    #    'path': ["layers_and_masks", "fill_layer_generator.html"],
    #    'header': "Fill Layer Generator",
    #}
    #with open(index_file, encoding="utf-8") as rfile:
        #index = json.load(rfile)
    try:
        record = list(filter(lambda record: record['path'] == path_id, index)).pop()
    except IndexError:
        logger.warning("Record with path_id='%s' has already been updated.", path_id)
        return
    for key in record:
        try:
            record[key] = new_record[key]
            logger.info("Setting record['%s'] = %r.", key, new_record[key])
        except KeyError:
            logger.debug("'%s' not found in provided record.", key)
    # - modify index.json as necessary. (NOTE: Warrants manual operation).
    # - Do NOT extract SampleImageType figures.

if __name__ == "__main__":
    import subprocess
    import sys

    # HELPER FUNCTIONS

    def get_soup_from_file(filepath: Path):
        """
        """
        soup = BeautifulSoup(filepath.read_text(encoding="utf-8"), "html.parser")
        return soup

    def write_soup_to_file(soup: bs4.BeautifulSoup, filepath: Path):
        """
        """
        return filepath.write_text(str(soup), encoding="utf-8")

    def view_files_with_vim(files: list[Path | str], *, pattern: str = None, view=False):
        """
        """
        if not view:
            return
        #return
        #user_response = input("These files have changed: %r\nView them? (y/n) " % files)
        #if user_response != "y":
            #return
        args = ["vim", "-R"]
        args.extend([str(Path(TARGET_DIR, file)) for file in files])
        if pattern is not None:
            args.append("+/'" + pattern + "'")
        elif pattern is None:
            pass
        elif not isinstance(pattern, str):
            raise TypeError("Pass in an argument of type 'str'. Argument was of type: %r" % type(pattern))
        subprocess.run(args)
        user_response = input("Stop building? (y/n) ")
        if user_response == "y":
            #subprocess.run(args)
            sys.exit()

    # clone raw-excerpts/ to excerpts/

    def clone_from_raw():
        """
        """
        logger.debug("Removing '%s'.", TARGET_DIR)
        shutil.rmtree(TARGET_DIR, ignore_errors=True)
        logger.debug("Cloning from '%s' to '%s'.", SOURCE_DIR, TARGET_DIR)
        shutil.copytree(SOURCE_DIR, TARGET_DIR)
        Path(TARGET_DIR, "..", "hrefs.txt").unlink(missing_ok=True)
        logger.debug("Removed 'hrefs.txt'.")

    # rename 'layers_and_masks/fill_layers.html' to 'layers_and_masks/fill_layer_generators.html'
    # - update index s.t. header = "Fill Layer Generators"
    # for renaming files
    #update_filename,
    #update_references_to_filename,
    #update_filename_record_of_index,

    def rename_fill_layers_to_fill_layer_generators():
        """
        """
        section = "layers_and_masks"
        src_name = "fill_layers.html"
        tgt_name = "fill_layer_generators.html"
        logger.info("Moving '%s/%s/%s' to '%s/%s/%s'.", TARGET_DIR, section, src_name, TARGET_DIR, section, tgt_name)
        update_filename(
            TARGET_DIR, Path(section, src_name), Path(section, tgt_name),
        )
        logger.info("Replacing all references to '%s/%s' with '%s/%s'.", section, src_name, section, tgt_name)
        for dirpath, dirnames, filenames in Path(TARGET_DIR).walk():
            for filename in filenames:
                filepath = dirpath.joinpath(filename)
                soup = get_soup_from_file(filepath)
                update_references_to_filename(soup, section, src_name, tgt_name)
                write_soup_to_file(soup, filepath)
            logger.info("Replaced references in '%s' section.", dirpath.name)
        with open(INDEX_FILE, encoding="utf-8") as rfile:
            index = json.load(rfile)
        path = [section, src_name]
        new_record = {
            #"path": [section, tgt_name],
            "header": "Fill Layer Generators",
            "isIndexFile": True,
            "path": "layers_and_masks/fill_layer_generators",
            }
        logger.info("Updating record where 'path'=%s to %s.", path, new_record)
        update_filename_record_of_index(index, path, new_record)
        with open(INDEX_FILE, encoding="utf-8", mode="w") as wfile:
            json.dump(index, wfile, indent=2)

    # update all references to files, then normalize them
    #update_img_src,

    def update_img_sources_in_files():
        """
        """
        section = "layers_and_masks"
        src_name = ""
        for dirpath, dirnames, filenames in Path(TARGET_DIR).walk():
            section = dirpath.name
            for filename in filenames:
                filepath = dirpath.joinpath(filename)
                logger.debug("Updating img['src'] in '%s'.", filepath)
                soup = get_soup_from_file(filepath)
                for img in soup.find_all('img'):
                    update_img_src(img)
                write_soup_to_file(soup, filepath)

    #update_references_to_blending_modes_sections_in_files
    def update_references_to_blending_modes_sections_in_files():
        """
        """
        for dirpath, dirnames, filenames in Path(TARGET_DIR).walk():
            for filename in filenames:
                filepath = dirpath.joinpath(filename)
                soup = get_soup_from_file(filepath)
                for a in soup.css.select("a"):
                    try:
                        update_references_to_blending_modes_sections(TARGET_DIR, a)
                    except FileNotFoundError:
                        logger.warning("Error occurred while trying to update %s.", a['href'])
                write_soup_to_file(soup, filepath)

    # for updating paths and references
    #a_href_exists,
    #normalize_internal_href,
    #replace_internal_reference_with_official,

    # strip headers
    #extract_h_tag,

    def strip_headers_from_files():
        """
        """
        for dirpath, dirnames, filenames in Path(TARGET_DIR).walk():
            if dirpath.parts[-1] == "hsx":
                h_level = 3
            elif dirpath.parts[-2] == "blending_modes":
                h_level = 2
            elif dirpath.parts[-1] == "blending_modes":
                h_level = 2
            else:
                h_level = 1
            for filename in filenames:
                filepath = dirpath.joinpath(filename)
                soup = get_soup_from_file(filepath)
                logger.debug("Attempting to extract <h%d> tag from '%s'.", h_level, filepath)
                extract_h_tag(soup, h_level=h_level)
                write_soup_to_file(soup, filepath)

    # replace section container with div.
    #replace_section_with_div,
    def replace_sections_with_divs_in_files():
        """
        """
        og_repl = ("section[id]", "div")
        #og_repl = ("div", "div")
        for dirpath, dirnames, filenames in Path(TARGET_DIR).walk():
            for filename in filenames:
                filepath = dirpath.joinpath(filename)
                soup = get_soup_from_file(filepath)
                replace_section_with_div(soup, og_repl=og_repl)
                if is_index_file(Path(dirpath, filename)):
                    div = soup.css.select_one("div")
                    div['class'] += " index"
                write_soup_to_file(soup, filepath)

    # replace section container with div.
    #replace_section_with_div,
    def promote_blending_modes_h_tags_in_files():
        """
        """
        for dirpath, dirnames, filenames in Path(TARGET_DIR).walk():
            if dirpath.parts[-2] == "blending_modes":
                h_level = 2
            for filename in filenames:
                filepath = dirpath.joinpath(filename)
                soup = get_soup_from_file(filepath)
                promote_h_tags(soup, h_levels=(h_level, h_level-1))
                write_soup_to_file(soup, filepath)

    # strip icons (note the exceptions)
    #extract_icon,
    def strip_icons_from_all_files():
        """
        """
        exceptional_files = (
            "crop.html", # tools
            "color_sampler.html", # tools
            "chalk_engine.html", # brush_engines
            )
        for dirpath, dirnames, filenames in Path(TARGET_DIR).walk():
            section = dirpath.name
            if section not in SECTIONS_WITH_ICONS:
                continue
            for filename in filter(lambda filename: filename not in exceptional_files, filenames):
                filepath = dirpath.joinpath(filename)
                soup = get_soup_from_file(filepath)
                logger.debug("Extracting icon from: '%s'.", filepath)
                extract_icon(soup)
                write_soup_to_file(soup, filepath)

    # strip index files, noting blending-mode and blending-mode-hsx exceptions
    # - leave 'blending_modes.html' alone
    # - remove subsections of blending_modes/*.html
    # - remove #hsx-blending-modes
    # for renovating index files
    #extract_subsections,
    #remove_links_from_index,
    #is_index_file,

    def strip_index_files():
        """
        """
        for dirpath, dirnames, filenames in Path(TARGET_DIR).walk():
            if dirpath.parts[-2] == "blending_modes": # if it's a blending mode subsection, skip
                continue
            #section = dirpath.name
            for filename in filenames:
                if filename == "blending_modes.html":
                    continue
                filepath = dirpath.joinpath(filename)
                logger.debug("Checking if %r is an index file.", filepath)
                if not is_index_file(filepath):
                    logger.debug("'%s' is not an index file. Skipping.", filepath)
                    continue
                logger.debug("'%s' is an index file. Processing.", filepath)
                soup = get_soup_from_file(filepath)
                section = filepath.with_suffix("").name
                remove_links_from_index(soup, section)
                write_soup_to_file(soup, filepath)
            logger.debug("Finished stripping index for '%s'.", section)

    def strip_blending_modes_index_files():
        """
        """
        for dirpath, dirnames, filenames in Path(TARGET_DIR).walk():
            logger.debug("dirpath.parts: %r", dirpath.parts)
            if dirpath.name != "blending_modes": # target only blending mode subsections
                continue
            logger.debug("Dissecting files in %r", dirpath)
            for filename in filenames:
                filepath = dirpath.joinpath(filename)
                soup = get_soup_from_file(filepath)
                if filename == "hsx.html":
                    soup.css.select_one("#hsx-blending-modes").decompose()
                else:
                    extract_subsections(soup)
                write_soup_to_file(soup, filepath)

    #have_a_tag_open_new_tab,
    def have_all_a_tags_open_new_tabs():
        """
        """
        for dirpath, dirnames, filenames in Path(TARGET_DIR).walk():
            for filename in filenames:
                filepath = dirpath.joinpath(filename)
                soup = get_soup_from_file(filepath)
                for a in soup.css.select("a"):
                    if 'external' not in a['class']:
                        continue
                    a['target'] = "_blank"
                write_soup_to_file(soup, filepath)

    #remove_empty_tags,
    def remove_empty_tags_from_files():
        """
        """
        for dirpath, dirnames, filenames in Path(TARGET_DIR).walk():
            for filename in filenames:
                filepath = dirpath.joinpath(filename)
                soup = get_soup_from_file(filepath)
                remove_empty_tags(soup)
                write_soup_to_file(soup, filepath)

    def remove_empty_toc_tags_from_files():
        """
        """
        for dirpath, dirnames, filenames in Path(TARGET_DIR).walk():
            for filename in filter(lambda filename: filename != "blending_modes.html", filenames):
                filepath = dirpath.joinpath(filename)
                soup = get_soup_from_file(filepath)
                for tag in soup.css.select('div[class="toctree-wrapper compound"]'):
                    tag.decompose()
                write_soup_to_file(soup, filepath)

    #replace_a_tags_with_reactlink_tags,
    def replace_all_a_tags_with_reactlink_tags():
        """
        """
        for dirpath, dirnames, filenames in Path(TARGET_DIR).walk():
            for filename in filenames:
                filepath = dirpath.joinpath(filename)
                soup = get_soup_from_file(filepath)
                replace_a_tags_with_reactlink_tags(soup)
                write_soup_to_file(soup, filepath)

    def normalize_all_hrefs():
        """
        """
        for dirpath, dirnames, filenames in Path(TARGET_DIR).walk():
            for filename in filenames:
                filepath = dirpath.joinpath(filename)
                soup = get_soup_from_file(filepath)
                for a in soup.css.select("a"):
                    normalize_internal_href(a)
                write_soup_to_file(soup, filepath)

    def compile_all_hrefs():
        """
        """
        hrefs = set()
        for dirpath, dirnames, filenames in Path(TARGET_DIR).walk():
            for filename in filenames:
                filepath = dirpath.joinpath(filename)
                soup = get_soup_from_file(filepath)
                for a in soup.css.select("a"):
                    hrefs.add(a['href'])
        href_list = list(hrefs)
        href_list.sort()
        text_to_write = "\n".join(href_list)
        list_file = Path(TARGET_DIR, "..", "hrefs.txt")
        list_file.write_text(text_to_write, encoding="utf-8")

    def check_if_path_is_in_index(path: list[str], index: list[dict]):
        """
        """
        try:
            record = list(filter(lambda record: record['path'] == path, index)).pop()
            return True
        except IndexError:
            raise KeyError("'%s' does not exist in index.", path)

    def update_all_hrefs():
        """
        """
        with open(INDEX_FILE, encoding="utf-8") as rfile:
            index = json.load(rfile)
        root_dir = Path(TARGET_DIR)
        for dirpath, dirnames, filenames in Path(TARGET_DIR).walk():
            path = list(dirpath.relative_to(root_dir).parts)
            #record_found = False
            logger.debug("dirpath: %r", dirpath)
            for filename in filenames:
                filepath = dirpath.joinpath(filename)
                #record = filter(lambda record: record['path'] == list(filepath.parts), index)
                path.append(filename)
                logger.debug("path: %r", path)
                check_if_path_is_in_index(path, index)
                num_levels = len(path)
                soup = get_soup_from_file(filepath)
                for a in soup.css.select("a"):
                    href = a['href']
                    if 'internal' not in a['class']:
                        continue
                    if '_images' in href:
                        a['href'] = '/' + href.lstrip('./_')
                    elif href.startswith('#'):
                        pass
                    elif internal_link_should_become_external(a, num_levels=num_levels):
                        logger.debug("Linking a['href'] ('%s') to official docs.", href)
                        replace_internal_reference_with_official(a)
                    else:
                        new_path = path[:-1]
                        parts = href.split('/')
                        for part in parts:
                            if part != '..':
                                continue
                            new_path.pop()
                        new_href = '/'.join([*new_path, href.lstrip('./')])
                        a['href'] = '/' + new_href
                    #href = a['href']
                    if "#" in href and ("blending_modes" in dirpath.parts or "blending_modes" in href):
                        file_id = href[href.index("#"):]
                        try:
                            correct_bm_path = get_correct_blending_modes_path(file_id, TARGET_DIR)
                            if "blending_modes" in correct_bm_path:
                                a['href'] = "/" + '/'.join(correct_bm_path)
                            else:
                                a['href'] = "/blending_modes/" + '/'.join(correct_bm_path)
                            a['href'] = a['href'].replace('/#', '#')
                        except KeyError as key_err:
                            logger.debug("KeyError: %s", key_err)
                    #href = a['href']
                    if href.endswith("#hsx-blending-modes"):
                        a['href'] = "/" + href[:href.index("#hsx-blending-modes")]
                    href = a['href']
                    if href.count('/') == 1 and '#' in href:
                        filename, file_id = tuple(href.lstrip('/').split("#"))
                        if not Path(TARGET_DIR, filename).exists():
                            logger.debug("Filename %s does not exist in root. Linking to official docs.", filename)
                            a['title'] = "To official Krita docs"
                            a['href'] = OFFICIAL_DOCS_ROOT + "reference_manual" + href
                            a['class'] = "reference external " + LINK_TO_OFFICIAL_DOCS_CLASSNAME
                            a['target'] = "_blank"
                write_soup_to_file(soup, filepath)
                path.pop()
                logger.debug("Replacing all internal links on 'blending_modes.html' to excerpt-links.")
                for a in filter(lambda a: "internal" in a['class'], soup.css.select("a")):
                    a['title'] = "To excerpt of '%s'" % a['href'].lstrip('/')
                    a['href'] = '/excerpts' + a['href']
                    a['target'] = '_blank'
                write_soup_to_file(soup, filepath)

    def check_index(check=False):
        """
        """
        if not check:
            return
        with open(INDEX_FILE, encoding="utf-8") as rfile:
            index = json.load(rfile)
        for record in index:
            path = record['path']
            if len(path) == 1:
                return True
        raise Exception("Unable to find path in index whose length is equal to one. ")

    clone_from_raw()
    print("Finished cloning files.")
    view_files_with_vim(["../index.json"])
    rename_fill_layers_to_fill_layer_generators()
    print("Finished renaming 'layers_and_masks/fill_layers.html' to 'layers_and_masks/fill_layer_generators.html'.")
    view_files_with_vim(["dockers/layers.html", "dockers/palette_docker.html", "filters/artistic.html"], pattern="fill_layer_generators.html")
    update_img_sources_in_files()
    print("Finished updating image sources.")
    view_files_with_vim(["blending_modes/arithmetic/addition.html"], pattern="src=")
    update_references_to_blending_modes_sections_in_files()
    print("Finished updating references to blending_mode sources.")
    view_files_with_vim(["blending_modes.html"], pattern="blending_modes/binary/xnor.html")
    strip_headers_from_files()
    print("Finished stripping <h[1-6]> tags.")
    view_files_with_vim(["tools.html"], pattern="<h")
    strip_icons_from_all_files()
    print("Finished stripping <img /> tags.")
    view_files_with_vim(["tools/assistant.html"], pattern="<img ")
    strip_blending_modes_index_files()
    #strip_index_files()
    #remove_empty_toc_tags_from_files()
    view_files_with_vim(["brushes.html", "blending_modes.html", "layers_and_masks/fill_layer_generators.html"])
    #print("Finished cleaning up index files.")
    print("Finished stripping 'blending_modes' index files.")
    view_files_with_vim(["tools.html", "brushes/brush_engines.html", "blending_modes/arithmetic.html"], pattern="<a href=")
    replace_sections_with_divs_in_files()
    print("Finished replacing section[id] with div[id].")
    view_files_with_vim(["layers_and_masks.html"], pattern="<div id=")
    #prepend_link_tags_to_all_excerpts()
    #print("Finished prepending <link /> tags.")
    view_files_with_vim(["brushes/brush_engines.html"], pattern="<link ")
    update_all_hrefs()
    compile_all_hrefs()
    print("Finished updating a.href references.")
    view_files_with_vim(["../hrefs.txt"])
    have_all_a_tags_open_new_tabs()
    print("Finished setting target='_blank' for external links.")
    view_files_with_vim(["layers_and_masks/fill_layer_generators/seexpr.html"], pattern="target=")

