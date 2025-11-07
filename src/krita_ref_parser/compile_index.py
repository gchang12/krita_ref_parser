"""
Defines functions to return list of objects of the form:
[
  {
    path: [str],
    header: str,
    icon: str|null,
    figures: [{img, figcaption}]|null,
  }
]
"""

from pathlib import Path

from bs4 import BeautifulSoup

from krita_ref_parser._logging import logger

PILCROW = "¶"

SOURCE_DIR = "./output/raw-excerpts/"
TARGET_DIR = "./output/"

DIRS_WITH_NO_INDICES = (
    Path(SOURCE_DIR, "layers_and_masks", "fill_layer_generators"),
)

# For exporting to .regenerate_docs
ALL_SECTIONS = {
    "tools": True,
    "brushes": False,
    "brushes/brush_engines": True,
    "brushes/brush_settings": False,
    "dockers": False,
    "filters": False,
    "layers_and_masks": False,
    "layers_and_masks/fill_layer_generators": False,
    "main_menu": False,
    "preferences": False,
    "resource_management": False,
    "blending_modes": False,
}
SECTIONS_WITHOUT_ICONS = tuple(
    map(
        lambda keyvalue: keyvalue[0],
        filter(lambda keyvalue: keyvalue[1] is False, ALL_SECTIONS.items())
    )
)
SECTIONS_WITH_ICONS = tuple(
    map(
        lambda keyvalue: keyvalue[0],
        filter(lambda keyvalue: keyvalue[1] is True, ALL_SECTIONS.items())
    )
)
BLENDING_MODE_SECTIONS = (
    "blending_modes/arithmetic",
    "blending_modes/binary",
    "blending_modes/darken",
    #"blending_modes/hsx",
    "blending_modes/lighten",
    "blending_modes/misc",
    "blending_modes/mix",
    "blending_modes/modulo",
    "blending_modes/negative",
    "blending_modes/quadratic",
)
BLENDING_MODE_HSX_SECTION = (
    "blending_modes/hsx",
)

def detect_index_files_for_directories(source_dir: Path | str, *, dirs_with_no_indices=DIRS_WITH_NO_INDICES):
    """
    """
    missing_files = set()
    for dirpath in filter(
        lambda path: not path.with_suffix(".html").exists(),
        filter(lambda path: path.is_dir(), Path(source_dir).iterdir()),
    ):
        missing_files.add(dirpath)
    if missing_files and set(dirs_with_no_indices) != missing_files:
        raise FileNotFoundError("These directories in '%s' lack complementing index files: %r" % (source_dir, missing_files))
    logger.info("All directories in '%s' have complementing index files.", source_dir)

def get_header(soup: BeautifulSoup, *, h_level: int):
    """
    """
    h_tag = "h%d" % h_level
    h_text = soup.find(h_tag).text
    h_text = h_text[:h_text.index(PILCROW)]
    logger.debug("Returning header: '%s'", h_text)
    return h_text

def get_section_id(soup: BeautifulSoup, *, h_level: int):
    """
    """
    h_tag = soup.find("h%d" % h_level)
    a_href = h_tag.find("a", class_="headerlink")['href']
    logger.debug("Returning header: '%s'", a_href)
    return a_href

def get_icon(soup: BeautifulSoup):
    """
    """
    try:
        img_src = Path(soup.find("img")['src']).name
        logger.debug("Image found. Returning source: '%s'", img_src)
    except TypeError:
        img_src = None
        logger.debug("No image found. Returning None.")
    return img_src

def get_figures(soup: BeautifulSoup):
    """
    """
    figures = []
    for figure in soup.find_all("figure"):
        img = figure.find('img')['src']
        try:
            figcaption = figure.find('figcaption').text.strip()
            figcaption = figcaption[:figcaption.index(PILCROW)]
        except AttributeError:
            figcaption = None
        fig_as_dict = {
            "img": Path(img).name,
            "figcaption": figcaption,
        }
        figures.append(fig_as_dict)
    if figures:
        logger.debug("(%d) figures found. Returning as dict-list.", len(figures))
        return figures
    logger.debug("No figures found. Returning None.")
    return None

