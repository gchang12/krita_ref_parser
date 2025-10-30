"""
"""

from io import open
import shutil
import json
from pathlib import Path

import bs4

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

SOURCE_DIR = "./output/raw-excerpts/"
TARGET_DIR = "./output/excerpts/"
INDEX_FILE = "./output/index.json"

LINK_TO_OFFICIAL_DOCS_CLASSNAME = "link-to-official-docs"

# ADD-AND-DELETE CONTENT

# - Prepend CSS link lines for files of these types: with-icon, without-icon, blending_modes, blending_mode-hsx
def prepend_link_tags_to_soup(soup: bs4.BeautifulSoup, href_list: list[str]):
    """
    """
    for href in href_list:
        tag = soup.new_tag("link", rel="stylesheet", type="text/css", href=href)
        soup.section.insert_before(tag)

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

def replace_section_with_div(soup: bs4.BeautifulSoup):
    """
    """
    section = soup.css.select_one("section[id]")
    section.name = "div"

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

# REFERENCE MANAGEMENT

# - check if a-href exists.
def a_href_exists(a: bs4.Tag, *, root_dir: Path | str):
    """
    """
    a_href = a['src']
    stripped_a_href = a_href.lstrip('./')
    normalized_a_href = Path(root_dir, stripped_a_href)
    return normalized_a_href.exists()

# - Change image sources to /images/{filename}
def update_img_src(img: bs4.Tag):
    """
    """
    #for img in soup.find_all("img"):
    img['src'] = "/images/" + Path(img['src']).name

def normalize_internal_href(a: bs4.Tag):
    """
    """
    a['href'] = "/" + a['href'].lstrip('./')

# - Change documentation links to official docs website as needed; add extra class denoting a link as an official-docs link.
def internal_link_should_stay_internal(a: bs4.Tag, *, num_levels: int):
    """
    """
    #for a in filter(lambda a: "internal" in a['class'], soup.find_all("a")):
    href_path = a['href'].split('/')
    return href_path.count('..') == num_levels

# - Delete references to extracted sections
def update_references_to_blending_modes_sections(root_dir: Path | str, internal_a: bs4.Tag):
    """
    """
    normalized_href = internal_a['href'].lstrip('./')
    renormalized_href = normalized_href.replace(".html#", "/") + ".html"
    full_path_to_tgt = Path(root_dir, renormalized_href)
    if not full_path_to_tgt.exists():
        raise FileNotFoundError("Fatal error: '%s' should exist, but it doesn't." % full_path_to_tgt)
    internal_a['href'] = "/" + renormalized_href
    # normalize link to blending_modes/* section
    # if link exists: further normalize
    # o.w.: raise Exception | replace with link to official docs.

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
def replace_a_tags_with_reactlink_tags(soup: bs4.BeautifulSoup):
    """
    """
    # NOTE: May change depending on web interface implementation
    for a in filter(lambda a: "internal" in a['class'], soup.find_all("a")):
        a.name = "Link"
        a['to'] = a.attrs.pop('href')

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
    for a in filter(lambda a: a['href'].startswith(section), soup.css.select("ul > li > a")):
        a.decompose()
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
    for internal_a in filter(
        lambda internal_a: internal_a['href'].endswith(src_path),
        soup.css.select("a[class='internal']"),
    ):
        internal_a['href'] = '/'.join([str(section), str(tgt_name)])
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
    for record in index:
        if record['path'] == path_id:
            break
    for key in record:
        try:
            record[key] = new_record[key]
            logger.info("Setting record['%s'] = %r.", key, new_record[key])
        except KeyError:
            logger.debug("'%s' not found in provided record.", key)
    #with open(index_file, encoding="utf-9", mode="w") as wfile:
        #json.dump(index, wfile)
    # - modify index.json as necessary. (NOTE: Warrants manual operation).
    # - Do NOT extract SampleImageType figures.

