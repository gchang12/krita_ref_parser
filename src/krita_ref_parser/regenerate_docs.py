"""
Modifies and finalizes excerpts and complementary files before writing them to disk.
"""

from io import open
import shutil
import json
from pathlib import Path

from typing import (
    Any,
    Tuple,
    List,
    Iterable,
)

from bs4 import (
    BeautifulSoup,
    Tag,
)

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

def extract_h_tag(soup: BeautifulSoup | Tag, *, h_level: int) -> None:
    """
    Removes first `h{h_level}` tag from `soup`; also removes href to `h{h_level}`.
    """
    h_tag = "h%d" % h_level
    soup.find(h_tag).decompose()

def extract_icon(soup: BeautifulSoup | Tag) -> None:
    """
    Removes first `img` tag from `soup`.
    """
    soup.find("img").decompose()

def replace_section_with_div(soup: BeautifulSoup | Tag, *, og_repl: Tuple[str, str] = ("section[id]", "div"), class_list: List[str] = []) -> None:
    """
    Replaces tag identified by first half of `og_repl` with second half in `soup`; sets tag.class = 'excerpt' also.
    """
    og, repl = og_repl
    section = soup.css.select_one(og)
    section.name = repl
    section['class'] = "excerpt"
    section['data-section'] = class_list

# REFERENCE MANAGEMENT

def update_img_src(img: Tag) -> None:
    """
    Changes `img`.src to '/images/' + `img`.src.
    """
    try:
        img['src'] = "/images/" + Path(str(img['src'])).name
    except KeyError as key_err:
        logger.error("%s has no 'src' attribute. Inspect.", img)
        raise key_err

def internal_link_should_become_external(a: Tag, *, num_levels: int) -> bool:
    """
    Determines if `a` should have 'internal' in class attribute, based on the number of occurrences of '..' inside `a`.href.
    """
    href_path = str(a['href']).split('/')
    logger.debug("Checking if '%s' has %d instances of '..'", a['href'], num_levels)
    return href_path.count('..') == num_levels

def update_references_to_blending_modes_section(root_dir: Path | str, internal_a: Tag) -> None:
    """
    Updates reference to 'blending_modes' subsection article in `internal_a` based on if it exists in `root_dir`.
    """
    minimal_href = str(internal_a['href']).lstrip('./')
    # e.g., blending_modes/arithmetic.html#addition -> blending_modes/arithmetic/addition.html
    def convert_blending_modes_href(href: str) -> str:
        """
        Converts href of the form: blending_modes/arithmetic.html#addition -> blending_modes/arithmetic/addition.html
        """
        return href.replace(".html#", "/") + ".html"
    blending_modes_href = convert_blending_modes_href(minimal_href)
    full_path_to_tgt = Path(root_dir, blending_modes_href)
    logger.debug("Checking if '%s' exists.", full_path_to_tgt)
    if not full_path_to_tgt.exists():
        raise FileNotFoundError("Fatal error: '%s' should exist, but it doesn't." % full_path_to_tgt)
    internal_a['href'] = "/" + blending_modes_href

