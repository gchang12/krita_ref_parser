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
    soup.find(h_tag).extract()

# - Extract icons
def extract_icon(soup: bs4.BeautifulSoup):
    """
    """
    soup.find("img").extract()

def remove_empty_tags(soup: bs4.BeautifulSoup):
    """
    """
    for tag in filter(lambda tag: tag.find() is None and tag.id is None, soup.find_all()):
        tag.extract()

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
def internal_link_must_be_replaced_with_official_docs_link(a: bs4.Tag, *, num_levels: int):
    """
    """
    #for a in filter(lambda a: "internal" in a['class'], soup.find_all("a")):
    href_path = a['href'].split('/')
    return href_path.count('..') == num_levels:

# - Delete references to extracted sections
def update_references_to_blending_modes_sections(root_dir: Path | str, internal_a: bs4.Tag):
    """
    """
    normalized_href = internal_a['href'].lstrip('./')
    renormalized_href = normalized_href.replace(".html#", "/") + ".html"
    full_path_to_tgt = Path(root_dir, renormalized_href)
    if full_path_to_tgt.exists():
        internal_a['href'] = "/" + renormalized_href
        return
    raise FileNotFoundError("Fatal error: '%s' should exist, but it doesn't." % full_path_to_tgt)
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
    internal_a['href'] = '/'.join([OFFICIAL_DOCS_ROOT.rstrip('/'), internal_a['href'].lstrip('/')])
    internal_a['class'].remove("internal")
    internal_a['class'].add(LINK_TO_OFFICIAL_DOCS_CLASSNAME)

# MODIFY LINK BEHAVIOR

# - Change documentation links to official docs website as needed; add extra class denoting a link as an official-docs link.
def replace_a_tags_with_reactlink_tags(soup: bs4.BeautifulSoup):
    """
    """
    # NOTE: May change depending on web interface implementation
    for a in filter(lambda a: "internal" in a['class'], soup.find_all("a")):
        react_link = soup.new_tag("Link", to=a['href'])
        a.replace_with(react_link)

# - Have links to external/official pages open new tabs.
def have_a_tag_open_new_tab(a: bs4.Tag):
    """
    """
    #for a in filter(lambda a: "external" in a['class'], soup.find_all("a")):
    a['target'] = "_blank"

# INDEX-FILE MANAGEMENT

# - Extract blending_modes/* subsections.
def extract_subsections(soup: bs4.BeautifulSoup):
    """
    """
    for section in soup.css.select("section[id] > section[id]"):
        section.extract()

def remove_links_from_index(soup: bs4.BeautifulSoup, root_dirname: str):
    """
    """
    for a in filter(lambda a: a['href'].startswith(root_dirname), soup.find_all("ul > li > a")):
        a.extract()
    for li in filter(lambda li: li.find() is None, soup.find_all("ul > li")):
        li.extract()
    for ul in filter(lambda ul: ul.find() is None, soup.find_all("ul")):
        ul.extract()

# RENAMING FILES
# - mv 'layers_and_masks/fill_layers.html' to 'layers_and_masks/fill_layer_generators.html'

def update_filename(root_dir: Path | str, src_path: Path | str, tgt_path: Path | str):
    """
    """
    #src_path = Path("layers_and_masks", "fill_layers.html")
    #tgt_path = Path("layers_and_masks", "fill_layer_generators.html")
    #root_dir = TARGET_DIR
    shutil.mv(
        Path(root_dir, src_path),
        Path(root_dir, tgt_path),
    )
# - and change header to 'Fill Layer Generators'