if __name__ == "__main__":
    # Walk file-tree and replicate it in JSON
    import json
    '''
    [
      {
        path: [str],
        header: str,
        icon: str|null,
        figures: [{img, figcaption}]|null,
      }
    ]
    '''
    ROOT_LEN = 2
    INDEX = []
    INDEX_NAME = "index.json"

    def validate_directory(dirname: Path | str):
        """
        """
        logger.info("Validating: An index file exists for each directory in '%s'.", dirname)
        detect_index_files_for_directories(dirname)
        logger.info("Success!")

    def determine_if_walk_entry_is_in_sections(sections_to_search: list[str]):
        """
        """
        def walk_entry_is_in_sections(dirpathdirnamesfilenames: tuple[Path, list[str], list[str]]):
            """
            """
            dirpath, dirnames, filenames = dirpathdirnamesfilenames
            content_path = "/".join(dirpath.parts[ROOT_LEN:])
            return content_path in sections_to_search
        return walk_entry_is_in_sections

    def compile_entries_from_dir(dirpath: Path | str, filenames: list[str], *, h_level: int):
        """
        """
        index = []
        path_root = list(dirpath.parts[ROOT_LEN:])
        for filename in filenames:
            #path = path_buf.copy()
            #path.append(filename)
            # path: DONE
            filepath = Path(dirpath, filename)
            filetext = filepath.read_text(encoding="utf-8")
            soup = BeautifulSoup(filetext, "html.parser")
            header_text = get_header(soup, h_level=h_level)
            # header: DONE
            section_id = get_section_id(soup, h_level=h_level)
            # section.id: DONE
            icon = get_icon(soup)
            # icon: DONE
            figures = get_figures(soup)
            # figures: DONE
            article = {
                "path": path_root + [filename],
                "header": header_text,
                "id": section_id,
                "icon": icon,
                "figures": figures,
                "isIndexFile": filepath.with_suffix("").exists(),
            }
            index.append(article)
        logger.info("Indexed (%d) sections from '%s'.", len(filenames), dirpath)
        return index

    # SOURCE_DIR
    validate_directory(SOURCE_DIR)
    # {'resource_management', 'blending_modes', 'dockers', 'filters', 'layers_and_masks', 'brushes', 'preferences', 'tools', 'main_menu'}
    # index files exist: YES

    def compile_entries_from_dirs(sections_to_search: list[str], *, h_level: int):
        """
        """
        index = []
        for dirpath, dirnames, filenames in filter(determine_if_walk_entry_is_in_sections(sections_to_search), Path(SOURCE_DIR).walk()):
            validate_directory(dirpath)
            determine_if_walk_entry_is_in_sections(sections_to_search)
            index.extend(compile_entries_from_dir(dirpath, filenames, h_level=h_level))
        return index

    def compile_entries_from_root():
        """
        """
        index = []
        h_level = 1
        for dirpath, dirnames, filenames in Path(SOURCE_DIR).walk():
            if dirpath != Path(SOURCE_DIR):
                continue
            index.extend(compile_entries_from_dir(dirpath, filenames, h_level=h_level))
            break
        return index

    # compile index for sections without icons
    INDEX.extend(compile_entries_from_dirs(SECTIONS_WITHOUT_ICONS, h_level=1))
    print("Entries from %s have been compiled." % (SECTIONS_WITHOUT_ICONS,))
    #"These directories in 'output/raw-excerpts/layers_and_masks' lack complementing index files: [PosixPath('output/raw-excerpts/layers_and_masks/fill_layer_generators')]"
    # compile index for sections with icons
    INDEX.extend(compile_entries_from_dirs(SECTIONS_WITH_ICONS, h_level=1))
    print("Entries from %s have been compiled." % (SECTIONS_WITH_ICONS,))
    # compile index for 'layers_and_masks' section because directories with nested directories are excluded.
    #INDEX.extend(compile_entries_from_dirs(["layers_and_masks"], h_level=3))
    # compile index for 'blending_modes/' section
    INDEX.extend(compile_entries_from_dirs(BLENDING_MODE_SECTIONS, h_level=2))
    print("Entries from %s have been compiled." % (BLENDING_MODE_SECTIONS,))
    # compile index for 'blending_modes/hsx' section
    INDEX.extend(compile_entries_from_dirs(BLENDING_MODE_HSX_SECTION, h_level=3))
    print("Entries from %s have been compiled." % (BLENDING_MODE_HSX_SECTION,))
    INDEX.extend(compile_entries_from_root())
    print("Entries from root have been compiled.")
    logger.info("(%d) entries compiled into index.", len(INDEX))
    logger.info("Fields of index: %s.", tuple(INDEX[0].keys()))

    def affirm_all_sections_are_in_index():
        """
        """
        all_sections = \
            SECTIONS_WITH_ICONS \
            + SECTIONS_WITHOUT_ICONS \
            + BLENDING_MODE_SECTIONS \
            + BLENDING_MODE_HSX_SECTION
        set_of_all_sections = set(all_sections)
        set_of_all_sections.add('')
        index_dirs = set(map(lambda entry: '/'.join(entry['path'][:-1]), INDEX))
        try:
            assert (set_of_all_sections == index_dirs) is True
        except AssertionError as assert_err:
            print("Expected sections: %r.\n Actual sections: %r" % (set_of_all_sections, index_dirs))
            raise assert_err
        logger.info("These sections compose the entirety of the index: %s.", set_of_all_sections)
    affirm_all_sections_are_in_index()

    index_path = Path(TARGET_DIR, INDEX_NAME)
    print("Saving index to: '%s'" % index_path)
    with open(index_path, mode="w") as wfile:
        json.dump(INDEX, wfile, indent=2)
    print("Save successful.")