if __name__ == "__main__":

    from krita_ref_parser.compile_index import (
        SECTIONS_WITHOUT_ICONS,
        SECTIONS_WITH_ICONS,
        )


    def clone_from_raw():
        """
        """
        logger.debug("Removing '%s'.", TARGET_DIR)
        shutil.rmtree(TARGET_DIR, ignore_errors=True)
        logger.debug("Cloning from '%s' to '%s'.", SOURCE_DIR, TARGET_DIR)
        shutil.copytree(SOURCE_DIR, TARGET_DIR)

    def rename_fill_layers_to_fill_layer_generators():
        """
        """
        section = "layers_and_masks"
        src_name = "fill_layers.html"
        tgt_name = "fill_layer_generators.html"
        logger.info("Moving '%s/%s/%s' to '%s/%s/%s'.", TARGET_DIR, section, src_name, TARGET_DIR, section, tgt_name)
        update_filename(
            TARGET_DIR,
            Path(section, src_name),
            Path(section, tgt_name),
        )
        logger.info("Replacing all references to '%s/%s' with '%s/%s'.", section, src_name, section, tgt_name)
        for dirpath, dirnames, filenames in Path(TARGET_DIR).walk():
            for filename in filenames:
                filepath = dirpath.joinpath(filename)
                soup = BeautifulSoup(
                    filepath.read_text(encoding='utf-8'),
                    'html.parser',
                )
                update_references_to_filename(
                    soup,
                    section,
                    src_name,
                    tgt_name,
                )
                filepath.write_text(str(soup))
            logger.info("Replaced references in '%s' section.", dirpath.name)
        with open(INDEX_FILE, encoding="utf-8") as rfile:
            index = json.load(rfile)
        path_id = [section, src_name]
        new_record = {"path": [section, tgt_name]}
        logger.info("Updating record where 'path'=%s to %s.", path_id, new_record)
        update_filename_record_of_index(
            index,
            path_id,
            new_record,
        )

    def strip_index_files():
        """
        """
        for dirpath, dirnames, filenames in Path(TARGET_DIR).walk():
            section = dirpath.name
            for filename in filenames:
                if filename == "blending_modes.html":
                    continue
                filepath = dirpath.joinpath(filename)
                if not is_index_file(filepath):
                    continue
                soup = BeautifulSoup(filepath.read_text(encoding="utf-8"), "html.parser")
                remove_links_from_index(soup, section)

    def strip_blending_modes_index_files():
        """
        """
        for dirpath, dirnames, filenames in Path(TARGET_DIR).walk():
            section = dirpath.name
            if section != "blending_modes":
                continue
            for filename in filenames:
                filepath = dirpath.joinpath(filename)
                soup = BeautifulSoup(filepath.read_text(encoding="utf-8"), "html.parser")
                if filename == "hsx.html":
                    hsx_blending_modes = soup.css.select_one("#hsx-blending_modes")
                    hsx_blending_modes.decompose()
                else:
                    extract_subsections(soup)
                filepath.write_text(str(soup), encoding="utf-8")
            break

    def strip_icons_from_files():
        """
        """
        exceptional_files = (
            "",
            )
        for dirpath, dirnames, filenames in Path(TARGET_DIR).walk():
            section = dirpath.name
            if section not in SECTIONS_WITH_ICONS:
                continue
            for filename in filenames:
                if filename in exceptional_files:
                    continue
                filepath = dirpath.joinpath(filename)
                soup = BeautifulSoup(filepath.read_text(encoding="utf-8"), "html.parser")
                extract_icon(soup)
                filepath.write_text(str(soup), encoding="utf-8")

    def strip_headers_from_files():
        """
        """
        for dirpath, dirnames, filenames in Path(TARGET_DIR).walk():
            for filename in filenames:
                filepath = dirpath.joinpath(filename)
                soup = BeautifulSoup(filepath.read_text(encoding="utf-8"), "html.parser")
                extract_h_tag(soup)
                filepath.write_text(str(soup), encoding="utf-8")

    def rename_sections_to_divs():
        """
        """
        for dirpath, dirnames, filenames in Path(TARGET_DIR).walk():
            for filename in filenames:
                filepath = dirpath.joinpath(filename)
                soup = BeautifulSoup(filepath.read_text(encoding="utf-8"), "html.parser")
                replace_section_with_div(soup)
                filepath.write_text(str(soup), encoding="utf-8")

    def remove_empty_tags_from_files():
        """
        """
        for dirpath, dirnames, filenames in Path(TARGET_DIR).walk():
            for filename in filenames:
                filepath = dirpath.joinpath(filename)
                soup = BeautifulSoup(filepath.read_text(encoding="utf-8"), "html.parser")
                remove_empty_tags(soup)
                filepath.write_text(str(soup), encoding="utf-8")

    def update_img_sources_in_files():
        """
        """
        for dirpath, dirnames, filenames in Path(TARGET_DIR).walk():
            for filename in filenames:
                filepath = dirpath.joinpath(filename)
                soup = BeautifulSoup(filepath.read_text(encoding="utf-8"), "html.parser")
                for img in soup.find_all("img"):
                    update_img_src(img)
                filepath.write_text(str(soup), encoding="utf-8")