def update_references_to_filename(
        soup: bs4.BeautifulSoup,
        root_dir: Path | str,
        src_path: Path | str,
        tgt_path: Path | str,
    ):
    """
    """
    for internal_a in filter(
        lambda internal_a: internal_a['href'].endswith(str(src_path)),
        soup.css.select("a[class='internal']"),
    ):
        internal_a['href'] = '/'.join([str(root_dir), str(tgt_path)])
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

    # OLD CODE HERE

    def _extract_h_tag(section, *, h_level: int):
        """
        Pops <h[1-6]> tag from HTML soup `section` and returns it.
        """
        # https://www.crummy.com/software/BeautifulSoup/bs4/doc/#extract
        # extract header tag
        # store filename-header pairs as JSON to be returned
        #logger.debug("Searching for tag: h%d", h_level)
        h = section.find('h%d' % h_level).extract().text
        #logger.debug("Searching for pilcrow in: '%s'", h)
        pilcrow_loc = h.index(PILCROW)
        #logger.debug("Returning: %r", h)
        return h[:pilcrow_loc]

    def _reset_anchor_tag_sources(section):
        """
        Sets href for <a> to links s.t. they reference official Krita docs.
        """
        # have all anchor tags reference the actual Krita-Docs website
        # from: '../../'
        # to: 'https://docs.krita.org/en/'
        # for reference: view-source:https://docs.krita.org/en/reference_manual/tools/assistant.html
        # (and add an additional class to this while you're at it)
        external_root = 'https://docs.krita.org/en/'
        #logger.debug("Setting <a> hrefs to reference '%s' instead of '../../'.", external_root)
        for a in filter(lambda a_: "internal" in a_['class'], section.find_all('a')):
            #href_path = a['href'].split('/')
            #a['href'] = external_root + '/'.join(href_path[2:])
            #a['class'].remove("internal")
            #a['class'].append(CLASS_FOR_LINKS_TO_OFFICIAL_DOCS)
            pass

    def _extract_dotsimg(section):
        """
        Pops first dots-img tag in a section.
        """
        dotsimg = None
        #logger.debug("Searching for <img> tag where src.endswith('_with_dots.png')")
        for img in section.find_all("img"):
            if img['src'].endswith("_with_dots.png"):
                dotsimg = img.extract()
                #logger.debug("Dots-image found: %s. Returning.", dotsimg)
                break
        return dotsimg

    def _replace_img_sources(section, *, levels, img_root="../../images/"):
        """
        Replaces src attributes in <img> tags to match new filetree.
        """
        # https://www.crummy.com/software/BeautifulSoup/bs4/doc/#changing-tag-names-and-attributes
        # change all image sources:
        # - from: '../../_images/'
        # - to: './images/'
        #logger.debug("Replacing `img-src` to ./images/`img-src[%d:]`", levels)
        for img in section.find_all("img"):
            img_src = img['src'].split('/')
            #logger.debug("Found `img-src`: %s", img['src'])
            # TODO: Delete leading './'
            new_img_src = img_root + '/'.join(img_src[levels:])
            img['src'] = new_img_src
            #logger.debug("Set `img-src`: %s", new_img_src)

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
            file_count = 0 
            for htmlfile in filter(lambda path: path.is_file(), path_to_section.iterdir()):
                htmltext = htmlfile.read_text(encoding='utf-8')
                soup = BeautifulSoup(htmltext, 'html.parser')
                for a in soup.find_all("a"):
                    if "internal" not in a['class']:
                        #a['class'].append('external')
                        continue
                    a['href'] = root + "/" + a['href'].lstrip('./')
                    try:
                        a['class'].remove('internal')
                    except ValueError:
                        pass
                    if 'link-to-official-docs' not in a['class']:
                        a['class'].append('link-to-official-docs')
                htmlfile.write_text(str(soup), encoding='utf-8')
                file_count += 1
            logging.debug("%d files have been modified for '%s'.", file_count, section)

    def have_anchor_tags_reference_source2(excerpt_dir):
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
        root = "https://docs.krita.org/en/"
        logging.debug("Changing a[src] to source where 'internal' in a[class].")
        sectors = ("user_manual", "general_concepts", "tutorials", "KritaFAQ", "contributors_manual", "resources_page")
        for section in sections:
            path_to_section = Path(excerpt_dir, section)
            file_count = 0
            for htmlfile in filter(lambda path: path.is_file(), path_to_section.iterdir()):
                htmltext = htmlfile.read_text(encoding='utf-8')
                soup = BeautifulSoup(htmltext, 'html.parser')
                for a in soup.find_all("a"):
                    #sector = a['href'].split('/')[4]
                    #print(sector)
                    #print(sector)
                    #print(a['href'])
                    #a['href'] = a['href'].replace(root, root + repl)
                    if a['href'].startswith("#"):
                        continue
                    if "blending_modes" in a['href']:
                        repl = root + "reference_manual/"
                        if "brush_" in section:
                            pattern = "../../"
                        else:
                            pattern = "../"
                        new_href = a['href'].replace(pattern, repl)
                    elif "brush_" not in section:
                        if a['href'].startswith("../../"):
                            repl = root
                            new_href = a['href'].replace("../../", repl)
                        else:
                            continue
                    elif "brush_" in section:
                        if a['href'].startswith("../../../"):
                            repl = root
                            new_href = a['href'].replace("../../../", repl)
                        else:
                            continue
                    else:
                        continue
                    if "reference_manual/brush_" in new_href:
                        new_href = new_href.replace("reference_manual/", "reference_manual/brushes/")
                    if ".." in new_href:
                        new_href = new_href.replace('..', '')
                    #print(new_href)
                    try:
                        a['class'].remove('internal')
                    except ValueError:
                        pass
                    a['class'].append('link-to-official-docs')
                    a['href'] = new_href
                htmlfile.write_text(str(soup), encoding='utf-8')
                file_count += 1
            logging.debug("%d files have been modified for '%s'.", file_count, section)

    def delete_orphaned_figcaption(excerpt_dir):
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
        for section in sections:
            path_to_section = Path(excerpt_dir, section)
            file_count = 0
            for htmlfile in filter(lambda path: path.is_file(), path_to_section.iterdir()):
                htmltext = htmlfile.read_text(encoding='utf-8')
                soup = BeautifulSoup(htmltext, 'html.parser')
                for figcaption in soup.find_all("figcaption"):
                    if figcaption.parent.find("img") is None:
                        figcaption.parent.extract()
                htmlfile.write_text(str(soup), encoding="utf-8")

    def set_rel_attribute(excerpt_dir):
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
        for section in sections:
            path_to_section = Path(excerpt_dir, section)
            file_count = 0
            for htmlfile in filter(lambda path: path.is_file(), path_to_section.iterdir()):
                htmltext = htmlfile.read_text(encoding='utf-8')
                soup = BeautifulSoup(htmltext, 'html.parser')
                for a in soup.find_all("a"):
                    if "external" in a['class']:
                        a['class'].remove("external")
                    if a['href'].startswith('http'):
                        a['rel'] = "external"
                htmlfile.write_text(str(soup), encoding="utf-8")

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

    def prepend_lines_to_section_excerpt(excerpt_dir, section, lines):
        """
        Prepends CSS links to HTML excerpt files.
        """
        for htmlfile in filter(
            lambda filepath: filepath.is_file(),
            Path(excerpt_dir, section).iterdir(),
        ):
            filetext = htmlfile.read_text(encoding='utf-8')
            soup = BeautifulSoup(filetext, 'html.parser')
            if soup.css.select('link[rel="stylesheet"][href][type="text/css"]') is None:
                continue
            new_filetext = lines + filetext.splitlines()
            htmlfile.write_text(
                "\n".join(new_filetext),
                encoding="utf-8",
            )

    def prepend_lines_to_all_section_excerpts(excerpt_dir, index, tgt_dir):
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
            htmlfile = Path(tgt_dir, "blending_modes", record['file'])
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
            htmlfile = Path(tgt_dir, "blending_modes", record['file'])
            filetext = htmlfile.read_text(encoding='utf-8').splitlines()
            new_filetext = lines + filetext
            htmlfile.write_text(
                "\n".join(new_filetext),
                encoding="utf-8",
            )

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