def get_correct_blending_modes_path(file_id: str, root_dir: Path | str) -> tuple[str, str, str]:
    """
    Returns 3-tuple that identifies path to 'blending_modes' subsubsection, if it exists.
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

def replace_internal_reference_with_official(internal_a: Tag) -> None:
    """
    Changes href of `internal_a` to full URL to official docs and changes class attribute accordingly.
    """
    internal_a['href'] = '/'.join([OFFICIAL_DOCS_ROOT.rstrip('/'), str(internal_a['href']).lstrip('./')])
    internal_a['class'].remove("internal")
    internal_a['class'].append(LINK_TO_OFFICIAL_DOCS_CLASSNAME)
    internal_a['class'].append("external")

# INDEX-FILE MANAGEMENT

def is_index_file(filename: Path | str) -> bool:
    """
    Returns True if `filename` represents an index file.
    """
    return Path(filename).with_suffix("").is_dir()

def extract_subsections(soup: BeautifulSoup | Tag) -> None:
    """
    Removes all subsections from `soup`.
    """
    for section in soup.css.select("section[id] > section[id]"):
        section.decompose()

# RENAMING FILES

def update_references_to_filename(
        soup: BeautifulSoup | Tag,
        section: Path | str,
        src_name: Path | str,
        tgt_name: Path | str,
    ) -> None:
    """
    Changes all references in `soup` from `section/src_name` to `section/tgt_name`.
    """
    src_path = '/'.join([str(section), str(src_name)])
    for internal_a in soup.css.select("a"):
        logger.debug("Checking if '%s' is present in '%s'.", src_path, internal_a['href'])
        if src_path not in str(internal_a['href']):
            continue
        dots = filter(lambda href_part: href_part == '..', str(internal_a['href']).split('/'))
        internal_a['href'] = '/'.join(list(dots) + [str(section), str(tgt_name)])
        logger.debug("Present.")

if __name__ == "__main__":
    import subprocess
    import sys

    # HELPER FUNCTIONS

    def get_soup_from_file(filepath: Path) -> BeautifulSoup:
        """
        Returns BeautifulSoup from `filepath`.
        """
        soup = BeautifulSoup(filepath.read_text(encoding="utf-8"), "html.parser")
        return soup

    def write_soup_to_file(soup: BeautifulSoup, filepath: Path) -> int:
        """
        Writes `soup` to `filepath`.
        """
        return filepath.write_text(str(soup), encoding="utf-8")

    def view_files(files: list[Path | str], *, view: bool = False) -> None:
        """
        Opens `files` in vim.
        """
        if not view:
            return
        args = ["vim", "-R"]
        args.extend([str(Path(TARGET_DIR, file)) for file in files])
        subprocess.run(args)

    # MAIN FUNCTIONS

    def clone_from_raw(target_dir: str | Path, source_dir: str | Path) -> None:
        """
        Recreates `target_dir` from `source_dir`; removes href directory also.
        """
        logger.debug("Removing '%s'.", target_dir)
        shutil.rmtree(target_dir, ignore_errors=True)
        logger.debug("Cloning from '%s' to '%s'.", source_dir, target_dir)
        shutil.copytree(source_dir, target_dir)
        Path(target_dir, "..", "hrefs.txt").unlink(missing_ok=True)
        logger.debug("Removed 'hrefs.txt'.")

    def rename_fill_layers_to_fill_layer_generators(target_dir: str | Path) -> None:
        """
        Renames 'layers_and_masks/fill_layers' to 'layers_and_masks/fill_layer_generators' and updates references in `target_dir` to former accordingly.
        """
        section = "layers_and_masks"
        src_name = "fill_layers.html"
        tgt_name = "fill_layer_generators.html"
        logger.info("Moving '%s/%s/%s' to '%s/%s/%s'.", target_dir, section, src_name, target_dir, section, tgt_name)
        shutil.move(
            Path(target_dir, section, src_name),
            Path(target_dir, section, tgt_name),
        )
        logger.info("Replacing all references to '%s/%s' with '%s/%s'.", section, src_name, section, tgt_name)
        for dirpath, dirnames, filenames in Path(target_dir).walk():
            for filename in filenames:
                filepath = dirpath.joinpath(filename)
                soup = get_soup_from_file(filepath)
                update_references_to_filename(soup, section, src_name, tgt_name)
                write_soup_to_file(soup, filepath)
            logger.info("Replaced references in '%s' section.", dirpath.name)

    def update_img_sources_in_files(target_dir: str | Path) -> None:
        """
        Prefixes all img.src attributes with '/images/' in `target_dir` files.
        """
        for dirpath, dirnames, filenames in Path(target_dir).walk():
            section = dirpath.name
            for filename in filenames:
                filepath = dirpath.joinpath(filename)
                logger.debug("Updating img['src'] in '%s'.", filepath)
                soup = get_soup_from_file(filepath)
                for img in soup.find_all('img'):
                    update_img_src(img)
                write_soup_to_file(soup, filepath)

    def update_references_to_blending_modes_sections_in_files(target_dir: str | Path) -> None:
        """
        Updates all references to 'blending_modes' subsubsection articles in `target_dir`.
        """
        for dirpath, dirnames, filenames in Path(target_dir).walk():
            for filename in filenames:
                filepath = dirpath.joinpath(filename)
                soup = get_soup_from_file(filepath)
                for a in soup.css.select("a"):
                    try:
                        update_references_to_blending_modes_section(target_dir, a)
                    except FileNotFoundError:
                        logger.warning("Error occurred while trying to update %s.", a['href'])
                write_soup_to_file(soup, filepath)

    def strip_headers_from_files(target_dir: str | Path) -> None:
        """
        Removes headers from all files in `target_dir`.
        """
        for dirpath, dirnames, filenames in Path(target_dir).walk():
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

    def replace_sections_with_divs_in_files(target_dir: str | Path) -> None:
        """
        Replaces main container for each file in `target_dir` from 'section' to 'div'.
        """
        og_repl = ("section[id]", "div")
        for dirpath, dirnames, filenames in Path(target_dir).walk():
            class_list = str(dirpath.relative_to(target_dir)).split("/")
            if class_list[0] == ".":
                class_list[0] = "_root"
            for filename in filenames:
                filepath = dirpath.joinpath(filename)
                soup = get_soup_from_file(filepath)
                replace_section_with_div(soup, og_repl=og_repl, class_list=class_list)
                if is_index_file(Path(dirpath, filename)):
                    div = soup.css.select_one("div")
                    div['class'] += " index"
                write_soup_to_file(soup, filepath)

    def strip_blending_modes_index_files(target_dir: str | Path) -> None:
        """
        Removes file-sections from 'blending_modes' index files.
        """
        for dirpath, dirnames, filenames in Path(target_dir).walk():
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

    def have_all_a_tags_open_new_tabs(target_dir: str | Path) -> None:
        """
        Makes <a> tags with 'external' in class attribute open URL in new tab.
        """
        for dirpath, dirnames, filenames in Path(target_dir).walk():
            for filename in filenames:
                filepath = dirpath.joinpath(filename)
                soup = get_soup_from_file(filepath)
                for a in soup.css.select("a"):
                    if 'external' not in a['class']:
                        continue
                    a['target'] = "_blank"
                write_soup_to_file(soup, filepath)

    def compile_all_hrefs(target_dir: str | Path) -> list[str]:
        """
        Compiles sorted list of 'href' values in `target_dir`.
        """
        hrefs = set()
        for dirpath, dirnames, filenames in Path(target_dir).walk():
            for filename in filenames:
                filepath = dirpath.joinpath(filename)
                soup = get_soup_from_file(filepath)
                for a in soup.css.select("a"):
                    hrefs.add(str(a['href']))
        href_list = list(hrefs)
        href_list.sort()
        return href_list

    def write_href_list_to_file(target_dir: str | Path, href_list: list[str], *, filename: str | Path = "hrefs.txt") -> None:
        """
        Writes `href_list` to `target_dir`/`filename`.
        """
        text_to_write = "\n".join(href_list)
        list_file = Path(target_dir, "..", filename)
        list_file.write_text(text_to_write, encoding="utf-8")

    def update_all_hrefs(index: list[dict[str, Any]], target_dir: str | Path) -> None:
        """
        Validates then normalizes all href values in `target_dir` in accordance with `index`.
        """
        def check_if_path_is_in_index(path: list[str], index: list[dict[str, Any]]) -> bool:
            """
            Returns True if `path` is in `index`.
            """
            try:
                record = list(filter(lambda record: record['path'] == path, index)).pop()
                return True
            except IndexError:
                raise KeyError("'%s' does not exist in index.", path)
        root_dir = Path(target_dir)
        for dirpath, dirnames, filenames in Path(target_dir).walk():
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
                    href = str(a['href'])
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
                        file_id = str(href[href.index("#"):])
                        try:
                            correct_bm_path = get_correct_blending_modes_path(file_id, target_dir)
                            if "blending_modes" in correct_bm_path:
                                a['href'] = "/" + '/'.join(correct_bm_path)
                            else:
                                a['href'] = "/blending_modes/" + '/'.join(correct_bm_path)
                            a['href'] = str(a['href']).replace('/#', '#')
                        except KeyError as key_err:
                            logger.debug("KeyError: %s", key_err)
                    #href = a['href']
                    if href.endswith("#hsx-blending-modes"):
                        a['href'] = "/" + href[:href.index("#hsx-blending-modes")]
                    og_href = str(a['href'])
                    if og_href.count('/') == 1 and '#' in og_href:
                        filename, file_id = tuple(og_href.lstrip('/').split("#"))
                        if not Path(target_dir, filename).exists():
                            logger.debug("Filename %s does not exist in root. Linking to official docs.", filename)
                            a['title'] = "To official Krita docs"
                            a['href'] = OFFICIAL_DOCS_ROOT + "reference_manual" + og_href
                            a['class'] = "reference external " + LINK_TO_OFFICIAL_DOCS_CLASSNAME
                            a['target'] = "_blank"
                write_soup_to_file(soup, filepath)
                path.pop()
                logger.debug("Replacing all internal links on 'blending_modes.html' to excerpt-links.")
                for a in filter(lambda a: "internal" in a['class'], soup.css.select("a")):
                    a_href = str(a['href'])
                    a['title'] = "To excerpt of '%s'" % a_href.lstrip('/')
                    a['href'] = '/reference_manual' + a_href
                    a['target'] = '_blank'
                write_soup_to_file(soup, filepath)

    def prepend_tags_to_all_files(tags: Iterable[Tag], target_dir: str | Path) -> None:
        """
        Prepends `tags` to all HTML files in `target_dir`.
        """
        for dirpath, dirnames, filenames in Path(target_dir).walk():
            for filename in filenames:
                filepath = dirpath.joinpath(filename)
                soup = get_soup_from_file(filepath)
                for tag in tags:
                    soup.div.insert_before(tag)
                write_soup_to_file(soup, filepath)

    def prepend_doctype_declaration_to_all_files(target_dir: str | Path) -> None:
        """
        Prepends '<!DOCTYPE html>' to all HTML files in `target_dir`.
        """
        prefix = "<!DOCTYPE html>\n"
        for dirpath, dirnames, filenames in Path(target_dir).walk():
            for filename in filenames:
                filepath = dirpath.joinpath(filename)
                filetext = filepath.read_text(encoding="utf-8")
                filepath.write_text(prefix + filetext, encoding="utf-8")

    def regenerate_docs() -> None:
        """
        Validates and prints processed documentation to disk.
        """
        clone_from_raw(TARGET_DIR, SOURCE_DIR)
        print("Finished cloning files.")
        view_files(["../index.json"])
        rename_fill_layers_to_fill_layer_generators(TARGET_DIR)
        print("Finished renaming 'layers_and_masks/fill_layers.html' to 'layers_and_masks/fill_layer_generators.html'.")
        view_files(["dockers/layers.html", "dockers/palette_docker.html", "filters/artistic.html"])
        update_img_sources_in_files(TARGET_DIR)
        print("Finished updating image sources.")
        view_files(["blending_modes/arithmetic/addition.html"])
        update_references_to_blending_modes_sections_in_files(TARGET_DIR)
        print("Finished updating references to blending_mode sources.")
        view_files(["blending_modes.html"])
        strip_headers_from_files(TARGET_DIR)
        print("Finished stripping <h[1-6]> tags.")
        view_files(["tools.html"])
        strip_blending_modes_index_files(TARGET_DIR)
        view_files(["brushes.html", "blending_modes.html", "layers_and_masks/fill_layer_generators.html"])
        print("Finished stripping 'blending_modes' index files.")
        view_files(["tools.html", "brushes/brush_engines.html", "blending_modes/arithmetic.html"])
        replace_sections_with_divs_in_files(TARGET_DIR)
        print("Finished replacing section[id] with div[id].")
        view_files(["layers_and_masks.html"])
        view_files(["brushes/brush_engines.html"])
        with open(INDEX_FILE, encoding="utf-8") as rfile:
            index = json.load(rfile)
        update_all_hrefs(index, TARGET_DIR)
        href_list = compile_all_hrefs(TARGET_DIR)
        write_href_list_to_file(TARGET_DIR, href_list)
        print("Finished updating a.href references.")
        view_files(["../hrefs.txt"])
        have_all_a_tags_open_new_tabs(TARGET_DIR)
        print("Finished setting target='_blank' for external links.")
        view_files(["layers_and_masks/fill_layer_generators/seexpr.html"])
        link_tag = BeautifulSoup().new_tag("link")
        link_tag['rel'] = "stylesheet"
        link_tag['href'] = "/styles/excerpts.css"
        link_tag['id'] = "excerpt-styles-link"
        link_tag['type'] = "text/css"
        prepend_tags_to_all_files([link_tag, "\n"], TARGET_DIR)
        print("Finished prepending %s to all files." % link_tag)
        view_files(["brushes.html"])
        prepend_doctype_declaration_to_all_files(TARGET_DIR)
        print("Finished prepending doctype declaration to all files.")
        view_files(["brushes.html"], view=True)

    regenerate_docs()

